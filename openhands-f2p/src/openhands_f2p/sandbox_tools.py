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

import ast
import hashlib
import json
import re
import shlex
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
# astropy's own report header, printed before every run: about 900 characters of versions
# and options from "Running tests with Astropy version" to "IS_CRON:". In
# no-second-chance-no-require-tools astropy-13398 it filled the clipped window, and the
# line that said why the test failed after the fix (`PytestReturnNotNoneWarning`) sat in
# "[2078 characters omitted]"; the agent finished on it. Every astropy verify carried it.
# Versions differ: 3.1 ends the block at "Using Astropy options:", 5.2 and 6.0 add
# "ARCH_ON_CI:" / "IS_CRON:" after it. The block also ends the moment real runner output
# appears, so a header without its end marker can never swallow the test's report.
_ASTROPY_HEADER_START = re.compile(r"^Running tests with Astropy version ")
_ASTROPY_HEADER_END = re.compile(r"^Using Astropy options: ")
_ASTROPY_LINE = re.compile(r"^(Internet access disabled$|hypothesis profile '|ARCH_ON_CI: "
                           r"|IS_CRON: )")
# A traceback frame inside pytest or pluggy themselves, and the source line under it: the
# runner calling the test, never the test. Same run: fourteen such frames pushed the one
# `E   ` line out of the window.
_RUNNER_FRAME = re.compile(r"^\S*/site-packages/(_pytest|pluggy)/\S+:\d+: in ")


def _spawn_note(box: Sandbox, target: str) -> str:
    """A note when the test starts a child process: coverage follows this process only.

    pytest-10081 (no-second-chance-no-require-tools) ran the changed code through
    `subprocess.run` -- its mutation call killed 4 of 4 -- and was told by `verify` and
    twice by `coverage` that the changed lines "never ran"; the caveat lived only in the
    restart's reach diagnosis, which this arm never reaches."""
    from openhands_f2p import verify as V
    if not V.starts_process(box.read(target.split("::")[0]) or ""):
        return ""
    return (" Your test starts a child process, and coverage records only its own process:"
            " a line that runs only in the child is listed here as never run. Where you can,"
            " call the changed code in the test's own process so what it does is what you"
            " assert.")


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


def _section(output: str, node: str) -> str:
    """What pytest printed under `node`'s failure header, or "" when there is none."""
    key = re.escape(".".join(node.split("::")[1:]))
    head = re.search(rf"^_{{3,}} (?:ERROR at \w+ of )?{key} _{{3,}}$", output, re.M)
    if not head:
        return ""
    end = re.search(r"^(_{3,} |={3,} )", output[head.end():], re.M)
    return output[head.end(): head.end() + end.start() if end else len(output)]


def _first_error(output: str, node: str) -> str:
    """The first `E   ` line pytest printed for `node`, or "" when there is none."""
    line = next((ln for ln in _section(output, node).splitlines() if ln.startswith("E ")), "")
    return line[1:].strip().replace("`", "'")[:200]


def _failing_line(output: str, node: str) -> tuple[int, str] | None:
    """The line of the test file itself where `node` failed, with its number, read from
    pytest's `--tb=short` frames (`tests/test_x.py:12: in test_x`); None when the
    output does not show it."""
    stem = Path(node.split("::")[0]).name
    lines = _section(output, node).splitlines()
    for i, ln in enumerate(lines):
        m = re.match(r"^(\S+\.py):(\d+): in \S+", ln)
        if m and Path(m.group(1)).name == stem and i + 1 < len(lines):
            src = lines[i + 1].strip()
            if src and not src.startswith("E "):
                return int(m.group(2)), src.replace("`", "'")[:200]
    return None


def _why_both(before: str, after: str, nodes: list[str]) -> str:
    """For tests failing on both sides: whether they fail the same way.

    scipy-22549 (ChaCo base, 2026-10-12) failed before the change on the missing
    `workers` keyword -- the right failure -- and after it on its own `hess=None`. Told
    only "still fail after the change", it ran `verify` ten more times without touching
    `hess`. pandas-60295 failed on the same ValueError on both sides.
    """
    said = []
    for n in nodes[:3]:
        b, a = _first_error(before, n), _first_error(after, n)
        if not (b and a):
            continue
        name = n.split("::")[-1]
        if b == a:
            said.append(f"`{name}` fails the same way on both sides (`{a}`), so the change "
                        f"does not touch what fails: fix that first.")
        else:
            said.append(f"`{name}` fails before the change with `{b}` and after it with "
                        f"`{a}`. The first can be the right failure -- what the change "
                        f"fixes; the second is a mistake in the test itself: fix that and "
                        f"keep the rest.")
    return (" " + " ".join(said)) if said else ""


def _backwards(after: str, nodes: list[str], wrong: list[str]) -> str:
    """For tests that pass before the change and fail after it: where each one fails, and
    that the assertion there is the one to reverse.

    sphinx-10807 (round 16, 2026-10-22) was told "backwards: ... assert what the change
    makes true" for `test_new_config_option_not_present`, read it as progress, and went on
    to tests that passed on both sides. The line that fails is named now, and that this is
    the opposite of what is needed.
    """
    said = []
    for n in nodes[:3]:
        name = n.split("::")[-1]
        w = next((x for x in wrong if x.startswith(f"`{name}`")), "")
        if w:
            said.append(w)
            continue
        at, err = _failing_line(after, n), _first_error(after, n)
        if at:
            said.append(f"`{name}` fails after the change at line {at[0]}: `{at[1]}`"
                        + (f" (`{err}`)." if err else "."))
        elif err:
            said.append(f"`{name}` fails after the change with `{err}`.")
    if not said:
        return ""
    many = len(said) > 1
    return (" " + " ".join(said) + (" Each of those assertions holds" if many else
                                    " That assertion holds")
            + " on the old code and breaks on the new one: it checks that the change is NOT "
            "there. Reverse " + ("each" if many else "it") + " -- assert what the change "
            "makes true -- and the same test fails before the change and passes after it.")


def _seed_changed(log: list, text: str, failing: list[str]) -> str:
    """For seeded tests among `failing` whose text differs from the copy the harness added:
    which lines the agent added to it, and to put the copy back."""
    said = []
    for e in log:
        if e.get("tool") != "seed" or "error" in e or not e.get("name"):
            continue
        name = e["name"]
        if not any(n.split("::")[-1].split("[")[0] == name for n in failing):
            continue
        was, now = _function_text(e.get("block") or "", name), _function_text(text, name)
        if not was or not now or was.strip() == now.strip():
            continue
        old = {ln.strip() for ln in was.splitlines()}
        added = [ln.strip() for ln in now.splitlines() if ln.strip() and ln.strip() not in old]
        said.append(f"`{name}` is the repository test the harness copied in (from "
                    f"`{e.get('from')}`); as copied it passed on both sides. Your version "
                    f"changes it"
                    + (f" -- it adds `{added[0][:160]}`" + (f" and {len(added) - 1} more line(s)"
                                                           if len(added) > 1 else "")
                       if added else "")
                    + " -- and now fails. Put the copy back exactly as it was added; make your "
                      "own changes in a new test next to it.")
    return (" " + " ".join(said)) if said else ""


