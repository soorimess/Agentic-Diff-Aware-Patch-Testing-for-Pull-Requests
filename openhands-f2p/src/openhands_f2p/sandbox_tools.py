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
            # pylint-4492 (mut-p10, 2026-10-24) was told only `assert 0 > 0` and never found
            # what the 0 was; pytest's own `where` lines and the line that failed say it
            at, where = _failing_line(after, n), _where(after, n)
            said.append(f"`{name}` fails before the change with `{b}` and after it with "
                        f"`{a}`" + (f" at line {at[0]}: `{at[1]}`" if at else "")
                        + (f" ({'; '.join(where)})" if where else "")
                        + ". The first can be the right failure -- what the change "
                        "fixes; the second is a mistake in the test itself: fix that and "
                        "keep the rest.")
            one = _one_value(a, at)
            if one:
                said.append(one)
            if a.startswith("SystemExit"):
                said.append(f"With the change applied the code still ends by raising `{a}` "
                            f"-- that is how it finishes, not an error: catch it with "
                            f"`pytest.raises(SystemExit)` and assert its code and what the "
                            f"run wrote.")
    return (" " + " ".join(said)) if said else ""


_LITERAL = r"-?\d+(?:\.\d+)?|'[^']*'|\"[^\"]*\"|True|False|None"


def _one_value(err: str, at: tuple[int, str] | None) -> str:
    """When the test fails after the change only on the value it expects: name that value.

    pylint-4492 (mut-p23, 2026-10-26) ran pylint with `--output-format=json:...,text:...`,
    failed before the change on the ImportError the change removes and after it on
    `assert 4 == 0` (`assert pylint_code == 0`; 4 = a warning was issued). Told "fix that and
    keep the rest", it dropped the new input instead and never flipped a test again.
    """
    m = re.fullmatch(rf"(?:AssertionError: )?assert ({_LITERAL}) == ({_LITERAL})", err.strip())
    s = re.fullmatch(rf"assert (.+?) == ({_LITERAL})(?:, .*)?", at[1].strip()) if at else None
    if not (m and s and m.group(2) == s.group(2)) or m.group(1) == m.group(2):
        return ""
    return (f"With the change applied `{s.group(1)}` is `{m.group(1)}`, where line {at[0]} "
            f"expects `{s.group(2)}`. If `{m.group(1)}` is the right result for this input, "
            f"put `{m.group(1)}` on line {at[0]} and change nothing else: the input is what "
            f"makes the test fail before the change, so keep it exactly as it is.")


def _where(output: str, node: str) -> list[str]:
    """pytest's `+  where 0 = len([])` lines for `node`: the values its failed assertion
    was made of."""
    got = [ln[1:].strip().lstrip("+").strip() for ln in _section(output, node).splitlines()
           if re.match(r"^E\s+\+\s+where ", ln)]
    return [g.replace("`", "'")[:160] for g in got[:3]]


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
        if not any(n.split("::")[-1].split("[")[0] == name.split("::")[-1] for n in failing):
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


def added_defs(patch: str, max_lines: int = 30) -> dict[str, tuple[str, str]]:
    """Functions and classes a diff adds to library code: name -> (path, its added lines).
    The agent is shown the diff whenever `verify` exists; this only points at a part of it."""
    out: dict[str, tuple[str, str]] = {}
    path, lines = "", (patch or "").splitlines()
    for k, ln in enumerate(lines):
        if ln.startswith("+++ "):
            path = ln[4:].removeprefix("b/").strip()
            continue
        m = re.match(r"^\+(\s*)(?:async\s+)?(?:def|class)\s+(\w+)", ln)
        if not m or not path.endswith(".py") or E.is_test_file(path) or m.group(2) in out:
            continue
        indent, body = len(m.group(1)), [ln[1:]]
        for nxt in lines[k + 1:k + max_lines]:
            if not nxt.startswith("+"):
                break
            text = nxt[1:]
            if text.strip() and len(text) - len(text.lstrip()) <= indent and not text.lstrip().startswith(("#", "@", ")")):
                break
            body.append(text)
        out[m.group(2)] = (path, "\n".join(body).rstrip())
    # A definition the diff also removes is rewritten, not added: it is in the checkout.
    removed = set(re.findall(r"^-\s*(?:async\s+)?(?:def|class)\s+(\w+)", patch or "", re.M))
    return {n: v for n, v in out.items() if n not in removed}


class RunExecutor(ToolExecutor[RunAction, RunObservation]):
    def __init__(self, box: Sandbox, log: list | None = None, guard: bool = True,
                 verify_named: bool = False, patch: str = ""):
        self.box = box
        self.log = log if log is not None else []
        self.guard = guard
        self.verify_named = verify_named
        # Names the change adds, for a search that cannot find them (only when `verify`
        # exists, which is when the agent is shown the diff at all).
        self.added = added_defs(patch) if verify_named and patch else {}

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
        # A search for something the change adds, which finds nothing because the change is
        # not applied (2026-10-23): django-13207 (B rerun) was told "it is new in this change,
        # so it is not in the code you can read now (read it in the diff)" and still grepped
        # the checkout for `_get_column_collations` six times, then gave up on it.
        if self.added and r.returncode != 0 and not (r.output or "").strip() and re.search(
                r"\b(grep|rg|ag|ack)\b", action.command or ""):
            named = [n for n in self.added if re.search(rf"\b{re.escape(n)}\b", action.command)]
            if named:
                n = named[0]
                path, code = self.added[n]
                body += (f"\n\n[harness] `{n}` is added by this change (in `{path}`), so it is "
                         f"not in this checkout: the change is not applied here, and searching "
                         f"for it finds nothing. `verify` applies the change when it runs your "
                         f"test. Its code, from the diff:\n\n```python\n{code}\n```")
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
                                        params.get("verify_named", False),
                                        params.get("patch", "")), "run"),
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
                and not re.search(rf"\bdef {re.escape(e['name'].split('::')[-1])}\(", action.content)]
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
        # A private module's tests drop the underscore: scikit-learn-24145 (B, 2026-10-23)
        # changed `_polynomial.py`, whose tests are `test_polynomial.py` -- never found, so
        # no measured example and no seed.
        stem = stem.lstrip("_")
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
        # Test files under the same package first (2026-10-23): for
        # `django/db/backends/sqlite3/introspection.py`, django-13207 (B) was pointed at the
        # base, mysql and oracle `test_introspection.py`, never `tests/backends/sqlite/`.
        dirs = [d for d in Path(p).parent.parts if len(d) >= 4]
        def near(f: str) -> int:
            parts = Path(f).parent.parts
            return sum(any(d.startswith(t) or t.startswith(d) for t in parts if len(t) >= 4)
                       for d in dirs)
        ranked = both + rest
        ranked = sorted(ranked, key=lambda f: (-near(f), ranked.index(f)))
        picked = ranked[:per_path]
        if picked:
            out[p] = picked
    return out


SEED_PREFIX = "test_seeded_"


