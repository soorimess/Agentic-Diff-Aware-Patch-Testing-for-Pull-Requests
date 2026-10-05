"""Of the lines this pull request changed, how many did the test execute?

The evaluation metric, and the harness computes it -- never the agent. Named
`coverage_metric` rather than `coverage` so it cannot be mistaken for the `coverage`
package it drives inside the container.

Four things make it easy to get wrong, and each returns a wrong number rather than an
error: it has to be measured at head, the line numbers have to come from diffing the file
rather than from the diff header, comments and blanks must leave the denominator, and the
repository\'s own coverage configuration has to be overridden.
"""
from __future__ import annotations

import ast
import difflib
import json
import shlex
from typing import TYPE_CHECKING

from openhands_f2p.runners import runner_for, test_command
from openhands_f2p.statements import statement_start
from openhands_f2p.sandbox import REPO_DIR

if TYPE_CHECKING:
    from openhands_f2p.sandbox import Sandbox



SYMPY_COV_DRIVER = "/tmp/f2p_cov_driver.py"
# Import the test module and call its test functions, rather than asking sympy to find
# them. `sympy.test(path)` treats its argument as a filter and returns True when it
# matches nothing at all, so a path it does not recognise is indistinguishable from a
# suite that passed: sympy-12096 reported 0% coverage on a one-line patch its test
# demonstrably exercises, because under coverage the test had never run and the driver
# had exited 0 to say so. Importing the file by path cannot fail quietly -- if the
# module or a test is missing, this exits non-zero and says which.
SYMPY_DRIVER_SRC = '''import importlib.util, pathlib, sys, traceback

ran = failed = 0
for target in sys.argv[1:]:
    path = pathlib.Path(target.split("::")[0])
    if not path.exists():
        print("driver: no such file:", path)
        sys.exit(2)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    spec.loader.exec_module(module)
    for name in sorted(vars(module)):
        fn = getattr(module, name)
        if name.startswith("test_") and callable(fn):
            ran += 1
            try:
                fn()
                print("PASSED", path, name)
            except Exception:
                failed += 1
                print("FAILED", path, name)
                traceback.print_exc()
print("driver: ran", ran, "test(s),", failed, "failed")
sys.exit(1 if failed or not ran else 0)
'''

# django's runner has to be able to import its own settings module, which lives in
# `tests/`. Running `./tests/runtests.py` directly puts that directory on the path;
# running it as `python -m coverage run ./tests/runtests.py` does not -- sys.path[0]
# becomes the working directory instead, and the run dies on
# `ModuleNotFoundError: No module named 'test_sqlite'` before a single test executes.
DJANGO_COV_PATH = "PYTHONPATH=$PWD/tests"


COV_RC = "/tmp/f2p_coverage.rc"
COV_DATA = "/tmp/f2p.coverage"

# Our own coverage configuration, imposed so the repository's cannot decide what we
# measure. Three settings in checked-in `.coveragerc` files quietly produce a wrong
# answer rather than an error:
#
#   parallel  -- pytest's sets `parallel = 1`, which writes `.coverage.<host>.<pid>.<n>`
#                instead of `.coverage`. `coverage json` then reports "No data to
#                report." and the instance is scored as having no coverage at all. This
#                is what silenced both sphinx runs and pytest-5262.
#   include   -- a whitelist. Any changed file outside it is invisible, so a test that
#                really does execute the patch reports 0%.
#   data_file -- moves the file out from under us for the same effect as `parallel`.
#
# `source` and `include` are deliberately left unset: we want everything the test
# imports, and the narrowing to the patch's own lines happens afterwards in
# `changed_line_coverage`.
COV_RC_SRC = f"""[run]
branch = True
parallel = False
data_file = {COV_DATA}
disable_warnings = no-data-collected, module-not-imported
"""


def coverage_command(box: "Sandbox", targets: list[str]) -> str:
    """The repo's own runner, wrapped in `coverage run`.

    Wrapping rather than pytest-cov, because two of the three runners are not pytest.
    sympy needs more than a wrapper though: `coverage run bin/test ...` reports 12% of
    bin/test and 0% of everything else, because that launcher does not run the tests in
    a way coverage follows. Calling `sympy.test()` in-process from a small driver traces
    the library properly. pytest is not an option there -- it is not installed in that
    image at all.
    """
    box.write(COV_RC, COV_RC_SRC)
    runner = runner_for(box)
    if runner["args"] == "paths":
        box.write(SYMPY_COV_DRIVER, SYMPY_DRIVER_SRC)
        args = " ".join(shlex.quote(t) for t in targets)
        inner = f"{SYMPY_COV_DRIVER} {args}"
    else:
        inner = test_command(box, targets)
        if inner.startswith("python -m "):
            inner = inner[len("python "):]      # -> `-m pytest ...`
    prefix = f"{DJANGO_COV_PATH} " if runner["args"] == "labels" else ""
    return f"{prefix}python -m coverage run --rcfile={COV_RC} {inner}"