def _condense(text: str) -> str:
    """`text` without the lines that describe the runner instead of the test."""
    kept, in_warnings, in_astropy, frame_body = [], False, False, False
    for line in text.splitlines():
        if frame_body:                       # the source line printed under a runner frame
            frame_body = False
            if line.startswith(" "):
                continue
        if _RUNNER_FRAME.match(line):
            frame_body = True
            continue
        if in_astropy:
            if (_SECTION.match(line) or "::" in line
                    or line.startswith(("rootdir:", "collecting", "platform "))):
                in_astropy = False             # the report has started: keep it
            else:
                in_astropy = not _ASTROPY_HEADER_END.match(line)
                continue
        if _ASTROPY_HEADER_START.match(line):
            in_astropy = True
            continue
        if _ASTROPY_LINE.match(line):
            continue
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
    def __init__(self, box: Sandbox, log: list | None = None, guard: bool = True,
                 verify_named: bool = False):
        self.box = box
        self.log = log if log is not None else []
        self.guard = guard
        self.verify_named = verify_named

    def __call__(self, action: RunAction, conversation=None) -> RunObservation:
        # 120s, not 900. `run` is for reading and searching; nothing legitimate there
        # takes two minutes, and a runaway recursive grep used to burn fifteen.
        r = self.box.exec(action.command, timeout=RUN_TIMEOUT)
        self.log.append({"tool": "run", "command": action.command,
                         "returncode": r.returncode, "output": r.output[:4000]})
        body = _clip(r.output) or "(no output)"
        # One of the agent's own tools typed as a shell command. pylint-4970
        # (no-second-chance) ran `verify tests/...` in bash, read "command not found",
        # and never called the tool in the whole run.
        typed = re.search(r"\b(verify|coverage|mutation|run_tests): command not found",
                          r.output or "")
        if typed:
            body += (f"\n\n[harness] `{typed.group(1)}` is not a shell command: it is one of "
                     f"your tools. Call the `{typed.group(1)}` tool itself, with `target` set "
                     f"to your test file.")
        # An attempt to apply the change by hand. sphinx-10807 (round 8, 2026-10-21) said
        # "let me run verify to see what happens when I apply the change", ran `git status`,
        # read "not a git repository", decided it "cannot apply the changes" and "does not
        # have the verify command", and never called the tool in 48 actions.
        elif self.verify_named and (
                "not a git repository" in (r.output or "")
                or re.search(r"(^|[;&|]\s*)(git\s+(apply|am|stash|checkout|diff)|patch\s+-p)\b",
                             action.command or "")):
            body += ("\n\n[harness] There is no git here, and you do not need it or any other "
                     "way to apply the change. `verify` is one of your tools, like `run_tests`: "
                     "it runs your test on this code, applies the change itself, runs the test "
                     "again and puts the code back. Call the `verify` tool with `target` set to "
                     "your test file.")
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
            executor=_Shown(RunExecutor(box, log, params.get("guard", True),
                                        params.get("verify_named", False)), "run"),
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
        # `sha` of the whole text: `content` is clipped for the log, and whether a write
        # changed the test (`V.test_writes`) must not depend on its first 4000 characters.
        # `tests`: the test names in the whole text, which the clipped `content` may not
        # reach -- the stop check reads them (`V.tests_now`).
        self.log.append({"tool": "write_file", "path": action.path,
                         "lines": lines, "content": action.content[:4000],
                         "sha": hashlib.sha1(action.content.encode()).hexdigest(),
                         "tests": re.findall(r"^\s*(?:async\s+)?def (test_\w+)", action.content,
                                             re.M)})
        # A seeded repository test the write leaves out (option 1, 2026-10-21): sphinx-10807
        # rewrote its file right after `test_seeded_rst_directive` was added, without it.
        from openhands_f2p import verify as V
        gone = [e for e in self.log if e.get("tool") == "seed" and "error" not in e
                and V.wrote_to(action.path, e.get("path", ""))
                and not re.search(rf"\bdef {re.escape(e['name'])}\(", action.content)]
        seen: set[str] = set()
        gone = [e for e in gone if not (e["name"] in seen or seen.add(e["name"]))]
        lost = ("".join(f"\n\n[harness] This write leaves out `{e['name']}`, the copy of "
                        f"`{e['from']}` the harness added: it runs code this change touches. "
                        f"Put it back unless you replace it with a test that runs the same code."
                        for e in gone) if gone else "")
        # ... or keeps it with fewer assertions: sphinx-10807 (base-it12, -it13) cut a seeded
        # test from 24 assertions to 3 while rewriting its file.
        for e in self.log:
            if (e.get("tool") != "seed" or "error" in e or e["name"] in seen
                    or not V.wrote_to(action.path, e.get("path", ""))):
                continue
            seen.add(e["name"])
            now, was = _function_text(action.content, e["name"]), _function_text(e["block"], e["name"])
            n_now, n_was = (len(re.findall(r"\bassert\w*\b", t)) for t in (now, was))
            if now and n_now < n_was:
                lost += (f"\n\n[harness] `{e['name']}` now has {n_now} of the {n_was} assertions "
                         f"it was copied with. Keep them: each checks behaviour that runs through "
                         f"the change. Add your own beside them.")
        undone = _undo_edits(self.box, self.log, self.guard)
        dropped = _ignored(action, "write_file")
        return WriteObservation.from_text(
            f"wrote {action.path} ({lines} lines){lost}{undone}{dropped}",
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
                 reveal_runner: bool = True, verify_named: bool = False):
        self.box = box
        # Whether `verify` exists, so the answer can point to it (2026-10-21).
        self.verify_named = verify_named
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
        # The agent's own tests only: an inner pytester session prints ids of a temp file
        # (pytest-10081: `test_one: ERROR` beside the agent's PASSED), as in `verify`.
        # Only for a test file: a directory or a django label holds no pytester temp file,
        # and filtering against it dropped every real id (pylint-4970, no-verify, ran
        # `tests/checkers/` and was shown only phantom ids).
        from openhands_f2p import verify as V
        file = action.target.split("::")[0]
        own = V.own_outcomes(outcomes, [file]) if file.endswith(".py") else outcomes
        summary = ", ".join(f"{k.split('::')[-1]}: {v}"
                            for k, v in list(own.items())[:12]) or "no tests ran"
        head = f"$ {command}" if self.reveal_runner else f"ran {action.target}"
        dropped = _ignored(action, "run_tests")
        # Which side of the change this was. xarray-7444 (round 5, 2026-10-21) ran
        # `run_tests` nineteen times and `verify` never: every run passed on the code before
        # the change, it rewrote the test blind each time, and it never saw what the same
        # tests do once the change is in -- what found the flip in rounds 1-3.
        side = ""
        if self.verify_named and own:
            passed = all(v == "PASSED" for v in own.values())
            side = ("\n\nThis ran on the code as it is -- before the change -- only. "
                    + ("Every test passes here, and a fail-to-pass test must fail on this "
                       "code. `verify` runs the same tests on both sides of the change and "
                       "says which ones flip: call it to see what the change does to them."
                       if passed else
                       "Whether these tests pass once the change is applied is what `verify` "
                       "answers: call it."))
        return TestObservation.from_text(
            f"{head}\nexit code {r.returncode}\n{summary}{side}\n\n{_clip(_condense(r.output))}{dropped}",
            is_error=not outcomes or bool(dropped))


class SandboxTestTool(ToolDefinition[TestAction, TestObservation]):
    name = "run_tests"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               log: list | None = None, reveal_runner: bool = True,
               verify_named: bool = False, **params):
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
            executor=_Shown(TestExecutor(box, repo, log, reveal_runner=reveal_runner,
                                         verify_named=verify_named),
                                  "run_tests"),
        )]



# ---------------------------------------------------------- verify's stages
def _ranges(lines: list[int]) -> str:
    """`[3, 4, 5, 9]` as `3-5, 9`."""
    out: list[str] = []
    for n in lines:
        if out and n == int(out[-1].split("-")[-1]) + 1:
            out[-1] = f"{out[-1].split('-')[0]}-{n}"
        else:
            out.append(str(n))
    return ", ".join(out)


def _missed_by_function(cov: dict) -> list[str]:
    """Every missed changed line, as line numbers grouped by file and the function holding
    them -- no source (user, 2026-10-19: the agent reads the lines itself). The source and
    guards of at most 20 lines per file, then "... and N more", hid most of a large change:
    pylint-4492 (large set) was told 15 of its missed lines only as a count."""
    groups = [g for g in cov.get("missed_by_function") or [] if g.get("missed")]
    if not groups:
        by_file: dict[str, list[int]] = {}
        for ref in cov.get("missed") or []:
            path, _, n = ref.rpartition(":")
            if n.isdigit():
                by_file.setdefault(path, []).append(int(n))
        groups = [{"path": p, "function": "<module>", "missed": len(ns), "lines": sorted(ns)}
                  for p, ns in by_file.items()]
    out: list[str] = []
    for path in dict.fromkeys(g["path"] for g in groups):
        mine = [g for g in groups if g["path"] == path]
        width = max(len(g["function"]) for g in mine)
        out.append(f"  {path}")
        for g in mine:
            n = g["missed"]
            nums = _ranges(g.get("lines") or [])
            word = "lines" if ("," in nums or "-" in nums) else "line"
            out.append(f"    {g['function']:<{width}}  {word} {nums}"
                       f"  ({n} line{'s' if n != 1 else ''})")
    return out


# Repository test files longer than this are not run for `_reach_of`: too slow to run
# whole under coverage inside a `verify` call. 4000 since 2026-10-23: sphinx-10807's
# `tests/test_ext_autodoc.py` (2536 lines, about 20 s) was the only test file for
# `ModuleDocumenter.add_content` and was never measured.
RELATED_RUN_MAX_LINES = 4000
# How many missed files get their first related test file measured.
RELATED_REACH_FILES = 6

# File stems too common to say which tests are about a file (`utils.py` -> every
# `test_utils.py` in the repository).
_GENERIC_STEMS = {"__init__", "utils", "util", "core", "base", "common", "main", "helpers",
                  "types", "compat", "misc", "api", "tools", "_base", "_utils"}


