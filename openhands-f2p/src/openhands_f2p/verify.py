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
    flow.record(flow.VERIFY, "second-chance probe",
                f"{rel}: " + (", ".join(sorted(set(outcomes.values()))) or "nothing collected"))
    if not outcomes:
        return ("collects_nothing",
                f"`{rel}` exists but running it collects no tests. Either the file has "
                f"no test function this project's runner recognises, or it fails to "
                f"import. Run it yourself and read the error.")
    if all(st == "PASSED" for st in outcomes.values()):
        return ("passes_at_base",
                f"Every test in `{rel}` passes on this code. The bug is still present "
                f"here, so a test that already passes is not testing the change -- "
                f"whatever it checks was true before the fix as well.")
    return None


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
    except Exception:                                           # noqa: BLE001
        cov = {}
    finally:
        box.apply_patch(patch, revert=True)
    # A test that never imports the changed file leaves no entry for it in the coverage
    # report, and the metric calls that unmeasurable -- right for a score, wrong here: it
    # is the plainest case of not reaching the change. django-16333's first live refusal
    # went out with no diagnosis for exactly this reason.
    if not cov.get("measured") and cov.get("reason") != "the changed file was never imported by this test":
        return ""
    flow.record(flow.VERIFY, "second-chance reach",
                f"{rel}: runs {cov.get('covered', 0)} of the changed lines"
                + ("" if cov.get("measured") else " (changed file never imported)"))
    if not cov.get("covered"):
        return ("\n\n**It does not reach the change.** Running it executes none of the "
                "lines this pull request changes, so whatever it asserts is about code the "
                "fix does not touch. Keep the idea and move the input: call the code the "
                "change modifies, with an input that sends execution through the changed "
                "lines. `coverage` shows which they are and the conditions above each.")
    return ("\n\n**It does reach the change, and still passes before the fix.** It runs "
            "lines this pull request changes, so the input is aimed at the right code -- "
            "the assertion is what is wrong: it checks something that is true both before "
            "and after the change. Keep the input. Work out what the changed lines compute "
            "differently, and assert that value or behaviour instead.")


def verify_settled(tool_log: list) -> bool:
    """Whether the test is fail-to-pass by the agent's own last `verify`, unchanged since."""
    found = [(i, e) for i, e in enumerate(tool_log) if e.get("tool") == "verify"]
    if not found:
        return False
    i, e = found[-1]
    still = [n for n, st in (e.get("after") or {}).items() if st in BEHAVIOURAL]
    wrote = any(x.get("tool") == "write_file" for x in tool_log[i + 1:])
    return bool(e.get("flipped")) and not still and not wrote


