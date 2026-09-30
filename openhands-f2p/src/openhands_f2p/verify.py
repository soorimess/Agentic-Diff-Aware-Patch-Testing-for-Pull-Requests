"""The F2P decision. One implementation, used by every arm.

This exists because there were two. The oracle had the base/head comparison inlined and
the agent had its own copy, and they had already drifted -- the agent's ran on the host
while the oracle's ran in a container. Two runs measured by different verification
code cannot be compared: any difference in their numbers is partly a difference in how they
were measured, and there is no way afterwards to say how much.

So the rule is that nothing computes an F2P verdict except `verify()`.

The decision itself:

    fails on the code before the fix, passes on the code after   ->  F2P

and three things that sentence leaves out, each of which produces a wrong number rather
than an error:

  1. Why it failed at base. A test that dies on an import also "fails at base" and
     proves nothing about the bug.
  2. Whether the environment was sane to begin with. PASS_TO_PASS answers that, and it
     is the caller's job to have checked.
  3. Whether the test is even reachable -- a generated file that does not import
     produces no outcomes at all, which is not the same as failing.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from openhands_f2p import flow
from openhands_f2p import swebench_env as E
from openhands_f2p.swebench_env import REPO_DIR, Sandbox

# Base-side failures that mean the test reached the behaviour it claims to check.
# A FAILED is an assertion or a wrong exception; an ERROR from the test body counts too
# (sympy reports the bug in 24562 as a TypeError raised inside Rational.__new__), but a
# collection error means the file never ran at all and shows up as no outcomes.
BEHAVIOURAL = {"FAILED", "ERROR"}

# `shortfall` reasons for a test that cannot be scored whatever the head run says: it has
# nothing failing at base. The refusal loop caps these at two rounds running.
UNSCOREABLE = ("passes_at_base", "collects_nothing", "skipped_at_base")


@dataclass
class Verdict:
    instance_id: str
    f2p: str                       # YES | NO | BROKEN
    why: str
    f2p_nodes: list[str] = field(default_factory=list)
    base: dict[str, str] = field(default_factory=dict)
    head: dict[str, str] = field(default_factory=dict)
    targets: list[str] = field(default_factory=list)
    changed_line_coverage: dict = field(default_factory=dict)
    base_log: str = ""
    head_log: str = ""

    @property
    def ok(self) -> bool:
        return self.f2p == "YES"

    def line(self) -> str:
        return f"F2P: {self.f2p} -- {self.why}"

    def as_dict(self, logs: bool = False) -> dict:
        d = {k: v for k, v in self.__dict__.items()
             if logs or k not in ("base_log", "head_log")}
        return d


def gen_test_path(instance_id: str, box: Sandbox | None = None) -> str:
    """Where a generated test has to live for this project's runner to collect it.

    `test_directory` reads it off the checkout: the shallowest directory named `tests`,
    `testing` or `test`, and among equals the one with the most test files in it. That
    covers all twelve repositories here without naming any of them -- `tests/` for flask,
    pylint, sphinx, seaborn and requests; `testing/` for pytest, which spells it
    differently; `<package>/tests/` for xarray, astropy, matplotlib and scikit-learn,
    whose tests sit beside the code; and the root for requests in 2013, which had no test
    directory at all.

    Shallowest matters: django's runner takes a label relative to `tests/`, and its
    deepest test directories hold ten times as many files as `tests/` itself, so picking
    the biggest would put the file where the runner cannot resolve a label for it.
    """
    name = f"test_f2p_{instance_id.replace('-', '_')}"
    if box is None:
        return f"tests/{name}.py"           # provisional, before a container exists
    directory = E.test_directory(box)
    return f"{directory}/{name}.py" if directory else f"{name}.py"


def _relative(path: str) -> str:
    """A path as the repository sees it, whatever form the agent wrote it in.

    `lstrip("./")` was doing this, and `lstrip` takes a *set of characters*: given the
    absolute `/testbed/astropy/tests/x.py` the agent actually used, it removed the
    leading slash and returned `testbed/astropy/tests/x.py` -- a path relative to the
    repository that names a directory the repository does not have. The verdict survived
    it, because the harness resolves its own target, but `shortfall` reads this path off
    the disk: it would have found nothing there and told the agent its test did not
    exist, which is both false and the most discouraging thing it could say.
    """
    path = path.strip().strip('"').strip("'")
    if path.startswith(REPO_DIR + "/"):
        path = path[len(REPO_DIR) + 1:]
    while path.startswith("./"):
        path = path[2:]
    return path.lstrip("/")


def written_test_path(box: Sandbox, tool_log: list, fallback: str) -> str:
    """Where the agent's test actually ended up.

    With `repo-facts` withheld the agent chooses the directory, so the path cannot be
    known before the run the way `gen_test_path` knows it. Everything downstream --
    `verify`, coverage, the mutants, the copy saved to out/ -- addresses the test by one
    path, so exactly one place resolves it and the rest are unchanged.

    The write log comes first because it records what the agent meant, and a path is
    only accepted once the file is confirmed present: `write_file` can fail, and a
    failed write that still named a path would send the whole verdict at an empty file.
    A `find` covers a test written some other way, and `fallback` keeps a path to
    address when there is nothing at all -- a run with no test is a `NO`, and it should
    report as one rather than crash here.
    """
    name = Path(fallback).name
    wrote = [e["path"] for e in tool_log
             if e.get("tool") == "write_file" and "error" not in e
             and e.get("path") and Path(e["path"]).name == name]
    for path in reversed(wrote):                    # the last write of it wins
        if box.read(path):
            return _relative(path)
    found = box.exec(f"find . -name '{name}' -not -path './.*' 2>/dev/null "
                     f"| head -5").output.split()
    if found:
        # Shallowest, for the same reason `test_directory` prefers it: a project runner
        # that takes a label relative to its own directory cannot resolve a deep one.
        return min((_relative(p) for p in found), key=lambda p: (p.count("/"), p))
    return fallback


def shortfall(box: Sandbox, instance: dict[str, Any], rel: str) -> tuple[str, str] | None:
    """What the agent could see for itself about not being finished, or `None`.

    This is the evidence a second chance is allowed to quote back, and the rule that
    decides what belongs here is the one the whole harness runs on: the agent works at
    base and has never seen the fix, so it may only be told things it could have
    established without leaving base. *There is no file.* *Your file collects nothing.*
    *Your test passes on this code.* Each of those is a command the agent could have run
    itself, and each is equally correct advice whether or not a judge exists.

    *Your test still fails after the fix* is the one that cannot appear here. It exists
    only in the head run. Feeding it back would make the agent fit its test to a diff it
    was never shown, and the test would stop being independent evidence about the pull
    request -- which is the only thing that makes it worth generating.

    That boundary is also the function's limit: a test that fails at base for the wrong
    reason looks identical from here to one that fails for the right reason, so this
    returns `None` for it and the ordinary verdict handles it.

    Returns `(reason, what_to_say)`, the first for the record and the second for the
    agent. `None` means nothing base-observable is wrong and the run should be scored as
    it stands.
    """
    if not box.read(rel):
        return ("no_test", f"There is no file at `{rel}`. Nothing was written, so there "
                           f"is no test to judge.")

    # The agent's own `verify` tool applies the patch and reverts it. If it left the tree
    # somewhere else, that is a different failure and a worse one -- say nothing and let
    # the verdict report it, rather than running a test against a tree of unknown state.
    if box.ensure_base(instance["patch"]) != "base":
        return None

    r = box.exec(E.test_command(box, [rel]), timeout=3600)
    outcomes = E.parse_output(r.output)
    flow.record(flow.VERIFY, "stop-check probe",
                f"{rel}: " + (", ".join(sorted(set(outcomes.values()))) or "nothing collected"))
    if not outcomes:
        found = ("collects_nothing",
                 f"`{rel}` exists but running it collects no tests. Either the file has "
                 f"no test function this project's runner recognises, or it fails to "
                 f"import. Read the error in the run below.")
    elif any(st in BEHAVIOURAL for st in outcomes.values()):
        return None
    elif all(st == "SKIPPED" for st in outcomes.values()):
        # django-16560 (no-cov+mut+require): every test skipped at base, and nothing
        # refused the stop -- the check above only knew "all PASSED".
        found = ("skipped_at_base",
                 f"Every test in `{rel}` is skipped on this code. A skipped test neither "
                 f"fails nor passes, so it cannot show the bug. Find what skips it in the "
                 f"run below -- a skip decorator, a feature this database backend lacks, "
                 f"an optional package that is not installed -- and write the test so it "
                 f"runs here.")
    else:
        found = ("passes_at_base",
                 f"Every test in `{rel}` passes on this code. The bug is still present "
                 f"here, so a test that already passes is not testing the change -- "
                 f"whatever it checks was true before the fix as well.")
    return found[0], found[1] + _evidence(box, rel, r.output)


# What a refusal under --second-chance hands back. The refused runs rewrote their test a
# median of five times after the refusal and converted 1 in 20 (experiments-v2): they
# were told what was wrong and asked to recall a file and a run from far up a long
# context. Both are base-side facts the agent could fetch itself with one `cat` and one
# `run_tests`, so giving them does not cross the line `shortfall` keeps; it saves the
# agent from working on its memory of the file instead of the file.
EVIDENCE_TEST_CHARS = 3000
EVIDENCE_RUN_CHARS = 2000


def _evidence(box: Sandbox, rel: str, run_output: str) -> str:
    text = box.read(rel) or ""
    if len(text) > EVIDENCE_TEST_CHARS:
        text = text[:EVIDENCE_TEST_CHARS] + f"\n# ... [{len(text) - EVIDENCE_TEST_CHARS} more characters]"
    out = run_output.strip()
    if len(out) > EVIDENCE_RUN_CHARS:
        half = EVIDENCE_RUN_CHARS // 2
        out = out[:half] + "\n... [clipped] ...\n" + out[-half:]
    return (f"\n\nThe file as it is on disk now:\n\n```python\n{text.rstrip()}\n```"
            f"\n\nRunning it on this code (the code before the fix) printed:\n\n"
            f"```\n{out}\n```")


def reach_diagnosis(box: Sandbox, instance: dict[str, Any], rel: str) -> str:
    """For a test that passes at base: which of the two very different mistakes is it?

    "Your test passes on this code" was the whole refusal, and it was the one that almost
    never worked: 156 refusals for it across the ten arms converted 3%, and on the new
    system seven of eight runs stuck on it spent all five rounds there. The agent rewrote
    every time -- it did not know which way it was wrong. There are two ways:

      it never executes the changed lines   the input is aimed at the wrong code
      it executes them and still passes     the input is right, the assertion checks
                                            something true on both sides of the change

    Those call for opposite corrections, and nothing in the old message told them apart.

    Only called when the agent holds `coverage`, which reports exactly this fact -- so the
    refusal tells it nothing it could not have asked for, and the base-only boundary that
    `shortfall` keeps is not crossed by what the agent learns, only by where it reads it.
    Measured with the patch applied, as the tool does, and always reverted.
    """
    patch = instance["patch"]
    if box.ensure_base(patch) != "base":
        return ""
    box.apply_patch(patch)
    try:
        cov = E.changed_line_coverage(box, [rel], patch)
        at_import = E.import_time_hits(box, cov) if cov.get("hit") else []
    except Exception:                                           # noqa: BLE001
        cov, at_import = {}, []
    finally:
        box.apply_patch(patch, revert=True)
    # A test that never imports the changed file leaves no entry for it in the coverage
    # report, and the metric calls that unmeasurable -- right for a score, wrong here: it
    # is the plainest case of not reaching the change. django-16333's first live refusal
    # went out with no diagnosis for exactly this reason.
    if not cov.get("measured") and cov.get("reason") != "the changed file was never imported by this test":
        return ""
    flow.record(flow.VERIFY, "stop-check reach",
                f"{rel}: runs {cov.get('covered', 0)} of the changed lines"
                + ("" if cov.get("measured") else " (changed file never imported)"))
    if not cov.get("covered"):
        return ("\n\n**It does not reach the change.** Running it executes none of the "
                "lines this pull request changes, so whatever it asserts is about code the "
                "fix does not touch. Keep the idea and move the input: call the code the "
                "change modifies, with an input that sends execution through the changed "
                "lines. `coverage` shows which they are and the conditions above each.")
    # Run only by importing it. A module-level line executes for any test that imports
    # the module, so "it runs the change" says nothing about the input; see
    # `E.import_time_hits` (django-15098: told "keep the input" twice while asserting on
    # its own copy of the changed regex).
    if at_import and len(at_import) == len(cov.get("hit") or []):
        shown = ", ".join(f"`{h}`" for h in at_import[:4])
        return ("\n\n**It only imports the change.** The changed lines it runs are "
                f"module-level ({shown}): they execute when the module is imported, "
                "whatever the test does, so that they run says nothing about the input. "
                "Call the code that *uses* the changed value, with an input where the old "
                "and the new value give different results, and assert on what that code "
                "returns or does. A copy of the value made inside the test checks the "
                "copy, not the project.")
    # Part of the change is not all of it. "It does reach the change ... Keep the input"
    # went out for sphinx-9602 (loop check) at 7 of 8 lines, and the line it never ran was
    # the one that turns the new nodes back into text -- the input was not yet right, and
    # the refusal told it to keep it.
    missed = cov.get("missed") or []
    if missed:
        shown = ", ".join(f"`{m}`" for m in missed[:5]) + (" ..." if len(missed) > 5 else "")
        return (f"\n\n**It reaches part of the change, and still passes before the fix.** "
                f"It runs {cov['covered']} of the {cov['executable_changed_lines']} lines "
                f"this pull request changes; these never run: {shown}. Either the "
                f"assertion checks something true on both sides of the change, or the "
                f"difference lies on a line the input never reaches. `coverage` shows those "
                f"lines and the conditions above each; work out what the changed lines "
                f"compute differently and assert that.")
    return ("\n\n**It does reach the change, and still passes before the fix.** It runs "
            "every line this pull request changes, so the input is aimed at the right code "
            "-- the assertion is what is wrong: it checks something that is true both "
            "before and after the change. Keep the input. Work out what the changed lines "
            "compute differently, and assert that value or behaviour instead.")


# Reading the project's own source and asserting on the text. Eight "fail-to-pass" tests
# across every run did this -- `inspect.getsource(UserCreationForm.save)` then
# `assertIn('hasattr(self, "save_m2m")', source)` -- which flips on this fix because the
# agent was shown its text, tests no behaviour, and fails on an equivalent fix worded
# differently. The judge rated all eight tangential / none / reject; the verdict counted
# them YES. Matched on the test's text, so it is the same check in every configuration.
#
# The target decides it. `inspect.getsource(UserCreationForm.save)` reads a named object
# of the project; `inspect.getsource(f)` on the function sympy's `lambdify` just generated
# reads the behaviour itself -- the generated source *is* what sympy-14976 changes. So a
# dotted or class-named target counts, a bare local name does not.
SOURCE_READING = re.compile(
    r"\bgetsource(?:lines|file)?\s*\(\s*(?:[A-Za-z_]\w*\.[\w.]+|[A-Z]\w*)\s*\)"
    r"|\bopen\s*\([^\n]*(?:__file__|\.py['\"])"
    r"|(?:__file__|\.py['\"])[^\n]*\.read_(?:text|bytes)\s*\(")
# `open(conf_py, 'w')` writes a fixture -- sphinx tests build a `conf.py` for the project
# under test -- and reads nothing. Matched as source reading in no-second-chance
# sphinx-9591 and no-require-tools sphinx-8459. A write, append or create mode anywhere
# in the call exempts the line.
WRITE_MODE = re.compile(r"""\bopen\s*\(.*?,\s*(?:mode\s*=\s*)?['"][rb+]*[wax]""")


def reads_source(text: str) -> str | None:
    """The first line of the test that reads project source as text, if any."""
    for line in (text or "").splitlines():
        if line.lstrip().startswith("#"):
            continue
        if SOURCE_READING.search(line) and not WRITE_MODE.search(line):
            return line.strip()[:120]
    return None


def source_gap(box: Sandbox, rel: str) -> tuple[str, str] | None:
    """Refuse a stop whose test asserts on source text rather than behaviour."""
    line = reads_source(box.read(rel) or "")
    if not line:
        return None
    flow.record(flow.VERIFY, "reads source", f"{rel}: {line}")
    return ("reads_source",
            f"`{rel}` reads the project's source code as text (`{line}`). A test that "
            f"checks what the fix *says* passes on this exact wording and fails on an "
            f"equivalent fix written differently; it tests nothing the pull request "
            f"changes about how the code behaves. Remove that. Call the code the change "
            f"modifies, with an input that goes through it, and assert on what it returns, "
            f"raises or does.")


def no_reach_gap(box: Sandbox, instance: dict[str, Any], rel: str) -> tuple[str, str] | None:
    """A test that flips while running none of the changed lines: worth one question.

    Soft by design. It is how a source-text test looks from outside (0% on all eight),
    but two genuine behavioural tests also measured 0% -- the change reached through a
    path coverage did not trace -- so the message allows the agent to say so and stop.
    Only with the coverage tool registered, for the reason `reach_diagnosis` gives.
    """
    patch = instance["patch"]
    if box.ensure_base(patch) != "base":
        return None
    box.apply_patch(patch)
    try:
        cov = E.changed_line_coverage(box, [rel], patch)
    except Exception:                                           # noqa: BLE001
        cov = {}
    finally:
        box.apply_patch(patch, revert=True)
    if not (cov.get("measured") and cov.get("covered") == 0):
        return None
    flow.record(flow.VERIFY, "flips without reaching",
                f"{rel}: runs 0 of {cov.get('executable_changed_lines')} changed lines")
    return ("runs_no_change",
            f"`{rel}` flips, but running it executes none of the lines this pull request "
            f"changes. A test that flips without running the change is usually checking "
            f"something other than behaviour -- a string, a file, an attribute that "
            f"happens to differ. Make it call the changed code and assert on the result. "
            f"If it genuinely reaches the change through a path coverage cannot follow, "
            f"say so in one sentence and finish.")


def same_file(named: str, rel: str) -> bool:
    """Whether a path or target the agent gave names the test file `rel`.

    Tolerates the forms a target arrives in: `/testbed/...`, `./...`, a pytest node id
    (`path::test`), a dotted django label (`auth_tests.test_x`). Anything else is another
    file."""
    t = _relative((named or "").split("::")[0])
    if not t or not rel:
        return False
    if not t.endswith(".py"):
        # `tests/test_x` (no-coverage-tool django-14725 verified it that way) or a
        # dotted label, `auth_tests.test_x`.
        t = (t if "/" in t else t.replace(".", "/")) + ".py"
    return t == rel or (Path(t).name == Path(rel).name
                        and (rel.endswith("/" + t) or t.endswith("/" + rel)))


def _verifies_of(tool_log: list, rel: str | None) -> list[tuple[int, dict]]:
    """The `verify` calls that ran, on `rel` when it is given.

    On `rel` because a verify on another file says nothing about the one that is scored:
    in six experiments-v2 runs a `verify` on a side file closed the loop for the real one,
    and four of them ended NO -- no-second-chance sklearn-10297 verified `..._simple.py`
    as fail-to-pass while the scored file still failed after the fix. A call that could not
    run (tree not at base) answered nothing and is left out too."""
    return [(i, e) for i, e in enumerate(tool_log)
            if e.get("tool") == "verify" and "error" not in e
            and (rel is None or same_file(e.get("target", ""), rel))]


def wrote_test_after(tool_log: list, i: int, rel: str | None) -> bool:
    """Whether the test file was written after entry `i`. Only `rel` counts: a scratch
    file written after a passing verify produced "you edited the test since" in two runs
    that had not touched it (no-mutation-tool django-14915, no-coverage+mutation
    matplotlib-20859)."""
    return any(e.get("tool") == "write_file" and "error" not in e
               and (rel is None or same_file(e.get("path", ""), rel))
               for e in tool_log[i + 1:])


def verify_settled(tool_log: list, rel: str | None = None) -> bool:
    """Whether the test is fail-to-pass by the agent's own last `verify`, unchanged since."""
    found = _verifies_of(tool_log, rel)
    if not found:
        return False
    i, e = found[-1]
    still = [n for n, st in (e.get("after") or {}).items() if st in BEHAVIOURAL]
    return bool(e.get("flipped")) and not still and not wrote_test_after(tool_log, i, rel)


def _last(tool_log: list, tool: str, rel: str) -> tuple[int, dict] | None:
    """The last call of `tool` on the scored file. An answer about another file is not an
    answer about this one."""
    found = (_verifies_of(tool_log, rel) if tool == "verify" else
             [(i, e) for i, e in enumerate(tool_log) if e.get("tool") == tool
              and same_file(e.get("target", ""), rel)])
    return found[-1] if found else None


def verify_gap(tool_log: list, rel: str) -> tuple[str, str] | None:
    """Whether the agent's own `verify` has established fail-to-pass for the file on disk.

    Part of `require-tools`' stop checks (for one day, 2026-09-28, the second chance's;
    see `features.py`). Judged by what `verify` last
    *said*, not by whether it was called: the first version of this check counted calls,
    and four of five failures in the run that introduced it ended immediately after
    `verify` reported NOT fail-to-pass -- requirement satisfied, goal unmet -- while
    `pylint-7277` called `verify` seventeen times and `matplotlib` once.

    Open when `verify` was never called on the scored file, when its last answer was not
    fail-to-pass, or when the test was written after that answer -- an answer about a
    file that has been edited is an answer about a file that no longer exists.

    Pure, and reads only the agent's own record, so nothing here can leak the head run.
    Returns `(reason, what_to_say)` or `None` when the test flips by its own last verify.
    """
    got = _last(tool_log, "verify", rel)
    elsewhere = [e.get("target") for _, e in _verifies_of(tool_log, None)
                 if not same_file(e.get("target", ""), rel)]
    if got is None and elsewhere:
        say = (f"Your `verify` calls ran on `{elsewhere[-1]}`, but the test this run is "
               f"scored on is `{rel}`, and nothing has verified that file. Only `{rel}` "
               f"counts: put the test there, call `verify` on it, and keep going until it "
               f"says fail-to-pass.")
    elif got is None:
        # What `verify` does, said here. astropy-13398 (second base run, 2026-09-30) wrote
        # "let me run `verify`" fourteen times, called something else every time -- it
        # believed it "cannot apply the change in this environment" -- and took all ten
        # refusals without one call. It never has to apply anything: `verify` does.
        say = (f"You never called `verify`, so nothing has established the one property "
               f"the test must have. `verify` works here and does the applying itself: it "
               f"runs your test on this code, applies the change, runs it again and puts "
               f"the code back -- you apply nothing. Call it now with `target` set to "
               f"`{rel}`, and keep going until it says fail-to-pass.")
    else:
        i, e = got
        still = [n for n, st in (e.get("after") or {}).items() if st in BEHAVIOURAL]
        flipped = e.get("flipped") or []
        edited = wrote_test_after(tool_log, i, rel)
        if (not flipped or still) and edited:
            # Said "the test has not changed since" here regardless, which was false for
            # every run that had edited after its last verify -- three of the nine
            # refusals in one 26-instance run.
            # What it said, quoted, and which calls do not count. matplotlib-22719 (loop
            # check) got the bare sentence ten times running, answered each with
            # `run_tests` and `coverage` -- both of which only ever run the test on one
            # side of the change -- and stopped again without calling `verify` once.
            last_said = (e.get("shown") or "").split("\n\n")[0].strip()
            quoted = f" Its answer was:\n\n> {last_said}\n\n" if last_said else " "
            say = (f"The last `verify` said **not fail-to-pass**, and you have edited the "
                   f"test since, so nothing has checked the file on disk now.{quoted}"
                   f"Call `verify` with `target` set to `{rel}`, and keep going until it "
                   f"says fail-to-pass. "
                   f"`run_tests` and `coverage` do not answer this: each runs the test on "
                   f"one side of the change only.")
        elif not flipped or still:
            if flipped and still:
                said = (f"{len(flipped)} test(s) already fail before the change and pass "
                        f"after -- keep them -- but {len(still)} still fail after it. Fix "
                        f"or delete the ones that still fail")
            else:
                said = (f"{len(still)} test(s) still failing after the change"
                        if still else "nothing flipped")
            say = (f"The last `verify` said **not fail-to-pass** -- {said}. That is the "
                   f"answer to the only question that decides this run, and the test has "
                   f"not changed since. Rewrite the test and call `verify` again, and keep "
                   f"doing that until it says fail-to-pass. Nothing else you could do with "
                   f"the remaining budget counts for anything while this is the answer.")
        elif edited:
            say = (f"You edited the test after the last `verify`, so the fail-to-pass "
                   f"result describes a file that no longer exists. Call `verify` again on "
                   f"what is on disk now.")
        else:
            return None
    return ("verify_open", f"`{rel}` is not fail-to-pass yet by its own last `verify`.\n\n"
                           f"* {say}")


def _no_better(tool_log: list, tool: str, rel: str, score) -> bool:
    """Whether the agent's last attempt to improve this answer did not improve it: the two
    latest calls of `tool` on the scored file have the test written between them, and the
    later score is no higher. That is what ends a coverage or mutation loop short of its
    goal -- a line no test can reach, a variant that breaks nothing observable. Trying and
    not moving is an answer; refusing again would only ask for padding."""
    calls = [(i, e) for i, e in enumerate(tool_log) if e.get("tool") == tool
             and same_file(e.get("target", ""), rel)]
    if len(calls) < 2:
        return False
    (i_prev, prev), (i_last, last) = calls[-2], calls[-1]
    tried = any(e.get("tool") == "write_file" and same_file(e.get("path", ""), rel)
                for e in tool_log[i_prev + 1:i_last])
    a, b = score(prev), score(last)
    # A score below the best this file ever had is a regression, not a plateau: the loop
    # stays open so the agent gets back what it lost.
    if b is not None and b < (_best_before(tool_log, tool, rel, score) or b):
        return False
    return tried and a is not None and b is not None and b <= a


def _best_before(tool_log: list, tool: str, rel: str, score) -> float | None:
    """The best score any earlier call of `tool` on the scored file reported."""
    calls = [e for e in tool_log if e.get("tool") == tool and same_file(e.get("target", ""), rel)]
    earlier = [x for x in (score(e) for e in calls[:-1]) if x is not None]
    return max(earlier) if earlier else None


def _lost(tool_log: list, tool: str, rel: str, score, now: float | None, unit: str) -> str:
    best = _best_before(tool_log, tool, rel, score)
    return (f"It reached {best}{unit} earlier and your last change lowered it -- get that "
            f"back. " if best is not None and now is not None and now < best else "")


def coverage_score(e: dict) -> float | None:
    cov = e.get("result") or {}
    return cov.get("percent") if cov.get("measured") else None


def mutation_score(e: dict) -> float | None:
    return round(100.0 * e["killed"] / e["total"], 1) if e.get("total") else None


def duty_gap(tool_log: list, instruments: tuple[str, ...], rel: str,
             scored: bool = False) -> tuple[str, str] | None:
    """The coverage and mutation loops, once the test flips. `require-tools`.

    Two loops (user, 2026-09-29), each on the tool's answer about the scored file:

    `coverage` until no changed line is missed; `mutation` until no variant survives.

    Each is open while its last answer falls short, and when the test was written after
    that answer (the answer describes a file that no longer exists -- call the tool
    again). Each ends at its goal, or when the agent's last attempt did not improve it
    (`_no_better`): a line no test can reach, a variant that breaks nothing observable.
    The loop makes the agent try; it does not make it pad. Only for a test that already
    flips by its own last `verify` -- until then these are questions about a test that
    does not exist yet (the qwen run made eight such calls before `verify` had flipped,
    and `mutation` answered one with "your test does not pass on the fixed code yet").

    `scored` (`--add-require-tools-with-score-report`): the same loops, with the scores
    named -- changed-line coverage and mutation score -- and the agent asked to reach
    100% and maximise. Before 2026-09-29 the plain duty was one reminder, and in score mode
    mutation had no loop; both loop now.

    Pure, reads only the agent's own record. Returns `(reason, what_to_say)` or `None`;
    the reason is `duties_open[coverage+mutation]`, naming the open loops.
    """
    if not verify_settled(tool_log, rel):
        return None
    gaps: list[tuple[str, str]] = []
    if "coverage" in instruments:
        got = _last(tool_log, "coverage", rel)
        if got is None:
            gaps.append(("coverage",
                         "Your test is fail-to-pass. Now call `coverage`: how much of the "
                         "change it reaches is the next question, and it is currently "
                         "unknown."))
        else:
            i, e = got
            cov = e.get("result") or {}
            pct = coverage_score(e)
            score = (f"Changed-line coverage is {pct}% ({cov.get('covered')} of "
                     f"{cov.get('executable_changed_lines')} lines); the target is 100%. "
                     if scored else "")
            if not cov.get("measured") or not cov.get("missed"):
                pass
            elif wrote_test_after(tool_log, i, rel):
                gaps.append(("coverage",
                             f"{score}You changed the test after the last `coverage`, so "
                             f"its answer describes a file that no longer exists. Call "
                             f"`coverage` again on what is on disk now."))
            elif not _no_better(tool_log, "coverage", rel, coverage_score):
                lost = _lost(tool_log, "coverage", rel, coverage_score, pct, "%")
                gaps.append(("coverage",
                             f"{score}{lost}`coverage` last listed {len(cov['missed'])} changed "
                             f"line(s) your test never runs. Keep going: work the missed "
                             f"lines one at a time -- the same behaviour by another route, a "
                             f"separate case that deserves its own test -- change the test, "
                             f"call `verify`, then `coverage` again. Reach each line through "
                             f"behaviour you assert; a call with no assertion behind it does "
                             f"not count. If an honest attempt leaves the lines missed, "
                             f"that ends this."))
    if "mutation" in instruments:
        got = _last(tool_log, "mutation", rel)
        if got is None:
            gaps.append(("mutation",
                         "You never called `mutation`. Call it and work the survivors: each "
                         "is a wrong version of this change your test cannot tell from the "
                         "right one."))
        else:
            i, e = got
            ms = mutation_score(e)
            score = (f"Mutation score is {ms}% ({e.get('killed')} of {e.get('total')} "
                     f"caught); maximise it. " if scored and ms is not None else "")
            if not e.get("survived"):
                pass
            elif wrote_test_after(tool_log, i, rel):
                gaps.append(("mutation",
                             f"{score}You changed the test after the last `mutation`, so "
                             f"its answer describes a file that no longer exists. Call "
                             f"`mutation` again on what is on disk now."))
            elif not _no_better(tool_log, "mutation", rel, mutation_score):
                lost = _lost(tool_log, "mutation", rel, mutation_score, ms, "%")
                gaps.append(("mutation",
                             f"{score}{lost}`mutation` last reported {len(e['survived'])} wrong "
                             f"version(s) of the fix your test does not notice. Keep going: "
                             f"for each, work out the behaviour it breaks, add an assertion "
                             f"about that behaviour -- what the code returns, raises or does "
                             f"-- call `verify`, then `mutation` again. Never assert on the "
                             f"exact expression a variant changed just to make it fail. If "
                             f"an honest attempt catches no more of them, that ends this: "
                             f"what is left breaks nothing a test here can observe."))
    if not gaps:
        return None
    names = "+".join(dict.fromkeys(n for n, _ in gaps))
    return (f"duties_open[{names}]",
            f"`{rel}` is fail-to-pass; the checks after that are not done.\n\n"
            + "\n\n".join(f"* {g}" for _, g in gaps))


def targets_for_gold(box: Sandbox, instance: dict[str, Any]) -> list[str]:
    """What to run when the candidate is the developer's own test.

    pytest repos can be handed exact node ids. django and sympy cannot -- django's ids
    are sometimes a test's docstring and sympy's carry no path -- so those run the whole
    module the test patch touches and the outcome is read out of the output.
    """
    if E.runner_for(box)["args"] == "nodes":
        return json.loads(instance["FAIL_TO_PASS"])
    return E.patched_test_files(instance["test_patch"])


def _decide(iid: str, repo: str, base: dict, head: dict, targets: list[str],
            expected: list[str] | None, base_log: str, head_log: str) -> Verdict:
    """The fail-to-pass verdict, from the two runs and nothing else.

    Pure: it touches no container. That is what lets it run before the patch is reverted,
    which in turn is what lets coverage be measured only for the tests that earned it.
    """
    if expected is not None:
        # Gold test: we know exactly which ids must flip, so check those and nothing else.
        pairs = [(n, E.outcome_of(base, n), E.outcome_of(head, n))
                 for n in expected]
        flipped = [n for n, b, h in pairs if b in BEHAVIOURAL and h == "PASSED"]
        missing = [n for n, b, _ in pairs if b is None]
    else:
        failed_before = {n for n, s in base.items() if s in BEHAVIOURAL}
        passed_after = {n for n, s in head.items() if s == "PASSED"}
        flipped = sorted(failed_before & passed_after)
        missing = []

    v = Verdict(instance_id=iid, f2p="NO", why="", f2p_nodes=flipped,
                base=base, head=head, targets=targets,
                base_log=base_log, head_log=head_log)

    # "Still failing after the fix" has to be scoped to the tests we are judging.
    #
    # A generated test lives in its own file, so every outcome belongs to us and all of
    # them must pass at head. The gold path is different: django and sympy cannot be
    # given node ids, so they run whole modules -- and sympy's test_numbers.py contains
    # test_mpmath_issues, which fails at base *and* at head, entirely unrelated to this
    # patch. Judging on every outcome in the module made a correct instance look like a
    # broken test.
    if expected is not None:
        still_failing = [n for n in expected
                         if E.outcome_of(head, n) in BEHAVIOURAL]
    else:
        still_failing = [n for n, s in head.items() if s in BEHAVIOURAL]

    # Passed before the fix and fails after it: the test found the behaviour and asserts
    # the side the fix removes. "Still failing" was false of these -- they never failed.
    backwards = [n for n in still_failing if E.outcome_of(base, n) == "PASSED"]
    if not base and not head:
        v.f2p, v.why = "BROKEN", "nothing collected on either side -- the file never ran"
    elif missing:
        v.f2p = "BROKEN"
        v.why = (f"{len(missing)} expected test(s) never appeared in the output "
                 f"({missing[:2]}) -- runner or parser problem, not a result")
    elif not head:
        v.f2p = "NO"
        v.why = "nothing collected after the fix -- the file stops importing once it is applied"
    elif still_failing and len(backwards) == len(still_failing):
        v.f2p = "NO"
        v.why = (f"backwards: passes before the fix and fails after ({backwards[:2]}) -- "
                 f"it asserts the behaviour the fix removes")
    elif still_failing:
        v.f2p = "NO"
        first = [n for n in still_failing if n not in backwards] + backwards
        v.why = (f"still failing after the fix ({first[:2]}) -- "
                 f"the test is wrong, not the code")
    elif not flipped:
        v.f2p = "NO"
        v.why = ("passes before the fix too, so it does not test the change"
                 if any(s == "PASSED" for s in base.values())
                 else "skipped before the fix, so it never ran against the bug"
                 if base and all(s == "SKIPPED" for s in base.values())
                 else "produced no usable failure before the fix")
    else:
        v.f2p = "YES"
        v.why = f"{len(flipped)} test(s) fail before the fix and pass after"
    return v


def verify(
    instance: dict[str, Any],
    box: Sandbox,
    *,
    generated_test: str | None = None,
    test_path: str = "",
    use_gold_test: bool = False,
    coverage: bool = True,
    quiet: bool = False,
) -> Verdict:
    """Run one candidate test on both states of the code inside `box`.

    The caller owns the sandbox, because the agent needs to work in the same container
    the verdict is computed in -- otherwise it is verifying a different tree than the
    one the agent saw.
    """
    iid, repo = instance["instance_id"], instance["repo"]

    if use_gold_test:
        box.apply_patch(instance["test_patch"])
        targets = targets_for_gold(box, instance)
        expected = json.loads(instance["FAIL_TO_PASS"])
    elif generated_test is not None:
        # `test_path` when the caller resolved one, because under `--repo-search` the
        # directory is the agent's choice and deriving it here quietly relocates the
        # file. That cost a run: an agent put its test in django's `tests/auth_tests/`,
        # beside the model it imports, wrote `from .models import ...` -- correct there
        # -- and this line moved the file to `tests/`, where there is no parent package.
        # The verdict came back "the test is wrong, not the code" about an import error
        # the harness had created.
        #
        # The fallback still probes with the box. Without it the answer is `tests/`, and
        # pytest's own repository has no such directory -- the agent wrote to `testing/`
        # where the briefing correctly pointed it, while the verdict was computed on an
        # empty file at `tests/`, reporting "nothing collected on either side" for a
        # test that was fine. Same failure, one layer earlier.
        rel = test_path or gen_test_path(iid, box)
        box.write(rel, generated_test)
        flow.record(flow.VERIFY, "install test", f"{rel} "
                    f"({generated_test.count(chr(10)) + 1} lines)")
        targets = [rel]
        expected = None            # node ids are unknown until it runs
    else:
        raise ValueError("verify() needs generated_test= or use_gold_test=True")

    def side(label: str) -> tuple[dict[str, str], str]:
        flow.record(flow.VERIFY, f"run {label.strip()}", f"targets={targets}")
        r = box.exec(E.test_command(box, targets), timeout=3600)
        outcomes = E.parse_output(r.output)
        tally = {}
        for st in outcomes.values():
            tally[st] = tally.get(st, 0) + 1
        flow.record(flow.VERIFY, f"result {label.strip()}",
                    ", ".join(f"{k.lower()}={v}" for k, v in sorted(tally.items()))
                    or "nothing collected")
        if not quiet:
            counts: dict[str, int] = {}
            for s in outcomes.values():
                counts[s] = counts.get(s, 0) + 1
            print(f"    {label}: " + (", ".join(f"{k.lower()}={v}" for k, v in
                                                sorted(counts.items()))
                                      or "nothing collected"))
        return outcomes, r.output

    # The agent can now apply the patch itself (its `verify` tool does exactly that), so
    # the tree's state is checked rather than assumed. A patch left applied would make
    # this "before" run actually be the after run, and the verdict would invert with
    # nothing on screen to say so.
    state = box.ensure_base(instance["patch"])
    if state != "base":
        flow.record(flow.VERIFY, "tree state", f"unexpected: {state}")
        return Verdict(instance_id=iid, f2p="BROKEN",
                       why=f"the working tree is not at base ({state}) -- something "
                           f"modified the source outside the test file",
                       targets=targets)

    base, base_log = side("before fix")
    # Snapshot the files the patch will touch, while the tree is still at base. Their
    # line numbers after the patch are worked out by comparing against these, not by
    # trusting the diff's own offsets.
    base_files = {p: text for p in E.patched_source_files(instance["patch"])
                  if (text := box.read(p)) is not None}
    box.apply_patch(instance["patch"])
    cov: dict = {}
    try:
        head, head_log = side("after fix ")
        v = _decide(iid, repo, base, head, targets, expected, base_log, head_log)
        # Only for a test that is actually fail-to-pass. "How much of the patch did this
        # test execute" presumes the test demonstrates the patch, and for a NO or a
        # BROKEN it presumes something false: astropy-7336 came back BROKEN carrying a
        # coverage of 100%, two numbers that cannot both be about the same test. The
        # metric is a property of a working test, so it is measured only once there is
        # one -- but still here, inside the window where the patch is applied, because
        # the lines it adds do not exist at any other moment.
        if coverage and v.f2p == "YES":
            cov = E.changed_line_coverage(box, targets, instance["patch"],
                                          base_files=base_files)
            v.changed_line_coverage = cov
    finally:
        box.apply_patch(instance["patch"], revert=True)

    if cov.get("measured"):
        flow.record(flow.VERIFY, "changed-line coverage",
                    f"{cov['percent']}% ({cov['covered']}/"
                    f"{cov['executable_changed_lines']} executable changed lines)")
    elif cov:
        flow.record(flow.VERIFY, "changed-line coverage", f"not measured: {cov['reason']}")
    elif coverage and v.f2p != "YES":
        flow.record(flow.VERIFY, "changed-line coverage",
                    f"not measured: the verdict is {v.f2p}, and coverage of a test that "
                    f"is not fail-to-pass says nothing about the patch")
    flow.record(flow.VERIFY, "verdict", f"{v.f2p} -- {v.why}",
                f2p_nodes=v.f2p_nodes)
    if not quiet:
        print(f"    {v.line()}")
    return v