def _function_text(text: str, name: str) -> str:
    """The source of the module-level function `name` in `text`, decorators included; a
    method when `name` is `Class::method`."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return ""
    lines = text.splitlines()
    body = tree.body
    if "::" in name:
        cls, name = name.split("::", 1)
        body = next((n.body for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls), [])
    for n in body:
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
    # A test that is a method of a test class (2026-10-24): pylint-4492's measured repository
    # test is `TestRunTC.test_abbreviations_are_not_supported` in `tests/test_self.py`, which
    # runs pylint through the class's `self._runtest`. Module-level functions only, nothing
    # was copied, and the example could not be copied as shown.
    in_class = None
    if not any(prefer and n.name == prefer for n in tests):
        for c in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            meth = next((m for m in c.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                         and m.name.startswith("test") and (m.name == prefer if prefer else True)), None)
            if meth is not None and (prefer or not tests):
                in_class = (c, meth)
                break
    if in_class is not None:
        return _seed_method(text, tree, lines, defs, in_class[0], in_class[1], taken)
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


def _seed_method(text: str, tree, lines: list[str], defs: dict, cls, meth,
                 taken: set[str]) -> tuple[str, str, str] | None:
    """`seed_block` for a test method: the class with that method, its setup and teardown,
    the fixtures and helper methods the test uses (through `self.` or as arguments, two
    levels), class attributes, and the module-level helpers and imports all of it needs.
    The class is renamed `TestSeeded<Name>`, the method `test_seeded_<name>`."""
    def src(n) -> str:
        first = min([n.lineno] + [d.lineno for d in getattr(n, "decorator_list", [])])
        return "\n".join(lines[first - 1:n.end_lineno])
    methods = {m.name: m for m in cls.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))}
    setup = {"setUp", "tearDown", "setup_method", "teardown_method", "setup_class",
             "teardown_class", "setUpClass", "tearDownClass", "setup", "teardown"}
    autouse = {n for n, m in methods.items()
               if any("fixture" in ast.unparse(d) and "autouse" in ast.unparse(d) for d in m.decorator_list)}

    def uses(m) -> set[str]:
        got = {x.attr for x in ast.walk(m) if isinstance(x, ast.Attribute)
               and isinstance(x.value, ast.Name) and x.value.id in ("self", "cls")}
        return got | {a.arg for a in m.args.args}
    keep = {meth.name} | (setup & set(methods)) | autouse
    for _ in range(3):
        keep |= {u for k in list(keep) for u in uses(methods[k]) if u in methods}
    attrs = [n for n in cls.body if isinstance(n, (ast.Assign, ast.AnnAssign))]
    seeded_cls = "TestSeeded" + cls.name.removeprefix("Test")
    k = 2
    while seeded_cls in taken:
        seeded_cls, k = f"TestSeeded{cls.name.removeprefix('Test')}{k}", k + 1
    seeded = SEED_PREFIX + meth.name[len("test_"):] if meth.name.startswith("test_") else SEED_PREFIX + meth.name
    head = src(cls).splitlines()
    cls_line = next(i for i, ln in enumerate(head) if re.match(rf"\s*class {re.escape(cls.name)}\b", ln))
    header = head[:cls_line] + [head[cls_line].replace(f"class {cls.name}", f"class {seeded_cls}", 1)]
    parts = [src(a) for a in attrs] + [src(m) for name, m in methods.items() if name in keep]
    body_text = "\n\n".join(parts)
    body_text = re.sub(rf"\bdef {re.escape(meth.name)}\(", f"def {seeded}(", body_text, count=1)
    block_cls = "\n".join(header) + "\n" + body_text
    # Module-level helpers, constants and imports the class needs (two levels).
    try:
        probe = ast.parse(block_cls)
    except SyntaxError:
        return None
    need = {x.id for x in ast.walk(probe) if isinstance(x, ast.Name)}
    helpers: list = []
    want = set(need)
    for _ in range(2):
        more = [defs[w] for w in sorted(want) if w in defs and defs[w] not in helpers
                and getattr(defs[w], "name", None) != cls.name]
        helpers += more
        want = {x.id for h in more for x in ast.walk(h) if isinstance(x, ast.Name)}
        need |= want
    imports = []
    for node in tree.body:
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        kept = [al for al in node.names if (al.asname or al.name.split(".")[0]) in need]
        if kept:
            names_s = ", ".join(al.name + (f" as {al.asname}" if al.asname else "") for al in kept)
            imports.append(f"from {'.' * node.level}{node.module or ''} import {names_s}"
                           if isinstance(node, ast.ImportFrom) else f"import {names_s}")
    helpers.sort(key=lambda h: h.lineno)
    code = [src(h) for h in helpers if getattr(h, "name", None) not in taken] + [block_cls]
    return (("\n".join(imports) + "\n\n\n" + "\n\n\n".join(code)).strip() + "\n",
            f"{cls.name}::{meth.name}", f"{seeded_cls}::{seeded}")


_COMMON_WORDS = frozenset(
    "self none true false return import from with class else elif raise assert test tests "
    "list dict name names value values args kwargs init str int len def pass for while "
    "lambda yield not and the this that".split())


def _words(text: str) -> set[str]:
    """Lower-case word parts of identifiers and strings (`sub_reporters` -> sub, reporters;
    `MultiReporter` -> multi, reporter), four letters or more, common ones left out."""
    parts = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9]*", text):
        parts += re.findall(r"[A-Z]?[a-z0-9]+|[A-Z]+(?![a-z])", tok)
    words = {p.lower() for p in parts if len(p) >= 4} - _COMMON_WORDS
    return {w[:-1] if w.endswith("s") and len(w) > 4 else w for w in words}


def _test_source(text: str, name: str) -> str:
    """The body of `def name(` in a test file, up to the next definition at its indent."""
    m = re.search(rf"^([ \t]*)def {re.escape(name)}\(", text, re.M)
    if not m:
        return ""
    end = re.compile(rf"^{m.group(1)}(def |class |@)", re.M).search(text, m.end())
    return text[m.start():end.start() if end else len(text)]


def _shared_words(source: str, diff_words: set[str]) -> int:
    return len(_words(source) & diff_words)


# Reading a file back: `open(...)` without a write mode, `.read()`, `read_text()`,
# `json.load(...)`, `readlines()`.
_READS = re.compile(r"\.read(?:lines)?\(|read_text\(|read_bytes\(|json\.load\(|\bopen\((?![^)\n]*['\"][wax]b?['\"])")


def _reads_back(text: str, name: str) -> bool:
    """Whether test `name` reads a file back, in its body or in a helper of the same file it
    calls (pylint's `self._test_output_file(...)`)."""
    src = _test_source(text, name)
    if _READS.search(src):
        return True
    return any(_READS.search(_test_source(text, h)) for h in set(re.findall(r"\b(\w+)\(", src))
               if h != name and not h.startswith("test"))


def read_back_example(u: dict) -> str:
    """How to read one unread output back, built from what the code wrote (2026-10-26):
    "read it back and assert what it holds" alone moved nothing in five rounds."""
    content = str(u.get("content") or "")
    name = Path(str(u.get("file") or "output")).name.replace("<tmp>", "out") or "output"
    m = re.search(r'"([A-Za-z][\w-]*)":\s*"([^"\\]{1,40})"', content)
    if content.lstrip("'\"").startswith(("[", "{")) and m:
        index = "[0]" if content.lstrip("'\"").startswith("[") else ""
        check = f'assert data{index}["{m.group(1)}"] == "{m.group(2)}"'
        read = "data = json.loads(out_file.read_text())"
    else:
        first = next((ln.strip() for ln in content.strip("'\"").split("\\n") if ln.strip()), "")[:50]
        check = f"assert {first!r} in out_file.read_text()" if first else "assert out_file.read_text() == ..."
        read = ""
    holder = u.get("closer") or ""
    shut = (" The code had not closed this file when the test ended -- a read inside the test "
            "sees it empty until the code closes it, so make the code close it first ("
            + (f"the run built a `{holder.split('.')[0]}` that holds `{holder.split('.')[1]}`: get "
               f"that object from what your test holds and call `.{holder.split('.')[1]}()` on it "
               f"before the read)." if holder else
               "its close or cleanup call on the object that writes it).")
            + str(u.get("reach") or "") if u.get("open") else "")
    return (f"For example: `out_file = tmp_path / \"{name}\"`, pass `out_file` to the run where "
            f"it now writes `{u.get('file')}`, then " + (f"`{read}` and " if read else "")
            + f"`{check}` -- with the values the change really writes, shown above." + shut)


def _closers(patch: str) -> list[str]:
    """What the change adds for closing things (`close_output_files` on pylint-4492)."""
    return sorted({c for c in re.findall(r"\b(\w*close\w*)\b", "\n".join(
        ln[1:] for ln in (patch or "").splitlines() if ln.startswith("+") and not ln.startswith("+++")))
        if c not in ("close", "closed")})[:2]


def closer_holder(rows: list, patch: str) -> str:
    """`MultiReporter.close_output_files`: the class whose constructor took or set one of the
    change's closers in the trace, or "" (2026-10-27). pylint-4492 (mut-p24) was told nine
    times to close the file "with its close or cleanup call" and never found which object
    had it."""
    for c in _closers(patch):
        for r in rows or []:
            func = r.get("func") or ""
            if func.endswith(".__init__") and (c in (r.get("args") or {}) or c in (r.get("set") or {})):
                return f"{func.rsplit('.', 2)[-2]}.{c}"
    return ""


def exit_callee(text: str) -> tuple[str, str]:
    """The imported name a test calls inside `pytest.raises(SystemExit)` (`Run`), with the
    import line that binds it; ("", "") when there is none."""
    import ast as _ast
    try:
        tree = _ast.parse(text or "")
    except SyntaxError:
        return "", ""
    imported = {}
    for n in _ast.walk(tree):
        if isinstance(n, _ast.ImportFrom) and n.module and not n.level:
            for a in n.names:
                imported[a.asname or a.name] = f"from {n.module} import {a.name}" + (f" as {a.asname}" if a.asname else "")
    for w in _ast.walk(tree):
        if not isinstance(w, _ast.With) or not any(
                isinstance(i.context_expr, _ast.Call) and getattr(i.context_expr.func, "attr", "") == "raises"
                and any(getattr(a, "id", "") == "SystemExit" for a in i.context_expr.args) for i in w.items):
            continue
        for c in (c for b in w.body for c in _ast.walk(b) if isinstance(c, _ast.Call)):
            if isinstance(c.func, _ast.Name) and c.func.id in imported:
                return c.func.id, imported[c.func.id]
    return "", ""


def exit_entry(box: Sandbox, text: str, holder: str, reach: dict | None = None) -> str:
    """How to keep the object that must be closed, when the test's run ends in `SystemExit`
    (2026-10-27). pylint-4492 (mut-p26) was told eleven times that a `MultiReporter` holds
    `close_output_files`, said "the file closing is complex to test", and dropped it: its
    `Run(args)` sat in `pytest.raises(SystemExit)`, so the test never held the run.
    `Run(..., exit=False)` returns it. The callee's real signature is read in the box.
    `reach` is the trace's path from that callee's object to the holder (mut-p27 was told
    all of the above and still never wrote `exit=False`): with it the lines are given whole."""
    callee, line = exit_callee(text)
    if not callee:
        return ""
    r = box.exec(f"python -c {shlex.quote(line + '; import inspect; print(inspect.signature(' + callee + '))')}",
                 timeout=60)
    sig = (r.stdout or "").strip().splitlines()[-1:] if r.returncode == 0 else []
    if not sig:
        return ""
    sig = re.sub(r"<[^<>]* at 0x[0-9a-f]+>", "...", f"{callee}{sig[0]}")[:200]
    exits = re.findall(r"\b(\w*exit\w*)=", sig)
    what = f"the `{holder.split('.')[0]}`" if holder else "the object that holds the file"
    if exits and reach and reach.get("root") == callee:
        return (f" Your test gets nothing back to close it with: `{callee}(...)` ends by raising "
                f"`SystemExit` inside `pytest.raises`. Its signature is `{sig}`. Write it like "
                f"this instead -- the same arguments, no `pytest.raises`:\n\n"
                f"    run = {callee}([...the same arguments...], {exits[0]}=False)\n"
                f"    run.{reach['path']}.{reach['closer']}()\n"
                f"    data = json.loads(out_file.read_text())\n\n"
                f"`run.{reach['path']}` is the `{reach['holder']}` your run built (read off the run "
                f"itself); after `{reach['closer']}()` the file holds what is shown above.")
    return (f" Your test gets nothing back to close it with: `{callee}(...)` ends by raising "
            f"`SystemExit` inside `pytest.raises`, so what the run built is gone when the test "
            f"reads. Its signature is `{sig}`"
            + (f": `{exits[0]}=False` makes it return instead -- keep what it returns "
               f"(`run = {callee}([...], {exits[0]}=False)`), reach {what} from it, close it, "
               f"then read the file." if exits else
               f": find a way to keep {what} (a parameter, or calling one level lower), close "
               f"it, then read the file."))


def _tool_cache(file: str, content: str) -> bool:
    """A file the tool keeps for itself, not its output (2026-10-27): pylint-4492 (mut-p24) was
    told to read back `/root/.pylint.d/test_module1.stats`, a pickle, ahead of the
    `output.json` its test asked for -- with the pickle's bytes as the example."""
    return bool(re.search(r"/\.[^/<]+/", file)) or "\\x00" in content


def unread_outputs(rows: list, text: str, flipped: list[str], limit: int = 3) -> list[dict]:
    """Files the changed code wrote during a flipping test that the test never reads back
    (2026-10-25): pylint-4492 (mut-p12) ran `-f json:output.json` and `-f json,text` with an
    exact exit code and never opened the file; the judge: "treats exit status as proof of
    output behaviour". Read off the trace's `wrote` rows and the test function's source."""
    names = {n.split("::")[-1].split("[")[0] for n in flipped}
    out, seen = [], set()
    for r in rows or []:
        if r.get("func") != "wrote":
            continue
        test = (r.get("test") or "").split("::")[-1].split("[")[0]
        file = (r.get("args") or {}).get("file", "")
        if test not in names or (test, file) in seen or any(
                s in file for s in (".pytest_cache", "__pycache__", ".coverage", "f2p_")):
            continue
        seen.add((test, file))
        content = str(r.get("ret"))
        if _tool_cache(file, content):
            continue
        if _READS.search(_test_source(text, test)):
            continue
        out.append({"test": test, "file": file, "size": r.get("size"), "content": content[:300],
                    "open": bool(r.get("open"))})
    # The files the test itself names first: the output it asked for.
    out.sort(key=lambda u: Path(u["file"]).name not in _test_source(text, u["test"]))
    return out[:limit]


def start_seed(box: Sandbox, patch: str, rel: str, log: list) -> str:
    """Before the agent starts (2026-10-24, user: useful tests): the repository test that
    runs the most changed lines, with the change applied, copied into the agent's test
    file with its class, setup and helpers -- kept only if it passes on both sides -- and
    the sentences for the opening message. Option 1's seed, given at the start: on
    pylint-4492 the seed was the only thing that ever got the agent's test to drive the
    reporters end to end (base-p2), and in base-p5/p6 the agent never got it, because it
    came only in the coverage loop. Never the pull request's own test."""
    from openhands_f2p import verify as V
    srcs = [p for p in E.patched_source_files(patch) if not E.is_test_file(p)]
    related = related_tests(box, srcs, rel) if srcs else {}
    files = [f for f in dict.fromkeys(fs[0] for fs in related.values() if fs)
             if (box.read(f) or "").count("\n") <= RELATED_RUN_MAX_LINES][:4]
    if not files:
        return ""
    base = E.base_texts(box, patch)
    added = "\n".join(l[1:] for l in patch.splitlines() if l.startswith("+") and not l.startswith("+++"))
    diff_words = _words(added)
    # A change that writes files is best seeded by a test that reads its output back
    # (2026-10-26): the agent copies the seed's pattern, and on pylint-4492 it never read
    # `output.json` while the seed it got only parsed stdout.
    writes = bool(re.search(r"open\([^)\n]*['\"][wa]", added) or "write_text(" in added)
    best = None
    box.apply_patch(patch)
    try:
        for f in files:
            try:
                got = E.changed_line_coverage(box, [f], patch, base, contexts=True)
            except Exception:
                continue
            if not got.get("measured"):
                continue
            count: dict[str, int] = {}
            for ctxs in (got.get("hit_by") or {}).values():
                for c in {c.split("|")[0].split(".")[-1] for c in ctxs}:
                    if c.startswith("test"):
                        count[c] = count.get(c, 0) + 1
            text = box.read(f) or ""
            for t, n in count.items():
                # many tests reach the same lines (every `Run(...)` test on pylint); the tie
                # went to set order, a different seed each run -- the one that shares the
                # change's words (output, reporter, ...) is the one worth building from
                # `writes and _reads_back(...)` was tried (mut-p18): the seed it chose asserts
                # exact output through a helper, the agent never matched it and got no flip.
                key = (n, _shared_words(_test_source(text, t), diff_words), t)
                if best is None or key > best[4]:
                    best = (f, t, n, got.get("executable_changed_lines"), key)
    finally:
        box.apply_patch(patch, revert=True)
    if best is None:
        return ""
    f, t, n, total, _ = best
    made = seed_block(box.read(f) or "", [], set(), prefer=t)
    if made is None:
        return ""
    block, original, seeded = made
    text = (f"# Copied unchanged by the harness from {f}::{original}, a test in this "
            f"repository before this change.\n" + block)
    box.write(rel, text)
    cmd = E.test_command(box, [f"{rel}::{seeded}"])
    sides = {"before": V.own_outcomes(E.parse_output(box.exec(cmd, timeout=600).output), [rel])}
    box.apply_patch(patch)
    try:
        sides["after"] = V.own_outcomes(E.parse_output(box.exec(cmd, timeout=600).output), [rel])
    finally:
        box.apply_patch(patch, revert=True)
    if any(not o or any(v != "PASSED" for v in o.values()) for o in sides.values()):
        box.exec(f"rm -f {shlex.quote(rel)}", timeout=60)
        log.append({"tool": "seed", "via": "harness", "path": rel, "part": "start",
                    "from": f"{f}::{original}", "error": f"does not pass on both sides: {sides}"})
        return ""
    log.append({"tool": "seed", "via": "harness", "path": rel, "target": rel, "content": text,
                "sha": hashlib.sha1(text.encode()).hexdigest(), "part": "start",
                "from": f"{f}::{original}", "name": seeded, "block": block})
    return (f"\n\n## A starting point\n\nThe harness has put a test from this repository in "
            f"`{rel}`: a copy, unchanged, of `{f}::{original}`. With the change applied it runs "
            f"{n} of the change's {total} changed lines -- its setup reaches the changed code in "
            f"this container, which is the hard part. It passes on both sides of the change, so "
            f"as it stands it tests nothing about the change. Build your test from it: keep it "
            f"and its helpers, and add tests next to it that use the same setup with input that "
            f"goes through what this change does, asserting what the change produces -- the "
            f"objects, the output, the files written. `compare` shows those exact values before "
            f"and after the change, and `verify` lists what the changed functions did in your "
            f"tests. Where it checks what the code wrote -- a file it reads back, the output it "
            f"captures -- check the same way in your tests."
            + _seed_entry(text))


def _seed_entry(text: str) -> str:
    """The seed's own asserting helper, named in the opening message (2026-10-26): every
    pylint-4492 run the judge called meaningful (p12, p13, p17) tested the change through the
    seed's `_runtest(args, code=N)` end to end; the runs that did not (27-53%) drifted into
    private attributes and `hasattr`. Both kinds started from the same message."""
    from openhands_f2p import verify as V
    helpers = V.asserting_helpers(text, limit=2)
    if not helpers:
        return ""
    return ("\n\nThe quickest real test of the change is the seed's own call with the change's "
            "new input: " + helpers.strip().replace(
                "This file already has helpers that check a result: ", "")
            + " Run the code the way a user does through it, with input only the changed code "
              "accepts, and assert the exact result and what it writes -- not that a name or "
              "an attribute exists.")


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


def mark_new(box: Sandbox, cov: dict, patch: str, base: dict[str, str]) -> None:
    """Mark each missed-lines group whose function the change adds (`new`), with the
    functions the changed code calls it from (`called_from`). Read at head, inside the
    patched window; `base` holds the changed files' text before the change."""
    groups = [g for g in cov.get("missed_by_function") or [] if g.get("function") != "<module>"]
    if not groups:
        return
    heads: dict[str, str] = {}
    spans: dict[str, list[tuple[int, int, str]]] = {}
    for p in E.patched_source_files(patch):
        text = box.read(p) or ""
        heads[p] = text
        got = []
        try:
            def walk(node, prefix=""):
                for n in ast.iter_child_nodes(node):
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        q = f"{prefix}{n.name}"
                        if not isinstance(n, ast.ClassDef):
                            got.append((n.lineno, n.end_lineno or n.lineno, q))
                        walk(n, q + ".")
            walk(ast.parse(text))
        except SyntaxError:
            pass
        spans[p] = got
    for g in groups:
        short = g["function"].rsplit(".", 1)[-1]
        if re.search(rf"^\s*(?:async\s+)?def {re.escape(short)}\(", base.get(g["path"]) or "", re.M):
            continue
        g["new"] = True
        callers = []
        for p, text in heads.items():
            for k, ln in enumerate(text.splitlines(), 1):
                if re.search(rf"\b{re.escape(short)}\(", ln) and not re.match(r"\s*(?:async\s+)?def ", ln):
                    inner = [s for s in spans.get(p, []) if s[0] <= k <= s[1]]
                    if not inner:
                        continue
                    q = min(inner, key=lambda s: s[1] - s[0])[2]
                    name = q if p == g["path"] else f"{q} in {p}"
                    if q.rsplit(".", 1)[-1] != short and name not in callers:
                        callers.append(name)
        if callers:
            g["called_from"] = callers[:3]


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
    # The whole path (2026-10-23): django-13207 (B) was sent to "`_get_column_collations`
    # in `introspection.py`" -- five changed files carry that name.
    fname = g["path"]
    if g.get("outer") and g["outer"] != g["function"]:
        return (f"`{g['function']}` in `{fname}` -- it is defined inside `{g['outer']}` and "
                f"runs only while that runs, so call `{g['outer']}`, or the code that calls it")
    said = f"`{g['function']}` in `{fname}`"
    # New in this change, and who calls it (2026-10-23): the same run grepped the checkout
    # for `_get_column_collations` five times, found nothing -- it exists only once the
    # change is applied -- and gave up on it.
    if g.get("new"):
        said += (" -- it is new in this change, so it is not in the code you can read now "
                 "(read it in the diff)")
        if g.get("called_from"):
            said += (f"; the change calls it from "
                     f"{', '.join(f'`{c}`' for c in g['called_from'][:3])}: call that, with "
                     f"input that takes it there")
    return said


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
                      "change at a time -- each function holding a missed line keeps its turns "
                      "while each one runs more of its lines -- until it reaches 100% or every "
                      "part has had its turns."]
    return "\n".join(lines)


