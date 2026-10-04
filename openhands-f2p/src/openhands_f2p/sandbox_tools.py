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

import re
from pathlib import Path

from pydantic import ConfigDict, Field

from openhands.sdk.tool import (
    Action,
    Observation,
    ToolAnnotations,
    ToolDefinition,
    ToolExecutor,
    register_tool,
)

from openhands_f2p import flow
from openhands_f2p import swebench_env as E
from openhands_f2p.features import FeatureSet
from openhands_f2p.swebench_env import REPO_DIR, Sandbox

MAX_OUTPUT = 4000        # what comes back to the model, per call
RUN_TIMEOUT = 120        # a shell command for reading or searching
TEST_TIMEOUT = 1800      # a test suite, which legitimately can take a while
# Was 12000. Eight `run` calls at that size is roughly 25k tokens of context, and the
# request that carried them timed out. Test output is the long thing here and its
# useful part is the head and the tail, so clipping loses little.


# Parameter names the models invented and how often, so the next reader can see whether
# this is still happening. Filled by ToolArgs below; reported at the end of a run.
INVENTED: dict[str, int] = {}


class ToolArgs(Action):
    """An Action that keeps parameters the model invented instead of refusing the call.

    The SDK's `Action` sets `extra="forbid"`, so a call carrying one unknown key dies with
    a pydantic error and the model gets no result at all. Weaker models guess plausible
    names -- `timeout` on a shell command, `commentary` beside a write -- and cannot
    recover: the rejection is answered with an empty assistant turn whose recovery plan
    sits in `reasoning_content`, where nothing reads it, and the same malformed call comes
    back. On `sympy-21612` gpt-oss-20b spent 91 of its 100 actions in that loop, which
    makes its score a measurement of this config line rather than of the model.

    `extra="allow"` rather than `"ignore"`, and the difference is the whole lesson. Ignore
    was silent, and silence turned out to be worse than the refusal it replaced: gpt-5-nano
    emits calls where the shell script arrives as a *key* rather than inside `command` --

        {"command": "bash -lc", "grep -RIn ... | head -n 200' }": false}

    -- so the dropped half was the command, `bash -lc` ran with no argument, and the only
    feedback was `bash: -c: option requires an argument`. Across one evaluation set that
    was 47 of 329 actions, and `pytest-7982` spent five consecutive actions on it and
    finished having written nothing. Keeping the extras lets the executor say what it
    ignored, which is the difference between a mistake the model can see and one it
    repeats.

    The emitted JSON schema is unchanged under all three settings -- pydantic adds no
    `additionalProperties` -- so the model is told exactly what it was told before.
    """

    model_config = ConfigDict(extra="allow", frozen=True)


class _Shown(ToolExecutor):
    """Keep, on the tool's log entry, the exact text the model was handed back.

    The log held structured results and `trajectory.py` re-rendered them in its own
    words, so the audit file drifted from what the agent read: coverage came out as
    "66.7% of changed lines executed" in the trajectory while the model saw lines and no
    number, and `mutation` came out empty. Recording the observation itself leaves
    nothing to re-render. Wraps every executor; changes nothing the model receives.
    """

    def __init__(self, inner: ToolExecutor, tool: str):
        self.inner, self.tool = inner, tool

    def __call__(self, action, conversation=None):
        log = self.inner.log
        n = len(log)
        obs = self.inner(action, conversation)
        # The entry for this call, not the last one: a `guard` revert is appended after it.
        for entry in reversed(log[n:]):
            if entry.get("tool") == self.tool:
                entry["shown"] = obs.text
                entry["shown_as_error"] = bool(obs.is_error)
                break
        return obs

    def close(self) -> None:
        self.inner.close()