def measure_coverage(box: "Sandbox", targets: list[str],
                     limit_files: int = 12) -> dict:
    """Which lines the given tests executed, per file.

    Deliberately knows nothing about `patch`. It reports coverage of the files the test
    actually touched, and never which lines the pull request changed -- those come from
    the answer, and an agent told "you missed lines 977 and 980" has been handed the
    location of the bug. Change-specific coverage stays a measurement the harness makes
    afterwards, never an objective the agent optimises against.
    """
    box.exec(f"rm -f {COV_DATA} {COV_DATA}.* .coverage .coverage.* f2p_cov.json",
             timeout=120)
    run = box.exec(coverage_command(box, targets), timeout=3600)
    # `combine` is a belt-and-braces step: our rcfile turns parallel mode off, but a
    # test suite that forks (pytest-xdist, django's --parallel) still leaves one data
    # file per process. With nothing to combine it is a no-op.
    box.exec(f"python -m coverage combine --rcfile={COV_RC} --append 2>/dev/null; true",
             timeout=300)
    rep = box.exec(f"python -m coverage json --rcfile={COV_RC} -o f2p_cov.json "
                   f"--pretty-print 2>&1 | tail -2", timeout=600)
    raw = box.read("f2p_cov.json")
    box.exec(f"rm -f {COV_DATA} {COV_DATA}.* f2p_cov.json", timeout=120)
    if not raw:
        # Both halves: `coverage json` says only "No data to report.", which is a
        # symptom. What the test run itself printed is the cause.
        missing = "No module named coverage" in (rep.output + run.output)
        return {"ok": False, "returncode": run.returncode, "files": {},
                "detail": ("`coverage` is not installed in this container, so nothing "
                           "could be measured. See the `install offline` line in "
                           "flow.log."
                           if missing else
                           f"coverage json: {rep.output.strip()[-200:]} | "
                           f"test run exit {run.returncode}: {run.output[-600:]}")}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"ok": False, "detail": "coverage produced unreadable json", "files": {}}

    files = {}
    raw: dict[str, dict[str, set[int]]] = {}
    for path, info in (data.get("files") or {}).items():
        rel = path[len(REPO_DIR) + 1:] if path.startswith(REPO_DIR) else path
        rel = rel.lstrip("./")
        summary = info.get("summary") or {}
        executed = set(info.get("executed_lines") or [])
        missing = set(info.get("missing_lines") or [])
        # `measurable` is what coverage can have an opinion about at all: comments,
        # blanks and docstrings appear in neither list.
        raw[rel] = {"executed": executed, "measurable": executed | missing}
        if not summary.get("num_statements"):
            continue
        # Test files themselves are noise here: of course the test ran.
        if is_test_file(rel) or rel.rsplit("/", 1)[-1] == "f2p_cov_driver.py":
            continue
        files[rel] = {
            "percent": round(summary.get("percent_covered", 0.0), 1),
            "executed": summary.get("covered_lines", 0),
            "statements": summary.get("num_statements", 0),
            "missing_lines": (info.get("missing_lines") or [])[:60],
        }
    ranked = sorted(files.items(), key=lambda kv: -kv[1]["executed"])
    top = dict(ranked if limit_files == 0 else ranked[:limit_files])
    return {"ok": True, "returncode": run.returncode, "files": top, "raw": raw,
            "test_output_tail": run.output[-600:]}


def changed_lines(diff: str) -> dict[str, set[int]]:
    """Post-image line numbers a unified diff adds or alters, per file.

    Post-image on purpose: these numbers only exist once the patch is applied, which is
    why the measurement has to happen at head.
    """
    result: dict[str, set[int]] = {}
    current: str | None = None
    new_ln = 0
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            path = path[2:] if path.startswith("b/") else path
            current = None if path == "/dev/null" else path
            if current:
                result.setdefault(current, set())
        elif line.startswith("@@") and current:
            try:
                new_ln = int(line.split("+", 1)[1].split("@@")[0].strip().split(",")[0])
            except (IndexError, ValueError):
                new_ln = 0
        elif current and new_ln:
            if line.startswith("+"):
                result[current].add(new_ln)
                new_ln += 1
            elif not line.startswith("-"):
                new_ln += 1
    return {k: v for k, v in result.items() if v}


