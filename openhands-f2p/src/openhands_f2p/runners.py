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

    The shallowest directory named `tests`, `testing` or `test` that actually holds test
    files, and among equals the one holding the most. Shallowest rather than biggest
    because django's runner takes a label relative to `tests/` and its deepest test
    directories hold far more files -- `tests/forms_tests/tests` has ten where `tests/`
    has one, and putting the file in the former asks the runner for a label it will not
    resolve.

    *That actually holds test files* is load-bearing, and was learned from matplotlib.
    The name filter matches `requirements/testing`, which is a directory of pip
    requirement `.txt` files and contains no test at all; at depth one it beat the real
    `lib/matplotlib/tests` at depth two, and every matplotlib instance was told to put
    its test where nothing would collect it. Emptiness is checked before depth, so a
    directory that already holds tests is ranked exactly as it was before -- this
    changes the answer only where the previous winner held none.

    Returns "" when the project keeps tests at the root, as requests did in 2013.
    """
    found = box.exec(
        "find . -maxdepth 4 -type d \\( -name tests -o -name testing -o -name test \\) "
        "-not -path '*/node_modules/*' -not -path './.*' 2>/dev/null | head -40").output
    best, best_key = "", None
    for line in found.split():
        # Not `lstrip("./")`: that takes a *set of characters*, so a path whose first
        # component begins with a dot loses letters from it rather than losing the
        # prefix. The same mistake turned `/testbed/x` into `testbed/x` elsewhere.
        d = line[2:] if line.startswith("./") else line
        d = d.rstrip("/")
        if not d:
            continue
        n = box.exec(f"ls -1 {d}/test_*.py {d}/*_test.py 2>/dev/null | wc -l").output.strip()
        try:
            count = int(n)
        except ValueError:
            count = 0
        # Empty first: a directory matching the name but holding no test is not a test
        # directory, however shallow it is.
        key = (count == 0, d.count("/"), -count)
        if best_key is None or key < best_key:
            best, best_key = d, key
    return best


def _holds_tests(box, d: str) -> int:
    n = box.exec(f"ls -1 {d}/test_*.py {d}/*_test.py 2>/dev/null | wc -l").output.strip()
    try:
        return int(n)
    except ValueError:
        return 0


def near_test_directory(box, sources: list[str]) -> str:
    """The test directory that belongs to the code a pull request changes, or "".

    For pytest projects only (nodes runner); a project runner keeps `test_directory`'s
    answer, because its labels are relative to its own directory. Two layouts, tried for
    each changed source file, most-changed first:

      beside the code   walk up from the file to the nearest `tests`/`test`/`testing`
                        directory that holds tests -- `scipy/stats/tests` for a
                        `scipy/stats` change;
      mirrored          tests in a separate tree that repeats the package path --
                        Qiskit's `test/python/circuit` for `qiskit/circuit/...`.

    The repo-wide rule put every SciPy test in `scipy/special/tests` -- for stats,
    linalg, signal and optimize PRs alike -- and offered special's tests as the examples
    to follow (ChaCo audit, 2026-10-11).
    """
    if runner_for(box)["args"] != "nodes":
        return ""
    names = ("tests", "test", "testing")
    for src in sources:
        parts = src.split("/")[:-1]
        for i in range(len(parts), 0, -1):
            for n in names:
                d = "/".join(parts[:i] + [n])
                if box.exists(d) and _holds_tests(box, d):
                    return d
    roots = [ln[2:] if ln.startswith("./") else ln for ln in box.exec(
        "find . -maxdepth 2 -type d \\( -name tests -o -name test \\) "
        "-not -path './.*' 2>/dev/null").output.split()]
    for src in sources:
        sub = src.split("/")[1:-1]          # the path inside the top-level package
        for k in range(len(sub), 0, -1):
            tail = "/".join(sub[:k])
            for root in roots:
                found = box.exec(f"find {root} -maxdepth 4 -type d -path '*/{tail}' "
                                 f"2>/dev/null | head -5").output.split()
                for d in sorted(found, key=lambda x: x.count("/")):
                    d = d[2:] if d.startswith("./") else d
                    if _holds_tests(box, d):
                        return d
    return ""


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
# A django verbose line whose status did not follow on the same line: the test printed
# something (argparse usage, a warning traceback) between `name ...` and `ok`. The status
# then arrives alone on a later line and belongs to the name still pending.
DJANGO_OPEN = re.compile(r"^(.*?) \.\.\.(?: |$)")
DJANGO_STATUS_ALONE = re.compile(r"^(ok|FAIL|ERROR|skipped.*|expected failure"
                                 r"|unexpected success)\s*$")
# Django 3+ at verbosity 2, for a test with a docstring: the id on a line of its own, then
# the docstring's first line carrying the status. Keyed on the docstring, two tests
# sharing one collapsed into a single outcome (django-14765: three tests, two counted).
DJANGO_ID_ALONE = re.compile(r"^(\w+ \([\w.]+\))$")
# The traceback header after the run. The only place a test with failing subTests gets
# its status: its own line is left open (`name ... ` and then the next test's name).
DJANGO_HEADER = re.compile(r"^(FAIL|ERROR): (\w+ \([\w.]+\))")
# A django load failure: the module never imported. It is reported as one erroring
# "test", but nothing of the file ran -- the same fact as pytest's collection error,
# which produces no outcome at all, and it is counted the same way.
DJANGO_LOAD_FAILURE = "unittest.loader._FailedTest"
# sympy's verbose runner writes the name, runs the test, then writes the status. A test
# that prints puts its output between the two, and the status arrives alone on a later
# line -- `ok` or `F`, with the file's `[OK]` / `[FAIL]` marker when it is the last one.
SYMPY_OPEN = re.compile(r"^(test_\w+)\s+\S")
SYMPY_STATUS_ALONE = re.compile(r"^(ok|F|E|fail|Fail|exception|skipped|w|s|X|f)"
                                r"(?:\s+\[[A-Z]+\])?\s*$")

_NORMAL = {"ok": "PASSED", "PASSED": "PASSED", "XPASS": "PASSED",
           "expected failure": "PASSED", "F": "FAILED", "FAIL": "FAILED",
           "FAILED": "FAILED", "fail": "FAILED", "Fail": "FAILED", "f": "FAILED",
           "E": "ERROR", "ERROR": "ERROR", "exception": "ERROR",
           "unexpected success": "FAILED"}


ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


class Outcomes(dict):
    """Per-test outcomes, plus the docstrings django printed for some of them.

    A plain dict to everything that reads it -- json, `.items()`, `len`. `aliases` maps a
    docstring line to the ids it stood for, so a FAIL_TO_PASS entry recorded as the
    docstring (which is what SWE-bench stored) still finds its test in `outcome_of`.
    """

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.aliases: dict[str, list[str]] = {}


def _status(word: str) -> str:
    return _NORMAL.get(word, "SKIPPED" if "skip" in word else word)


def parse_output(output: str) -> dict[str, str]:
    """Per-test outcome, whatever runner produced the output.

    Every pattern is tried on every line rather than choosing one by project. The three
    formats are distinctive enough that they barely collide -- pytest prints a node id
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
    out = Outcomes()
    # experiments-v2: django-16454 printed argparse usage between `name ...` and `ERROR`,
    # the test was dropped, and a test still failing after the fix scored YES in two
    # arms; django-16136's coroutine warning did the same to a passing test and scored a
    # real YES as NO.
    pending: str | None = None          # a django test whose status has not come yet
    sympy_pending: str | None = None    # the same for sympy
    named: str | None = None            # a django id printed alone, docstring to follow
    unresolved: list[str] = []          # django tests whose own line never got a status
    headers: dict[str, str] = {}        # django traceback headers, id -> FAIL/ERROR
    sympy = "test process starts" in output

    def django(shown: str, status: str | None) -> None:
        """Record one django line: `shown ... status`, or an open one if status is None.

        `shown` can hold several tests: one whose subTests failed prints `name ... ` and
        nothing more, so the next test's name runs on after it. Each earlier part is a
        test whose status comes only from its traceback header."""
        nonlocal pending, named
        if pending is not None:
            unresolved.append(pending)
        keys = [p.strip() for p in shown.split(" ... ")]
        if named is not None and keys[0] != named:
            out.aliases.setdefault(keys[0], []).append(named)
            keys[0] = named
        named = None
        unresolved.extend(keys[:-1])
        if status is None:
            pending = keys[-1]
        else:
            out[keys[-1]] = _status(status)
            pending = None

    for raw in output.splitlines():
        # Stripped even with --color=no: some runners colour regardless of the flag,
        # and the escape sequences sit *inside* the node id, not just around it.
        line = ANSI.sub("", raw).strip()
        m = PYTEST_LINE.match(line)
        # django's closing summary, `FAILED (errors=1)`, fits the pytest short-summary
        # pattern too, and was being read as a failing test named "(errors=1)". It never
        # changed a verdict -- it only appears beside a real failure -- but it reached the
        # agent as one of the tests that "still fail after the change". No test id starts
        # with a parenthesis. Nor with a bracket: pytest's skip summary,
        # `SKIPPED [1] sklearn/tests/test_x.py:90: reason`, was read as a skipped test named
        # "[1]" (scikit-learn-25232, no-verify) and shown to the agent beside its own.
        if m and not m.group(2).startswith(("(", "[")):
            out[m.group(2)] = _NORMAL.get(m.group(1), m.group(1))
            continue
        m = PYTEST_VERBOSE.match(line)
        if m:
            out[m.group(1)] = _NORMAL.get(m.group(2), m.group(2))
            continue
        m = DJANGO_HEADER.match(line)
        if m:
            headers.setdefault(m.group(2), m.group(1))
            continue
        m = DJANGO_LINE.match(line)
        if m:
            django(m.group(1), m.group(2))
            continue
        if pending is not None:
            m = DJANGO_STATUS_ALONE.match(line)
            if m:
                out[pending] = _status(m.group(1))
                pending = None
                continue
        m = DJANGO_OPEN.match(line)
        if m and not line.startswith(("Ran ", "FAILED", "OK")):
            django(m.group(1), None)
            # What follows an open test on its line: the next test's id when the open
            # one had failing subTests (django-14792), else whatever the test printed.
            rest = line[m.end():].strip()
            if DJANGO_ID_ALONE.match(rest):
                named = rest
            elif (m := DJANGO_LINE.match(rest)):
                django(m.group(1), m.group(2))
            continue
        m = DJANGO_ID_ALONE.match(line)
        if m and not sympy:
            named = m.group(1)
            continue
        if sympy:
            m = SYMPY_LINE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), "SKIPPED")
                sympy_pending = None
                continue
            if sympy_pending is not None:
                m = SYMPY_STATUS_ALONE.match(line)
                if m:
                    out[sympy_pending] = _NORMAL.get(m.group(1), "SKIPPED")
                    sympy_pending = None
                    continue
            m = SYMPY_OPEN.match(line)
            if m:
                sympy_pending = m.group(1)
                continue
        else:
            m = SYMPY_LINE.match(line)
            if m:
                out[m.group(1)] = _NORMAL.get(m.group(2), "SKIPPED")
                continue
        named = None                    # the docstring line comes straight after its id
    if pending is not None:
        unresolved.append(pending)
    for name in unresolved:
        if name not in out and name in headers:
            out[name] = _NORMAL[headers[name]]
    # A module that failed to import: not a test, and not a failure of one.
    for name in [n for n in out if DJANGO_LOAD_FAILURE in n]:
        del out[name]
    return out


