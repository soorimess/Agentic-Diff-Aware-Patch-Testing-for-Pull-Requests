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

# How a project runs its tests, worked out from what is in the checkout rather than from
# the project's name. A table keyed on `django/django` is right for the repositories we
# happened to look at and silently wrong for the next one; a hand-written table also caps
# the system at the twelve repositories someone remembered to fill in. These signs are
# properties of the tree, so an unseen repository with a `runtests.py` gets the same
# treatment as django does, and one with neither sign falls back to pytest, which is what
# most Python projects use.
#
# `args` says what the runner wants to be pointed at, which is the part that differs most:
#
#   labels  a dotted module path relative to the runner's own directory (django)
#   paths   a filesystem path (sympy's bin/test)
#   nodes   pytest node ids, `path::name`
RUNNER_SIGNS = (
    ("tests/runtests.py", "./tests/runtests.py --verbosity 2", "labels", "tests"),
    ("runtests.py",       "./runtests.py --verbosity 2",       "labels", ""),
    ("bin/test",          "bin/test -C --verbose",             "paths",  ""),
)

DEFAULT_RUNNER = {"cmd": PYTEST, "args": "nodes", "root": "",
                  "why": "no project runner found"}


def runner_for(box) -> dict[str, str]:
    """`detect_runner`, once per container.

    Cached on the box itself, never in a dict keyed by `id(box)`. CPython reuses the
    address of a collected object, so a module-level cache keyed that way hands one
    container's answer to the next: in a six-instance oracle run django went first, its
    sandbox was destroyed, and sympy's sandbox landed on the same address and was told to
    run `./tests/runtests.py`, which does not exist there. An attribute dies with the
    object it belongs to.
    """
    cached = getattr(box, "_runner", None)
    if cached is None:
        cached = detect_runner(box)
        try:
            box._runner = cached
        except AttributeError:
            pass                # a box that will not hold an attribute just re-detects
    return cached


def detect_runner(box) -> dict[str, str]:
    """The command this checkout runs its tests with.

    Looks for a runner script the project ships. Everything else is pytest -- including
    projects with no test configuration at all, like requests in 2013, where pytest
    collecting `test_*.py` from the root is exactly right.
    """
    for path, cmd, args, root in RUNNER_SIGNS:
        if box.exists(path):
            return {"cmd": cmd, "args": args, "root": root,
                    "why": f"{path} is in the checkout"}
    return dict(DEFAULT_RUNNER)


def test_directory(box) -> str:
    """Where a new test file goes so that this project's runner will collect it.

    The shallowest directory named `tests`, `testing` or `test`, and among equals the one
    holding the most test files. Shallowest rather than biggest because django's runner
    takes a label relative to `tests/` and its deepest test directories hold far more
    files -- `tests/forms_tests/tests` has ten where `tests/` has one, and putting the
    file in the former asks the runner for a label it will not resolve.

    Returns "" when the project keeps tests at the root, as requests did in 2013.
    """
    found = box.exec(
        "find . -maxdepth 4 -type d \\( -name tests -o -name testing -o -name test \\) "
        "-not -path '*/node_modules/*' -not -path './.*' 2>/dev/null | head -40").output
    best, best_key = "", None
    for line in found.split():
        d = line.lstrip("./")
        if not d:
            continue
        n = box.exec(f"ls -1 {d}/test_*.py {d}/*_test.py 2>/dev/null | wc -l").output.strip()
        try:
            count = int(n)
        except ValueError:
            count = 0
        key = (d.count("/"), -count)
        if best_key is None or key < best_key:
            best, best_key = d, key
    return best


def patched_test_files(test_patch: str) -> list[str]:
    """Test files the developer's patch touches -- the modules an instance lives in."""
    out = []
    for line in test_patch.splitlines():
        if line.startswith("diff --git "):
            path = line.split(" b/", 1)[-1].strip()
            if path.endswith(".py"):
                out.append(path)
    return out


def dotted_label(box, path: str) -> str:
    """A path turned into the dotted label a project runner wants.

    Relative to the directory the runner lives in, which for django is `tests/`:
    'tests/apps/tests.py' -> 'apps.tests'. Derived from where the runner script was found
    rather than from a hardcoded 'tests/' prefix, so a project that keeps its runner
    somewhere else still gets a label it can resolve.
    """
    root = runner_for(box).get("root", "")
    rel = path[len(root) + 1:] if root and path.startswith(root + "/") else path
    return rel[:-3].replace("/", ".") if rel.endswith(".py") else rel


def test_command(box, targets: list[str]) -> str:
    """The command that runs `targets` here, in the form this project's runner wants."""
    r = runner_for(box)
    if r["args"] == "labels":
        args = " ".join(shlex.quote(dotted_label(box, t)) for t in targets)
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


