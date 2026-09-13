"""OpenHands tools whose executors run inside the SWE-bench container.

Why these exist rather than the built-in ones
---------------------------------------------
An OpenHands tool call is: the model names a tool and passes JSON, the agent validates
that into an Action, and then calls the tool's *executor*. The executor is the only part
that touches anything real -- the schema is just how the model states an intention.

The built-in TerminalTool's executor spawns tmux panes on the host. So with the built-in
tools, nothing in the loop ever creates a container: the agent works on the host, which
on this machine has direct internet (measured: pypi.org 200, github.com 200,
`git ls-remote https://github.com/psf/requests` succeeds). An agent there can simply
`pip download requests==2.28` and read both the fix and the developer's test out of a
later release.

Swapping the executor -- same protocol, same model behaviour -- routes every action
through `Sandbox.exec` into a container started with `--network none`, where that same
pip command fails on DNS. One function then carries three jobs at once: the isolation
boundary, the audit log, and the place the arbiter will decide whether the harness or
the model makes a given call.

Three tools, deliberately not more:

  run          a shell, for reading and searching. `grep`/`ls`/`cat` need no wrapper.
  write_file   multi-line writes, because doing that through a shell heredoc is where
               models reliably mangle quoting.
  run_tests    repo-aware. The agent should not have to know that django needs
               `./tests/runtests.py <label>` and sympy needs `bin/test -C <path>`; that
               knowledge is ours and belongs in the harness.
"""
from __future__ import annotations

from pydantic import Field

from openhands.sdk.tool import (
    Action,
    Observation,
    ToolAnnotations,
    ToolDefinition,
    ToolExecutor,
    register_tool,
)

from openhands_f2p import swebench_env as E
from openhands_f2p.features import FeatureSet
from openhands_f2p.swebench_env import REPO_DIR, Sandbox

MAX_OUTPUT = 4000        # what comes back to the model, per call
RUN_TIMEOUT = 120        # a shell command for reading or searching
TEST_TIMEOUT = 1800      # a test suite, which legitimately can take a while
# Was 12000. Eight `run` calls at that size is roughly 25k tokens of context, and the
# request that carried them timed out. Test output is the long thing here and its
# useful part is the head and the tail, so clipping loses little.