def outcome_of(outcomes: dict[str, str], node_id: str) -> str | None:
    """Look a node id up in parsed output, tolerating the formats' small differences."""
    if node_id in outcomes:
        return outcomes[node_id]
    # A docstring django printed for one or more tests. Several tests sharing it answer
    # together, and the worst of them is the answer: one failing is a failure.
    ids = getattr(outcomes, "aliases", {}).get(node_id)
    if ids:
        got = [outcomes[i] for i in ids if i in outcomes]
        for bad in ("ERROR", "FAILED"):
            if bad in got:
                return bad
        return got[0] if got else None
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
    """The project's own pytest configuration, verbatim -- when pytest is what runs.

    Not summarised. `xfail_strict = true` means an unexpected pass is a failure and
    `filterwarnings = error` means a warning ends the test -- both change what a test has
    to look like here, and both are clearer in the file than in a description of it.

    Withheld when the project ships its own runner, because then the file is not
    describing what will happen. sympy has a `pytest.ini` and runs `bin/test`, its own
    framework, in an image with no pytest installed; handing the agent that file under
    the heading "test configuration, verbatim from the checkout" read as permission to
    write a pytest test. `sympy-21612` opened with `import pytest`, the module never
    imported, and the verdict was BROKEN -- nothing collected on either side. The
    configuration was true and irrelevant, which is the worst thing a fact in a prompt
    can be.
    """
    if runner_for(box)["cmd"] != PYTEST:
        return ""
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
    """A few files near the new one that actually define a test.

    Named by content, not by filename. The first version listed `test_*.py` in the
    target directory, and for django that directory holds exactly one such file,
    `tests/test_sqlite.py` -- a settings module with no test in it. It was the only
    style example django agents were ever shown, and 31 of them went on to write
    module-level `def test_*` functions the runner never collects. The directory first,
    then one level down, where django keeps its real tests.
    """
    d = directory or "."
    probe = (f"for f in {d}/test_*.py {d}/*_test.py {d}/*/tests.py {d}/*/test_*.py; do "
             f"[ -f \"$f\" ] && grep -qE '^[[:space:]]*def test|^class [A-Za-z0-9_]*Test' "
             f"\"$f\" && echo \"$f\"; done 2>/dev/null | head -{limit}")
    found = box.exec(probe).output.split()
    return [f.strip().removeprefix("./") for f in found if f.strip()]