# Wrong versions the mutation stage runs per `verify`: the model's plausible ones first,
# then `mutmut`'s on the changed lines. It ran the whole shown half before -- up to 20 per
# call, which made every base+mutation run half again as long for no change in the test.
OBSERVE_MAX = 6


def _trace_diff(fix: list, wrong: list, limit: int = 2) -> list[str]:
    """What the changed functions did differently, in the same tests, under a wrong
    version: the observable difference a test could assert. Empty when none showed."""
    def key(r):
        return (r.get("test"), r.get("func"), json.dumps(r.get("args") or {}, sort_keys=True))
    a = {key(r): r for r in fix if r.get("func") != "reach"}
    b = {key(r): r for r in wrong if r.get("func") != "reach"}
    said = []
    # a file the code wrote is the plainest thing to assert, so its differences go first
    for k, r in sorted(a.items(), key=lambda kv: kv[1].get("func") != "wrote"):
        test = (r.get("test") or "?").split("::")[-1]
        args = ", ".join(f"{x}={v}" for x, v in (r.get("args") or {}).items())
        call = f"`{r['func']}({args if len(args) <= 80 else args[:80] + '...'})`"
        w = b.get(k)
        if r.get("func") == "wrote":
            file = (r.get("args") or {}).get("file", "?")
            if w is None:
                said.append(f"in `{test}`, the file `{file}` was never written")
            elif (w.get("ret"), w.get("size")) != (r.get("ret"), r.get("size")):
                got, want = str(w.get("ret")), str(r.get("ret"))
                if got[:150] == want[:150]:   # same start: only the length shows it
                    said.append(f"in `{test}`, the file `{file}` held {w.get('size')} bytes instead "
                                f"of {r.get('size')}, starting the same: `{want[:100]}`")
                else:
                    said.append(f"in `{test}`, the file `{file}` held `{got[:150]}` instead of "
                                f"`{want[:150]}`")
        elif w is None:
            said.append(f"in `{test}`, {call} never ran")
        elif w.get("ret") != r.get("ret"):
            said.append(f"in `{test}`, {call} returned `{w.get('ret')}` instead of `{r.get('ret')}`")
        else:
            for attr, v in (r.get("set") or {}).items():
                if (w.get("set") or {}).get(attr) != v:
                    said.append(f"in `{test}`, {call} set `self.{attr}` to "
                                f"`{(w.get('set') or {}).get(attr)}` instead of `{v}`")
                    break
        if len(said) >= limit:
            break
    return [x.replace("\n", " ")[:400] for x in said]