def _clip(text: str, limit: int = MAX_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    half = limit // 2
    return (text[:half] + f"\n\n... [{len(text) - limit} characters omitted] ...\n\n"
            + text[-half:])


# --------------------------------------------------------------------------- run
class RunAction(Action):
    command: str = Field(description="Shell command to run inside the repository.")


class RunObservation(Observation):
    pass


class RunExecutor(ToolExecutor[RunAction, RunObservation]):
    def __init__(self, box: Sandbox, log: list | None = None):
        self.box = box
        self.log = log if log is not None else []

    def __call__(self, action: RunAction, conversation=None) -> RunObservation:
        # 120s, not 900. `run` is for reading and searching; nothing legitimate there
        # takes two minutes, and a runaway recursive grep used to burn fifteen.
        r = self.box.exec(action.command, timeout=RUN_TIMEOUT)
        self.log.append({"tool": "run", "command": action.command,
                         "returncode": r.returncode, "output": r.output[:4000]})
        body = _clip(r.output) or "(no output)"
        return RunObservation.from_text(
            f"exit code {r.returncode}\n{body}", is_error=r.returncode != 0)


class SandboxRunTool(ToolDefinition[RunAction, RunObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None,
               log: list | None = None, **params):
        assert box is not None, "SandboxRunTool needs a Sandbox"
        return [cls(
            name="run",
            description=(
                f"Run a shell command inside the repository at {REPO_DIR}. "
                "Use it to search and read: grep, ls, cat, sed. There is no network, "
                f"and a command is killed after {RUN_TIMEOUT}s -- keep searches inside "
                "the repository rather than starting from / or .."),
            action_type=RunAction,
            observation_type=RunObservation,
            annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
            executor=RunExecutor(box, log),
        )]


# -------------------------------------------------------------------- write_file
class WriteAction(Action):
    path: str = Field(description="Path to write, relative to the repository root.")
    content: str = Field(description="Full contents of the file.")


class WriteObservation(Observation):
    pass


class WriteExecutor(ToolExecutor[WriteAction, WriteObservation]):
    def __init__(self, box: Sandbox, log: list | None = None):
        self.box = box
        self.log = log if log is not None else []

    def __call__(self, action: WriteAction, conversation=None) -> WriteObservation:
        try:
            self.box.write(action.path, action.content)
        except Exception as exc:
            self.log.append({"tool": "write_file", "path": action.path,
                             "error": str(exc)[:400]})
            return WriteObservation.from_text(f"write failed: {exc}", is_error=True)
        lines = action.content.count("\n") + 1
        self.log.append({"tool": "write_file", "path": action.path,
                         "lines": lines, "content": action.content[:4000]})
        return WriteObservation.from_text(f"wrote {action.path} ({lines} lines)")


class SandboxWriteTool(ToolDefinition[WriteAction, WriteObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None,
               log: list | None = None, **params):
        assert box is not None, "SandboxWriteTool needs a Sandbox"
        return [cls(
            name="write_file",
            description=("Create or overwrite a file with the exact contents given. "
                         "Use this for the test file rather than shell redirection."),
            action_type=WriteAction,
            observation_type=WriteObservation,
            annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True),
            executor=WriteExecutor(box, log),
        )]


# --------------------------------------------------------------------- run_tests
class TestAction(Action):
    target: str = Field(
        description="A test file path, or a specific test to run. "
                    "The correct runner for this repository is chosen for you.")


class TestObservation(Observation):
    pass


class TestExecutor(ToolExecutor[TestAction, TestObservation]):
    def __init__(self, box: Sandbox, repo: str, log: list | None = None,
                 reveal_runner: bool = True):
        self.box = box
        self.repo = repo
        self.log = log if log is not None else []
        self.reveal_runner = reveal_runner
        """Whether the observation may quote the command it ran. With `repo-facts`
        withheld the runner is exactly what the agent is supposed to work out, and one
        echoed `$ ./tests/runtests.py --verbosity 2 auth_tests.test_x` hands over both
        the command and the label convention. The tool still runs; it just stops
        narrating. The log keeps the command either way -- that is for us."""

    def __call__(self, action: TestAction, conversation=None) -> TestObservation:
        command = E.test_command(self.box, [action.target])
        r = self.box.exec(command, timeout=TEST_TIMEOUT)
        outcomes = E.parse_output(r.output)
        self.log.append({"tool": "run_tests", "target": action.target,
                         "command": command, "returncode": r.returncode,
                         "outcomes": outcomes, "output": r.output[:4000]})
        summary = ", ".join(f"{k.split('::')[-1]}: {v}"
                            for k, v in list(outcomes.items())[:12]) or "no tests ran"
        head = f"$ {command}" if self.reveal_runner else f"ran {action.target}"
        return TestObservation.from_text(
            f"{head}\nexit code {r.returncode}\n{summary}\n\n{_clip(r.output)}",
            is_error=not outcomes)


class SandboxTestTool(ToolDefinition[TestAction, TestObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               log: list | None = None, reveal_runner: bool = True, **params):
        assert box is not None and repo, "SandboxTestTool needs a Sandbox and a repo"
        # The tool schema reaches the model before it takes a single action, and it used
        # to carry `runner_for(box)["cmd"]` verbatim -- django's
        # `./tests/runtests.py --verbosity 2`. That is the most repo-specific fact the
        # harness computes, and it was being handed over in `--repo-search` runs whose
        # whole point is to withhold it. The prompt scan could not see it either: that
        # reads the assembled prompt, and this is a tool description.
        #
        # So the runner is named only when the briefing names it too. The capability is
        # identical in both; only the knowledge differs.
        if reveal_runner:
            what = (f"Invokes `{E.runner_for(box)['cmd']}` for you, so pass a test file "
                    f"path (or a pytest node id where that applies) and nothing else.")
        else:
            what = ("Runs it with this project's own test runner, whatever that is, so "
                    "pass a test file path (or a pytest node id where that applies) and "
                    "nothing else.")
        return [cls(
            name="run_tests",
            description=f"Run tests in this repository. {what}",
            action_type=TestAction,
            observation_type=TestObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=TestExecutor(box, repo, log, reveal_runner=reveal_runner),
        )]



# ------------------------------------------------------------------- coverage
class CoverageAction(Action):
    target: str = Field(
        description="The test file to measure, same value you would pass to run_tests.")


class CoverageObservation(Observation):
    pass


class CoverageExecutor(ToolExecutor[CoverageAction, CoverageObservation]):
    """How much of the pull request's change the test actually executes.

    One definition, and it is the same number the harness scores: of the executable
    lines this PR changed, what fraction did your test run. Measured with the patch
    applied, because the lines it adds do not exist at any other moment -- and always
    reverted afterwards, so the tree is left where the agent found it.
    """

    def __init__(self, box: Sandbox, repo: str, patch: str, log: list | None = None):
        self.box = box
        self.repo = repo
        self.patch = patch
        self.log = log if log is not None else []

    def __call__(self, action: CoverageAction, conversation=None) -> CoverageObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return CoverageObservation.from_text(
                "cannot measure: the working tree is in an unexpected state "
                f"({state}) -- some file was modified outside the test", is_error=True)
        self.box.apply_patch(self.patch)
        try:
            cov = E.changed_line_coverage(self.box, [action.target], self.patch)
        finally:
            self.box.apply_patch(self.patch, revert=True)

        self.log.append({"tool": "coverage", "target": action.target, "result": cov})
        if not cov.get("measured"):
            return CoverageObservation.from_text(
                f"could not measure change coverage: {cov.get('reason')}", is_error=True)

        lines = [f"Your test executes {cov['percent']}% of the lines this pull request "
                 f"changed ({cov['covered']} of {cov['executable_changed_lines']} "
                 f"executable changed lines)."]
        if not cov["missed"]:
            lines.append("Every executable changed line is covered. Nothing to add.")
            return CoverageObservation.from_text("\n".join(lines))

        # The source and the guards, not just the numbers. "line 1631 is uncovered" is
        # not something an agent can act on; "line 1631 is `Q *= q.p`, and it sits under
        # `if not isinstance(q, SYMPY_INTS)`" says exactly what the input has to look
        # like for that line to run.
        lines += ["", "These changed lines never ran. For each one you can see the code "
                      "and the conditions above it -- those conditions are what your "
                      "input has to satisfy:", ""]
        for item in cov.get("missed_source") or []:
            lines.append(f"  {item['ref']}")
            for g in item["guards"]:
                lines.append(f"      {g}")
            ref_ln = item["ref"].rpartition(":")[2]
            lines.append(f"    > {ref_ln}: {item['line']}")
            lines.append("")
        extra = len(cov["missed"]) - len(cov.get("missed_source") or [])
        if extra > 0:
            lines.append(f"  ... and {extra} more uncovered changed lines")
        lines += ["Pick inputs that make those conditions true, or add a second case to "
                  "the same test file. Then measure again."]
        return CoverageObservation.from_text("\n".join(lines))


class SandboxCoverageTool(ToolDefinition[CoverageAction, CoverageObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="coverage",
            description=("Measure what fraction of the pull request's changed lines your "
                         "test executes, and list the changed lines it misses."),
            action_type=CoverageAction,
            observation_type=CoverageObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=CoverageExecutor(box, repo, patch, log),
        )]


# --------------------------------------------------------------------- verify
class VerifyAction(Action):
    target: str = Field(
        description="The test file to check, same value you would pass to run_tests.")


class VerifyObservation(Observation):
    pass


class VerifyExecutor(ToolExecutor[VerifyAction, VerifyObservation]):
    """Whether the test is fail-to-pass, checked the way the harness checks it.

    This tool exists now only because the agent is shown the change. While the change
    was hidden, letting the agent apply it would have handed over the answer -- so the
    F2P check had to stay behind the harness, and the agent could see its test fail but
    never see it pass. With the diff already in the prompt, that reason is gone, and
    withholding the check just left the agent guessing at the half of the criterion it
    could not observe.

    The harness still runs its own verification after the agent finishes. This is the
    agent's instrument; that one is the measurement.
    """

    def __init__(self, box: Sandbox, repo: str, patch: str, log: list | None = None,
                 reveal_missed: bool = True):
        self.box = box
        self.repo = repo
        self.patch = patch
        self.log = log if log is not None else []
        # Whether `coverage` is registered alongside. Without it there is no tool to
        # send the agent to, and naming one it does not have is exactly the failure the
        # prompt scan catches -- one layer later, in a tool's own output, where no scan
        # reaches.
        self.reveal_missed = reveal_missed

    def __call__(self, action: VerifyAction, conversation=None) -> VerifyObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return VerifyObservation.from_text(
                f"cannot verify: the working tree is in an unexpected state ({state})",
                is_error=True)
        cmd = E.test_command(self.box, [action.target])
        before = self.box.exec(cmd, timeout=3600)
        base_out = E.parse_output(before.output)
        self.box.apply_patch(self.patch)
        missed = ""
        try:
            after = self.box.exec(cmd, timeout=3600)
            head_out = E.parse_output(after.output)
            # Inside the patched window, which is the only moment the lines the change
            # adds exist at all. Computed here rather than after the revert -- doing it
            # afterwards measures coverage of a tree where those line numbers hold
            # different code, and the run fails outright.
            if {n for n, v in base_out.items() if v in ("FAILED", "ERROR")} & {
                    n for n, v in head_out.items() if v == "PASSED"}:
                missed = self._reach(action.target)
        finally:
            self.box.apply_patch(self.patch, revert=True)

        failed_before = {n for n, v in base_out.items() if v in ("FAILED", "ERROR")}
        passed_after = {n for n, v in head_out.items() if v == "PASSED"}
        flipped = sorted(failed_before & passed_after)
        still_failing = [n for n, v in head_out.items() if v in ("FAILED", "ERROR")]
        self.log.append({"tool": "verify", "target": action.target,
                         "before": base_out, "after": head_out, "flipped": flipped})

        if not base_out and not head_out:
            head = "NOT fail-to-pass: nothing was collected -- the file does not import."
        elif still_failing:
            head = (f"NOT fail-to-pass: {still_failing[:3]} still fail after the change "
                    f"is applied. The test is wrong, not the code.")
        elif not flipped:
            head = ("NOT fail-to-pass: the test already passes before the change, so it "
                    "does not exercise this pull request.")
        else:
            head = f"Fail-to-pass: {len(flipped)} test(s) fail before and pass after."

        # Reported here rather than left for the agent to ask about. The `coverage` tool
        # already offered this, and across twenty-six runs it was called twelve times --
        # every one of them last, with nothing after it, and every one already reaching
        # the whole change. It was a formality, never feedback, because asking was a
        # decision the agent only made once it was confident. This removes the decision.
        #
        # Lines, not a percentage. A percentage is a score, and a score in front of the
        # agent is a score to raise; a list of lines it did not reach is a fact about the
        # code, and the conditions above each one say what the input has to look like.
        body = (f"\n\nbefore the change:\n{_clip(before.output, 1800)}"
                f"\n\nafter the change:\n{_clip(after.output, 1200)}"
                if base_out or head_out else "")
        return VerifyObservation.from_text(head + missed + body, is_error=not flipped)

    def _reach(self, target: str) -> str:
        """How much of the change this test runs, and what to do if it is not all of it.

        A pointer, not the answer. Earlier this printed the missed lines here in full,
        which made `coverage` redundant -- the agent had everything already and never
        called it. Naming the shortfall and naming the tool that explains it keeps both:
        the agent cannot miss that something is unfinished, and the explaining is still
        the other tool's job.

        No percentage is shown when the test reaches everything either; "all of them" is
        a fact, and a figure invites raising a figure.
        """
        try:
            cov = E.changed_line_coverage(self.box, [target], self.patch)
        except Exception:
            return ""
        if not cov.get("measured"):
            return ""
        missed = len(cov.get("missed") or [])
        if not missed:
            return "\n\nIt runs every line this pull request changed."
        total = cov["executable_changed_lines"]
        head = (f"\n\nIt runs {cov['covered']} of the {total} lines this pull request "
                f"changed; {missed} never execute.")
        where = (" Call `coverage` on this file to see which they are, the code on each "
                 "one and the conditions above it."
                 if self.reveal_missed else
                 " Which ones is not something you can be shown here, so work back from "
                 "the behaviour: the change has more than one path through it and your "
                 "input took one.")
        return (head + where +
                " Then decide: part of the behaviour you set out to pin down and worth "
                "another assertion, a separate case that deserves its own test "
                "function, or genuinely outside what this test is for. If you change "
                "the test, run `verify` again -- a new test is a new answer and the "
                "old one no longer describes it.")


class SandboxVerifyTool(ToolDefinition[VerifyAction, VerifyObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, reveal_missed: bool = True,
               **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="verify",
            description=("Check whether your test is fail-to-pass: run it on the code "
                         "before the change, apply the change, run it again. Reverts the "
                         "change afterwards."),
            action_type=VerifyAction,
            observation_type=VerifyObservation,
            annotations=ToolAnnotations(readOnlyHint=False),
            executor=VerifyExecutor(box, repo, patch, log, reveal_missed),
        )]


def register(box: Sandbox, repo: str, log: list, patch: str = "",
             features: FeatureSet | None = None, gen_path: str = "",
             version: str = "") -> list[str]:
    """Register the agent's tools against one sandbox. Returns their names.

    Which tools exist is part of the run's configuration, and the registry in `features`
    is the single place that says so -- each `Feature` names the tools that live and die
    with it. A withheld feature leaves its tools out rather than registering a degraded
    version of them, so the difference between two configurations is the component
    itself and not the same component answering worse.

    `verify` and `coverage` both need the patch: without it there is no second state to
    run a test against, and nothing to measure coverage of.
    """
    features = features if features is not None else FeatureSet.of()
    briefed = "repo-facts" in features
    made = {"run": SandboxRunTool.create(box=box, log=log)[0],
            "write_file": SandboxWriteTool.create(box=box, log=log)[0],
            "run_tests": SandboxTestTool.create(box=box, repo=repo, log=log,
                                                reveal_runner=briefed)[0]}
    for n, tool in made.items():
        register_tool(n, tool)
    names = ["run", "write_file", "run_tests"]
    # `patch` here is the harness's copy, held by the executor and applied by it. It is
    # not the same question as whether the agent was *shown* the diff: `verify` reports
    # whether the agent's test flips without quoting a line of it, so it survives
    # `--no-patch`. `coverage` does not -- it prints the source of the lines the test
    # missed, which is the diff.
    if "verify-tool" in features:
        register_tool("verify", SandboxVerifyTool.create(
            box=box, repo=repo, patch=patch, log=log,
            reveal_missed=("coverage-tool" in features))[0])
        names.append("verify")
        if "coverage-tool" in features:
            register_tool("coverage", SandboxCoverageTool.create(
                box=box, repo=repo, patch=patch, log=log)[0])
            names.append("coverage")
    _check_no_leak(made, box, features)
    return names


def _check_no_leak(made: dict, box: Sandbox, features: FeatureSet) -> None:
    """No tool may name the runner while `repo-facts` is withheld.

    The prompt has had this guarantee since the feature registry existed -- `build`
    refuses to assemble text that names an unregistered tool. Tool *descriptions* had no
    such check, and that is precisely where the leak was: `run_tests` carried
    `./tests/runtests.py --verbosity 2` into every `--repo-search` run for django. The
    two channels reach the same model, so they need the same guarantee.
    """
    if "repo-facts" in features:
        return
    runner = E.runner_for(box)["cmd"].split()[0]
    named = sorted(n for n, t in made.items()
                   if runner in getattr(t, "description", ""))
    if named:
        raise AssertionError(
            f"the description of {', '.join(named)} names {runner!r}, which "
            f"--repo-search exists to withhold. The agent reads tool descriptions "
            f"before it acts, so this hands over the runner as surely as the briefing "
            f"would.")