def _clip(text: str, limit: int = MAX_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    half = limit // 2
    return (text[:half] + f"\n\n... [{len(text) - limit} characters omitted] ...\n\n"
            + text[-half:])


# What a runner prints about itself rather than about the test: pytest's session header
# and its warnings summary, django's banner. matplotlib-22719 (loop check, 2026-09-29) lost
# its whole run to these: `verify` clipped each side to its first and last few hundred
# characters, the header and the warnings summary filled both ends, and the one line that
# said why the test still failed after the change -- `DID NOT WARN`, from a bare
# `pytest.warns()` -- sat in the omitted middle all four times. The agent concluded
# `verify` was broken and spent sixty actions re-running a test it could already see fail.
_RUNNER_NOISE = re.compile(
    r"^(=+ test session starts =+$|platform |rootdir: |configfile: |plugins: |cachedir: "
    r"|libraries: |base tempdir: |collecting \.\.\. |Testing against Django installed "
    r"|Skipping setup of unused database|System check identified )")
_SECTION = re.compile(r"^=+ .+ =+$")


def _import_only(box: Sandbox, cov: dict) -> str:
    """A note when every changed line the test runs is one that runs on import.

    Call inside the patched window: `import_time_hits` reads the file at head.
    """
    hits = cov.get("hit") or []
    at_import = E.import_time_hits(box, cov) if hits else []
    if not hits or len(at_import) != len(hits):
        return ""
    shown = ", ".join(f"`{h}`" for h in at_import[:4]) + (" ..." if len(at_import) > 4 else "")
    return ("\n\nNote: every changed line it runs is module-level (" + shown + ") -- it "
            "executes when the module is imported, whatever the test does. That it runs "
            "is no sign the test uses the change: the test has to call the code that "
            "uses it, and a copy of the changed value made inside the test checks the "
            "copy, not the project.")


def _condense(text: str) -> str:
    """`text` without the lines that describe the runner instead of the test."""
    kept, in_warnings = [], False
    for line in text.splitlines():
        if _SECTION.match(line):
            in_warnings = "warnings summary" in line
            if in_warnings:
                continue
        elif in_warnings or line.startswith("-- Docs: https://docs.pytest.org"):
            continue
        if not _RUNNER_NOISE.match(line):
            kept.append(line)
    return "\n".join(kept).strip()


def _ignored(action, tool: str) -> str:
    """What to append when a call carried arguments this tool does not have.

    Named rather than counted: "ignored 1 unknown argument" would not have told nano that
    the thing it lost was the command itself. The keys are truncated because the usual
    offender is an entire shell script that arrived where a parameter name belongs.
    """
    extra = getattr(action, "model_extra", None) or {}
    if not extra:
        return ""
    for key in extra:
        INVENTED[key] = INVENTED.get(key, 0) + 1
    shown = ", ".join(f"`{k[:60]}{'...' if len(k) > 60 else ''}`" for k in list(extra)[:3])
    known = ", ".join(f"`{f}`" for f in type(action).model_fields)
    return (f"\n\n[harness] Ignored {len(extra)} argument(s) that `{tool}` does not "
            f"take: {shown}. It accepts only {known}, and everything else was discarded "
            f"before this ran -- so if the result looks truncated, that is why. Put the "
            f"whole value inside the argument rather than beside it.")


def _undo_edits(box: Sandbox, log: list, on: bool = True) -> str:
    """Put back anything the agent changed that was already here. Returns what to tell it.

    The prompt has always forbidden this and the audit has always caught it afterwards,
    and neither stopped it: on the nano evaluation set the agent wrote its test correctly
    and then rewrote `xarray/core/indexing.py` and `sklearn/impute/_iterative.py` with
    shell heredocs -- `applypatch`, `python - <<PY` -- until its own test passed. Both runs
    scored BROKEN, which is the right verdict and arrives far too late to help: forty of
    that run's sixty-five actions went into a file whose every edit was going to be
    discarded.

    So the tree is repaired between actions instead. A file the agent created is untracked
    in the snapshot and never appears here, which is the distinction that matters -- a new
    file is present in the before run and the after run alike and cannot manufacture a
    flip, while an edited one can.

    Returns "" when nothing was touched, which is the overwhelmingly common case and costs
    one `git diff --name-only` against a snapshot that lives outside the work tree.
    """
    if not on:
        # Without `--add-guard`. The prompt still forbids the edit and `audit` still reports a
        # dirty tree as BROKEN; what is withheld is the repair, so the arm measures how
        # often the agent reaches for the library rather than how often it is stopped.
        return ""
    # A file the fix itself creates, written by the agent: the patch can no longer be
    # applied over it, so every `verify` and the verdict fail on "tree not at base"
    # (astropy-13398, fix check). Removed, as an edit to an existing file is put back.
    reserved = list(getattr(box, "reserved_paths", None) or [])
    created = []
    if reserved:
        quoted = " ".join("'" + p.replace("'", "'\\''") + "'" for p in reserved)
        r = box.exec(f"for f in {quoted}; do [ -e \"$f\" ] && echo \"$f\"; done; true",
                     timeout=60)
        created = [ln.strip() for ln in r.output.splitlines() if ln.strip()]
        if created:
            box.exec("rm -f " + " ".join("'" + p.replace("'", "'\\''") + "'"
                                         for p in created), timeout=60)
    altered = box.altered_paths()
    if not altered and not created:
        return ""
    restored = box.restore(altered) if altered else []
    log.append({"tool": "guard", "reverted": restored + created})
    flow.record(flow.AGENT, "reverted edit", ", ".join((restored + created)[:4]))
    say = ""
    if restored:
        shown = ", ".join(f"`{p}`" for p in restored[:4])
        more = f" (and {len(restored) - 4} more)" if len(restored) > 4 else ""
        say += (f"\n\n[harness] You changed {shown}{more}, which existed before you "
                f"started, so it has been put back. The test has to fail on this code as "
                f"it is -- editing what it tests destroys the measurement rather than "
                f"passing it. Create new files freely; do not edit the ones that were "
                f"already here.")
    if created:
        shown = ", ".join(f"`{p}`" for p in created[:4])
        say += (f"\n\n[harness] You created {shown}, a file this pull request adds -- "
                f"writing it is writing the fix, and the change could no longer be applied "
                f"over it. It has been removed. Your test has to work against the code as "
                f"it is here, without that file.")
    return say


# --------------------------------------------------------------------------- run
class RunAction(ToolArgs):
    command: str = Field(description="Shell command to run inside the repository.")


class RunObservation(Observation):
    pass


class RunExecutor(ToolExecutor[RunAction, RunObservation]):
    def __init__(self, box: Sandbox, log: list | None = None, guard: bool = True):
        self.box = box
        self.log = log if log is not None else []
        self.guard = guard

    def __call__(self, action: RunAction, conversation=None) -> RunObservation:
        # 120s, not 900. `run` is for reading and searching; nothing legitimate there
        # takes two minutes, and a runaway recursive grep used to burn fifteen.
        r = self.box.exec(action.command, timeout=RUN_TIMEOUT)
        self.log.append({"tool": "run", "command": action.command,
                         "returncode": r.returncode, "output": r.output[:4000]})
        body = _clip(r.output) or "(no output)"
        undone = _undo_edits(self.box, self.log, self.guard)
        dropped = _ignored(action, "run")
        return RunObservation.from_text(
            f"exit code {r.returncode}\n{body}{undone}{dropped}",
            is_error=r.returncode != 0 or bool(undone) or bool(dropped))


class SandboxRunTool(ToolDefinition[RunAction, RunObservation]):
    # The name the model calls. Without it the SDK derives one from the class --
    # `SandboxVerifyTool` became `sandbox_verify` -- while every prompt, tool output and
    # refusal says `verify`. Two runs of 52 spent all five refusals looking for a
    # `verify` command that did not exist under that name; the `name=` passed to the
    # constructor below never reached the model, because the SDK holds it on the class.
    name = "run"

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
            executor=_Shown(RunExecutor(box, log, params.get("guard", True)), "run"),
        )]