def wrong_versions_report(got: list | dict, target: str, require_tools: bool) -> tuple[str, dict]:
    """The mutation stage of `verify` (2026-10-24, user): wrong versions of the change run
    against the test, and for each that it still passes, what the changed code did
    differently in the agent's own tests -- the value to assert. Survivors that showed no
    difference in those tests are counted, not listed: either the tests never reach what
    they change, or they change nothing a test here can observe."""
    if isinstance(got, dict):
        return (f"\n\n## Wrong versions of the change\n\nCould not run them: {got.get('why')}.",
                {"tool": "mutation", "via": "verify", "target": target, "error": got.get("why", "")})
    if not got:
        return ("\n\n## Wrong versions of the change\n\nNone could be made from these lines.",
                {"tool": "mutation", "via": "verify", "target": target, "total": 0})
    killed = [g for g in got if g["killed"]]
    by_assert = sum(1 for g in killed if g["kind"] == "assertion")
    seen = [g for g in got if not g["killed"] and g["seen"]]
    blind = [g for g in got if not g["killed"] and not g["seen"]]
    entry = {"tool": "mutation", "via": "verify", "target": target, "total": len(got),
             "killed": len(killed), "by_assertion": by_assert,
             "survived": [g["mutant"].operator for g in seen + blind],
             "observable": len(seen)}
    lines = [f"\n\n## Wrong versions of the change: your test catches {len(killed)} of {len(got)}"
             f" ({by_assert} by an assertion, {len(killed) - by_assert} only because the code "
             f"crashed)"]
    if seen:
        lines += ["", "Your test still passes on these, though your own tests can see the "
                      "difference:"]
        for g in seen:
            m = g["mutant"]
            lines.append(f"* {m.operator} (`{m.file}` line {m.line}): " + "; ".join(g["seen"]) + ".")
        lines += ["", "For each, assert the value the real change gives in that call -- what it "
                      "returns, or holds afterwards -- and this wrong version fails your test. "
                      "First ask whether a reviewer would call that behaviour part of what the "
                      "change is for; if not, say so and leave it."]
    # a model-written version names a behaviour, which is worth listing even when the trace
    # saw nothing -- what it breaks is often a file or stdout, which the trace does not record
    named = [g for g in blind if g["mutant"].name.startswith("wrong-")]
    if named:
        lines += ["", "Your test also passes on these, and the calls it makes look the same under "
                      "them -- what they break is something your test does not check, such as "
                      "the file or text the code writes:"]
        lines += [f"* {g['mutant'].operator} (`{g['mutant'].file}` line {g['mutant'].line})"
                  for g in named]
        lines += ["", "For each one a reviewer would call part of what the change is for, run the "
                      "code the way the change is used and assert the result this version gets "
                      "wrong -- read the file it writes, the output it prints, the value it "
                      "returns -- so this version fails your test. If it is not part of the "
                      "change, say so and leave it."]
    if len(blind) > len(named):
        lines += ["", f"{len(blind) - len(named)} more pass your test with no difference your "
                      f"tests can see: your calls do not reach what they change, or they change "
                      f"nothing observable."]
    if not seen and not blind:
        lines += ["", "Every wrong version tried was caught."]
    return "\n".join(lines), entry


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