def related_tests(box: Sandbox, paths: list[str], own: str, per_path: int = 3) -> dict[str, list[str]]:
    """For each changed file, test files already in the repository that use it: they name
    its module, or carry its name. Read from the checkout, no model.

    sphinx-10807 (2026-10-20) reached 11.5% with `hasattr` checks: its change runs only
    inside a Sphinx build, which the repository's own `tests/test_environment_toctree.py`
    sets up with a fixture and a small project. The model wrote one build by hand, hit an
    import error in its own setup, and never found that pattern."""
    out: dict[str, list[str]] = {}
    script = []
    for k, p in enumerate(paths):
        mod = p[:-3] if p.endswith(".py") else p
        mod = re.sub(r"/__init__$", "", mod)
        mod = re.sub(r"^(src|lib)/", "", mod).replace("/", ".")
        # A package's `__init__.py` goes by the package's name.
        stem = Path(p).parent.name if Path(p).stem == "__init__" else Path(p).stem
        script.append(f"echo '@@I {k}'; grep -rlF --include='test_*.py' --include='*_test.py' "
                      f"--include='tests.py' -e {shlex.quote(mod)} . 2>/dev/null | head -40")
        if len(stem) >= 4 and stem not in _GENERIC_STEMS:
            script.append(f"echo '@@N {k}'; find . -path ./.git -prune -o -type f \\( -name "
                          f"{shlex.quote(f'test_*{stem}*.py')} -o -name "
                          f"{shlex.quote(f'*{stem}*_test.py')} \\) -print 2>/dev/null | head -40")
    if not script:
        return out
    r = box.exec("; ".join(script), timeout=120)
    found: dict[int, dict[str, set[str]]] = {}
    kind, k = "", -1
    for line in (r.output or "").splitlines():
        m = re.match(r"^@@([IN]) (\d+)$", line.strip())
        if m:
            kind, k = m.group(1), int(m.group(2))
            continue
        f = line.strip()
        if k < 0 or not f.endswith(".py"):
            continue
        f = f[2:] if f.startswith("./") else f
        if f == own or "test_f2p_" in Path(f).name:
            continue
        found.setdefault(k, {"I": set(), "N": set()})[kind].add(f)
    for k, p in enumerate(paths):
        got = found.get(k)
        if not got:
            continue
        both = sorted(got["I"] & got["N"])
        rest = sorted(got["N"] - got["I"]) + sorted(got["I"] - got["N"], key=lambda f: (len(f), f))
        picked = (both + rest)[:per_path]
        if picked:
            out[p] = picked
    return out


SEED_PREFIX = "test_seeded_"


def _function_text(text: str, name: str) -> str:
    """The source of the module-level function `name` in `text`, decorators included."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ""
    lines = text.splitlines()
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            first = min([n.lineno] + [d.lineno for d in n.decorator_list])
            return "\n".join(lines[first - 1:n.end_lineno])
    return ""


def seed_block(text: str, names: list[str], taken: set[str],
               prefer: str = "") -> tuple[str, str, str] | None:
    """A whole module-level test from a repository test file, to copy into the agent's file:
    the module-level helpers and fixtures it uses (two levels), the imports all of that
    needs, and the test renamed `test_seeded_<name>`. Picked like `related_example`: one
    that names a missed function, else one with a setup, else the first. Returns
    `(block, original name, seeded name)`, or None. Option 1 (user, 2026-10-21): the
    harness gives the agent the repository's own test when it does not take it itself --
    tests that exist before the change, never the pull request's."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return None
    lines = text.splitlines()
    defs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    tests = [n for n in defs.values() if n.name.startswith("test_")]
    # Module-level constants too -- a parametrized test reads its cases from one
    # (xarray-7444's seed of `test_cftimeindex_resample.py::test_resample` did not collect).
    for n in tree.body:
        targets = (n.targets if isinstance(n, ast.Assign)
                   else [n.target] if isinstance(n, ast.AnnAssign) else [])
        for t in targets:
            if isinstance(t, ast.Name) and t.id not in defs:
                defs[t.id] = n
    if not tests:
        return None

    def src(n) -> str:
        first = min([n.lineno] + [d.lineno for d in getattr(n, "decorator_list", [])])
        return "\n".join(lines[first - 1:n.end_lineno])

    def used(n) -> set[str]:
        got = {x.id for x in ast.walk(n) if isinstance(x, ast.Name)}
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            got |= {a.arg for a in n.args.args}
        return got - {getattr(n, "name", None)}

    def names_any(n) -> bool:
        body = src(n)
        return any(re.search(rf"\b{re.escape(m)}\b", body) for m in names)

    pick = (next((n for n in tests if prefer and n.name == prefer), None)
            or next((n for n in tests if names_any(n)), None)
            or next((n for n in tests if n.decorator_list or n.args.args), None) or tests[0])
    helpers: list = []
    want = used(pick)
    for _ in range(2):
        more = [defs[w] for w in sorted(want) if w in defs and defs[w] is not pick
                and defs[w] not in helpers]
        helpers += more
        want = set().union(*[used(h) for h in more]) if more else set()
    need = used(pick).union(*[used(h) for h in helpers]) if helpers else used(pick)
    imports = []
    for node in tree.body:
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        keep = [al for al in node.names if (al.asname or al.name.split(".")[0]) in need]
        if keep:
            names_s = ", ".join(al.name + (f" as {al.asname}" if al.asname else "") for al in keep)
            imports.append(f"from {'.' * node.level}{node.module or ''} import {names_s}"
                           if isinstance(node, ast.ImportFrom) else f"import {names_s}")
    seeded = SEED_PREFIX + pick.name[len("test_"):]
    k = 2
    while seeded in taken:
        seeded, k = f"{SEED_PREFIX}{pick.name[len('test_'):]}_{k}", k + 1
    body = re.sub(rf"\bdef {re.escape(pick.name)}\(", f"def {seeded}(", src(pick), count=1)
    helpers.sort(key=lambda h: h.lineno)
    code = [src(h) for h in helpers if getattr(h, "name", None) not in taken] + [body]
    return ("\n".join(imports) + "\n\n\n" + "\n\n\n".join(code)).strip() + "\n", pick.name, seeded


def related_example(text: str, names: list[str], max_lines: int = 18,
                    prefer: str = "") -> tuple[str, str]:
    """One test function from a repository test file, decorators included, cut at
    `max_lines`: the first that mentions one of `names` (the missed functions' short
    names), else the first. sphinx-10807 (round 2, 2026-10-20) was pointed at
    `tests/test_environment_toctree.py`, read only its first 30 lines -- the imports --
    and never saw the `@pytest.mark.sphinx(testroot=...)` and `app.build()` below them."""
    lines = text.splitlines()
    starts = [i for i, ln in enumerate(lines) if re.match(r"\s*(async\s+)?def test_\w*\(", ln)]
    if not starts:
        return "", ""
    # Where each test's decorators begin, from the parse: a `@pytest.mark.parametrize(`
    # spread over several lines ends in `)`, not `@` -- xarray-7444's `test_resample` was
    # shown without its five parametrize decorators.
    deco_top: dict[int, int] = {}
    try:
        for n in ast.walk(ast.parse(text)):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.decorator_list:
                deco_top[n.lineno - 1] = min(d.lineno for d in n.decorator_list) - 1
    except SyntaxError:
        pass
    spans = []
    for i in starts:
        indent = len(lines[i]) - len(lines[i].lstrip())
        top = deco_top.get(i, i)
        while top > 0 and lines[top - 1].strip().startswith("@"):
            top -= 1
        end = i + 1
        while end < len(lines) and (not lines[end].strip()
                                    or len(lines[end]) - len(lines[end].lstrip()) > indent):
            end += 1
        while end > i + 1 and not lines[end - 1].strip():
            end -= 1
        spans.append((top, end))
    # Else one with a setup -- decorators, or fixtures it takes -- before the first:
    # sphinx-10807's `test_domain_rst.py` opens with `test_parse_directive`, a string parser
    # that reaches none of the change, while its `app`-fixture tests reach most of it.
    def has_setup(a: int, b: int) -> bool:
        d = next(i for i in range(a, b) if re.match(r"\s*(async\s+)?def test_", lines[i]))
        params = re.search(r"\(([^)]*)\)", lines[d])
        own = [x.strip() for x in (params.group(1) if params else "").split(",")
               if x.strip() and x.strip() not in ("self", "cls")]
        return d > a or bool(own)
    def name_of(a: int, b: int) -> str:
        d = next(i for i in range(a, b) if re.match(r"\s*(async\s+)?def test_", lines[i]))
        return re.match(r"\s*(?:async\s+)?def (test_\w*)", lines[d]).group(1)
    pick = (next(((a, b) for a, b in spans if prefer and name_of(a, b) == prefer), None)
            or next(((a, b) for a, b in spans
                     if any(re.search(rf"\b{re.escape(n)}\b", "\n".join(lines[a:b])) for n in names)),
                    next(((a, b) for a, b in spans if has_setup(a, b)), spans[0])))
    a, b = pick
    body = lines[a:min(b, a + max_lines)]
    # Its pytest node name, `Class::test` for a method.
    d = next(i for i in range(a, b) if re.match(r"\s*(async\s+)?def test_", lines[i]))
    name = re.match(r"\s*(?:async\s+)?def (test_\w*)", lines[d]).group(1)
    indent = len(lines[d]) - len(lines[d].lstrip())
    owner = next((m.group(1) for ln in reversed(lines[:a]) if indent and
                  (m := re.match(r"class (\w+)", ln))), "")
    node = f"{owner}::{name}" if owner else name
    # The file's imports the example uses, so it can be copied as it is (2026-10-21):
    # sphinx-10807 (round 10) was shown `test_rst_directive(app)` without its
    # `restructuredtext` and `assert_node` imports, invented a `testroot` for it, hit "test
    # root directory doesn't exist" and deleted the test.
    shown = "\n".join(body)
    used = set(re.findall(r"[A-Za-z_]\w*", "\n".join(lines[a:b])))
    imports = []
    try:
        tree = ast.parse("\n".join(lines))
    except SyntaxError:
        tree = None
    for node in (tree.body if tree else []):
        if node.lineno > a or not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        keep = [al for al in node.names if (al.asname or al.name.split(".")[0]) in used]
        if not keep:
            continue
        names = ", ".join(al.name + (f" as {al.asname}" if al.asname else "") for al in keep)
        imports.append(f"from {'.' * node.level}{node.module or ''} import {names}"
                       if isinstance(node, ast.ImportFrom) else f"import {names}")
    head = "\n".join(imports[:8])
    # Helpers and constants it uses from its own file, named so they are copied too:
    # xarray-7444's `test_calendars` calls `da(...)`, sphinx-10807's `test_abstractmethods`
    # calls `do_autodoc(...)`, both defined in the test file and shown nowhere else.
    own = {}
    for node in (tree.body if tree else []):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            own[node.name] = 1
        elif isinstance(node, ast.Assign):
            own.update({t.id: 1 for t in node.targets if isinstance(t, ast.Name)})
    helpers = sorted(n for n in own if n in used and n != name and not n.startswith("test_"))
    tail = (f"\n# also uses {', '.join(helpers[:6])} -- defined in this same file: copy "
            f"{'them' if len(helpers) > 1 else 'it'} too" if helpers else "")
    return ((head + "\n\n\n" if head else "") + shown
            + ("\n    ..." if b > a + max_lines else "") + tail), node