# -------------------------------------------------------------------- write_file
class WriteAction(ToolArgs):
    path: str = Field(description="Path to write, relative to the repository root.")
    content: str = Field(description="Full contents of the file.")


class WriteObservation(Observation):
    pass


class WriteExecutor(ToolExecutor[WriteAction, WriteObservation]):
    def __init__(self, box: Sandbox, log: list | None = None, guard: bool = True):
        self.box = box
        self.log = log if log is not None else []
        self.guard = guard

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
        undone = _undo_edits(self.box, self.log, self.guard)
        dropped = _ignored(action, "write_file")
        return WriteObservation.from_text(
            f"wrote {action.path} ({lines} lines){undone}{dropped}",
            is_error=bool(undone) or bool(dropped))


class SandboxWriteTool(ToolDefinition[WriteAction, WriteObservation]):
    name = "write_file"

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
            executor=_Shown(WriteExecutor(box, log, params.get("guard", True)), "write_file"),
        )]


# --------------------------------------------------------------------- run_tests
class TestAction(ToolArgs):
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
        dropped = _ignored(action, "run_tests")
        return TestObservation.from_text(
            f"{head}\nexit code {r.returncode}\n{summary}\n\n{_clip(_condense(r.output))}{dropped}",
            is_error=not outcomes or bool(dropped))


class SandboxTestTool(ToolDefinition[TestAction, TestObservation]):
    name = "run_tests"

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
            executor=_Shown(TestExecutor(box, repo, log, reveal_runner=reveal_runner),
                                  "run_tests"),
        )]



# ------------------------------------------------------------------- coverage
class CoverageAction(ToolArgs):
    target: str = Field(
        description="The test file to measure, same value you would pass to run_tests.")


class CoverageObservation(Observation):
    pass


