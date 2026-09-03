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

from openhands_f2p import repo_info
from openhands_f2p import swebench_env as E
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
    def __init__(self, box: Sandbox, repo: str, log: list | None = None):
        self.box = box
        self.repo = repo
        self.log = log if log is not None else []

    def __call__(self, action: TestAction, conversation=None) -> TestObservation:
        command = E.test_command(self.repo, [action.target])
        r = self.box.exec(command, timeout=TEST_TIMEOUT)
        outcomes = E.parse_output(self.repo, r.output)
        self.log.append({"tool": "run_tests", "target": action.target,
                         "command": command, "returncode": r.returncode,
                         "outcomes": outcomes, "output": r.output[:4000]})
        summary = ", ".join(f"{k.split('::')[-1]}: {v}"
                            for k, v in list(outcomes.items())[:12]) or "no tests ran"
        return TestObservation.from_text(
            f"$ {command}\nexit code {r.returncode}\n{summary}\n\n{_clip(r.output)}",
            is_error=not outcomes)


class SandboxTestTool(ToolDefinition[TestAction, TestObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               log: list | None = None, **params):
        assert box is not None and repo, "SandboxTestTool needs a Sandbox and a repo"
        runner = E.runner_for(repo)["cmd"]
        return [cls(
            name="run_tests",
            description=(f"Run tests in this repository. Invokes `{runner}` for you, "
                         "so pass a test file path (or a pytest node id where that "
                         "applies) and nothing else."),
            action_type=TestAction,
            observation_type=TestObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=TestExecutor(box, repo, log),
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
            cov = E.changed_line_coverage(self.box, self.repo, [action.target],
                                          self.patch)
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

    def __init__(self, box: Sandbox, repo: str, patch: str, log: list | None = None):
        self.box = box
        self.repo = repo
        self.patch = patch
        self.log = log if log is not None else []

    def __call__(self, action: VerifyAction, conversation=None) -> VerifyObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return VerifyObservation.from_text(
                f"cannot verify: the working tree is in an unexpected state ({state})",
                is_error=True)
        cmd = E.test_command(self.repo, [action.target])
        before = self.box.exec(cmd, timeout=3600)
        base_out = E.parse_output(self.repo, before.output)
        self.box.apply_patch(self.patch)
        try:
            after = self.box.exec(cmd, timeout=3600)
            head_out = E.parse_output(self.repo, after.output)
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
        body = (f"\n\nbefore the change:\n{_clip(before.output, 1800)}"
                f"\n\nafter the change:\n{_clip(after.output, 1200)}"
                if base_out or head_out else "")
        return VerifyObservation.from_text(head + body, is_error=not flipped)


class SandboxVerifyTool(ToolDefinition[VerifyAction, VerifyObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="verify",
            description=("Check whether your test is fail-to-pass: run it on the code "
                         "before the change, apply the change, run it again. Reverts the "
                         "change afterwards."),
            action_type=VerifyAction,
            observation_type=VerifyObservation,
            annotations=ToolAnnotations(readOnlyHint=False),
            executor=VerifyExecutor(box, repo, patch, log),
        )]


# ------------------------------------------------------------- repo_info_finder
class RepoInfoAction(Action):
    pass


class RepoInfoObservation(Observation):
    pass


class RepoInfoExecutor(ToolExecutor[RepoInfoAction, RepoInfoObservation]):
    """How testing works in this project, answered by a sub-agent.

    Three properties, and each is about leakage.

    **No arguments.** A tool with a free-form path or query is a general file reader, and
    a general file reader is a channel: every guard then becomes a guess about what the
    forbidden answer looks like. With no input there is one fixed question.

    **A sub-agent, not a string check.** The earlier version scanned a template we wrote
    for lines of the developer's test -- which catches an exact substring and nothing
    else, and was checking our own output against a leak it could not have contained. The
    sub-agent is instead never *shown* the issue, the diff or the test patch, so it cannot
    leak them in paraphrase either, and its reply is filtered to six named fields so
    anything it volunteers has nowhere to land.

    **No web search.** Raised as an option; refused deliberately. The container has no
    network, but even with one, searching "psf/requests proxy 407" is the shortest path
    to the merged pull request and the developer's test -- the single thing the
    assignment says must stay hidden.
    """

    def __init__(self, box: Sandbox, repo: str, gen_path: str, version: str,
                 log: list | None = None):
        self.box = box
        self.repo = repo
        self.gen_path = gen_path
        self.version = version
        self.log = log if log is not None else []
        self._cached: str | None = None

    def __call__(self, action, conversation=None) -> RepoInfoObservation:
        # Cached: the answer cannot change during a run, and a second call would spend
        # another sub-agent request to say the same thing.
        if self._cached is None:
            try:
                info = repo_info.describe(self.box, self.repo, self.gen_path,
                                         self.version)
                self._cached = repo_info.render(info)
                self.log.append({"tool": "repo_info", "info": info})
            except Exception as exc:
                self._cached = (f"the conventions sub-agent failed ({exc!s:.120}). "
                                f"Read an existing test with `run` instead; this "
                                f"project's runner is "
                                f"{E.runner_for(self.repo)['cmd']}.")
                self.log.append({"tool": "repo_info", "error": str(exc)[:300]})
        return RepoInfoObservation.from_text(self._cached)


class SandboxRepoInfoTool(ToolDefinition[RepoInfoAction, RepoInfoObservation]):
    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               gen_path: str = "", version: str = "", log: list | None = None,
               **params):
        assert box is not None and repo, "SandboxRepoInfoTool needs a Sandbox and a repo"
        return [cls(
            name="repo_info",
            description=("How this project organises and runs its tests, at this "
                         "version: where tests live, how they are named and structured, "
                         "conventional fixtures, and the command that runs them. Takes "
                         "no arguments. Call it first."),
            action_type=RepoInfoAction,
            observation_type=RepoInfoObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=RepoInfoExecutor(box, repo, gen_path, version, log),
        )]


def register(box: Sandbox, repo: str, log: list, patch: str = "",
             coverage_tool: bool = True, gen_path: str = "",
             version: str = "") -> list[str]:
    """Register the agent's tools against one sandbox. Returns their names.

    `coverage` and `verify` both need the patch, and both exist only because the agent
    is shown it. Without a patch they are left out rather than silently degraded, which
    is what makes a blind arm a real comparison instead of the same arm with worse tools.
    """
    register_tool("run", SandboxRunTool.create(box=box, log=log)[0])
    register_tool("write_file", SandboxWriteTool.create(box=box, log=log)[0])
    register_tool("run_tests", SandboxTestTool.create(box=box, repo=repo, log=log)[0])
    register_tool("repo_info", SandboxRepoInfoTool.create(
        box=box, repo=repo, gen_path=gen_path, version=version, log=log)[0])
    names = ["run", "write_file", "run_tests", "repo_info"]
    if patch:
        register_tool("verify", SandboxVerifyTool.create(
            box=box, repo=repo, patch=patch, log=log)[0])
        names.append("verify")
        if coverage_tool:
            register_tool("coverage", SandboxCoverageTool.create(
                box=box, repo=repo, patch=patch, log=log)[0])
            names.append("coverage")
    return names