_CONFIG_READ = re.compile(r"\b(?:config|settings)\.([A-Za-z_]\w*)")


def config_branches(box: Sandbox, cov: dict) -> None:
    """Mark each missed-lines group with the configuration values its missed lines, or the
    line above each, read (`config`). Read at head, inside the patched window.

    sphinx-10807 (round 9, 2026-10-21): of the 23 changed lines no test in the repository
    or the pull request runs, most are the `toc_object_entries_show_parents == 'hide'` and
    `== 'all'` returns -- reachable by building with that value set, which nothing does."""
    texts: dict[str, list[str]] = {}
    for g in cov.get("missed_by_function") or []:
        if not g.get("missed"):
            continue
        lines = texts.setdefault(g["path"], (box.read(g["path"]) or "").splitlines())
        names: set[str] = set()
        for n in g.get("lines") or []:
            for ln in lines[max(n - 2, 0):n]:
                names.update(_CONFIG_READ.findall(ln))
        if names:
            g["config"] = sorted(names)


def related_note(cov: dict) -> str:
    """The `related_tests` of a coverage measurement, as one paragraph; "" without any."""
    rel = cov.get("related_tests") or {}
    if not rel:
        return ""
    rows = [f"  {p}: {', '.join(fs)}" for p, fs in rel.items()]
    out = ("\n\nTests already in the repository that use this code -- read how one of them "
           "sets it up and calls it (fixtures, sample inputs, a small project it builds) "
           "and do the same in your test:\n" + "\n".join(rows))
    reach = cov.get("related_reach") or {}
    if reach:
        parts = ", ".join(f"`{x['function']}` {x['reached']} of {x['missed']}"
                          for x in reach["parts"])
        ex = cov.get("related_example") or {}
        out += (f"\n\n**`{reach['file']}` reaches the code your test misses.** Run here with "
                f"the change applied, it runs {reach['lines']} of the {reach['of']} changed "
                f"lines your test never runs ({parts}). So its setup works in this container "
                f"and goes through this change: build your test the same way -- the same "
                f"fixtures, the same kind of input -- with assertions about what this change "
                f"does."
                + (f" One of its tests:\n\n```python\n{ex['text']}\n```" if ex.get("text") else ""))
    return out


def where_to_call(g: dict) -> str:
    """How to name one missed-lines group as something a test can call."""
    if g["function"] == "<module>":
        return f"the module-level code of `{g['path']}`"
    fname = g["path"].rsplit("/", 1)[-1]
    if g.get("outer") and g["outer"] != g["function"]:
        return (f"`{g['function']}` in `{fname}` -- it is defined inside `{g['outer']}` and "
                f"runs only while that runs, so call `{g['outer']}`, or the code that calls it")
    return f"`{g['function']}` in `{fname}`"


def coverage_report(box: Sandbox, target: str, cov: dict, require_tools: bool,
                    import_only: str = "") -> str:
    """The coverage stage of `verify`: the score against its target, then every changed
    line the test never ran, by function. Only for a fail-to-pass test. `import_only` is
    `_import_only`, worked out while the change was applied (it reads the files there)."""
    if not cov.get("measured"):
        files = cov.get("changed_files") or []
        hint = (f" This pull request changes {', '.join(f'`{f}`' for f in files[:4])}; your "
                f"test has to import that code and call it before any changed line can run."
                if files and cov.get("reason") == "the changed file was never imported by this test"
                else "")
        return f"\n\n## Coverage\n\nCould not measure: {cov.get('reason')}.{hint}"
    pct, covered, total = cov["percent"], cov["covered"], cov["executable_changed_lines"]
    head = (f"\n\n## Coverage: {pct}% of the changed lines run ({covered} of {total}). "
            f"The target is 100%.")
    if not cov["missed"]:
        return head + "\n\nYour test runs every executable line this pull request changed." + import_only
    lines = [head]
    # A test that flips while hardly touching the change (fix 3, 2026-10-19): Qiskit-12904
    # (large set) imported three functions and stopped at 0%, Qiskit-12474 checked a
    # signature at 5%, scipy-21777 caught its own TypeError at 6.5% -- each then made small
    # additions for ten refusals. Asked for a rewrite, not another assertion.
    groups = sorted((g for g in cov.get("missed_by_function") or [] if g.get("missed")),
                    key=lambda g: -g["missed"])
    # Also when every line it runs is one that runs on import (`import_only`): sphinx-10807
    # (2026-10-20) sat at 11.5% -- all of it import-time -- with `hasattr` checks, above the
    # 10% bar, so the alarm never fired after the first versions.
    if (pct < 10 or import_only) and groups:
        g = groups[0]
        lines += ["", f"Your test hardly touches this change. A test that only imports the new "
                      f"code, checks that a name exists, inspects a signature or catches the "
                      f"error a call raises can flip without testing anything. Rewrite it "
                      f"around a call to {where_to_call(g)} ({g['missed']} missed lines), with "
                      f"an input that goes through the changed lines, and assert on what it "
                      f"returns, raises or does."]
    lines += ["", "Changed lines your test never runs, by function. Line numbers are in the "
                  "files *with* the change applied -- the `+` side of the diff -- not in this "
                  "checkout, which is the code before it; read each one in the diff, with "
                  "the conditions above it, which your input has to satisfy:",
              *_missed_by_function(cov),
              "",
              "Make every changed line run: pick inputs that make those conditions true, or "
              "add a second test for a separate case the same change fixes. Reach each line "
              "through the behaviour you assert. Then call `verify` again."
              + related_note(cov) + _spawn_note(box, target) + import_only]
    if require_tools:
        lines += ["", "You will be sent back while coverage is below 100%, one part of the "
                      "change at a time -- each function holding a missed line gets one turn, "
                      "two when the first runs none of its lines -- until it reaches 100% or "
                      "every part has had its turn."]
    return "\n".join(lines)