class CoverageExecutor(ToolExecutor[CoverageAction, CoverageObservation]):
    """Which of the pull request's changed lines the test never executes.

    The same lines the harness scores, shown as lines and never as a percentage. The
    earlier output led with the figure and closed with "100% is the target", while
    58-finish.md told the same agent "none of these figures is a target" -- and the
    figure it was told to maximise was the one the report published as an independent
    measure of test quality. The harness still computes the percentage; the agent is
    shown only what it can act on. Measured with the patch applied, because the lines it
    adds do not exist at any other moment, and always reverted afterwards.
    """

    def __init__(self, box: Sandbox, repo: str, patch: str, log: list | None = None,
                 require_tools: bool = False, scored: bool = False):
        self.box = box
        self.repo = repo
        self.patch = patch
        # `--add-require-tools-with-score-report`: the percentage is shown and is a target.
        # Everywhere else it is withheld, for the reason the class docstring gives.
        self.scored = scored
        # Whether the run will refuse a stop that leaves this unanswered. When it will,
        # the tool says so itself -- the rule is otherwise only in the prompt the agent
        # read once at the start and in the refusal it gets after deciding it is done.
        self.require_tools = require_tools
        self.log = log if log is not None else []

    def __call__(self, action: CoverageAction, conversation=None) -> CoverageObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return CoverageObservation.from_text(
                "cannot measure: the working tree is in an unexpected state "
                f"({state}) -- some file was modified outside the test", is_error=True)
        base = E.base_texts(self.box, self.patch)
        self.box.apply_patch(self.patch)
        try:
            cov = E.changed_line_coverage(self.box, [action.target], self.patch, base)
            import_only = _import_only(self.box, cov) if cov.get("measured") else ""
        finally:
            self.box.apply_patch(self.patch, revert=True)

        self.log.append({"tool": "coverage", "target": action.target, "result": cov})
        if not cov.get("measured"):
            return CoverageObservation.from_text(
                f"could not measure change coverage: {cov.get('reason')}", is_error=True)

        score = (f"Changed-line coverage: {cov['percent']}% ({cov['covered']} of "
                 f"{cov['executable_changed_lines']} executable changed lines).\n\n"
                 if self.scored else "")
        # The run this measured is the test with the change applied, so it already knows
        # whether the test passes there. matplotlib-22719 (loop check) read "runs every
        # line" eight times as a sign it was done, about a test that failed once the change
        # was in -- and never called `verify` again, which is the check that says so.
        failing = ("\n\nNote: with the change applied, this test run did not pass (exit "
                   f"code {cov['test_run_returncode']}), so at least one test here fails "
                   "once the fix is in. Which lines run says nothing about that -- the file "
                   "is not fail-to-pass until `verify` says it is."
                   if cov.get("test_run_returncode") not in (0, None) else "")
        if not cov["missed"]:
            return CoverageObservation.from_text(
                score + "Your test runs every executable line this pull request changed."
                + import_only + failing)
        # The import-time note went out only when nothing was missed, so astropy-13398
        # (base, cap 125), whose 31 "covered" lines were all imports, constants and `def`
        # lines, never saw it in four calls.
        lines = [score + "Some lines this pull request changed never ran under your test."
                 + import_only]

        # The source and the guards, not just the numbers. "line 1631 is uncovered" is
        # not something an agent can act on; "line 1631 is `Q *= q.p`, and it sits under
        # `if not isinstance(q, SYMPY_INTS)`" says exactly what the input has to look
        # like for that line to run.
        lines += ["", "For each one you can see the code and the conditions above it -- "
                      "those conditions are what your input has to satisfy:", ""]
        for item in cov.get("missed_source") or []:
            lines.append(f"  {item['ref']}")
            for g in item["guards"]:
                lines.append(f"      {g}")
            ref_ln = item["ref"].rpartition(":")[2]
            lines.append(f"    > {ref_ln}: {item['line']}")
            lines.append("")
        extra = len(cov["missed"]) - len(cov.get("missed_source") or [])
        if extra > 0:
            lines.append(f"  ... and {extra} more changed lines that never ran")
        lines += ["Write the test so that every line the change touched runs: pick inputs "
                  "that make those conditions true, or add a second test for a separate "
                  "case the same change fixes. Reach each line through the behaviour you "
                  "are asserting. Then call `coverage` again."]
        # The rule, where the shortfall is read. Deliberately paired with the escape
        # hatch: some changed lines cannot be reached from a test at all, and an
        # assertion written only to execute one buys a number and costs a reviewer's
        # trust. Saying why a line is unreachable satisfies this as fully as reaching it.
        if self.scored:
            lines += ["",
                      "The target is 100%: you will be sent back while it is below, until "
                      "it gets there or an honest attempt raises it no further."]
        elif self.require_tools:
            lines += ["",
                      "You will be sent back while lines are missed: change the test and "
                      "call `coverage` again, until every changed line runs or an honest "
                      "attempt reaches no more of them."]
        return CoverageObservation.from_text("\n".join(lines) + failing)


class SandboxCoverageTool(ToolDefinition[CoverageAction, CoverageObservation]):
    name = "coverage"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, require_tools: bool = False,
               scored: bool = False, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="coverage",
            description=("List the lines this pull request changed that your test never "
                         "runs, with the code of each and the conditions above it."),
            action_type=CoverageAction,
            observation_type=CoverageObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=_Shown(CoverageExecutor(box, repo, patch, log, require_tools, scored),
                                  "coverage"),
        )]


# -------------------------------------------------------------------- mutation
class MutationAction(ToolArgs):
    target: str = Field(
        description="The test file to try, same value you would pass to run_tests.")


class MutationObservation(Observation):
    pass