def repo_facts(box, test_file: str, environment: list[str] | None = None) -> str:
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
        # "in that directory" was wrong when the examples came from one level down
        # (Qiskit: `test/` holds no test file; `test/python/...` does).
        here = all("/".join(f.split("/")[:-1]) == directory for f in others)
        lines += ["", "Tests already in that directory:" if here
                  else "Tests in and below that directory:"]
        lines += [f"  {f}" for f in others]
    config = test_config(box)
    if config:
        lines += ["", "Test configuration, verbatim from the checkout:", ""]
        lines += [f"  {line}" for line in config.splitlines()]
    # Settings the instance's image makes that change how the code or its tests behave
    # (the dataset row's `environment_notes`). Without them the agent could not know that
    # pandas' future string dtype was on, which is the only thing some PRs change (ChaCo
    # canary pandas-59854, 2026-10-11). SWE-bench rows carry none.
    if environment:
        lines += ["", "Environment (set in this container):"]
        lines += [f"  {note}" for note in environment]
    if runner["args"] == "labels":
        # A hard rule, not a style. A labels runner is unittest discovery underneath,
        # and unittest collects methods named test_* on TestCase subclasses and nothing
        # else. A module-level `def test_x():` is skipped without a word: the run reports
        # "Ran 0 tests ... OK", exits 0, and scores as nothing collected. Across the ten
        # arms, 127 of 127 successful django runs used a TestCase class and not one
        # bare-function file ever passed -- while the briefing only ever described how
        # common each style was. Keyed on the runner kind, not the repository.
        lines += ["", "**This runner only collects test methods on a `unittest.TestCase` "
                      "subclass.** Put each test in a class that inherits from "
                      "`unittest.TestCase` (or the project's own subclass of it, if the "
                      "tests nearby use one), as a method whose name starts with `test`. "
                      "A module-level `def test_...():` is never collected -- the run says "
                      "`Ran 0 tests` and exits successfully, and your file counts as "
                      "having no test at all."]
    if not config and runner["cmd"] != PYTEST:
        # Said outright rather than left to be inferred from the runner line above it.
        # A `pytest.ini` can still be sitting in the checkout for the agent to find, and
        # the import failure it invites costs the whole run: the file does not import, so
        # nothing is collected on either side and there is no verdict to read.
        lines += ["", f"This project does not run pytest -- it runs `{runner['cmd']}`. "
                      f"Write for that runner: plain `assert`, no `import pytest`, no "
                      f"fixtures or decorators from it. pytest may not be installed here "
                      f"at all, and a file that imports it never runs."]
    return "\n".join(lines)