# What the changed functions did while the agent's tests ran with the change applied
# (2026-10-24, user: useful tests). pylint-4492 wrote test after test that only checked
# names, option strings or "does not raise": it never saw what the change builds -- its
# checkout is the code before the change, `verify` says pass or fail, and it called
# `compare` to print `hasattr(...)`. This records, for each changed function its tests
# ran, the arguments, the return value and the attributes it set on `self`, so the answer
# can say "`PyLinter._load_reporters()` set `self.reporter = MultiReporter(...)`".
TRACE_PLUGIN = r'''"""Records what the changed functions did during each test (F2P harness)."""
import json, os, re, sys
try:
    import pytest
except Exception:  # pragma: no cover
    pytest = None
try:
    _SPEC = [tuple(x) for x in json.load(open(os.environ.get("F2P_TRACE_SPEC", "")))]
except Exception:
    _SPEC = []
_NAMES = {n for _, n in _SPEC}
_REC, _CUR, _SEEN, _STACK = [], {"test": None}, {}, {}
# The entry point a test runs inside `pytest.raises(SystemExit)` (`Run`) and the change's
# close functions (`close_output_files`): instances of the first are kept while the test runs,
# and at its end the attribute path from one to an object with a closer is recorded
# (`run.linter.reporter`). mut-p26/p27 were told the holder and how to keep the run, and
# never found the path between them.
_ROOTS = {x for x in os.environ.get("F2P_TRACE_ROOTS", "").split(",") if x}
_CLOSERS = [x for x in os.environ.get("F2P_TRACE_CLOSERS", "").split(",") if x]
_KEPT = []


import tempfile
_BASES = "|".join(re.escape(b) for b in sorted({tempfile.gettempdir(), os.path.realpath(tempfile.gettempdir())}, key=len, reverse=True))
_TMP = re.compile(rf"(?:{_BASES})/(?:pytest-of-[^/\s'\"]+/pytest-\d+|tmp[\w-]+)"
                  # and a bare `tempfile` name -- the module pylint names after a
                  # NamedTemporaryFile, `tmp9yztff7a` (mut-p14: every wrong version "never ran")
                  rf"|\btmp[a-z0-9_]{{8}}\b")


def _short(v, depth=0):
    # Memory addresses and temporary directories (pytest-1, pytest-2, ...) differ from run
    # to run; without this, the same call under the fix and under a wrong version read as
    # two different calls.
    return _TMP.sub("<tmp>", re.sub(r" at 0x[0-9a-fA-F]+", "", _short_raw(v, depth)))


# Files the code writes during a test: the output of a command-line tool is often a file,
# not a return value (pylint-4492's `--output-format=json:out.json`), and a wrong version
# that leaves it empty showed no difference in the calls alone.
import builtins, io
_REAL_OPEN = builtins.open
_WROTE, _OPEN = {}, []


def _wrote(path, test=None, copy=None, still_open=False):
    # `test`: the test that opened the file -- pylint's output file is closed by garbage
    # collection, often while the next test runs, and was put down to that one.
    # `copy`: what was written through the file object, for a file the test deleted
    # before it ended (mut-p15 unlinked its JSON and text outputs: nothing was recorded).
    test = test or _CUR["test"]
    try:
        if test is None or any(s in path for s in ("site-packages", "__pycache__", ".coverage")):
            return
        # Temporary directories inside the content too (pylint's JSON names the linted
        # file by its path): measured after that, or the same output under the fix and a
        # wrong version read "578 bytes instead of 578" (mut-p13).
        if os.path.exists(path):
            with _REAL_OPEN(path, errors="replace") as f:
                whole = f.read(1 << 20)
        elif copy is not None:
            whole = "".join(x if isinstance(x, str) else x.decode("utf-8", "replace") for x in copy)
        else:
            return
        whole = _TMP.sub("<tmp>", whole)
        text = (len(whole), whole[:600], still_open)
        name = _TMP.sub("<tmp>", os.path.relpath(path) if not os.path.isabs(path) or path.startswith(os.getcwd()) else path)
        _WROTE[(test, name)] = text
    except Exception:
        pass


class _Watched:
    def __init__(self, f, path):
        object.__setattr__(self, "_f", f)
        object.__setattr__(self, "_p", path)
        object.__setattr__(self, "_t", _CUR["test"])
        object.__setattr__(self, "_c", [])

    def write(self, s):
        if sum(len(x) for x in self._c) < (1 << 20):
            self._c.append(s)
        return self._f.write(s)

    def writelines(self, lines):
        for s in lines:
            self.write(s)

    def __getattr__(self, n):
        return getattr(self._f, n)

    def __setattr__(self, n, v):
        setattr(self._f, n, v)

    def __iter__(self):
        return iter(self._f)

    def __enter__(self):
        self._f.__enter__()
        return self

    def __exit__(self, *a):
        r = self._f.__exit__(*a)
        _wrote(self._p, self._t, self._c)
        return r

    def close(self):
        self._f.close()
        _wrote(self._p, self._t, self._c)


_STDLIB = os.path.dirname(os.__file__)


def _by_test():
    # The first frame outside the standard library: when it is the test file itself, the
    # test is writing its own input (a module to lint), not the code under test its output.
    f = sys._getframe(2)
    while f is not None and f.f_code.co_filename.startswith(_STDLIB):
        f = f.f_back
    return f is not None and os.path.abspath(f.f_code.co_filename) == _CUR.get("file")


def _open(file, mode="r", *args, **kwargs):
    f = _REAL_OPEN(file, mode, *args, **kwargs)
    if isinstance(file, (str, bytes, os.PathLike)) and any(c in mode for c in "wax") and not _by_test():
        try:
            w = _Watched(f, os.fsdecode(file))
            _OPEN.append(w)
            return w
        except Exception:
            return f
    return f


def _short_raw(v, depth=0):
    try:
        if isinstance(v, (set, frozenset)) and depth < 2:
            # hash order changes between processes; sorted, the same set reads the same
            items = sorted(_short(x, depth + 1) for x in v)[:5]
            return ("{" + ", ".join(items) + (", ..." if len(v) > 5 else "") + "}")[:240]
        if isinstance(v, (list, tuple)) and depth < 2:
            items = [_short(x, depth + 1) for x in list(v)[:5]]
            o, c = ("[", "]") if isinstance(v, list) else ("(", ")")
            return (o + ", ".join(items) + (", ..." if len(v) > 5 else "") + c)[:240]
        if isinstance(v, dict) and depth < 2:
            items = [f"{k!r}: {_short(x, depth + 1)}" for k, x in list(v.items())[:5]]
            return ("{" + ", ".join(items) + (", ..." if len(v) > 5 else "") + "}")[:240]
        r = repr(v)
        if " object at 0x" in r or (r.startswith("<") and r.endswith(">")):
            name = type(v).__name__
            if depth == 0 and hasattr(v, "__dict__"):
                parts = [f"{k}={_short(x, 1)}" for k, x in list(vars(v).items())[:6]]
                return f"{name}({', '.join(parts)})"[:240]
            return name
        return r[:160]
    except Exception:
        return "<unrepresentable>"


def _reach():
    import types
    skip = (types.ModuleType, type, types.FunctionType, types.MethodType, types.BuiltinFunctionType,
            str, bytes, int, float, bool, list, tuple, dict, set, frozenset, type(None))
    seen, level = set(), [(o, type(o).__name__, "") for o in _KEPT]
    for _ in range(4):
        nxt = []
        for o, root, p in level:
            if id(o) in seen:
                continue
            seen.add(id(o))
            for c in _CLOSERS:
                if p and callable(getattr(o, c, None)):
                    return {"root": root, "path": p, "closer": c, "holder": type(o).__name__}
            d = getattr(o, "__dict__", None)
            if isinstance(d, dict):
                nxt += [(v, root, f"{p}.{k}" if p else k) for k, v in list(d.items())
                        if not k.startswith("__") and not isinstance(v, skip)]
        level = nxt
    return None


def _prof(frame, event, arg):
    code = frame.f_code
    if _ROOTS and event == "call" and code.co_name == "__init__":
        me = frame.f_locals.get("self")
        if me is not None and type(me).__name__ in _ROOTS and len(_KEPT) < 20:
            _KEPT.append(me)
    if code.co_name not in _NAMES or event not in ("call", "return"):
        return
    if not any(code.co_filename.endswith(p) and code.co_name == n for p, n in _SPEC):
        return
    key = id(frame)
    me = frame.f_locals.get("self")
    if event == "call":
        _STACK[key] = ({k: _short(x, 1) for k, x in vars(me).items()}
                       if me is not None and hasattr(me, "__dict__") else None)
        return
    snap = _STACK.pop(key, None)
    seen = (_CUR["test"], code.co_name)
    if _SEEN.get(seen, 0) >= 2:
        return
    _SEEN[seen] = _SEEN.get(seen, 0) + 1
    changed = {}
    if snap is not None and me is not None and hasattr(me, "__dict__"):
        for k, x in vars(me).items():
            if snap.get(k) != _short(x, 1):
                changed[k] = _short(x)
    names = code.co_varnames[:code.co_argcount + code.co_kwonlyargcount]
    args = {k: _short(frame.f_locals[k], 1) for k in names if k != "self" and k in frame.f_locals}
    qual = (type(me).__name__ + "." if me is not None else "") + code.co_name
    _REC.append({"test": _CUR["test"], "func": qual, "args": args,
                 "ret": _short(arg), "set": changed})


if pytest is not None:
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_call(item):
        _CUR["test"] = item.nodeid
        _CUR["file"] = os.path.abspath(str(item.fspath))
        old = sys.getprofile()
        sys.setprofile(_prof)
        builtins.open = io.open = _open
        try:
            yield
        finally:
            builtins.open = io.open = _REAL_OPEN
            sys.setprofile(old)
            # pylint leaves its output file open until garbage collection: what it holds
            # at the end of the test is read after a flush
            for w in _OPEN:
                try:
                    if not w._f.closed:
                        # still open when the test ended: what a read inside the test saw is
                        # only what had been flushed -- pylint's output file read back as ''
                        # (mut-p18); flushed here so the record shows what it will hold
                        w._f.flush()
                        _wrote(w._p, w._t, w._c, still_open=True)
                except Exception:
                    pass
            if _KEPT and _CLOSERS:
                try:
                    got = _reach()
                    if got:
                        _REC.append({"test": item.nodeid, "func": "reach", "args": got, "ret": None, "set": {}})
                except Exception:
                    pass
            del _KEPT[:]
            del _OPEN[:]
            for (test, name), text in list(_WROTE.items()):
                if test == item.nodeid:
                    _REC.append({"test": test, "func": "wrote", "args": {"file": name},
                                 "ret": repr(text[1]), "size": text[0], "set": {},
                                 "open": bool(text[2])})
            _CUR["test"] = None


def pytest_sessionfinish(session, exitstatus):
    out = os.environ.get("F2P_TRACE_OUT")
    if out:
        try:
            with open(out, "w") as f:
                wrote = [r for r in _REC if r["func"] in ("wrote", "reach")][:60]
                json.dump([r for r in _REC if r["func"] not in ("wrote", "reach")][:200] + wrote, f)
        except Exception:
            pass
'''