def patched_source_files(patch: str) -> list[str]:
    """The non-test Python files a patch touches -- the subject of the measurement."""
    return [p for p in changed_lines(patch) if p.endswith(".py") and not is_test_file(p)]


def added_lines_between(base_text: str, head_text: str) -> set[int]:
    """Line numbers *in head* that the patch introduced or rewrote.

    Read off the two files rather than the diff header, because the header can be wrong
    about where the change lands. `git apply` matches on context and will relocate a
    hunk that no longer sits at its recorded offset -- for scikit-learn-10908 it
    reported `Hunk #1 succeeded at 993 (offset 22 lines)`, so the diff's 974-976 pointed
    22 lines above the real change, at an unrelated method. Coverage was then measured
    against three lines the pull request never touched and reported 0%, with nothing
    anywhere to say the number was meaningless.

    Pure deletions contribute nothing, which is correct: a line that no longer exists
    cannot be executed, and counting it would make full coverage unreachable.
    """
    base = base_text.splitlines()
    head = head_text.splitlines()
    added: set[int] = set()
    for tag, _, _, j1, j2 in difflib.SequenceMatcher(
            None, base, head, autojunk=False).get_opcodes():
        if tag in ("insert", "replace"):
            added.update(range(j1 + 1, j2 + 1))     # 1-based, as coverage reports them
    return added


def is_test_file(path: str) -> bool:
    """Whether a repository path is a test rather than the code under test.

    By convention, not by substring. `"test" in name` reads `src/_pytest/unittest.py` --
    the file pytest-10081 actually patches -- as a test file and drops it from the
    denominator, so the instance reports "the fix touches no source .py lines" for a fix
    that is entirely source. The conventions below are the ones pytest itself collects
    by, plus the two directory names these twelve repositories use.
    """
    name = path.rsplit("/", 1)[-1]
    parts = path.split("/")
    return (name.startswith("test_") or name.endswith("_test.py")
            or name == "conftest.py"
            or "tests" in parts[:-1] or "testing" in parts[:-1])


