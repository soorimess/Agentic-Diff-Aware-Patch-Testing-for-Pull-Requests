"""The F2P decision. One implementation, used by every arm.

This exists because there were two. The oracle had the base/head comparison inlined and
the agent had its own copy, and they had already drifted -- the agent's ran on the host
while the oracle's ran in a container. Two arms running different verification code
cannot be compared: any difference in their numbers is partly a difference in how they
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
from typing import Any

from openhands_f2p import flow
from openhands_f2p import swebench_env as E
from openhands_f2p.swebench_env import Sandbox

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
        # With the box, so the probe can look. Without it the fallback is `tests/`,
        # and pytest's own repository has no such directory -- the agent wrote its test
        # to `testing/` (where the briefing correctly pointed it) while the verdict was
        # computed on an empty file at `tests/`, giving "nothing collected on either
        # side" for a test that was fine.
        rel = gen_test_path(iid, box)
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