def watched_functions(box: Sandbox, patch: str) -> list[list[str]]:
    """`[path, name]` for each function holding a line the change adds or alters, read at
    head -- call it with the change applied."""
    out: list[list[str]] = []
    for path, lines in E.changed_lines(patch).items():
        if not path.endswith(".py") or E.is_test_file(path):
            continue
        try:
            tree = ast.parse(box.read(path) or "")
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and \
                    any(n.lineno <= ln <= (n.end_lineno or n.lineno) for ln in lines):
                if [path, n.name] not in out:
                    out.append([path, n.name])
    return out


def trace_said(rows: list, limit: int = 8, patch: str = "",
               watched: list | None = None) -> str:
    """The section of a `verify` answer that says what the changed functions did. Only the
    attributes the diff itself sets or reads on `self` are shown -- `PyLinter.__init__`
    sets dozens, and pylint-4492 (base-p6) was shown `msgs_store` first -- and the changed
    functions the tests never ran are named."""
    named = set(re.findall(r"\bself\.(\w+)", "\n".join(
        ln[1:] for ln in (patch or "").splitlines() if ln.startswith("+") and not ln.startswith("+++"))))
    said, seen = [], set()
    # Calls that return something first: a public result is the thing to assert; a private
    # attribute (`_name`) only when nothing public shows the change (the user's mutation
    # briefing, 2026-10-24: a test on implementation details rejects valid alternatives).
    # What the change adds for closing things (`close_output_files` on pylint-4492): named
    # beside a file that was still open when the test ended.
    closers, holder = _closers(patch), closer_holder(rows, patch)
    rows = sorted((r for r in rows if r.get("func") != "reach"),
                  key=lambda r: (r.get("func") != "wrote", r.get("ret") in (None, "None")))
    for r in rows:
        if r.get("func") == "wrote":
            file = (r.get("args") or {}).get("file", "?")
            if ("wrote", file, r.get("ret")) in seen or _tool_cache(file, str(r.get("ret"))):
                continue
            seen.add(("wrote", file, r.get("ret")))
            text = str(r.get("ret"))
            said.append(f"* the run wrote the file `{file}` ({r.get('size', '?')} bytes): "
                        f"`{text if len(text) <= 300 else text[:300] + '...'}`"
                        + (" -- STILL OPEN when the test ended: the code had not closed it, so a "
                           "read inside your test sees only what was flushed so far (often "
                           "nothing). Close it the way the code does -- its close or cleanup call"
                           + (f" (the run built a `{holder.split('.')[0]}` that holds "
                              f"`{holder.split('.')[1]}`: call it on that object)" if holder else
                              " (the change adds " + ", ".join(f"`{c}`" for c in closers) + ")"
                              if closers else "")
                           + " -- before you read it" if r.get("open") else "")
                        + f" -- in `{(r.get('test') or '?').split('::')[-1]}`")
            if len(said) >= limit:
                break
            continue
        if named and r.get("set"):
            r = dict(r, set={k: v for k, v in r["set"].items() if k in named})
        key = (r.get("func"), tuple(sorted((r.get("args") or {}).items())), tuple(sorted((r.get("set") or {}).items())), r.get("ret"))
        # A call that set nothing and returned nothing says nothing to assert.
        if key in seen or (not r.get("set") and r.get("ret") in (None, "None")):
            continue
        seen.add(key)

        def cut(v: str, n: int = 120) -> str:
            v = str(v).replace("\n", " ")
            return v if len(v) <= n else v[:n] + "..."
        args = ", ".join(f"{k}={cut(v, 60)}" for k, v in (r.get("args") or {}).items())
        line = f"* `{r['func']}({args})`"
        if r.get("set"):
            line += " set " + ", ".join(f"`self.{k} = {cut(v)}`" for k, v in list(r["set"].items())[:3])
        if r.get("ret") not in (None, "None"):
            line += (" and" if r.get("set") else "") + f" returned `{cut(r['ret'])}`"
        line += f" -- in `{(r.get('test') or '?').split('::')[-1]}`"
        said.append(line.replace("\n", " "))
        if len(said) >= limit:
            break
    ran = {(r.get("func") or "").rsplit(".", 1)[-1] for r in rows}
    unrun = [n for _, n in (watched or []) if n not in ran and not n.startswith("__")]
    if not said and not unrun:
        return ""
    return ("\n\n## What the change did while your tests ran (with it applied)\n\n"
            + ("\n".join(said) + "\n\nThese are the values the changed code produced in your "
               "own tests. Assert them -- the value returned, the output written, what the "
               "public objects hold -- not that the call ran or that a name exists. Prefer "
               "what the code gives through its public interface; assert a private attribute "
               "(`_name`) only when nothing public shows the change, since another correct "
               "implementation may not have it." if said else "")
            + (("\n\n" if said else "") + "Changed functions your tests never ran: "
               + ", ".join(f"`{n}`" for n in unrun[:6]) + ". Call the code that runs them, with "
               "input that takes it there, and assert on what they produce." if unrun else ""))


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