class MutationExecutor(ToolExecutor[MutationAction, MutationObservation]):
    """Small wrong variants of the fix, and which ones the test fails to notice.

    The agent's instrument. The harness measures a mutation score of its own after the
    agent has finished, and -- because this tool exists -- it measures it on the half of
    the mutant pool this one never shows. Tuning a test until the ten mutants in front of
    you die is easy and proves nothing; the score is taken on ten others.

    `test_patch` is never applied here. The developer's test is the held-out answer, and
    a tool that installed it during the agent's turn would put it in a tree the agent can
    read.
    """

    def __init__(self, box: Sandbox, repo: str, patch: str, log: list | None = None,
                 n: int = 5, require_tools: bool = False, scored: bool = False):
        self.box = box
        self.repo = repo
        self.patch = patch
        self.log = log if log is not None else []
        self.n = n
        self.scored = scored
        # See CoverageExecutor: the obligation is stated where the answer arrives.
        self.require_tools = require_tools

    def __call__(self, action: MutationAction,
                 conversation=None) -> MutationObservation:
        from openhands_f2p import mutants as M
        from openhands_f2p import verify as V
        # Only for a test that is fail-to-pass by its own last `verify`, unchanged since
        # (user, 2026-10-04). On a test that passes before the fix too, "2 of 2 caught"
        # is no sign of anything -- the test cannot tell the fix from no fix -- yet the
        # nine NO runs of the base at cap 125 made 18 such calls, and pylint-6903 went on
        # to work a survivor of a test that was never fail-to-pass.
        if not V.verify_settled(self.log, action.target):
            self.log.append({"tool": "mutation", "target": action.target,
                             "error": "not fail-to-pass by its last verify"})
            return MutationObservation.from_text(
                f"not run: `mutation` asks whether {action.target} tells the fix from "
                f"wrong versions of it, which only means something once the test tells "
                f"the fix from no fix. Its last `verify` did not say fail-to-pass for the "
                f"file as it is now. Call `verify` and get it there first.", is_error=True)
        r = M.probe(self.box, self.patch, action.target, self.n)
        if not r.get("ok"):
            self.log.append({"tool": "mutation", "target": action.target,
                             "error": r.get("why", "")})
            return MutationObservation.from_text(
                f"could not run mutants: {r.get('why', 'unknown')}", is_error=True)
        got = r.get("mutants") or []
        if not got:
            self.log.append({"tool": "mutation", "target": action.target,
                             "total": 0, "why": r.get("why", "")})
            return MutationObservation.from_text(
                f"{r.get('why', 'no mutants available')}. Nothing to read into that -- "
                f"it is a property of the change, not of your test.")
        killed = [m for m in got if m.agent_kills]
        lived = [m for m in got if not m.agent_kills]
        self.log.append({"tool": "mutation", "target": action.target,
                         "total": len(got), "killed": len(killed),
                         "survived": [m.operator for m in lived]})
        lines = [f"{len(killed)} of {len(got)} wrong variants of the fix were caught by "
                 f"{action.target}."]
        if self.scored:
            lines[0] = (f"Mutation score: {round(100.0 * len(killed) / len(got), 1)}% -- "
                        + lines[0])
        if lived:
            lines += ["", "Not caught -- each of these is a broken version of the fix "
                          "that your test still passes on:"]
            lines += [f"  {m.file}:{m.line}    {m.operator}" for m in lived]
            lines += ["",
                      "Answer each one. Ask whether a reviewer would call the behaviour "
                      "it breaks part of what this pull request fixes. Where the answer "
                      "is yes, your test is missing an assertion about that behaviour: "
                      "add one that checks what the code returns, raises or does, then "
                      "call `verify` and `mutation` again. Where the answer is no -- the "
                      "variant breaks something the change was never about, or nothing "
                      "observable at all -- say so in one sentence and leave it. Never "
                      "assert on the exact expression a variant changed just to make it "
                      "fail."]
            if self.scored or self.require_tools:
                # "Leave it" above, and a loop that closes only on an attempt: requests-1142
                # (base, cap 125) said in eight rounds that its survivor was harmless and
                # was sent back eight times. What ends the loop is said here.
                lines += ["",
                          ("Maximise the score: y" if self.scored else "Y")
                          + "ou will be sent back while variants survive: add assertions "
                          "about the behaviour they break and call `mutation` again, until "
                          "none survives or an honest attempt catches no more. An attempt "
                          "is a changed test followed by `mutation`; saying a variant is "
                          "harmless does not end it."]
        else:
            lines += ["", "Every variant tried was caught."]
        return MutationObservation.from_text("\n".join(lines))


class SandboxMutationTool(ToolDefinition[MutationAction, MutationObservation]):
    name = "mutation"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, n: int = 5,
               require_tools: bool = False, scored: bool = False, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="mutation",
            description=("Break the fix in small ways on purpose and see whether your "
                         "test notices. Reports each variant your test still passes on, "
                         "which is a behaviour the change makes and your test does not "
                         "check."),
            action_type=MutationAction,
            observation_type=MutationObservation,
            annotations=ToolAnnotations(readOnlyHint=True),
            executor=_Shown(MutationExecutor(box, repo, patch, log, n=n,
                                             require_tools=require_tools, scored=scored),
                            "mutation"),
        )]


