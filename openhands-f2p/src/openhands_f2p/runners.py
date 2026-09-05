"""Three test-runner conventions, and how to read what they print.

Twelve repositories, three ways of naming and running a test, and a version spread that
matters as much as the repository: pytest 3.3 prints no short-summary section at all,
and `--no-header` is a usage error in the 4.5 that pytest\'s own repository runs.

Pure functions and tables. No container, no subprocess -- which is what makes the parsers
testable without Docker.
"""
from __future__ import annotations

import re
import shlex



# --------------------------------------------------------------- test invocation
#
# Three conventions live in this dataset, and a node id from one is meaningless to the
# others. Worse, only one of them can be passed on a command line at all:
#
#   pytest repos  'sklearn/utils/tests/test_set_output.py::test_set_output_pandas_keep_index'
#   django        'test_clear_cache (apps.tests.AppsTests.test_clear_cache)'
#                 'If the __path__ attr is empty, use __file__ if set.'      <-- a docstring
#   sympy         'test_issue_24543'                                        <-- no path
#
# Django's verbose runner prints a test's docstring in place of its name when it has
# one, and SWE-bench recorded whatever the runner printed. Those entries are not labels
# and never will be, so django cannot be driven by passing ids. sympy's ids carry no
# path, so they cannot locate a file.
#
# The way out is the one SWE-bench itself uses: run whole test *modules*, and decide
# per test by parsing the runner's output. So each repo needs two things -- what to run,
# and how to read what came back.
# No `--no-header`: pytest only grew that flag in 6.0, and these images span versions
# back to 4.5, where an unknown option is a usage error -- exit 4, nothing collected, and
# a verdict of BROKEN for a test that never got the chance to run. The header it would
# have suppressed is four lines of noise in a log nobody greps for.
# `-v` as well as `-rA`, because they are not the same guarantee. `-rA` prints a short
# summary section that pytest 3.3 -- astropy 1.3's pytest -- does not produce at all,
# leaving the log with a pass/fail count and not a single node id in it: "nothing
# collected on either side" for a run whose test really had failed and then passed.
# `-v` prints one `path::test STATUS` line per test on every version from 3 to 8.
PYTEST = ("python -m pytest -v -rA -p no:cacheprovider --tb=short "
          "--color=no")   # colour codes land inside the node id and defeat parsing

TEST_RUNNER: dict[str, dict[str, str]] = {
    "django/django": {"cmd": "./tests/runtests.py --verbosity 2", "kind": "django",
                      "gen_path": "tests/{name}.py"},
    "sympy/sympy": {"cmd": "bin/test -C --verbose", "kind": "sympy",
                    "gen_path": "sympy/core/tests/{name}.py"},
}
DEFAULT_RUNNER = {"cmd": PYTEST, "kind": "pytest", "gen_path": "tests/{name}.py"}


def runner_for(repo: str) -> dict[str, str]:
    return TEST_RUNNER.get(repo, DEFAULT_RUNNER)


def patched_test_files(test_patch: str) -> list[str]:
    """Test files the developer's patch touches -- the modules an instance lives in."""
    out = []
    for line in test_patch.splitlines():
        if line.startswith("diff --git "):
            path = line.split(" b/", 1)[-1].strip()
            if path.endswith(".py"):
                out.append(path)
    return out


def django_module(path: str) -> str:
    """'tests/apps/tests.py' -> 'apps.tests';  'tests/f2p_x.py' -> 'f2p_x'."""
    rel = path[len("tests/"):] if path.startswith("tests/") else path
    return rel[:-3].replace("/", ".") if rel.endswith(".py") else rel


def test_command(repo: str, targets: list[str]) -> str:
    """`targets` are node ids for pytest repos, and file paths everywhere else."""
    r = runner_for(repo)
    if r["kind"] == "django":
        args = " ".join(shlex.quote(django_module(t)) for t in targets)
    else:
        args = " ".join(shlex.quote(t) for t in targets)
    return f"{r['cmd']} {args}".strip()


PYTEST_LINE = re.compile(r"^(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s+(\S+)")
# The verbose form, `astropy/tests/test_x.py::test_y PASSED   [ 50%]`. Non-greedy up to
# the status word so that a parametrised id containing spaces -- `test_x[1 2]` -- stays
# in one piece.
PYTEST_VERBOSE = re.compile(
    r"^(\S.*?::.+?)\s+(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)(?:\s|$)")
DJANGO_LINE = re.compile(r"^(.*?) \.\.\. (ok|FAIL|ERROR|skipped.*|expected failure"
                         r"|unexpected success)\s*$")
SYMPY_LINE = re.compile(r"^(test_\w+)\s+(ok|F|E|fail|Fail|exception|skipped|w|s|X|f)\b")

_NORMAL = {"ok": "PASSED", "PASSED": "PASSED", "XPASS": "PASSED",
           "expected failure": "PASSED", "F": "FAILED", "FAIL": "FAILED",
           "FAILED": "FAILED", "fail": "FAILED", "Fail": "FAILED", "f": "FAILED",
           "E": "ERROR", "ERROR": "ERROR", "exception": "ERROR",
           "unexpected success": "FAILED"}


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def parse_output(repo: str, output: str) -> dict[str, str]:
    """Per-test outcome, keyed the way this repo's node ids are keyed.

    For django the key is whatever the runner printed, which is exactly what
    FAIL_TO_PASS/PASS_TO_PASS contain -- docstrings included.
    """
    kind = runner_for(repo)["kind"]
    out: dict[str, str] = {}
    for raw in output.splitlines():
        # Stripped even with --color=no: some runners colour regardless of the flag,
        # and the escape sequences sit *inside* the node id, not just around it.
        line = ANSI.sub("", raw).strip()
        if kind == "django":
            m = DJANGO_LINE.match(line)
            if m:
                name, status = m.group(1).strip(), m.group(2)
                out[name] = _NORMAL.get(status, "SKIPPED" if "skip" in status else status)
        elif kind == "sympy":
            m = SYMPY_LINE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), "SKIPPED")
        else:
            m = PYTEST_LINE.match(line)
            if m:
                out[m.group(2)] = _NORMAL.get(m.group(1), m.group(1))
                continue
            m = PYTEST_VERBOSE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), m.group(2))
    return out


def outcome_of(repo: str, outcomes: dict[str, str], node_id: str) -> str | None:
    """Look a node id up in parsed output, tolerating the formats' small differences."""
    if node_id in outcomes:
        return outcomes[node_id]
    if runner_for(repo)["kind"] == "django":
        # 'test_x (a.b.C.test_x)' may be printed as just 'test_x (a.b.C)' by some versions
        head = node_id.split(" (")[0]
        for k, v in outcomes.items():
            if k == head or k.startswith(head + " ("):
                return v
    return None