def changed_line_coverage(box: "Sandbox", targets: list[str],
                          patch: str, base_files: dict[str, str] | None = None) -> dict:
    """Of the lines this pull request changed, how many does the test execute?

    The evaluation metric, and the harness computes it -- never the agent. The `coverage`
    tool the agent holds is deliberately blind to the diff; this is the half that reads
    it, and it runs only after the F2P verdict is settled.

    Three things make this harder than it sounds, and each one silently returns a wrong
    number rather than an error:

      * It must be measured at HEAD. A patch that adds lines has nothing at those line
        numbers until it is applied, so intersecting them with anything measured at base
        is empty by construction.
      * Comments and blank lines are invisible to coverage. Counting them in the
        denominator reports a fully covered four-line fix, two lines of which are
        comments, as 50%.
      * Test files in the patch are not the subject. A patch that also edits its own
        tests should be neither credited nor penalised for them.

    The caller is responsible for having applied `patch` before calling this.
    """
    # Preferred: diff the file against the copy taken before the patch went on, which
    # is what actually happened to the tree. The diff header is only a fallback for a
    # file the caller could not read at base -- a file the patch creates, say.
    wanted: dict[str, set[int]] = {}
    heads: dict[str, str] = {}                     # for mapping a line to its statement
    from_diff = changed_lines(patch)
    for path in patched_source_files(patch):
        base_text = (base_files or {}).get(path)
        head_text = box.read(path)
        if head_text is not None:
            heads[path] = head_text
        if base_text is not None and head_text is not None:
            lines = added_lines_between(base_text, head_text)
        else:
            lines = from_diff.get(path, set())
        if lines:
            wanted[path] = lines
    if not wanted:
        return {"measured": False, "reason": "the fix touches no source .py lines"}

    traced = measure_coverage(box, targets, limit_files=0)
    if not traced.get("ok"):
        return {"measured": False, "reason": traced.get("detail", "coverage failed")}

    hit: list[str] = []
    missed: list[str] = []
    matched: dict[str, str] = {}
    for path, lines in wanted.items():
        info = traced["raw"].get(path)
        if info is not None:
            matched[path] = path
        else:
            # Suffix matching, but only at a path boundary. Plain `endswith` will happily
            # match an *installed* copy of the library in site-packages, which is not the
            # tree the patch was applied to -- its line numbers belong to the unpatched
            # code, so every number after that is measured against the wrong file.
            for k, v in traced["raw"].items():
                if k == path or k.endswith("/" + path) or path.endswith("/" + k):
                    info, matched[path] = v, k
                    break
        info = info or {"executed": set(), "measurable": set()}
        # A changed line coverage cannot speak about may still belong to a statement it
        # can. A continuation line is not a statement, so it never appears in
        # `missing_lines` and appears in `executed_lines` only when it runs -- scoreable
        # as *hit*, never as *missed*. `sympy-21612` changes exactly one such line and
        # was reported unmeasurable when the honest answer was 0%. Mapping it onto the
        # statement it continues asks the question the patch actually raises.
        elsewhere = {ln: at for ln, at in
                     statement_start(heads.get(path, ""),
                                     {ln for ln in lines
                                      if ln not in info["measurable"]}).items()
                     if at in info["measurable"]}
        scored: set[int] = set()
        for ln in sorted(lines):
            at = ln if ln in info["measurable"] else elsewhere.get(ln)
            if at is None or at in scored:
                continue               # a comment or blank, or a statement already counted
            scored.add(at)
            (hit if at in info["executed"] else missed).append(f"{path}:{at}")
    total = len(hit) + len(missed)
    if not total:
        # Say which of the two it was. django-16333 reported this with the fix's two
        # lines plainly executable, and the message gave no way to tell whether the file
        # had been missed or the lines had -- so the evidence needed to tell them apart
        # is carried out of the container here rather than guessed at afterwards.
        seen = sorted(traced["raw"])
        near = [k for k in seen if any(k.endswith(w) or w.endswith(k) for w in wanted)]
        # A fix that deletes code and adds none (scikit-learn-25747 removes two lines and
        # rewords a docstring) has nothing at head for a test to execute. Called "all
        # comments or blanks" before, which described the added lines and hid the point.
        removed = any(ln.startswith("-") and not ln.startswith("---")
                      and ln[1:].strip() and not ln[1:].strip().startswith("#")
                      for ln in patch.splitlines())
        return {"measured": False,
                "reason": (("the fix only removes code -- it adds no executable line for a "
                            "test to run" if removed else
                            "the changed lines are all comments or blanks") if near else
                           "the changed file was never imported by this test"),
                "changed_files": sorted(wanted),
                "matched_traced_files": near,
                "traced_file_count": len(seen),
                "test_run_returncode": traced.get("returncode"),
                "test_output_tail": traced.get("test_output_tail", "")[-600:]}

    # A bare line number tells the agent nothing it can act on: to reach line 1631 it
    # has to know what is *on* that line and what guards it. So the source is read back
    # -- the line itself, plus the enclosing `if`/`def`, which is usually the condition
    # that has to be made true for the line to run at all.
    return {"measured": True, "percent": round(100 * len(hit) / total, 1),
            "covered": len(hit), "executable_changed_lines": total,
            "hit": hit, "missed": missed,
            # Which traced file each changed file was scored against. When these differ
            # from the key, coverage followed a copy of the library somewhere else and
            # the line numbers are not comparable -- worth being able to see.
            "matched_files": matched,
            # Carried even when the measurement succeeds, because a *low* number is as
            # likely to be a harness fault as a thin test and there is no way to tell
            # them apart afterwards without it. sympy-12096 reported 0% on a one-line
            # patch its test demonstrably exercises; the only thing that could settle
            # whether the test ran at all under `coverage` was this output.
            "test_run_returncode": traced.get("returncode"),
            "test_output_tail": traced.get("test_output_tail", "")[-600:],
            "missed_source": _annotate(box, missed),
            "missed_by_function": _by_function(box, hit, missed)}