# --------------------------------------------------------------------- verify
class VerifyAction(ToolArgs):
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
                 reveal_missed: bool = True, point_at_mutation: bool = False,
                 require_tools: bool = False, scored_name: str = "",
                 gated: bool = False, scored: bool = False):
        self.box = box
        self.scored = scored
        # Whether a stop is refused while this says not fail-to-pass -- `require-tools`'
        # stop checks. Kept apart from `require_tools` only so the two sentences can be
        # read separately; both come from the same feature.
        self.gated = gated
        # The file name the run is scored on. A verify on any other file answers about
        # that file only: three -repo-facts django runs verified a test under
        # `tests/<app>/` as fail-to-pass and stopped, while the file carrying the scored
        # name sat at the repository root, where django cannot import it.
        self.scored_name = scored_name
        self.repo = repo
        self.patch = patch
        # See CoverageExecutor: the obligation is stated where the answer arrives.
        self.require_tools = require_tools
        self.log = log if log is not None else []
        # Whether `mutation` is registered alongside. Same reasoning as `reveal_missed`
        # one field below, and found the same way: on the first five-instance test of the
        # mutation tool the agent read "fail-to-pass" plus "it runs every line this pull
        # request changed", concluded it was done, and finished -- never calling
        # `mutation`, which is the only check nothing else answers. Verify is where the
        # agent feels finished, so verify is where the remaining question belongs.
        self.point_at_mutation = point_at_mutation
        # Whether `coverage` is registered alongside. Without it there is no tool to
        # send the agent to, and naming one it does not have is exactly the failure the
        # prompt scan catches -- one layer later, in a tool's own output, where no scan
        # reaches.
        self.reveal_missed = reveal_missed

    def __call__(self, action: VerifyAction, conversation=None) -> VerifyObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            # Logged like any other call -- it was missing from `tool_log`, so a run that
            # hit this read as though the agent had never tried.
            self.log.append({"tool": "verify", "target": action.target,
                             "error": f"tree not at base ({state})"})
            return VerifyObservation.from_text(
                f"cannot verify: the working tree is in an unexpected state ({state})",
                is_error=True)
        cmd = E.test_command(self.box, [action.target])
        from openhands_f2p import verify as V
        before = self.box.exec(cmd, timeout=3600)
        base_out = V.own_outcomes(E.parse_output(before.output), [action.target])
        self._base = E.base_texts(self.box, self.patch)
        self._reach_full = False
        self.box.apply_patch(self.patch)
        missed = ""
        try:
            after = self.box.exec(cmd, timeout=3600)
            head_out = V.own_outcomes(E.parse_output(after.output), [action.target])
            # Inside the patched window, which is the only moment the lines the change
            # adds exist at all. Computed here rather than after the revert -- doing it
            # afterwards measures coverage of a tree where those line numbers hold
            # different code, and the run fails outright.
            # Only for a file that meets the harness's verdict: something flipped AND
            # nothing still fails once the change is applied. Keyed on `flipped` alone,
            # a file with two good tests and one broken one got a coverage report here --
            # a working test's feedback, attached to a NO.
            flips = ({n for n, v in base_out.items() if v in ("FAILED", "ERROR")}
                     & {n for n, v in head_out.items() if v == "PASSED"})
            # Only when `coverage` is registered. Without it this line was the whole of
            # the coverage feedback -- "not every changed line runs" -- and the
            # -coverage arm lost only *which* lines (42 such lines in 18 of its runs,
            # against 45 in 16 for base). Removing the tool now removes the feedback.
            if (self.reveal_missed and flips
                    and not any(v in ("FAILED", "ERROR") for v in head_out.values())):
                missed = self._reach(action.target)
        finally:
            self.box.apply_patch(self.patch, revert=True)

        failed_before = {n for n, v in base_out.items() if v in ("FAILED", "ERROR")}
        passed_after = {n for n, v in head_out.items() if v == "PASSED"}
        flipped = sorted(failed_before & passed_after)
        still_failing = [n for n, v in head_out.items() if v in ("FAILED", "ERROR")]
        # `reach_full`: this call's own coverage said every changed line runs, which
        # answers the coverage loop for this file (`V.duty_gap`, user 2026-10-04).
        self.log.append({"tool": "verify", "target": action.target,
                         "before": base_out, "after": head_out, "flipped": flipped,
                         "reach_full": self._reach_full})

        # `inverted` before `still_failing`. A test that passed at base and fails at head
        # is the closest possible near-miss -- it found the behaviour and asserted the
        # side of it the change removes -- and the generic branch calls that "still
        # fail", which is false (it did not fail before) and points at rewriting rather
        # than at flipping one assertion. django-13279 hit it twice in six verifies.
        inverted = sorted({n for n, v in base_out.items() if v == "PASSED"}
                          & {n for n, v in head_out.items() if v in ("FAILED", "ERROR")})
        if not base_out and not head_out:
            head = "NOT fail-to-pass: nothing was collected -- the file does not import."
        elif inverted:
            head = (f"NOT fail-to-pass, and backwards: {inverted[:3]} pass on the code as "
                    f"it is and fail once the change is applied. You have found the right "
                    f"behaviour and asserted the old side of it. Assert what the change "
                    f"makes true, not what it replaces.")
        elif still_failing and flipped:
            # Part of the file is right. Said as such, because "the test is wrong" alone
            # sent seaborn-3069 into adding tests beside a flipping one for four verifies,
            # and then deleting the one that flipped. Twenty-one of the 700 runs ended
            # holding a correct test next to a broken one.
            head = (f"NOT fail-to-pass yet, but part of it is right: {flipped[:3]} fail "
                    f"before the change and pass after -- keep those. {still_failing[:3]} "
                    f"still fail after the change is applied: fix them or delete them. "
                    f"Every test in the file has to pass once the change is in.")
        elif still_failing:
            head = (f"NOT fail-to-pass: {still_failing[:3]} still fail after the change "
                    f"is applied. The test is wrong, not the code.")
        elif not flipped and base_out and all(v == "SKIPPED" for v in base_out.values()):
            head = ("NOT fail-to-pass: every test was skipped before the change, so none "
                    "of them ran against the bug. Find what skips them in the output "
                    "below and make the test run here.")
        elif not flipped:
            head = ("NOT fail-to-pass: the test already passes before the change, so it "
                    "does not exercise this pull request.")
        else:
            head = f"Fail-to-pass: {len(flipped)} test(s) fail before and pass after."

        # The harness's rule, in one place, for everything below the headline. The
        # headline was always right, but the duty line, the coverage pointer, the mutation
        # pointer and the error flag all asked `flipped` -- "did anything flip" -- which is
        # not the verdict. `scikit-learn-14087` wrote three tests, two flipped and one
        # still failed: it read "NOT fail-to-pass ... still fail" and then, underneath,
        # "That it flips, and what it reaches, are two of the three questions", with no
        # duty line. It scored NO having been told both things.
        ok = bool(flipped) and not still_failing
        # The file as it stood when `verify` said fail-to-pass, kept for the record only:
        # `f2p_history` in the result says whether the test the agent finally handed in
        # is still that one, or it edited a passing test into a failing one afterwards.
        # Nothing picks or restores it -- the agent's last file is its answer (user,
        # 2026-09-30).
        if ok:
            self.log[-1]["f2p_test"] = self.box.read(action.target.split("::")[0]) or ""

        # The obligation, said where the answer arrives. It used to live only in the
        # prompt block the agent read once at the start and in the refusal it gets after
        # deciding it was finished -- neither of which is in front of it at the moment it
        # reads a failing verdict and chooses what to do next. Four of five failures in
        # an earlier run stopped on exactly this observation.
        duty = ("\n\nYou cannot finish while this is the answer. Rewrite the test and "
                "call `verify` again, as many times as it takes."
                if self.gated and not ok else "")

        # Reported here rather than left for the agent to ask about. The `coverage` tool
        # already offered this, and across twenty-six runs it was called twelve times --
        # every one of them last, with nothing after it, and every one already reaching
        # the whole change. It was a formality, never feedback, because asking was a
        # decision the agent only made once it was confident. This removes the decision.
        #
        # Lines *and* the percentage. This used to withhold the figure, on the grounds
        # that a score in front of the agent is a score to raise -- true, and the reason
        # the guidance beside it still talks about lines and the conditions above them.
        # But withholding it left the agent no handle on how far from done it was, and
        # the obligation the run enforces is expressed in that number, so stating the
        # rule while hiding the measure is the worse of the two failures.
        #
        # The side that holds the reason gets the room. A test that still fails, or fails
        # only, once the change is in is explained by the run after it; every other answer
        # (passes at base, skipped, nothing collected, fail-to-pass) by the run before.
        after_matters = bool(still_failing or inverted)
        body = (f"\n\nbefore the change:\n"
                f"{_clip(_condense(before.output), 1000 if after_matters else 2400)}"
                f"\n\nafter the change:\n"
                f"{_clip(_condense(after.output), 2400 if after_matters else 1000)}"
                if base_out or head_out else "")
        # Only when the test actually flips: asking what a test would notice about a
        # wrong fix presumes it notices the right one, and saying this after a NOT
        # fail-to-pass would send the agent at the wrong problem.
        nxt = ("\n\nThat it flips, and what it reaches, are two of the three questions. "
               "Whether it would notice a fix that is subtly *wrong* is the third, and "
               "nothing above answers it -- `mutation` does."
               if ok and self.point_at_mutation else "")
        # Never an error. The tool ran and answered; "no" is an answer. It was flagged
        # `is_error=not flipped`, so every negative verdict reached the model prefixed
        # "[An error occurred during execution.]" -- a median of five of them already in
        # context by the time a second chance began. `is_error` is kept for the cases
        # where the tool genuinely could not run (the tree in an unexpected state).
        elsewhere = ""
        if self.scored_name and Path(action.target.split("::")[0]).name != self.scored_name:
            elsewhere = (f"\n\nNote: this run is scored on the file named "
                         f"`{self.scored_name}`, and `{action.target}` is not it. This "
                         f"answer is about `{action.target}` only.")
        return VerifyObservation.from_text(head + elsewhere + duty + missed + nxt + body,
                                           is_error=False)

    def _reach(self, target: str) -> str:
        """How much of the change this test runs, and what to do if it is not all of it.

        A pointer, not the answer. Earlier this printed the missed lines here in full,
        which made `coverage` redundant -- the agent had everything already and never
        called it. Naming the shortfall and naming the tool that explains it keeps both:
        the agent cannot miss that something is unfinished, and the explaining is still
        the other tool's job.

        No percentage and no count, in either direction. "All of them" and "not all of
        them" are facts the agent can act on; a figure is a score, and a score in front
        of the agent is a score to raise.
        """
        try:
            cov = E.changed_line_coverage(self.box, [target], self.patch,
                                          getattr(self, "_base", None))
        except Exception:
            return ""
        if not cov.get("measured"):
            return ""
        missed = len(cov.get("missed") or [])
        pct = (f" Changed-line coverage: {cov['percent']}%." if self.scored else "")
        import_only = _import_only(self.box, cov)
        if not missed:
            self._reach_full = True
            return ("\n\nIt runs every line this pull request changed." + pct
                    + import_only)
        # Called only with `coverage` registered, so there is always a tool to point at.
        # The duty sentence was keyed on `require_tools` alone and went out in arms with
        # no `coverage`, where no check enforced it -- a rule nothing carried out.
        head = ("\n\nSome lines this pull request changed never run under this test." + pct
                + (" You cannot finish having read that and left it alone: either make "
                   "them run, or establish that a line cannot be reached from a test."
                   if self.require_tools else ""))
        where = (" Call `coverage` on this file to see which they are, the code on each "
                 "one and the conditions above it.")
        return (head + where +
                " Then decide: part of the behaviour you set out to pin down and worth "
                "another assertion, a separate case that deserves its own test "
                "function, or genuinely outside what this test is for. If you change "
                "the test, run `verify` again -- a new test is a new answer and the "
                "old one no longer describes it." + import_only)