def parse_output(output: str) -> dict[str, str]:
    """Per-test outcome, whatever runner produced the output.

    Every pattern is tried on every line rather than choosing one by project. The three
    formats are distinctive enough that they do not collide -- pytest prints a node id
    containing `::`, django prints `name ... ok`, sympy prints a bare function name and a
    single-letter status -- and trying all of them removes the need to know which runner
    ran before the output can be read.

    That matters beyond tidiness: knowing the runner used to be a lookup on the
    repository's name, so a project nobody had tabulated was parsed with the wrong
    pattern and came back as "nothing collected". Detection now comes from the checkout,
    and parsing needs no detection at all.

    For django the key is whatever the runner printed, which is exactly what
    FAIL_TO_PASS/PASS_TO_PASS contain -- docstrings included.
    """
    out: dict[str, str] = {}
    for raw in output.splitlines():
        # Stripped even with --color=no: some runners colour regardless of the flag,
        # and the escape sequences sit *inside* the node id, not just around it.
        line = ANSI.sub("", raw).strip()
        m = PYTEST_LINE.match(line)
        if m:
            out[m.group(2)] = _NORMAL.get(m.group(1), m.group(1))
            continue
        m = PYTEST_VERBOSE.match(line)
        if m:
            out[m.group(1)] = _NORMAL.get(m.group(2), m.group(2))
            continue
        m = DJANGO_LINE.match(line)
        if m:
            name, status = m.group(1).strip(), m.group(2)
            out[name] = _NORMAL.get(status, "SKIPPED" if "skip" in status else status)
            continue
        m = SYMPY_LINE.match(line)
        if m:
            out[m.group(1)] = _NORMAL.get(m.group(2), "SKIPPED")
    return out


def outcome_of(outcomes: dict[str, str], node_id: str) -> str | None:
    """Look a node id up in parsed output, tolerating the formats' small differences."""
    if node_id in outcomes:
        return outcomes[node_id]
    # 'test_x (a.b.C.test_x)' may be printed as just 'test_x (a.b.C)' by some versions.
    # Tried unconditionally: the shape of the id says whether this applies, and asking
    # the repository's name whether it is django was the coupling this module shed.
    if " (" in node_id:
        head = node_id.split(" (")[0]
        for k, v in outcomes.items():
            if k == head or k.startswith(head + " ("):
                return v
    return None


# --------------------------------------------------------------------------------
# Everything the agent needs to know about this project's tests, in one place.
#
# It used to be four: `detect_runner` and `test_directory` here, `gen_test_path` in
# verify, and a `repo_info` sub-agent that ran its own `find` over the same directories
# and then spent a model call summarising a config file. Two of those duplicated each
# other's work and the sub-agent's summary was worse than the file it summarised --
# `xfail_strict=true` and `filterwarnings = error` say more, and say it exactly, than any
# paraphrase of them.
#
# So: one function, no model, and the raw configuration passed through untouched. What a
# summary cannot give -- how tests are *written* here -- the agent gets by reading one,
# which is a better source than a description of one.

CONFIG_FILES = ("setup.cfg", "tox.ini", "pytest.ini", "pyproject.toml")

ARGS_HELP = {
    "nodes":  "pytest node ids (`path::name`) -- `run_tests` takes the file path",
    "labels": "a dotted label relative to the runner's directory -- `run_tests` converts "
              "the path for you",
    "paths":  "a file path",
}


def test_config(box) -> str:
    """The project's own pytest configuration, verbatim.

    Not summarised. `xfail_strict = true` means an unexpected pass is a failure and
    `filterwarnings = error` means a warning ends the test -- both change what a test has
    to look like here, and both are clearer in the file than in a description of it.
    """
    out = []
    for name in CONFIG_FILES:
        if not box.exists(name):
            continue
        section = box.exec(
            f"grep -A18 -iE '^\\[(tool:)?pytest\\]|^\\[tool\\.pytest' {name} "
            f"2>/dev/null | head -20").output.strip()
        if section:
            out.append(f"--- {name}\n{section}")
    return "\n".join(out)


def example_tests(box, directory: str, limit: int = 3) -> list[str]:
    """A few tests already in the directory the new one goes into."""
    found = box.exec(
        f"ls -1 {directory or '.'}/test_*.py {directory or '.'}/*_test.py "
        f"2>/dev/null | head -{limit}").output.split()
    return [f.strip().lstrip("./") for f in found if f.strip()]


def repo_facts(box, test_file: str) -> str:
    """A short briefing on how testing works here, for the prompt."""
    runner = runner_for(box)
    directory = test_file.rsplit("/", 1)[0] if "/" in test_file else ""
    lines = [
        "## How this project runs its tests",
        "",
        f"Runner        {runner['cmd']}",
        f"              ({runner['why']})",
        f"Targets       {ARGS_HELP.get(runner['args'], runner['args'])}",
        f"Your test     {test_file}",
    ]
    others = [f for f in example_tests(box, directory) if f != test_file]
    if others:
        lines += ["", "Tests already in that directory:"]
        lines += [f"  {f}" for f in others]
    config = test_config(box)
    if config:
        lines += ["", "Test configuration, verbatim from the checkout:", ""]
        lines += [f"  {line}" for line in config.splitlines()]
    return "\n".join(lines)