def _by_function(box: "Sandbox", hit: list[str], missed: list[str]) -> list[dict]:
    """The changed lines grouped by the function holding them: how many ran, how many did
    not. A list of 65 missed lines is not something to act on; "these three new functions
    never run" is (astropy-13398, base: 31 of 96 lines, every one at import, through four
    refusals that listed the lines). Read at head, like the measurement. Lines outside any
    function are grouped under `<module>`."""
    by_file: dict[str, list[tuple[int, bool]]] = {}
    for refs, ran in ((hit, True), (missed, False)):
        for ref in refs:
            path, _, n = ref.rpartition(":")
            if n.isdigit():
                by_file.setdefault(path, []).append((int(n), ran))
    out: dict[tuple[str, str], dict] = {}
    for path, lines in by_file.items():
        source = box.read(path)
        try:
            tree = ast.parse(source or "")
        except SyntaxError:
            continue
        spans: list[tuple[int, int, str, int]] = []

        def walk(node, prefix=""):
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    name = f"{prefix}{child.name}"
                    if not isinstance(child, ast.ClassDef):
                        first = min([child.lineno] + [d.lineno for d in child.decorator_list])
                        spans.append((first, child.end_lineno or child.lineno, name,
                                      child.body[0].lineno))
                    walk(child, name + ".")
        walk(tree)
        for n, ran in lines:
            inner = [sp for sp in spans if sp[0] <= n <= sp[1]]
            sp = min(inner, key=lambda sp: sp[1] - sp[0]) if inner else None
            # The `def` and decorator lines run on import, whatever the test does: a hit
            # there does not mean the function was entered.
            if sp and ran and n < sp[3]:
                continue
            name = sp[2] if sp else "<module>"
            g = out.setdefault((path, name), {"path": path, "function": name,
                                              "ran": 0, "missed": 0})
            g["ran" if ran else "missed"] += 1
    return sorted(out.values(), key=lambda g: (-g["missed"], g["path"], g["function"]))


def _annotate(box: "Sandbox", refs: list[str], guards: int = 4) -> list[dict]:
    """For each `path:line`, the source of that line plus the conditions guarding it."""
    out: list[dict] = []
    by_file: dict[str, list[int]] = {}
    for ref in refs:
        path, _, ln = ref.rpartition(":")
        if ln.isdigit():
            by_file.setdefault(path, []).append(int(ln))
    for path, lines in by_file.items():
        text = box.read(path)
        if text is None:
            continue
        src = text.splitlines()
        for ln in sorted(lines)[:20]:
            if not 1 <= ln <= len(src):
                continue
            body = src[ln - 1]
            indent = len(body) - len(body.lstrip())
            context: list[str] = []
            for j in range(ln - 2, max(-1, ln - 80), -1):
                prev = src[j]
                if not prev.strip():
                    continue
                prev_indent = len(prev) - len(prev.lstrip())
                if prev_indent < indent and prev.lstrip().startswith(
                        ("if ", "elif ", "else", "for ", "while ", "with ", "try",
                         "except", "def ", "async def ", "class ")):
                    context.insert(0, f"{j + 1}: {prev.rstrip()}")
                    indent = prev_indent
                    if prev.lstrip().startswith(("def ", "async def ", "class ")):
                        break
                if len(context) >= guards:
                    break
            out.append({"ref": f"{path}:{ln}", "line": body.rstrip(),
                        "guards": context})
    return out


def import_time_hits(box: "Sandbox", cov: dict) -> list[str]:
    """The changed lines this run hit that execute when their module is imported.

    Anything outside a function body -- a module-level assignment, a class attribute, a
    decorator, a default argument -- runs on import, whatever the test then does. So
    "the test runs it" is true of every test that imports the module, and is no sign the
    test uses the change. django-15098 (first 36-instance base run, 2026-09-29) changed a
    module-level regex; its test copied that regex into itself and asserted on the copy,
    and coverage, the refusal ("It does reach the change ... Keep the input") and the
    agent all read "runs every changed line" as aimed at the right code.

    Read at head, so call it while the patch is applied, as the coverage run is.
    """
    by_file: dict[str, list[int]] = {}
    for ref in cov.get("hit") or []:
        path, _, line = ref.rpartition(":")
        if line.isdigit():
            by_file.setdefault(path, []).append(int(line))
    found: list[str] = []
    for path, lines in by_file.items():
        source = box.read(path)
        if source is None:
            continue
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        in_body: set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                in_body.update(range(node.body[0].lineno, (node.end_lineno or 0) + 1))
            elif isinstance(node, ast.Lambda):
                in_body.update(range(node.body.lineno, (node.body.end_lineno or 0) + 1))
        found += [f"{path}:{n}" for n in sorted(lines) if n not in in_body]
    return found


def base_texts(box: "Sandbox", patch: str) -> dict[str, str]:
    """The files `patch` changes, read now -- call this before applying it.

    `changed_line_coverage` needs them to find where the patch's lines actually landed.
    Without them it falls back to the diff header's line numbers, and `git apply` moves a
    hunk whose context has shifted: scikit-learn-10908 (base run, 2026-09-30) had its
    lines 22 below the header, so the agent's `coverage` tool measured an unrelated line,
    reported 0% seven times, and drove three coverage refusals and a "runs none of the
    change" refusal -- while the harness, which passed these, scored the same test 100%.
    """
    out: dict[str, str] = {}
    for path in patched_source_files(patch):
        text = box.read(path)
        if text is not None:
            out[path] = text
    return out