def mutation_report(r: dict, target: str, require_tools: bool) -> tuple[str, dict]:
    """The mutation stage of `verify`, from one `mutants.probe`: the score, then each wrong
    variant of the fix the test still passes on. Returns the text and the log entry."""
    if not r.get("ok"):
        return (f"\n\n## Mutation\n\nCould not run the variants: {r.get('why', 'unknown')}.",
                {"tool": "mutation", "via": "verify", "target": target,
                 "error": r.get("why", "")})
    got = r.get("mutants") or []
    if not got:
        return (f"\n\n## Mutation\n\n{r.get('why', 'no variants available')}. Nothing to "
                f"read into that -- it is a property of the change, not of your test.",
                {"tool": "mutation", "via": "verify", "target": target, "total": 0,
                 "why": r.get("why", "")})
    killed = [m for m in got if m.agent_kills]
    lived = [m for m in got if not m.agent_kills]
    entry = {"tool": "mutation", "via": "verify", "target": target, "total": len(got),
             "killed": len(killed), "survived": [m.operator for m in lived]}
    lines = [f"\n\n## Mutation: {round(100.0 * len(killed) / len(got), 1)}% of wrong variants "
             f"caught ({len(killed)} of {len(got)}). Maximise it."]
    if not lived:
        return "\n".join(lines + ["", "Every variant tried was caught."]), entry
    lines += ["", "Not caught -- each of these is a broken version of the fix that your test "
                  "still passes on:",
              *[f"  {m.file}:{m.line}    {m.operator}" for m in lived],
              "",
              "Answer each one. Ask whether a reviewer would call the behaviour it breaks "
              "part of what this pull request fixes. Where the answer is yes, your test is "
              "missing an assertion about that behaviour: add one that checks what the code "
              "returns, raises or does, then call `verify` again. Where the answer is no -- "
              "the variant breaks something the change was never about, or nothing "
              "observable at all -- say so in one sentence and leave it. Never assert on the "
              "exact expression a variant changed just to make it fail."]
    if require_tools:
        lines += ["", "You will be sent back while variants survive: add assertions about the "
                      "behaviour they break and call `verify` again, until none survives or an "
                      "honest attempt catches no more. A survivor you judged harmless still "
                      "brings that one attempt."]
    return "\n".join(lines), entry


# What each `pytest.raises` / `pytest.warns` caught, recorded in `verify`'s two runs
# (2026-10-21). xarray-7444 (base-it14) asserted `pytest.raises(ValueError)` twelve times
# and passed on both sides: a ValueError is raised before and after the change, and only
# its message changes ("'offset' and 'base' cannot be present ..." from pandas becomes
# xarray's "base and offset cannot be present ..."). Every good xarray run had `match=`.
CATCH_DIR = "/tmp/f2p_plugin"
CATCH_PLUGIN = r'''"""Records what pytest.raises / pytest.warns caught, per test (F2P harness)."""
import json, os
try:
    import pytest
    _orig_raises, _orig_warns = pytest.raises, pytest.warns
except Exception:  # pragma: no cover
    pytest = None
_REC, _CUR = [], {"test": None}


def pytest_runtest_setup(item):
    _CUR["test"] = item.nodeid


def _name(x):
    if isinstance(x, tuple):
        return "(" + ", ".join(_name(y) for y in x) + ")"
    return getattr(x, "__name__", repr(x))


class _Raises:
    def __init__(self, cm, expected, match):
        self.cm, self.expected, self.match = cm, expected, match

    def __enter__(self):
        __tracebackhide__ = True
        return self.cm.__enter__()

    def __exit__(self, et, ev, tb):
        __tracebackhide__ = True   # the test's traceback shows its own line, not this file
        try:
            _REC.append({"test": _CUR["test"], "kind": "raises", "expected": _name(self.expected),
                         "match": None if self.match is None else str(self.match),
                         "caught": None if et is None else et.__name__,
                         "type_ok": et is not None and issubclass(et, self.expected),
                         "message": None if ev is None else str(ev)[:300]})
        except Exception:
            pass
        return self.cm.__exit__(et, ev, tb)


class _Warns:
    def __init__(self, cm, expected, match):
        self.cm, self.expected, self.match = cm, expected, match

    def __enter__(self):
        __tracebackhide__ = True
        return self.cm.__enter__()

    def __exit__(self, et, ev, tb):
        __tracebackhide__ = True
        try:
            return self.cm.__exit__(et, ev, tb)
        finally:
            try:
                got = [(w.category.__name__, str(w.message)[:300]) for w in list(self.cm)]
                _REC.append({"test": _CUR["test"], "kind": "warns", "expected": _name(self.expected),
                             "match": None if self.match is None else str(self.match),
                             "caught": [g[0] for g in got], "message": [g[1] for g in got]})
            except Exception:
                pass


if pytest is not None:
    def raises(expected, *args, **kwargs):
        if args:
            return _orig_raises(expected, *args, **kwargs)
        return _Raises(_orig_raises(expected, **kwargs), expected, kwargs.get("match"))

    def warns(expected=Warning, *args, **kwargs):
        if args:
            return _orig_warns(expected, *args, **kwargs)
        return _Warns(_orig_warns(expected, **kwargs), expected, kwargs.get("match"))

    try:
        pytest.raises, pytest.warns = raises, warns
    except Exception:
        pass


def pytest_sessionfinish(session, exitstatus):
    out = os.environ.get("F2P_CATCH_OUT")
    if out:
        try:
            with open(out, "w") as f:
                json.dump(_REC, f)
        except Exception:
            pass
'''


def caught_differences(before: list, after: list, limit: int = 3) -> list[str]:
    """For tests whose `pytest.raises` / `pytest.warns` caught something different on the
    two sides -- another message, another type -- one line each."""
    def by_test(rows):
        got: dict[str, list] = {}
        for r in rows or []:
            got.setdefault(r.get("test") or "?", []).append(r)
        return got
    b, a = by_test(before), by_test(after)
    out = []
    for test in b:
        for rb, ra in zip(b[test], a.get(test, [])):
            if rb.get("kind") != ra.get("kind") or (rb.get("caught"), rb.get("message")) == (ra.get("caught"), ra.get("message")):
                continue
            name = test.split("::")[-1]
            call = f"pytest.{rb['kind']}({rb['expected']}" + (f", match={rb['match']!r}" if rb.get("match") else "") + ")"
            def said(r):
                if r["kind"] == "raises":
                    return f"`{r['caught']}: {r['message']}`" if r.get("caught") else "nothing"
                pairs = [f"{c}: {m}" for c, m in zip(r.get("caught") or [], r.get("message") or [])]
                return ", ".join(f"`{p}`" for p in pairs[:2]) or "no warning"
            out.append(f"`{name}`: `{call}` caught {said(rb)} before the change and {said(ra)} after it.")
            if len(out) >= limit:
                return out
    return out