# --------------------------------------------------------------------- compare
class CompareAction(ToolArgs):
    code: str = Field(
        description="A short Python script that calls the changed code and prints what it "
                    "returns or writes, e.g. `print(result)` or the contents of a file it "
                    "creates. It runs in an empty temporary directory, with the project "
                    "importable.")


class CompareObservation(Observation):
    pass


# The script's output per side, at most this many characters.
COMPARE_MAX = 2500


class CompareExecutor(ToolExecutor[CompareAction, CompareObservation]):
    """Run a script on the code before the change and with it applied, and show both
    outputs (2026-10-24, user: useful tests). The checkout is the code before the change,
    so the agent cannot see what the changed code returns -- only `verify`'s pass or fail.
    pylint-4492 (base-p2) ran pylint with `--output-format=json:output.json,text` and could
    only assert `len(output) > 0`; the developer's test asserts the JSON written, line by
    line. This shows the agent the values to assert."""

    def __init__(self, box: Sandbox, patch: str, log: list | None = None):
        self.box, self.patch = box, patch
        self.log = log if log is not None else []

    def __call__(self, action: CompareAction, conversation=None) -> CompareObservation:
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return CompareObservation.from_text(
                f"cannot compare: the working tree is in an unexpected state ({state})",
                is_error=True)
        script = "/tmp/f2p_compare/script.py"
        self.box.write(script, action.code)
        # A fresh directory per side, so a file the script writes is that side's own.
        cmd = ("rm -rf /tmp/f2p_compare/run && mkdir -p /tmp/f2p_compare/run && "
               "cd /tmp/f2p_compare/run && PYTHONPATH=" + REPO_DIR + "${PYTHONPATH:+:$PYTHONPATH} "
               "timeout 120 python " + script + " 2>&1")
        before = self.box.exec(cmd, timeout=180)
        self.box.apply_patch(self.patch)
        try:
            after = self.box.exec(cmd, timeout=180)
        finally:
            self.box.apply_patch(self.patch, revert=True)
        self.box.exec("rm -rf /tmp/f2p_compare/run", timeout=60)
        b, a = (before.output or "").rstrip(), (after.output or "").rstrip()
        self.log.append({"tool": "compare", "code": action.code[:4000],
                         "before": b[:COMPARE_MAX], "after": a[:COMPARE_MAX]})
        same = b == a
        text = (f"before the change (exit {before.returncode}):\n{_clip(b, COMPARE_MAX) or '(no output)'}"
                f"\n\nafter the change (exit {after.returncode}):\n{_clip(a, COMPARE_MAX) or '(no output)'}"
                + ("\n\nThe two outputs are the same: this script does not reach what the change does."
                   if same else
                   "\n\nWhat differs is what your test should assert -- the exact values printed "
                   "after the change -- and it should fail on what was printed before."))
        return CompareObservation.from_text(text, is_error=False)