def loop_gap(tool_log: list, instruments: tuple[str, ...],
             rel: str) -> tuple[str, str] | None:
    """Whether the finishing loop actually closed, read off the agent's own actions.

    The earlier version of this asked only whether each tool *appeared* in the log, and
    that was the same Goodhart mistake the prompt rules are written to avoid: it measured
    the call instead of the answer. Four of five failures in the run that introduced it
    ended immediately after `verify` reported NOT fail-to-pass -- requirement satisfied,
    goal unmet -- while `pylint-7277` called `verify` seventeen times and `matplotlib`
    once. The count carried almost no information about whether the loop had closed.

    So each instrument is judged by what it last said and whether that answer still
    describes the file on disk:

    They are checked **in order**, and only the first open one is reported. Until the
    test is fail-to-pass the other two are questions about a test that does not exist
    yet, and asking all three at once told the qwen run to go measure something it had
    not built -- eight `coverage` and `mutation` calls before `verify` had ever flipped,
    one of which `mutation` answered with "your test does not pass on the fixed code
    yet". The tool knew the demand was premature. The demand was made anyway.

    `verify`   must have been called, must last have reported fail-to-pass, and nothing
               may have been written since -- an answer about a file that has been edited
               is an answer about a file that no longer exists. While this is open it is
               the *only* thing said.
    `coverage` must have been called, and if it last listed missed lines the agent must
               have edited the test after seeing them. The agent is shown lines, never a
               percentage: the percentage is what the report publishes, and a number the
               agent is told to push up stops measuring anything. The demand enforced
               here is that missed lines were answered rather than read and passed over,
               since a line can be genuinely unreachable and an assertion written only to
               execute one is worth less than saying why.
    `mutation` must have been called, and that is all. Survivors are for the agent to
               weigh -- some are genuinely outside what the change fixes -- and requiring
               a response would be an instruction to close the list rather than to
               understand it. Read `astropy-13398` before loosening this: mutation
               reported 0 of 10 killed, the agent added a second test to answer it, the
               new test failed on both sides, and a file whose first test flipped
               correctly scored NO.

    Pure, and reads only the agent's own record, so nothing here can leak the head run.
    Returns `(reason, what_to_say)` or `None` when the loop is closed.
    """
    def last(tool: str) -> tuple[int, dict] | None:
        found = [(i, e) for i, e in enumerate(tool_log) if e.get("tool") == tool]
        return found[-1] if found else None

    def wrote_after(i: int) -> bool:
        return any(e.get("tool") == "write_file" for e in tool_log[i + 1:])

    # One obligation at a time, in the order the goal imposes. Until the test is
    # fail-to-pass there is nothing for `coverage` or `mutation` to be about: coverage
    # asks how much of the change a working test reaches, and mutation asks what a
    # working test would notice -- both are questions about a test that has already met
    # the bar. Asking all three at once is what the qwen run did, and it produced eight
    # calls to those two tools before `verify` had ever flipped, one of which `mutation`
    # answered with "your test does not pass on the fixed code yet". The tool said the
    # demand was premature; the demand was made anyway.
    gaps = []
    settled = "verify" not in instruments      # nothing to establish if it was withheld
    if "verify" in instruments:
        got = last("verify")
        if got is None:
            gaps.append(f"You never called `verify`, so nothing has established the one "
                        f"property the test must have. Write a test, call `verify`, and "
                        f"keep going until it says fail-to-pass.")
        else:
            i, e = got
            still = [n for n, st in (e.get("after") or {}).items() if st in BEHAVIOURAL]
            if not e.get("flipped") or still:
                said = (f"{len(still)} test(s) still failing after the change"
                        if still else "nothing flipped")
                gaps.append(f"The last `verify` said **not fail-to-pass** -- {said}. That "
                            f"is the answer to the only question that decides this run, "
                            f"and the test has not changed since. Rewrite the test and "
                            f"call `verify` again, and keep doing that until it says "
                            f"fail-to-pass. Nothing else you could do with the remaining "
                            f"budget counts for anything while this is the answer.")
            elif wrote_after(i):
                gaps.append(f"You edited the test after the last `verify`, so the "
                            f"fail-to-pass result describes a file that no longer exists. "
                            f"Call `verify` again on what is on disk now.")
            else:
                settled = True

    # Below this line every obligation is about a test that already flips. When it does
    # not, the message stays a single instruction rather than a list of three, two of
    # which the agent cannot act on yet.
    if not settled:
        return ("loop_open", f"The finishing loop on `{rel}` is not closed.\n\n"
                             + "\n\n".join(f"* {g}" for g in gaps)) if gaps else None

    if "coverage" in instruments:
        got = last("coverage")
        if got is None:
            gaps.append(f"Your test is fail-to-pass. Now call `coverage`: how much of "
                        f"the change it reaches is the next question, and it is "
                        f"currently unknown.")
        else:
            i, e = got
            cov = e.get("result") or {}
            if cov.get("measured") and cov.get("missed") and not wrote_after(i):
                gaps.append(f"`coverage` last listed lines of the change your test never "
                            f"runs, and you changed nothing after reading it. Keep "
                            f"changing the test and calling `coverage` until every "
                            f"changed line runs or you can say why a line is out of "
                            f"reach. Work the missed lines one at a time: decide for "
                            f"each whether it is the same behaviour by another route, a "
                            f"separate case that deserves its own test, or genuinely "
                            f"outside this test -- then act on that and call `coverage` "
                            f"again. An assertion added only to execute a line is worth "
                            f"less than an honest reason it stays unreached.")
    if "mutation" in instruments and last("mutation") is None:
        gaps.append(f"You never called `mutation`. Call it and read the survivors: each "
                    f"is a wrong version of this change your test cannot tell from the "
                    f"right one. You are not required to close them -- some are outside "
                    f"what the pull request fixes -- but you are required to have looked, "
                    f"because it is the only check that asks whether your assertions "
                    f"have force.")
    if not gaps:
        return None
    return ("loop_open", f"The finishing loop on `{rel}` is not closed.\n\n"
                         + "\n\n".join(f"* {g}" for g in gaps))


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

    if not base and not head:
        v.f2p, v.why = "BROKEN", "nothing collected on either side -- the file never ran"
    elif missing:
        v.f2p = "BROKEN"
        v.why = (f"{len(missing)} expected test(s) never appeared in the output "
                 f"({missing[:2]}) -- runner or parser problem, not a result")
    elif still_failing:
        v.f2p = "NO"
        v.why = (f"still failing after the fix ({still_failing[:2]}) -- "
                 f"the test is wrong, not the code")
    elif not flipped:
        v.f2p = "NO"
        v.why = ("passes before the fix too, so it does not test the change"
                 if any(s == "PASSED" for s in base.values())
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