def wrong_matches(before: list, after: list, tests: list[str], limit: int = 3) -> list[str]:
    """For tests that fail once the change is in: a `pytest.raises` / `pytest.warns` whose
    `match=` the code's message after the change does not meet, with that message.

    xarray-7444 (round 15, 2026-10-22) had six of its seven restores on one test,
    `pytest.raises(ValueError, match="'offset' and 'base' ...")`: pandas' message, which
    the old code gives. Once the change is in, xarray raises "base and offset cannot be
    present at the same time" first. The verdict said "assert what the change makes true"
    and the model kept the same `match=`.
    """
    def hit(pattern, message):
        try:
            return bool(re.search(pattern, message or ""))
        except re.error:
            return pattern in (message or "")
    old = {}
    for r in before or []:
        old.setdefault((r.get("test"), r.get("kind"), r.get("match")), r)
    keep = set(tests)
    out = []
    for r in after or []:
        if r.get("test") not in keep or not r.get("match") or not r.get("caught"):
            continue
        name = (r["test"] or "?").split("::")[-1]
        if r["kind"] == "raises":
            got = [(r["caught"], r.get("message") or "")]
        else:
            got = list(zip(r.get("caught") or [], r.get("message") or []))
        if not got or any(hit(r["match"], m) for _, m in got):
            continue
        b = old.get((r["test"], r["kind"], r["match"]))
        b_msgs = ([b.get("message")] if b and b["kind"] == "raises" else (b or {}).get("message") or [])
        was_old = any(hit(r["match"], m) for m in b_msgs if m)
        kind, msg = got[0]
        msg = msg.replace("`", "'")
        line = (f"`{name}`: `pytest.{r['kind']}({r['expected']}, match={r['match']!r})` -- "
                + ("that is the message the code gives BEFORE the change. " if was_old else "")
                + f"Once the change is applied the code {'raises' if r['kind'] == 'raises' else 'warns'} "
                f"`{kind}: {msg[:200]}`, which that `match=` does not meet. ")
        if r["kind"] == "raises" and not r.get("type_ok", kind == r["expected"]):
            line += (f"Its type is not `{r['expected']}` either: expect the type and message the "
                     f"code gives once the change is in.")
        else:
            line += "Put the new message in `match=` (escape regex characters such as `(` `.` `[`)."
        if line not in out:
            out.append(line)
        if len(out) >= limit:
            break
    return out


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
                 coverage: bool = False, mutation: bool = False, probe_mutants: int = 5,
                 require_tools: bool = False, scored_name: str = "", gated: bool = False):
        self.box = box
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
        # Whether the run refuses a stop that leaves a stage's shortfall unanswered; said
        # where the answer arrives.
        self.require_tools = require_tools
        self.log = log if log is not None else []
        # The stages after fail-to-pass (user, 2026-10-19): one `verify` runs every stage
        # its configuration has, on every call once the test flips, and reports them all.
        # They were the `coverage` and `mutation` tools; an agent that felt done after
        # "fail-to-pass" often never asked them.
        self.coverage = coverage
        self.mutation = mutation
        self.probe_mutants = probe_mutants

    def _related(self, cov: dict, target: str) -> dict[str, list[str]]:
        """`related_tests` for the files holding missed lines, biggest first; looked up once
        per file -- the repository's own tests do not change during a run."""
        cache = self.__dict__.setdefault("_related_cache", {})
        groups = sorted((g for g in cov.get("missed_by_function") or [] if g.get("missed")),
                        key=lambda g: -g["missed"])
        paths = list(dict.fromkeys(g["path"] for g in groups))[:4]
        todo = [p for p in paths if p not in cache]
        if todo:
            cache.update({p: [] for p in todo})
            cache.update(related_tests(self.box, todo, target.split("::")[0]))
        # What the repository's own tests reach (2026-10-21): the first file found for each
        # of the two biggest missed files, run once under coverage with the change applied
        # -- this is called inside the patched window. sphinx-10807 was shown a file, an
        # example and "it passes here" for three rounds and still wrote "this is a very
        # constrained environment ... I can't easily create a full Sphinx build"; the lines
        # that setup runs are evidence, not advice.
        missed = set(cov.get("missed") or [])
        # Every missed file's first related test file, not only the two biggest (2026-10-21):
        # sphinx-10807 (round 9) was shown `test_domain_js.py` for its `rst.py` targets --
        # it reaches 1 of the 59 lines left -- while `test_domain_rst.py`, never measured,
        # reaches 30 of them.
        all_paths = list(dict.fromkeys(g["path"] for g in groups))[:RELATED_REACH_FILES]
        todo = [p for p in all_paths if p not in cache]
        if todo:
            cache.update({p: [] for p in todo})
            cache.update(related_tests(self.box, todo, target.split("::")[0]))
        files = list(dict.fromkeys(cache[p][0] for p in all_paths if cache.get(p)))
        # A missed file no repository test names gets the test files of the rest of the
        # change (2026-10-23): xarray-7444 (round 17) never reached the new private
        # `pdcompat._convert_base_to_offset`, which no test imports -- while
        # `test_cftimeindex_resample.py`, the test file of `resample_cftime.py` (the change's
        # caller, with nothing missed and so never measured), runs 4 of its 5 lines.
        if any(not cache.get(p) for p in all_paths):
            others = [p for p in E.patched_source_files(self.patch) if p not in cache]
            if others:
                cache.update({p: [] for p in others})
                cache.update(related_tests(self.box, others, target.split("::")[0]))
            files += [f for f in dict.fromkeys(cache[p][0] for p in E.patched_source_files(self.patch)
                                               if cache.get(p)) if f not in files]
        gains = {f: (self._reach_of(f) or set()) & missed for f in files}
        gains = {f: g for f, g in gains.items() if g}

        def parts_of(gain: set[str]) -> list[dict]:
            got = [{"path": g["path"], "function": g["function"], "missed": g["missed"],
                    "reached": sum(1 for n in g.get("lines") or [] if f"{g['path']}:{n}" in gain)}
                   for g in groups]
            return [x for x in got if x["reached"]]

        def example(f: str, parts: list[dict], best: str = "") -> str:
            # One of its tests: the one that runs most of the part (`best`, from coverage's
            # per-test contexts), else one that names a reached function, else its first.
            # Only for a file that reaches the missed code -- round 4 showed xarray-7444
            # `test_consolidate_slices`, which has nothing to do with it. The test that runs
            # the part since 2026-10-23: sphinx-10807 was shown `test_parse_name(app)` for
            # `ModuleDocumenter.add_content` -- it takes a fixture, and runs none of it.
            key = ("example", f, tuple(x["function"] for x in parts), best)
            if key not in cache:
                names = [x["function"].rsplit(".", 1)[-1] for x in parts
                         if x["function"] != "<module>"]
                cache[key] = related_example(self.box.read(f) or "", names, prefer=best)[0]
            return cache[key]

        if gains:
            f = max(gains, key=lambda f: len(gains[f]))
            parts = parts_of(gains[f])
            cov["related_reach"] = {"file": f, "lines": len(gains[f]), "of": len(missed),
                                    "parts": parts[:6]}
            if ex := example(f, parts):
                cov["related_example"] = {"file": f, "text": ex}
            # For each part, the file that reaches most of it, with its own example: what the
            # target refusal shows.
            by_part: dict[str, dict] = {}
            for f, gain in gains.items():
                for x in parts_of(gain):
                    k = f"{x['path']}::{x['function']}"
                    if k not in by_part or x["reached"] > by_part[k]["reached"]:
                        by_part[k] = {"file": f, "reached": x["reached"], "missed": x["missed"]}
            for k, v in by_part.items():
                g = next((g for g in groups if f"{g['path']}::{g['function']}" == k), {})
                part_lines = {f"{g.get('path')}:{n}" for n in g.get("lines") or []} & gains[v["file"]]
                v["test"] = self._best_test(v["file"], part_lines)
                v["example"] = example(v["file"], [x for x in parts_of(gains[v["file"]])
                                                   if f"{x['path']}::{x['function']}" == k],
                                       v["test"])
            cov["related_by_part"] = by_part
        return {p: cache[p] for p in paths if cache.get(p)}

    def _reach_of(self, test_file: str) -> set[str] | None:
        """The changed lines one repository test file runs, with the change applied; once
        per file. None when it is too big to run here or could not be measured."""
        cache = self.__dict__.setdefault("_related_cache", {})
        key = ("reach", test_file)
        if key not in cache:
            text = self.box.read(test_file) or ""
            if not text or text.count("\n") > RELATED_RUN_MAX_LINES:
                cache[key] = None
            else:
                try:
                    got = E.changed_line_coverage(self.box, [test_file], self.patch, self._base,
                                                  contexts=True)
                    cache[key] = set(got.get("hit") or []) if got.get("measured") else None
                    # Which of its tests ran each line: coverage's `test_function` context,
                    # `module.test_x` or `module.Class.test_x`.
                    by: dict[str, set[str]] = {}
                    for line, ctxs in (got.get("hit_by") or {}).items():
                        for c in ctxs:
                            parts = c.split("|")[0].split(".")
                            if parts and parts[-1].startswith("test"):
                                by.setdefault(line, set()).add(parts[-1])
                    cache[("by_test", test_file)] = by
                except Exception:
                    cache[key] = None
        return cache[key]

    def _best_test(self, test_file: str, lines: set[str]) -> str:
        """The test in `test_file` that runs most of `lines`, from `_reach_of`'s contexts;
        "" when they were not recorded."""
        by = self.__dict__.get("_related_cache", {}).get(("by_test", test_file)) or {}
        count: dict[str, int] = {}
        for ln in lines:
            for t in by.get(ln, ()):
                count[t] = count.get(t, 0) + 1
        return max(sorted(count), key=lambda t: count[t]) if count else ""

    def _unswallowed(self, rel: str, text: str, names: set[str]) -> str:
        """What the test's `except ...: pass` blocks hide: a copy of the file with each of
        them re-raising, run on both sides; the tests of `names` that then fail before the
        change and pass after it, with the old code's error. "" when none do.

        sphinx-10807 (round 16, 2026-10-22) wrapped `config.toc_object_entries_show_parents`
        in `try: ... except AttributeError: pass` -- the exact failure the change fixes --
        passed on both sides, and was told only that an `except: pass` hides errors. Two
        extra runs, and only for a file that passes on both sides and has such a block.
        """
        from openhands_f2p import verify as V
        spots = list(V._SWALLOW.finditer(text))
        if not spots:
            return ""
        copy = V._SWALLOW.sub(lambda m: m.group(0)[:-len("pass")] + "raise", text)
        tmp = str(Path(rel).with_name("test_f2p_unswallow_tmp.py"))
        cmd = E.test_command(self.box, [tmp])
        self.box.write(tmp, copy)
        try:
            before = self.box.exec(cmd, timeout=3600)
            self.box.apply_patch(self.patch)
            try:
                after = self.box.exec(cmd, timeout=3600)
            finally:
                self.box.apply_patch(self.patch, revert=True)
        finally:
            self.box.exec(f"rm -f {shlex.quote(tmp)}", timeout=60)
        b = V.own_outcomes(E.parse_output(before.output), [tmp])
        a = V.own_outcomes(E.parse_output(after.output), [tmp])
        flips = sorted(n for n, v in b.items() if v in ("FAILED", "ERROR")
                       and a.get(n) == "PASSED" and n.split("::")[-1] in names)
        if not flips:
            return ""
        # Which `except` lines sit inside each test, for the sentence.
        where: dict[str, list[int]] = {}
        try:
            lines = [text.count("\n", 0, m.start()) + 1 for m in spots]
            for f in ast.walk(ast.parse(text)):
                if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    where[f.name] = [n for n in lines if f.lineno <= n <= (f.end_lineno or n)]
        except SyntaxError:
            pass
        said = []
        for n in flips[:3]:
            name = n.split("::")[-1]
            at = where.get(name.split("[")[0]) or []
            err = _first_error(before.output, n)
            said.append("Without the `except ...: pass`"
                        + (f" at line {', '.join(map(str, at))}" if at else "")
                        + f", `{name}` fails before the change"
                        + (f" with `{err}`" if err else "") + " and passes after it.")
        return ("\n\nWhat your `except ...: pass` hides -- the harness ran a copy of your file "
                "with those blocks re-raising, on both sides: " + " ".join(said)
                + " That error is your test catching what the change fixes, and the `except` "
                "throws it away. Remove the `try`/`except` around it (keep the assertions) "
                "and that test is fail-to-pass.")

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
        from openhands_f2p import runners
        # Under pytest, both runs load the plugin that records what `pytest.raises` /
        # `pytest.warns` caught (`CATCH_PLUGIN`); the outcomes are the same either way.
        catch = runners.runner_for(self.box)["args"] == "nodes"
        if catch:
            if not getattr(self, "_catch_ready", False):
                self.box.write(f"{CATCH_DIR}/f2p_catch.py", CATCH_PLUGIN)
                self._catch_ready = True
            self.box.exec(f"rm -f {CATCH_DIR}/before.json {CATCH_DIR}/after.json", timeout=60)

        def caught_cmd(side: str) -> str:
            return (f"F2P_CATCH_OUT={CATCH_DIR}/{side}.json PYTHONPATH={CATCH_DIR}${{PYTHONPATH:+:$PYTHONPATH}} "
                    f"{cmd} -p f2p_catch") if catch else cmd
        before = self.box.exec(caught_cmd("before"), timeout=3600)
        base_out = V.own_outcomes(E.parse_output(before.output), [action.target])
        self._base = E.base_texts(self.box, self.patch)
        self.box.apply_patch(self.patch)
        cov: dict | None = None
        import_only = ""
        try:
            after = self.box.exec(caught_cmd("after"), timeout=3600)
            head_out = V.own_outcomes(E.parse_output(after.output), [action.target])
            # A file that did not import at base and does now: its tests failed at base
            # (`V.unimportable_at_base`, the verdict's own rule).
            base_out = V.unimportable_at_base(base_out, head_out)
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
            passes = flips and not any(v in ("FAILED", "ERROR") for v in head_out.values())
            # The coverage stage, inside the patched window (the lines the change adds exist
            # only now). For a fail-to-pass file; and for one that lost an earlier flip, so
            # the hand-back can tell a test that went further from one that fell back.
            if self.coverage and head_out and (passes or any(
                    e.get("f2p_test") for e in self.log if e.get("tool") == "verify")):
                try:
                    cov = E.changed_line_coverage(self.box, [action.target], self.patch,
                                                  self._base)
                    import_only = _import_only(self.box, cov) if cov.get("measured") else ""
                    if cov.get("measured") and cov.get("missed"):
                        cov["related_tests"] = self._related(cov, action.target)
                        config_branches(self.box, cov)
                except Exception as exc:
                    cov = {"measured": False, "reason": f"{type(exc).__name__}: {exc}"}
        finally:
            self.box.apply_patch(self.patch, revert=True)

        failed_before = {n for n, v in base_out.items() if v in ("FAILED", "ERROR")}
        passed_after = {n for n, v in head_out.items() if v == "PASSED"}
        flipped = sorted(failed_before & passed_after)
        still_failing = [n for n, v in head_out.items() if v in ("FAILED", "ERROR")]
        # `reach`: how many changed lines this version runs, read by the hand-back
        # (`V.lost_flip`) to tell a test that went further from one that fell back.
        self.log.append({"tool": "verify", "target": action.target,
                         "before": base_out, "after": head_out, "flipped": flipped,
                         "reach": (cov or {}).get("covered") if (cov or {}).get("measured")
                         else None})

        # `inverted` before `still_failing`. A test that passed at base and fails at head
        # is the closest possible near-miss -- it found the behaviour and asserted the
        # side of it the change removes -- and the generic branch calls that "still
        # fail", which is false (it did not fail before) and points at rewriting rather
        # than at flipping one assertion. django-13279 hit it twice in six verifies.
        inverted = sorted({n for n, v in base_out.items() if v == "PASSED"}
                          & {n for n, v in head_out.items() if v in ("FAILED", "ERROR")})

        # What each `pytest.raises` / `pytest.warns` caught on the two sides (`CATCH_PLUGIN`).
        def rows(side):
            try:
                return json.loads(self.box.read(f"{CATCH_DIR}/{side}.json") or "[]")
            except ValueError:
                return []
        caught_before, caught_after = (rows("before"), rows("after")) if catch else ([], [])
        # A `match=` the message after the change does not meet (fix 5, 2026-10-23).
        wrong = wrong_matches(caught_before, caught_after, still_failing)
        # Tests with a `match=` finding are left out of `_why_both`: their pytest error reads
        # the same on both sides ("DID NOT WARN ... matching the regex") while the message
        # behind it changed, and "fails the same way, the change does not touch what fails"
        # contradicted the `match=` line -- xarray-7444 (round 17) took three tries.
        def explain(nodes):
            return _why_both(before.output, after.output,
                             [n for n in nodes
                              if not any(w.startswith(f"`{n.split('::')[-1]}`") for w in wrong)])
        rel = action.target.split("::")[0]
        hidden = ""
        if not base_out and not head_out:
            head = "NOT fail-to-pass: nothing was collected -- the file does not import."
        elif inverted and not flipped:
            # The others that still fail are named too: requests-1142 (no-second-chance-
            # no-require-tools) had one failing on both sides beside the backwards one,
            # and the headline named only the backwards one.
            both = [n for n in still_failing if n not in inverted]
            head = (f"NOT fail-to-pass, and backwards: {inverted[:3]} pass on the code "
                    f"before the change and fail once it is applied -- the opposite of what "
                    f"is needed, so this is not progress yet. You have found the right "
                    f"behaviour and asserted the old side of it."
                    + (_backwards(after.output, inverted, wrong)
                       or " Assert what the change makes true, not what it replaces.")
                    + (f" {both[:3]} fail on both sides: fix them or delete them."
                       + explain(both) if both else ""))
        elif still_failing and flipped:
            # Part of the file is right. Said as such, because "the test is wrong" alone
            # sent seaborn-3069 into adding tests beside a flipping one for four verifies,
            # and then deleting the one that flipped. Twenty-one of the 700 runs ended
            # holding a correct test next to a broken one.
            # Checked before "backwards" when something also flipped: django-15098
            # (no-second-chance) had one test flip and one backwards and was told only
            # "backwards", never to keep the one that worked.
            back = [n for n in still_failing if n in inverted]
            # The backwards ones named once, under "backwards": Qiskit-12483 (ChaCo wave 2)
            # was told the same test "still fails" and "passes before and fails after".
            both = [n for n in still_failing if n not in back]
            head = (f"NOT fail-to-pass yet, but part of it is right: {flipped[:3]} fail "
                    f"before the change and pass after -- keep those. "
                    + (f"{both[:3]} still fail after the change is applied: fix them or "
                       f"delete them.{explain(both)} "
                       if both else "") +
                    f"Every test in the file has to pass once the change is in."
                    + (f" {back[:3]} pass before the change and fail after: those assert "
                       f"the old side of the behaviour."
                       + (_backwards(after.output, back, wrong)
                          or " Assert what the change makes true instead.") if back else ""))
            head += "".join(f" {w}" for w in wrong
                            if not any(w.startswith(f"`{n.split('::')[-1]}`") for n in back))
        elif still_failing:
            head = (f"NOT fail-to-pass: {still_failing[:3]} still fail after the change "
                    f"is applied. The test is wrong, not the code."
                    + explain(still_failing)
                    + "".join(f" {w}" for w in wrong))
        elif not flipped and base_out and all(v == "SKIPPED" for v in base_out.values()):
            head = ("NOT fail-to-pass: every test was skipped before the change, so none "
                    "of them ran against the old code. Find what skips them in the output "
                    "below and make the test run here.")
        elif not flipped and any(v == "SKIPPED" for v in base_out.values()):
            n_skip = sum(v == "SKIPPED" for v in base_out.values())
            head = (f"NOT fail-to-pass: before the change nothing fails -- "
                    f"{len(base_out) - n_skip} test(s) pass and {n_skip} are skipped. A "
                    f"skipped test cannot show the change; if it skips because something "
                    f"the change adds is missing, let it fail on that instead.")
        elif not flipped:
            head = ("NOT fail-to-pass: the test already passes before the change, so it "
                    "does not test what this pull request changes.")
            # What its own checks caught differently on the two sides (2026-10-21).
            diffs = caught_differences(caught_before, caught_after)
            # What its `except ...: pass` blocks hide (fix 2, 2026-10-23); pytest only, like
            # the plugin.
            if catch:
                try:
                    hidden = self._unswallowed(rel, self.box.read(rel) or "",
                                               {n.split("::")[-1] for n in head_out})
                except Exception:
                    hidden = ""
                head += hidden
            if diffs:
                head += ("\n\nBut your test does see the change -- it just does not assert on it:\n"
                         + "\n".join(f"* {d}" for d in diffs)
                         + "\nThe same call raises or warns on both sides, with a different message "
                           "or type. Assert on what changed -- `match=` with the message the code "
                           "gives once the change is applied, or the type -- and that test fails "
                           "before the change and passes after it.")
        else:
            head = f"Fail-to-pass: {len(flipped)} test(s) fail before and pass after."
            # Which old-code failure is the catch, said so it is kept (2026-10-21).
            # xarray-7444 (round 6) read its own `pytest.raises(match=...)` failing on the
            # old code's message as "the error message matching is too strict", loosened
            # it, passed on the old code and was restored -- three times, never reaching
            # the coverage loop that took it to 94% in rounds 1-3.
            caught = [(n.split("::")[-1], _first_error(before.output, n)) for n in flipped[:3]]
            caught = [(n, e) for n, e in caught if e]
            if caught:
                head += (" " + " ".join(f"`{n}` fails on the old code with `{e}`." for n, e in caught)
                         + " That failure is your test catching what this change fixes: it is "
                           "meant to fail there. Keep those assertions as they are -- loosening "
                           "one so it passes on the old code undoes the flip.")
        # A seeded repository test that fails now, changed from the copy that passed on both
        # sides (2026-10-23): sphinx-10807 (round 18) added `@pytest.mark.sphinx('dummy',
        # testroot='domain-rst')` to its seed -- a test project that does not exist -- was
        # told only "fails the same way on both sides", and then deleted the seed.
        if still_failing:
            head += _seed_changed(self.log, self.box.read(action.target.split("::")[0]) or "",
                                  still_failing)
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
                if self.gated and not ok
                and not (not flipped and not still_failing
                         and getattr(self.box, "_unscoreable_capped", False)) else "")

        # The before and after runs, the side that holds the reason getting the room. A
        # test that still fails, or fails only, once the change is in is explained by the
        # run after it; every other answer by the run before.
        after_matters = bool(still_failing or inverted)
        body = (f"\n\nbefore the change:\n"
                f"{_clip(_condense(before.output), 1000 if after_matters else 2400)}"
                f"\n\nafter the change:\n"
                f"{_clip(_condense(after.output), 2400 if after_matters else 1000)}"
                if base_out or head_out else "")
        # The stages, each logged as a part of this call (`via`), so the stop checks read
        # them the way they read the old tools' answers.
        stages = ""
        f2p_text = self.log[-1].get("f2p_test", "")
        if ok and self.coverage and cov is not None:
            self.log.append({"tool": "coverage", "via": "verify", "target": action.target,
                             "result": cov, "measured_text": f2p_text})
            stages += coverage_report(self.box, action.target, cov, self.require_tools,
                                      import_only)
        if ok and self.mutation:
            from openhands_f2p import mutants as M
            text, entry = mutation_report(
                M.probe(self.box, self.patch, action.target, self.probe_mutants),
                action.target, self.require_tools)
            if entry.get("total"):
                entry["measured_text"] = f2p_text
            self.log.append(entry)
            stages += text
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
        # Tests that skip on the old code and pass on the new one tested nothing before
        # the change. A file is still fail-to-pass when another test flips, but the agent
        # is told: scipy-21996 (ChaCo wave 2) caught the new API's TypeError and skipped
        # in 9 of 15 tests, was credited with all of them, and never heard about it.
        skipped_base = sorted(n for n, v in base_out.items()
                              if v == "SKIPPED" and head_out.get(n) == "PASSED")
        if ok and skipped_base:
            head += (f" But {len(skipped_base)} test(s) are skipped on the code before the "
                     f"change ({skipped_base[:3]}): they never ran against the old code, so "
                     f"they do not test the change. Make each one fail on the old code for "
                     f"the right reason: drop the skip and let the missing behaviour fail "
                     f"the test there. Remove one only if it does not test the change.")
        from openhands_f2p import verify as V
        rel = action.target.split("::")[0]
        current = self.box.read(rel)
        # The general note only when the rerun above did not say what the swallow hides.
        swallow = "" if hidden else V.swallow_note(current)
        # The best fail-to-pass version, put back by the harness itself when this one lost
        # the flip or a real share of the coverage (`V.restore_reason`, user 2026-10-21).
        # The agent is told what was restored and why, and goes on from there.
        got = V.restore_reason(self.log, rel, ok, cov, current)
        if got is not None:
            (i, text, then), why = got
            seeded = V.with_seeds(text, self.log, rel)
            seeds_back = seeded != text
            text = seeded
            self.box.write(rel, text)
            self.log.append({"tool": "restore", "via": "verify", "path": rel, "target": rel,
                             "content": text, "sha": hashlib.sha1(text.encode()).hexdigest(),
                             "from_call": V.call_number(self.log, i),
                             "why": why})
            covered = f", running {then} changed lines" if then is not None else ""
            head += (f"\n\n## Restored\n\nThe version you just checked is worse than your best "
                     f"one: {why}. So the harness has put the best fail-to-pass version back in "
                     f"`{rel}` -- the one `verify` checked at tool call "
                     f"{V.call_number(self.log, i)}{covered}"
                     + (", with the repository tests the harness copied in added back"
                        if seeds_back else "") + ". That is the file on disk now; "
                     f"you do not need to write it back. Everything below is about the version "
                     f"you wrote, so you can see what went wrong in it. To improve on the "
                     f"restored file, change it in small steps -- keep its tests and add to "
                     f"them, one new test at a time -- and call `verify` after each step.")
            duty = ""
        # The version that flipped, when this one does not.
        elif not ok:
            # The whole log, this call's entry included: with `self.log[:-1]`, `_reach_now`
            # read the previous version's reach, so "keep the new calls" (fix 2) never
            # fired from here -- sphinx-10807 (2026-10-20) reached 7 lines against 5 and
            # was told to write the 5-line version back, and did.
            back_to = V.lost_flip(self.log, action.target.split("::")[0],
                                  self.box.read(action.target.split("::")[0]))
            # No "or delete them" beside "keep the new calls": sphinx-10807 (round 2,
            # 2026-10-20) was told both, twice, and deleted the tests that ran more.
            if V.KEEP_NEW_SAID in back_to:
                head = head.replace(" still fail after the change is applied: fix them or delete them.",
                                    " still fail after the change is applied: fix them -- they run "
                                    "more of the change than the version that flipped, so do not "
                                    "delete them.")
            head += back_to
        return VerifyObservation.from_text(head + swallow + elsewhere + duty + stages + body,
                                           is_error=False)