class SandboxCompareTool(ToolDefinition[CompareAction, CompareObservation]):
    name = "compare"

    @classmethod
    def create(cls, conv_state=None, box: Sandbox | None = None, patch: str = "",
               log: list | None = None, **params):
        assert box is not None and patch, "needs a Sandbox and the patch"
        return [cls(
            name="compare",
            description=("Run a short Python script on the code before the change and again "
                         "with the change applied, and show what it printed each time. Use it "
                         "to see what the changed code returns or writes once the change is "
                         "in -- the exact values -- and assert those in your test. Print what the "
                         "calls produce, not only that they ran: the objects they return or build "
                         "(`type(x).__name__`, `vars(x)`), files they write, text they print. "
                         "Reverts the change afterwards."),
            action_type=CompareAction,
            observation_type=CompareObservation,
            annotations=ToolAnnotations(readOnlyHint=False),
            executor=_Shown(CompareExecutor(box, patch, log), "compare"),
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
                 coverage: bool = False, mutation: bool = False, probe_mutants: int = 5,
                 require_tools: bool = False, scored_name: str = "", gated: bool = False,
                 wrong_fixes: list | None = None):
        # Plausible wrong versions of the change from `wrong_fixes.generate`, for the
        # mutation stage (2026-10-24).
        self.wrong_fixes = wrong_fixes or []
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

    def _observe(self, target: str, fix_rows: list) -> list | dict:
        """Run wrong versions of the change -- the model's, then `mutmut`'s -- against the
        test, with the trace plugin under pytest, and say for each whether the test caught
        it, how, and what the changed functions did differently from the real fix in the
        same tests (`_trace_diff`)."""
        from openhands_f2p import mutants as M
        from openhands_f2p import runners
        from openhands_f2p import verify as V
        from openhands_f2p import wrong_fixes as W
        rel = target.split("::")[0]
        state = self.box.ensure_base(self.patch)
        if state != "base":
            return {"why": f"the working tree is {state}, not base"}
        pytest_runner = runners.runner_for(self.box)["args"] == "nodes"
        for path in E.patched_source_files(self.patch):
            text = self.box.read(path)
            if text is not None:
                self.box.write(f"{M.BASE_COPIES}/{path}", text)
        cmd = E.test_command(self.box, [rel])
        if pytest_runner:
            cmd = (f"F2P_TRACE_SPEC={CATCH_DIR}/trace_spec.json F2P_TRACE_OUT={CATCH_DIR}/trace_m.json "
                   f"PYTHONPATH={CATCH_DIR}${{PYTHONPATH:+:$PYTHONPATH}} {cmd} -p f2p_trace")
        out = []
        self.box.apply_patch(self.patch)
        try:
            cands = W.build(self.box, self.wrong_fixes)[:OBSERVE_MAX // 2 + 1]
            shown, _held = M.split_pool(self.box, self.patch, self.probe_mutants)
            for m in shown:
                if len(cands) >= OBSERVE_MAX:
                    break
                if not M.same_bytecode(self.box.read(m.file) or "", m.source, m.file):
                    cands.append(m)
            for m in cands:
                original = self.box.read(m.file) or ""
                self.box.write(m.file, m.source)
                try:
                    self.box.exec(f"rm -f {CATCH_DIR}/trace_m.json", timeout=60)
                    r = self.box.exec(cmd, timeout=900)
                    got = V.own_outcomes(E.parse_output(r.output), [rel])
                    killed = not got or any(v in ("FAILED", "ERROR") for v in got.values())
                    rows = []
                    if pytest_runner and not killed:
                        try:
                            rows = json.loads(self.box.read(f"{CATCH_DIR}/trace_m.json") or "[]")
                        except ValueError:
                            rows = []
                finally:
                    self.box.write(m.file, original)
                out.append({"mutant": m, "killed": killed,
                            "kind": M._kind(r.output) if killed else None,
                            "seen": _trace_diff(fix_rows, rows) if not killed and pytest_runner else []})
        finally:
            if self.box.patch_state(self.patch) == "head":
                self.box.apply_patch(self.patch, revert=True)
            self.box.exec(f"rm -rf {M.BASE_COPIES}", timeout=60)
        return out

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
        # Tests that check nothing about what the code does (`V.trick_tests`, 2026-10-24):
        # they count neither for the flip nor for coverage.
        from openhands_f2p import verify as _V
        tricks = _V.trick_tests(self.box.read(action.target.split("::")[0]) or "")
        from openhands_f2p import verify as V
        from openhands_f2p import runners
        # Under pytest, both runs load the plugin that records what `pytest.raises` /
        # `pytest.warns` caught (`CATCH_PLUGIN`); the outcomes are the same either way.
        catch = runners.runner_for(self.box)["args"] == "nodes"
        if catch:
            if not getattr(self, "_catch_ready", False):
                self.box.write(f"{CATCH_DIR}/f2p_catch.py", CATCH_PLUGIN)
                self.box.write(f"{CATCH_DIR}/f2p_trace.py", TRACE_PLUGIN)
                self._catch_ready = True
            self.box.exec(f"rm -f {CATCH_DIR}/before.json {CATCH_DIR}/after.json "
                          f"{CATCH_DIR}/trace.json", timeout=60)

        def caught_cmd(side: str) -> str:
            if not catch:
                return cmd
            # With the change applied, the trace plugin as well (`TRACE_PLUGIN`).
            callee = exit_callee(self.box.read(action.target.split("::")[0]) or "")[0]
            closers = ",".join(_closers(self.patch))
            trace = (f"F2P_TRACE_SPEC={CATCH_DIR}/trace_spec.json F2P_TRACE_OUT={CATCH_DIR}/trace.json "
                     + (f"F2P_TRACE_ROOTS={callee} F2P_TRACE_CLOSERS={closers} " if callee and closers else "")
                     if side == "after" else "")
            return (f"{trace}F2P_CATCH_OUT={CATCH_DIR}/{side}.json PYTHONPATH={CATCH_DIR}${{PYTHONPATH:+:$PYTHONPATH}} "
                    f"{cmd} -p f2p_catch" + (" -p f2p_trace" if side == "after" else ""))
        before = self.box.exec(caught_cmd("before"), timeout=3600)
        base_out = V.own_outcomes(E.parse_output(before.output), [action.target])
        self._base = E.base_texts(self.box, self.patch)
        self.box.apply_patch(self.patch)
        cov: dict | None = None
        import_only = ""
        try:
            if catch:
                self.box.write(f"{CATCH_DIR}/trace_spec.json",
                               json.dumps(watched_functions(self.box, self.patch)))
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
                                                  self._base, exclude_tests=set(tricks))
                    import_only = _import_only(self.box, cov) if cov.get("measured") else ""
                    if cov.get("measured") and cov.get("missed"):
                        cov["related_tests"] = self._related(cov, action.target)
                        config_branches(self.box, cov)
                        mark_new(self.box, cov, self.patch, self._base)
                except Exception as exc:
                    cov = {"measured": False, "reason": f"{type(exc).__name__}: {exc}"}
        finally:
            self.box.apply_patch(self.patch, revert=True)

        failed_before = {n for n, v in base_out.items() if v in ("FAILED", "ERROR")}
        passed_after = {n for n, v in head_out.items() if v == "PASSED"}
        flipped = sorted(failed_before & passed_after)
        still_failing = [n for n, v in head_out.items() if v in ("FAILED", "ERROR")]
        # A flip from tests that check nothing is not one (2026-10-24): pylint-4492 flipped on
        # `assert hasattr(linter, '_reporter_names')` -- the name is new, so any version of
        # the change, right or wrong, passes it.
        def _short(n: str) -> str:
            return n.split("::")[-1].split("[")[0]
        trick_flips = [n for n in flipped if _short(n) in tricks]
        only_tricks = bool(flipped) and len(trick_flips) == len(flipped)
        if only_tricks:
            flipped = []
        # `reach`: how many changed lines this version runs, read by the hand-back
        # (`V.lost_flip`) to tell a test that went further from one that fell back.
        self.log.append({"tool": "verify", "target": action.target,
                         "before": base_out, "after": head_out, "flipped": flipped,
                         "tricks": tricks, "trick_flips": trick_flips,
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
        elif only_tricks and not still_failing:
            head = (f"NOT fail-to-pass in a way that counts: {trick_flips[:3]} fail before the "
                    f"change and pass after, but none of them checks what the changed code does. "
                    + " ".join(f"`{_short(n)}`: {tricks[_short(n)][0]}." for n in trick_flips[:3])
                    + " A test like that passes on any version of the change, right or wrong, so it "
                      "tests nothing. Call the changed code with real input and assert on what it "
                      "returns, writes or raises -- the exact value, the output, the exception and "
                      "its message -- with no `try`/`except` around it."
                    + V.asserting_helpers(self.box.read(action.target.split("::")[0]) or ""))
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
        # What the changed functions did in the agent's own tests (`TRACE_PLUGIN`).
        fix_trace: list = []
        if catch:
            try:
                fix_trace = json.loads(self.box.read(f"{CATCH_DIR}/trace.json") or "[]")
            except ValueError:
                fix_trace = []
        if catch:
            try:
                head += trace_said(json.loads(self.box.read(f"{CATCH_DIR}/trace.json") or "[]"),
                                   patch=self.patch,
                                   watched=json.loads(self.box.read(f"{CATCH_DIR}/trace_spec.json") or "[]"))
            except ValueError:
                pass
        # Output the code wrote in a flipping test that the test never reads back.
        if ok and fix_trace:
            unread = unread_outputs(fix_trace, self.box.read(action.target.split("::")[0]) or "",
                                    flipped)
            if unread:
                holder = closer_holder(fix_trace, self.patch)
                opened = {u["test"] for u in unread if u.get("open")}
                path = next((r.get("args") for r in fix_trace if r.get("func") == "reach"
                             and (r.get("test") or "").split("::")[-1].split("[")[0] in opened), None)
                reach = exit_entry(self.box, self.box.read(action.target.split("::")[0]) or "", holder, path) \
                    if any(u.get("open") for u in unread) else ""
                unread = [dict(u, closer=holder, reach=reach) if u.get("open") else u for u in unread]
                self.log[-1]["unread"] = unread
                head += ("\n\n## Output your tests never read\n\n"
                         + "\n".join(f"* `{u['test']}` made the changed code write `{u['file']}` "
                                      f"({u['size']} bytes): `{u['content']}`" for u in unread)
                         + "\n\nThat file is what the change produces, and the test passes "
                           "whatever is in it -- an exit code or \"no error\" is true of a version "
                           "that writes it empty or wrong. Read it back in the test (give the "
                           "run a path under `tmp_path`, then `json.load`/`read_text` it) and "
                           "assert what it holds: the entries, their fields, the text. "
                         + read_back_example(unread[0]))
        # The tests that do not count, said with every answer while there are any.
        if tricks and not only_tricks:
            unchecked = len((cov or {}).get("unchecked") or [])
            head += ("\n\n## Tests that do not count\n\n"
                     + "\n".join(f"* `{n}`: " + "; ".join(w) for n, w in list(tricks.items())[:6])
                     + (f"\n* and {len(tricks) - 6} more: " + ", ".join(f"`{n}`" for n in list(tricks)[6:])
                        if len(tricks) > 6 else "")
                     + ("\n\nThey count neither for fail-to-pass nor for coverage"
                        + (f": {unchecked} changed line(s) run only inside them and are left out "
                           f"of the coverage below" if unchecked else "")
                        + ". Make each one assert on what the changed code returns, writes or "
                          "raises, with no `try`/`except` around it, or delete it -- `compare` "
                          "shows the exact values the changed code gives, to assert. You cannot "
                          "finish while they are in the file.")
                     + V.asserting_helpers(self.box.read(action.target.split("::")[0]) or ""))
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
            text, entry = wrong_versions_report(self._observe(action.target, fix_trace),
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
            # The restored file is byte for byte one `verify` already answered for: that answer
            # is put back with it, so the stop check does not ask for it again (2026-10-23,
            # user): pylint-5136 (B) spent about half its ten refusal rounds re-verifying
            # restores. Not when copied repository tests were added back -- that file as a
            # whole was never checked.
            replayed = False
            if not seeds_back:
                was = {k: v for k, v in self.log[i].items()}
                was.update({"via": "restore", "replay_of": V.call_number(self.log, i)})
                self.log.append(was)
                # Every stage of that call: coverage, and mutation too -- left out, the
                # mutation loop read the discarded version's score after each restore,
                # "5.0% (1 of 20) ... you changed the test after the last `verify`", four
                # refusals of nine in scikit-learn-24145's base+mutation trial (2026-10-23).
                for stage in self.log[i + 1:i + 4]:
                    if stage.get("tool") == "verify":
                        break
                    if stage.get("tool") in ("coverage", "mutation") and stage.get("via") == "verify":
                        self.log.append(dict(stage, replay_of=V.call_number(self.log, i)))
                replayed = True
            head += (f"\n\n## Restored\n\nThe version you just checked is worse than your best "
                     f"one: {why}. So the harness has put the best fail-to-pass version back in "
                     f"`{rel}` -- the one `verify` checked at tool call "
                     f"{V.call_number(self.log, i)}{covered}"
                     + (", with the repository tests the harness copied in added back"
                        if seeds_back else "") + ". That is the file on disk now; "
                     f"you do not need to write it back."
                     + (" It is byte for byte the file `verify` checked then, so that answer "
                        "stands -- it is fail-to-pass, and you need not call `verify` on it "
                        "before going on." if replayed else "")
                     + f" Everything below is about the version "
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
               scored_name: str = "", gated: bool = False, wrong_fixes: list | None = None,
               **params):
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
                                           probe_mutants, require_tools, scored_name, gated,
                                           wrong_fixes),
                            "verify"),
        )]


def register(box: Sandbox, repo: str, log: list, patch: str = "",
             features: FeatureSet | None = None, gen_path: str = "",
             version: str = "", probe_mutants: int = 5,
             wrong_fixes: list | None = None) -> list[str]:
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
                                         verify_named="verify-tool" in features,
                                         patch=patch)[0],
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
            wrong_fixes=wrong_fixes,
            scored_name=Path(gen_path).name if gen_path else "",
            gated="require-tools" in features)[0]
        register_tool("verify", made["verify"])
        names.append("verify")
        # Only when the agent is shown the diff: it shows what the changed code does.
        if "patch" in features:
            made["compare"] = SandboxCompareTool.create(box=box, patch=patch, log=log)[0]
            register_tool("compare", made["compare"])
            names.append("compare")
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