class SandboxVerifyTool(ToolDefinition[VerifyAction, VerifyObservation]):
    name = "verify"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, reveal_missed: bool = True,
               point_at_mutation: bool = False, require_tools: bool = False,
               scored_name: str = "", gated: bool = False, scored: bool = False, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        return [cls(
            name="verify",
            description=("Check whether your test is fail-to-pass: run it on the code "
                         "before the change, apply the change, run it again. Reverts the "
                         "change afterwards."),
            action_type=VerifyAction,
            observation_type=VerifyObservation,
            annotations=ToolAnnotations(readOnlyHint=False),
            executor=_Shown(VerifyExecutor(box, repo, patch, log, reveal_missed,
                                           point_at_mutation, require_tools,
                                           scored_name, gated, scored), "verify"),
        )]


def register(box: Sandbox, repo: str, log: list, patch: str = "",
             features: FeatureSet | None = None, gen_path: str = "",
             version: str = "", probe_mutants: int = 5) -> list[str]:
    """Register the agent's tools against one sandbox. Returns their names.

    Which tools exist is part of the run's configuration, and the registry in `features`
    is the single place that says so -- each `Feature` names the tools that live and die
    with it. A withheld feature leaves its tools out rather than registering a degraded
    version of them, so the difference between two configurations is the component
    itself and not the same component answering worse.

    `verify` and `coverage` both need the patch: without it there is no second state to
    run a test against, and nothing to measure coverage of.
    """
    features = features if features is not None else FeatureSet.full()
    # One process handles one instance under --parallel, but a serial run reuses this
    # one, and a count that carried over would be attributed to the wrong instance.
    INVENTED.clear()
    briefed = "repo-facts" in features
    guard = "guard" in features
    require_tools = "require-tools" in features
    scored = "require-tools-with-score-report" in features
    made = {"run": SandboxRunTool.create(box=box, log=log, guard=guard)[0],
            "write_file": SandboxWriteTool.create(box=box, log=log, guard=guard)[0],
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
        made["verify"] = SandboxVerifyTool.create(
            box=box, repo=repo, patch=patch, log=log,
            reveal_missed=("coverage-tool" in features),
            point_at_mutation=("mutation-tool" in features),
            require_tools=require_tools,
            scored_name=Path(gen_path).name if gen_path else "",
            gated="require-tools" in features, scored=scored)[0]
        register_tool("verify", made["verify"])
        names.append("verify")
        if "coverage-tool" in features:
            made["coverage"] = SandboxCoverageTool.create(
                box=box, repo=repo, patch=patch, log=log,
                require_tools=require_tools, scored=scored)[0]
            register_tool("coverage", made["coverage"])
            names.append("coverage")
        # Beside `coverage` and for the same reason: it reports on the lines the change
        # touched, so it needs the change. It also needs the test to already pass on the
        # fixed code, which is what `verify` establishes.
        if "mutation-tool" in features:
            made["mutation"] = SandboxMutationTool.create(
                box=box, repo=repo, patch=patch, log=log, n=probe_mutants,
                require_tools=require_tools, scored=scored)[0]
            register_tool("mutation", made["mutation"])
            names.append("mutation")
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