class SandboxVerifyTool(ToolDefinition[VerifyAction, VerifyObservation]):
    name = "verify"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, repo: str = "",
               patch: str = "", log: list | None = None, coverage: bool = False,
               mutation: bool = False, probe_mutants: int = 5, require_tools: bool = False,
               scored_name: str = "", gated: bool = False, **params):
        assert box is not None and repo and patch, "needs a Sandbox, repo and patch"
        stages = [s for s, on in (("which changed lines it runs (coverage, target 100%)",
                                   coverage),
                                  ("which wrong variants of the fix it catches (mutation "
                                   "score)", mutation)) if on]
        return [cls(
            name="verify",
            description=("Check whether your test is fail-to-pass: run it on the code "
                         "before the change, apply the change, run it again. Reverts the "
                         "change afterwards."
                         + (" Once it is fail-to-pass, also reports "
                            + " and ".join(stages) + "." if stages else "")),
            action_type=VerifyAction,
            observation_type=VerifyObservation,
            annotations=ToolAnnotations(readOnlyHint=False),
            executor=_Shown(VerifyExecutor(box, repo, patch, log, coverage, mutation,
                                           probe_mutants, require_tools, scored_name, gated),
                            "verify"),
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

    `verify` needs the patch: without it there is no second state to run a test against,
    and nothing to measure coverage of or mutate.
    """
    features = features if features is not None else FeatureSet.full()
    # One process handles one instance under --parallel, but a serial run reuses this
    # one, and a count that carried over would be attributed to the wrong instance.
    INVENTED.clear()
    briefed = "repo-facts" in features
    guard = "guard" in features
    require_tools = "require-tools" in features
    made = {"run": SandboxRunTool.create(box=box, log=log, guard=guard,
                                         verify_named="verify-tool" in features)[0],
            "write_file": SandboxWriteTool.create(box=box, log=log, guard=guard)[0],
            "run_tests": SandboxTestTool.create(box=box, repo=repo, log=log,
                                                reveal_runner=briefed,
                                                verify_named="verify-tool" in features)[0]}
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
            coverage=("coverage-tool" in features), mutation=("mutation-tool" in features),
            probe_mutants=probe_mutants, require_tools=require_tools,
            scored_name=Path(gen_path).name if gen_path else "",
            gated="require-tools" in features)[0]
        register_tool("verify", made["verify"])
        names.append("verify")
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
