"""The agent arm: an OpenHands agent that writes fail-to-pass tests inside a container.

What changed from the earlier host-based version, and why it mattered
--------------------------------------------------------------------
That version handed the agent OpenHands' built-in terminal, whose executor spawns tmux
panes on the host. Two consequences, both fatal:

  * No isolation. This host has direct internet, so the agent could `pip download` a
    later release of the library under test and read the fix and the developer's test
    straight out of it. Nothing in the harness stopped that; the network audit only
    noticed afterwards, and only if it looked.
  * Three of the five instances could not run at all. django, sympy and scikit-learn
    need their prepared environments; a host venv does not have them.

Here the tools are ours and their executors go through `Sandbox.exec` into a container
started with `--network none`, with `.git` deleted before the agent is let in. Same
tool-call protocol and the same model behaviour -- only the executor changed.

The agent and the verifier share one container on purpose. Verifying in a second box
would mean judging a different tree than the one the agent worked in.

    uv run python -m openhands_f2p.agent            # all five
    uv run python -m openhands_f2p.agent 3          # django only
    uv run python -m openhands_f2p.agent 1 --dry-run
"""
from __future__ import annotations

import argparse
from dataclasses import replace
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import time

from openhands_f2p import (compare, docs, flow, llm_config, prompt, runs,
                           sandbox_tools, swebench_env as E, trajectory, verify as V)
from openhands_f2p.checks import audit, budget_exhausted, token_usage
from openhands_f2p.dataset import load
from openhands_f2p import image_cache, mutants
from openhands_f2p import models
from openhands_f2p import models as M
from openhands_f2p.features import FeatureSet, add_arguments, instruments
from openhands_f2p.layout import CACHE, OUT, PROJECT_ROOT
from openhands_f2p.parallel import (CHILD_ENV_FLAG, _child_argv, _needs_retry,
                                    _run_children)
from openhands_f2p.prs import pick


def instance_dir(out_root: Path | None, pr: dict, child: bool) -> Path:
    """Where one instance's files go.

    `do_pr`, `recheck` and `mutate_saved` all take the *exact* directory, because a child
    process is handed one on its own `--out-root` and must not second-guess it. Appending
    the id there would nest it twice. So the id is appended here, in the parent -- and it
    has to happen in every branch, not only the one that fans out.

    It did not. A single instance with `--out-root out_x` ran in-process and passed the
    run root straight through, so the files landed in `out_x/` beside the other
    instances' directories, and the next single run overwrote them. Two `--out-root` runs
    of one instance each looked like one run of the second.
    """
    return out_root if child else (out_root or OUT) / pr["id"]


def field(label: str, text: str) -> None:
    """One aligned line. Every status line in this file goes through here."""
    print(f"  {label:<9} {text}")


def _recap(counts: dict[str, int], tool_log: list) -> str:
    """What the agent did, in the terms it did it in.

    Only its own actions, which is the cheapest thing on the base-observable side of the
    line `V.shortfall` draws: the agent is being reminded of its own transcript, not told
    anything about the fix. It is here because "you stopped" lands differently next to a
    count -- thirty-one shell commands and no file written is a description of the
    failure, where "you did not finish" is only an assertion of it.
    """
    lines = []
    if counts:
        lines.append("* " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
                     + f" -- {sum(counts.values())} actions in total")
    used: dict[str, int] = {}
    # `guard` entries are the harness putting a file back, not a tool the agent called.
    reverted = sum(1 for e in tool_log if e.get("tool") == "guard")
    for e in tool_log:
        if e.get("tool") == "guard":
            continue
        used[e.get("tool") or "?"] = used.get(e.get("tool") or "?", 0) + 1
    if used:
        lines.append("* tools: " + ", ".join(f"`{k}` x{v}" for k, v in
                                             sorted(used.items(), key=lambda kv: -kv[1])))
    wrote = [e.get("path") for e in tool_log
             if e.get("tool") == "write_file" and e.get("path")]
    lines.append("* files written: " + (", ".join(f"`{w}`" for w in dict.fromkeys(wrote))
                                        if wrote else "**none**"))
    if reverted:
        lines.append(f"* edits to pre-existing files put back by the harness: {reverted}")
    return "\n".join(lines)


def _elsewhere(run: dict, test_file: str) -> str:
    """What the agent did write, when it was not the file that gets scored.

    "Wrote no test" was true of the target and false of the run: `seaborn-3069` wrote
    `tests/test_f2p_mwaskom__seaborn_3269.py` -- one digit off -- and the record read as
    though it had written nothing. Naming the files turns a puzzle into a typo.
    """
    target = Path(test_file).name
    wrote = sorted({e["path"] for e in run.get("tool_log", [])
                    if e.get("tool") == "write_file" and e.get("path")
                    and Path(e["path"]).name != target})
    tests = [w for w in wrote if Path(w).name.startswith("test")]
    return f" (it wrote {', '.join(tests[:3])} instead)" if tests else ""


def _clip(text: str, n: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= n else text[:n] + f" ... [{len(text) - n} more characters]"


# How much of the first attempt the restart carries. Its record is the agent's own tool
# calls and the text each returned (`shown` is exactly what the model read), clipped per
# step and, past the cap, kept from the end: the last steps are the ones nearest the
# state the restart begins in. About 10k tokens at the cap.
HISTORY_CHARS = 40000


def _history(run: dict) -> str:
    """The first attempt, step by step, in the terms the agent saw it."""
    refusals: dict[int, list[str]] = {}
    for m in run.get("injected") or []:
        refusals.setdefault(m.get("at_tool", 0), []).append(m.get("text", ""))
    steps: list[str] = []
    log = run.get("tool_log") or []
    for i, e in enumerate(log + [{}]):
        for text in refusals.get(i, []):
            steps.append("[the harness refused your stop]\n" + _clip(text, 900))
        tool = e.get("tool")
        if not tool:
            continue
        if tool == "run":
            steps.append(f"run: {_clip(e.get('command', ''), 300)}\n"
                         f"{_clip(e.get('shown') or e.get('output', ''), 700)}")
        elif tool == "write_file":
            steps.append(f"write_file {e.get('path', '')} ({e.get('lines', '?')} lines)"
                         + (f" -- failed: {e['error']}" if e.get("error") else
                            f"\n{_clip(e.get('content', ''), 1500)}"))
        elif tool == "guard":
            steps.append(f"[the harness put back pre-existing files you changed: "
                         f"{', '.join(e.get('reverted') or [])}]")
        else:
            steps.append(f"{tool} {e.get('target', '')}\n"
                         f"{_clip(e.get('shown') or e.get('error', ''), 900)}")
    last = next((r for r in reversed(run.get("transcript") or [])
                 if r.get("action") == "FinishAction"), None)
    if last:
        steps.append(f"finish: {_clip(last.get('detail', ''), 500)}")
    out, total = [], 0
    for step in reversed(steps):
        if total + len(step) > HISTORY_CHARS:
            out.append(f"[... {len(steps) - len(out)} earlier step(s) left out ...]")
            break
        out.append(step)
        total += len(step)
    return "\n\n".join(reversed(out)) or "(no tool calls)"


def _outcomes(side: dict) -> str:
    """`test_a FAILED, test_b PASSED` -- one side of the harness's run, short names."""
    if not side:
        return "nothing collected"
    shown = [f"{n.split('::')[-1].split(' (')[0]} {st}" for n, st in list(side.items())[:8]]
    more = f", and {len(side) - 8} more" if len(side) > 8 else ""
    return ", ".join(shown) + more


def _restart_note(run: dict, verdict: V.Verdict, test_file: str, code: str | None,
                  cap: int, budget: int) -> str:
    """The second chance's message: why the first attempt was not accepted, the test it
    left, and its record.

    The test goes in whenever there is one, whatever the verdict -- a BROKEN run's test
    is still the agent's own work to start from. The reason is the harness's verdict in
    full, with what each test did before and after the fix (user decision, 2026-09-28):
    the agent could learn it with `verify`, and at the start of a second attempt it is
    the most useful thing to know. It is also the one place the head run reaches the
    agent directly."""
    why = [f"The harness's verdict was **{verdict.f2p}**: {verdict.why}."]
    if verdict.base or verdict.head:
        why.append(f"Before the fix: {_outcomes(verdict.base)}.")
        why.append(f"After the fix: {_outcomes(verdict.head)}.")
    if code:
        block = (f"The test it left at `{test_file}` is still there. As it is on disk now:"
                 f"\n\n```python\n{_clip(code, 6000)}\n```")
    else:
        block = f"It left no test at `{test_file}`."
    return prompt.followup("restart", used=run.get("actions", 0), cap=cap,
                           why="\n".join(why), test_block=block,
                           history=_history(run), budget=budget)


def _joined(first: dict, second: dict, note: str) -> dict:
    """One record for a run the second chance restarted: both conversations in order.

    The tool log and transcript are concatenated so the test path, the audit and the
    trajectory see the whole run; the restart message joins the injected ones at the
    point it was sent; refusal rounds of both conversations are kept, each marked with
    the attempt it belongs to. Status, error and cap are the second conversation's --
    they describe how the run ended."""
    at = len(first.get("tool_log") or [])
    shifted = [{**m, "at_tool": m.get("at_tool", 0) + at}
               for m in second.get("injected") or []]
    rounds = ([{**r, "attempt": 1} for r in ((first.get("retry") or {}).get("rounds") or [])]
              + [{**r, "attempt": 2} for r in ((second.get("retry") or {}).get("rounds") or [])])
    retry = None
    if rounds:
        retry = {"reason": rounds[0]["reason"], "said": rounds[0]["said"],
                 "budget": rounds[0]["budget"],
                 "actions": sum(r["actions"] for r in rounds), "rounds": rounds}
    invented = dict(first.get("invented") or {})
    for k, v in (second.get("invented") or {}).items():
        invented[k] = invented.get(k, 0) + v
    return {**second,
            "tool_log": (first.get("tool_log") or []) + (second.get("tool_log") or []),
            "transcript": (first.get("transcript") or []) + (second.get("transcript") or []),
            "injected": ((first.get("injected") or [])
                         + [{"at_tool": at, "after_action": first.get("actions", 0),
                             "reason": "restart", "text": note}] + shifted),
            "retry": retry, "invented": invented,
            "actions": first.get("actions", 0) + second.get("actions", 0),
            "task": first.get("task")}


# How many times a stop may be refused. The budget bounds a run anyway; this bounds the
# number of times the same kind of message is appended to the context, and a run still
# open after five refusals has usually stopped moving.
# Ten since 2026-09-29, when coverage and mutation became loops after the verify loop:
# three loops in five rounds would end on the cap rather than on their answers. The
# action budget still bounds the run.
MAX_REFUSALS = 10
# Fewer actions than this cannot answer a refusal or use a restart: rewriting the test and
# calling `verify` is two, and stopping is a third. sphinx-9602 (fix check, 2026-09-29) was
# refused with 1 action left, and a restart can be handed 1 or 2.
MIN_USEFUL_ACTIONS = 3
# A test that cannot be scored -- `passes_at_base` or `collects_nothing` -- refused at
# most this many rounds in a row. On the new system's first run seven of eight instances
# that reached `passes_at_base` stayed there for all five rounds; the one that recovered
# left it after the first. `collects_nothing` joined after eval5-arms, where one run spent
# five rounds on a file that never collected; the one collects_nothing conversion on
# record left it after the second. A third identical refusal has not converted anything.
# `skipped_at_base` joined after experiments-v2: the same state -- nothing fails at base.
MAX_PASSES_AT_BASE_ROUNDS = 2


def run_agent(instance: dict, box: E.Sandbox, test_file: str, max_iterations: int,
              out_dir: Path, features: FeatureSet, n_mutants: int = 0,
              model: str | None = None, provider: str | None = None,
              temperature: float | None = M.DEFAULT_TEMPERATURE,
              restart_note: str = "") -> dict:
    """One conversation with the agent, and the stop checks that answer its stops.

    `restart_note` makes this the second chance's conversation: a fresh one, sent the
    same task with the note after it -- the record of the first attempt, the test it
    left, the budget that remains (see `_restart_note`). `max_iterations` is then what
    remains, not the run's cap."""
    from openhands.sdk import Agent, Conversation, Tool
    from openhands.sdk.event import ActionEvent, MessageEvent, ObservationEvent

    t_start = time.time()
    llm, model, proxy = llm_config.configure_llm(out_dir / "completions",
                                                 model=model, provider=provider,
                                                 temperature=temperature)
    # Read back from the LLM that will make the calls, not from the flag: what is
    # recorded is what was configured.
    temperature = llm.temperature
    tool_log: list = []
    # Two different questions, kept apart. `verify` and `coverage` need the harness to
    # *hold* the patch, which it always does -- it applies it and reverts it itself. The
    # `patch` feature is about whether the agent is *shown* it, which only the prompt
    # cares about. Conflating them once made `--no-patch` silently remove the feedback
    # loop as well as the input, so a drop in the result could not be attributed to
    # either.
    # The same `n` the harness will use, so the two halves of the pool are the halves
    # of one pool: `probe` takes `split_pool(...)[0]`, `measure` takes `[1]`. Passing
    # different sizes here would draw two pools and the "held out" half could contain
    # mutants the agent had already been shown.
    names = sandbox_tools.register(box, instance["repo"], tool_log,
                                   patch=instance["patch"], features=features,
                                   gen_path=test_file,
                                   probe_mutants=(n_mutants or mutants.DEFAULT_MUTANTS))
    agent = Agent(llm=llm, tools=[Tool(name=n) for n in names])

    transcript: list[dict] = []
    counts: dict[str, int] = {}
    live = sys.stdout.isatty()

    def on_event(event) -> None:
        row = {"kind": type(event).__name__,
               "at": datetime.now(timezone.utc).isoformat()}
        if isinstance(event, ActionEvent):
            if event.action is None:
                # The SDK could not turn the tool call into an action (bad arguments, an
                # unknown tool) and answers it with an error. It still costs an action.
                # Logged as "NoneType None" before, and shown to the model under that
                # name in its own tally when a stop was refused.
                row["action"] = "unparsed call"
                row["detail"] = (f"{event.tool_name}: "
                                 f"{getattr(event.tool_call, 'arguments', '')}")[:2500]
            else:
                row["action"] = type(event.action).__name__
                row["detail"] = str(event.action)[:2500]
            short = {"RunAction": "run", "WriteAction": "write",
                     "TestAction": "test", "FinishAction": "finish",
                     "ThinkAction": "think", "VerifyAction": "verify",
                     "CoverageAction": "coverage", "MutationAction": "mutation",
                     }.get(row["action"], row["action"])
            counts[short] = counts.get(short, 0) + 1
            n = sum(counts.values())
            if live:
                # One line that rewrites itself, so a 46-action run does not scroll
                # the useful output off the screen.
                print(f"\r  {'agent':<9} working... {n:2d} actions "
                      f"({', '.join(f'{v} {k}' for k, v in counts.items())})"
                      f"{' ' * 12}", end="", flush=True)
            flow.record(flow.AGENT, row["action"],
                        row["detail"].replace("\n", " ")[:110])
        elif isinstance(event, (ObservationEvent, MessageEvent)):
            row["detail"] = str(getattr(event, "observation", None)
                                or getattr(event, "llm_message", event))[:2500]
        else:
            row["detail"] = str(event)[:1200]
        transcript.append(row)

    # Assembled from prompts/, one file per instruction. See prompts/README.md.
    # With the briefing withheld the destination is the agent's to establish, so the
    # prompt names the file and not the directory. The harness keeps the filename: it is
    # not repo knowledge, it keeps the name unique enough to find afterwards, and it
    # stops the agent overwriting a test that was already there.
    briefed = "repo-facts" in features
    shown = test_file if briefed else Path(test_file).name
    task = prompt.build(repo=instance["repo"], test_file=shown,
                        repo_facts=E.repo_facts(box, test_file) if briefed else "",
                        problem=instance["problem_statement"] if "issue" in features
                        else "",
                        patch=instance["patch"] if "patch" in features else "",
                        features=features,
                        skip=set(filter(None, (os.getenv("F2P_PROMPT_SKIP") or "")
                                        .split(","))))
    field("model", f"{model}   {llm.api_mode} api"
                   f"{', via proxy' if proxy else ''}")
    field("tools", f"{', '.join(names)}   (+ finish, think from the SDK)")
    used = prompt.build.last_pieces
    field("prompt", f"{len(task)} chars from {len(used)} pieces: {', '.join(used)}")
    # The SDK's own EventLog goes under .cache, not out/. We never read it -- our
    # trajectory.json covers the same events in the format the visualizer wants -- but
    # dropping persistence_dir entirely makes the SDK warn about an in-memory store on
    # every run, so it is redirected rather than disabled.
    # Its own store for the restart, so the SDK cannot pick the first conversation back up.
    conversation = Conversation(agent=agent, workspace=str(CACHE / "ws"),
                                persistence_dir=str(CACHE / "openhands"
                                                    / (instance["instance_id"]
                                                       + ("-restart" if restart_note else ""))),
                                callbacks=[on_event],
                                max_iteration_per_run=max_iterations, visualizer=None)
    flow.record(flow.AGENT, "tools registered", ", ".join(names))
    opening = task + (f"\n\n{restart_note}" if restart_note else "")
    flow.record(flow.AGENT, "restart sent" if restart_note else "task sent",
                f"{len(opening)} chars, max_iter={max_iterations}")
    conversation.send_message(opening)
    # Every message the harness sends after the task, in order. The trajectory export is
    # rebuilt from disk and used to show the opening task alone -- so a run that was
    # refused twice read, in the trajectory, as an agent that simply kept going.
    injected: list[dict] = []
    error = None
    try:
        conversation.run()
        status = str(conversation.state.execution_status)
    except Exception as exc:
        # Deliberately swallowed. A raised exception here used to abort do_pr() before
        # anything was written, so a run that had already taken eight tool actions left
        # no transcript and no tool log -- the most interesting evidence, lost precisely
        # when something went wrong.
        error = f"{type(exc).__name__}: {exc}"
        status = "ERROR"
        flow.record(flow.AGENT, "run raised", error[:200])
    flow.record(flow.AGENT, "agent finished", status)

    # Refusing the stop, for as long as there is a reason to and budget to do it with.
    #
    # This used to happen once. `conversation.run()` was called a single time after the
    # nudge, so the agent was refused, edited the test, called `finish` again -- and that
    # second stop went through unchecked. Across the ten arms 162 of 630 runs with a
    # verify tool ended on an edit they never verified, 144 of them after the nudge had
    # already fired; 103 had edited after a verify that said NOT fail-to-pass, and 102 of
    # those failed. The nudge told the agent "you cannot finish while this is the answer"
    # and nothing made that true: `finish` stayed callable and a second call was free.
    #
    # Now every stop is checked, and each one that leaves a gap is refused with the
    # current reason. That is what gating `finish` means in practice -- the SDK's finish
    # still ends `run()`, and this loop answers it -- without reaching into the SDK's own
    # terminal action. It ends when the gap closes, the budget is spent, the round cap is
    # reached, or the agent stops doing anything between refusals.
    #
    # All of it is `require-tools` (2026-09-28): `V.shortfall` (the harness runs the file
    # at base), `V.verify_gap` (the agent's own last `verify`), then `V.duty_gap`
    # (coverage and mutation answers once it flips). All of them say only base-observable
    # facts and return None when there is nothing to say. The second chance is not here:
    # it is a restart after the run is scored, in `do_pr`.
    scored = "require-tools-with-score-report" in features
    retry: dict | None = None
    # The cap is a fact about the first stop. Counting the continuation's actions into it
    # would report a run as capped because the two stretches together passed the limit,
    # when neither did.
    first_run_actions = sum(counts.values())
    rounds: list[dict] = []
    if "require-tools" in features and error is None:
        while True:
            spent = sum(counts.values())
            left = max_iterations - spent
            rel = V.written_test_path(box, tool_log, test_file)
            # Independent grounds for refusing the stop, each with its own flag. They share
            # one message because sending two would spend two turns saying one thing.
            gaps: list[tuple[str, str]] = []
            if left > 0:
                # The harness's own base run first: when it finds the file missing, empty
                # or passing, that is the whole story, told with the file and its output,
                # and the agent's last `verify` would only repeat it. The duties only
                # start once the test flips by its own verify.
                found = (V.shortfall(box, instance, rel)
                         or V.verify_gap(tool_log, rel)
                         or V.duty_gap(tool_log, instruments(features), rel, scored=scored))
                if found:
                    gaps.append(found)
            # A test that asserts on the project's source text rather than on behaviour.
            # Checked in every configuration: it reads only the test file. See
            # `V.source_gap`.
            if left > 0:
                found = V.source_gap(box, rel)
                if found:
                    gaps.append(found)
            # A test that flips while running none of the changed lines: asked once, and
            # only when nothing else is open and the agent holds `coverage`.
            if (left > 0 and not gaps and "coverage-tool" in features
                    and V.verify_settled(tool_log, rel)
                    and not any("runs_no_change" in r["reason"] for r in rounds)):
                found = V.no_reach_gap(box, instance, rel)
                if found:
                    gaps.append(found)
            gap = None if not gaps else (
                "+".join(r for r, _ in gaps), "\n\n".join(say for _, say in gaps))
            if left <= 0:
                flow.record(flow.AGENT, "stop check", "no budget left at the cap")
                break
            if left < MIN_USEFUL_ACTIONS and gap is not None:
                flow.record(flow.AGENT, "stop check",
                            f"{left} action(s) left, too few to answer a refusal; "
                            f"gap still open ({gap[0]})")
                break
            # A tree off base -- only reachable without --add-guard, where a library edit is
            # left in place -- cannot be verified by the agent or scored by the harness.
            # Refusing there asked for a `verify` that answers only "unexpected state"
            # (sklearn-10297 under -guard, refused until the cap). Telling the agent to
            # put the file back would be the guard the arm removes, so the loop stops and
            # the verdict reports the tree.
            if gap is not None and box.ensure_base(instance["patch"]) != "base":
                flow.record(flow.AGENT, "stop check",
                            "tree not at base (a pre-existing file was changed); "
                            "not refusing")
                break
            if gap is None:
                flow.record(flow.AGENT, "stop check",
                            "not needed" if not rounds else
                            f"gap closed after {len(rounds)} refusal(s)")
                break
            if len(rounds) >= MAX_REFUSALS:
                flow.record(flow.AGENT, "stop check",
                            f"stopped refusing after {MAX_REFUSALS} rounds; gap still open")
                break
            # Two rounds in a row where the agent did nothing but stop again. Refusing a
            # third time buys another identical stop and another few thousand tokens of
            # the same message; the gap stays recorded in `rounds`.
            if len(rounds) >= 2 and rounds[-1]["actions"] <= 1 and rounds[-2]["actions"] <= 1:
                flow.record(flow.AGENT, "stop check",
                            "agent stopped acting between refusals; not refusing again")
                break

            reason, say = gap
            # A test that already flips is in the coverage and mutation loops (user,
            # 2026-09-29): refused while either falls short, until each reaches its goal
            # or an honest attempt stops improving it (`V._no_better`). Until then a flipping
            # test got one reminder -- xarray-7233 and scikit-learn-10908 had been refused
            # five times each while already passing, back when "answered" meant nothing
            # measurable; the loops now end on the tool's own answer.
            settled = V.verify_settled(tool_log, rel)
            # Rounds spent on a test that cannot be scored: nothing fails at base
            # (`V.UNSCOREABLE`). A test failing on both sides is not capped here: those
            # rounds do convert (four runs recovered after a third such refusal).
            def stuck(why: str) -> bool:
                return any(k in why for k in V.UNSCOREABLE)

            streak = 0
            for r in reversed(rounds):
                if not stuck(r["reason"]):
                    break
                streak += 1
            if stuck(reason) and streak >= MAX_PASSES_AT_BASE_ROUNDS:
                flow.record(flow.AGENT, "stop check",
                            f"not scoreable (passes or is skipped at base, or collects "
                            f"nothing) after {streak} refusals running; not refusing again")
                break
            # Which of the two mistakes a passing-at-base test is making. Only with the
            # coverage tool registered: see `V.reach_diagnosis`.
            if "passes_at_base" in reason and "coverage-tool" in features:
                diag = V.reach_diagnosis(box, instance, rel)
                if diag:
                    marker = "whatever it checks was true before the fix as well."
                    say = (say.replace(marker, marker + diag, 1) if marker in say
                           else say + diag)
            nudge = prompt.followup("second-chance", shortfall=say,
                                    recap=_recap(counts, tool_log), test_file=rel,
                                    budget=left, cap=max_iterations)
            flow.record(flow.AGENT, "stop check",
                        f"round {len(rounds) + 1}: {reason}; {left} actions left")
            if not rounds:
                field("retry", f"{reason} -- carrying on with {left} of "
                               f"{max_iterations} actions left")
            # `run()` restarts its own iteration count from zero, so what is left of the
            # cap has to be set here. Without this the continuation silently gets a
            # second full cap, and one flag doubles what a run is allowed to spend.
            conversation.max_iteration_per_run = left
            conversation.send_message(nudge)
            # Kept for the trajectory: the SDK's event log holds this turn, but the
            # export was built from the opening task alone and never showed it.
            injected.append({"at_tool": len(tool_log), "after_action": spent,
                             "reason": reason, "text": nudge})
            before = sum(counts.values())
            try:
                conversation.run()
                status = str(conversation.state.execution_status)
            except Exception as exc:
                error = f"{type(exc).__name__}: {exc}"
                status = "ERROR"
                flow.record(flow.AGENT, "retry raised", error[:200])
            after = sum(counts.values())
            rounds.append({"reason": reason, "said": say, "budget": left,
                           "actions": after - before, "settled": settled})
            flow.record(flow.AGENT, "stop check done",
                        f"round {len(rounds)}: {after - before} more actions, {status}")
            if error:
                break
    if rounds:
        # The first round's reason and budget at the top level, where every existing
        # reader looks; the total the continuation spent; and every round beneath.
        retry = {"reason": rounds[0]["reason"], "said": rounds[0]["said"],
                 "budget": rounds[0]["budget"],
                 "actions": sum(r["actions"] for r in rounds),
                 "rounds": rounds}

    elapsed = time.time() - t_start
    if live:
        print("\r" + " " * 78 + "\r", end="")
    # OpenHands reports a hit iteration cap as ERROR with no exception attached, which
    # reads as a crash. Budget exhaustion and a crash need different responses -- one
    # wants a bigger cap, the other wants a fix -- so they are named differently.
    n_actions = sum(counts.values())
    short_status = status.rsplit(".", 1)[-1].lower()
    if short_status == "error" and error is None and n_actions >= max_iterations:
        short_status = f"hit the {max_iterations}-action cap"
    detail = ", ".join(f"{v} {k}" for k, v in counts.items()) or "nothing"
    field("agent", f"{n_actions} actions ({detail})   "
                   f"{short_status} in {elapsed:.0f}s")
    if error:
        field("", f"error: {error[:120]}")
    if sandbox_tools.INVENTED:
        flow.record(flow.AGENT, "invented parameters",
                    ", ".join(f"{k} x{v}" for k, v in
                              sorted(sandbox_tools.INVENTED.items(),
                                     key=lambda kv: -kv[1])))
    return {"status": status, "error": error,
            # One budget covers both stretches, so this is the whole run again -- the
            # continuation cannot push a run over a cap it shares.
            "capped": n_actions >= max_iterations,
            "invented": dict(sandbox_tools.INVENTED), "retry": retry,
            "injected": injected,
            "transcript": transcript,
            "tool_log": tool_log, "model": model, "temperature": temperature,
            "task": task, "opening": opening,
            "actions": sum(1 for r in transcript if "action" in r)}



def recheck(pr: dict, root: Path | None = None) -> dict:
    """Re-judge a test the agent already wrote, without running the agent again.

    A harness bug that only affects the verdict or the coverage measurement -- not the
    generation -- does not need a fresh $0.06 of tokens and a fresh roll of the dice to
    correct. The saved test is the agent's answer; re-running it under the fixed harness
    asks the same question again and gets the answer we should have had the first time.
    Kept separate from `do_pr` so it cannot be mistaken for a run: nothing here calls an
    LLM, and the trajectory and token counts of the original are left untouched.
    """
    d = (root or OUT) / pr["id"]
    inst = load(pr["id"])
    saved = next((f for f in d.glob("test_f2p_*.py")), None)
    if saved is None:
        return {"id": pr["id"], "f2p": "BROKEN", "why": "no saved test to re-judge"}
    code = saved.read_text()
    old = json.loads((d / "result.json").read_text())
    print(f"  rechecking {pr['id']}  ({saved.name}, {code.count(chr(10)) + 1} lines)")

    with E.Sandbox(pr["id"], quiet=True, extra_packages=("coverage",)) as box:
        box.strip_git()
        # The path the run itself recorded, so a re-judge of a `--repo-search` result
        # does not relocate the test and contradict the verdict it is re-checking.
        verdict = V.verify(inst, box, generated_test=code, quiet=True,
                           test_path=old.get("test_path") or "")

    cov = verdict.changed_line_coverage or {}
    old.update({"f2p": verdict.f2p, "why": verdict.why, "f2p_nodes": verdict.f2p_nodes,
                "targets": verdict.targets, "changed_line_coverage": cov,
                "rechecked": True})
    (d / "result.json").write_text(json.dumps(old, indent=2))
    (d / "before_fix.log").write_text(verdict.base_log or "")
    (d / "after_fix.log").write_text(verdict.head_log or "")
    pct = f"{cov['percent']}%" if cov.get("measured") else "-"
    print(f"    -> {verdict.f2p}  cov {pct}  {verdict.why[:60]}")
    return old


def mutate_saved(pr: dict, n: int, root: Path | None = None) -> dict:
    """Measure mutation on a test the agent already wrote, and nothing else.

    Kept apart from `recheck`, which re-runs the verdict and the coverage measurement:
    those numbers are already recorded for these instances and re-deriving them would
    quietly replace committed results with a fresh roll of the same dice. This adds one
    field. If the mutation step fails, the row it is added to is unchanged.

    Only a `YES` is eligible. Asking what a test would notice about a wrong fix presumes
    it notices the right one, and for a `NO` the question has no meaning.
    """
    # Same convention as `do_pr`: when given, this is the exact directory for this
    # instance, not a parent to append the id to. The parent computes those when it
    # fans out, and a child is handed one directly.
    d = root if root is not None else OUT / pr["id"]
    rj = d / "result.json"
    if not rj.exists():
        return {"id": pr["id"], "skipped": "no result to add to"}
    r = json.loads(rj.read_text())
    if r.get("f2p") != "YES":
        return {"id": pr["id"], "skipped": f"f2p is {r.get('f2p')}, not YES"}
    saved = next((f for f in d.glob("test_f2p_*.py")), None)
    if saved is None:
        return {"id": pr["id"], "skipped": "no saved test"}
    code = saved.read_text()
    inst = load(pr["id"])
    print(f"\n{'-' * 74}")
    print(f"  [{pr['tier']}] {pr['id']}".ljust(52) + inst["repo"].rjust(20))
    print(f"  mutation only, on the saved test ({saved.name}, "
          f"{code.count(chr(10)) + 1} lines)")

    image = E.image_for(pr["id"])
    with flow.recording(d, f"{pr['id']}  mutation on the saved test"), \
            E.Sandbox(pr["id"], quiet=True, extra_packages=("coverage",)) as box:
        box.strip_git()
        test_file = r.get("test_path") or V.gen_test_path(pr["id"], box)
        score = mutants.measure(inst, box, code, test_file, n, out_dir=d,
                                quiet=False)
    field("mutants", mutants.line(score.as_dict()))

    new = score.as_dict()
    old = r.get("mutation") or {}
    if not new.get("measured") and old.get("measured"):
        # A failed attempt does not erase a successful one. The sweep re-ran an instance
        # that had already been measured 2/2, timed out, and wrote the timeout over the
        # number -- losing a real measurement to a transient gateway problem.
        print(f"    keeping the earlier measurement "
              f"({old.get('agent', {}).get('killed')}/{old.get('total')}); "
              f"this attempt: {new.get('why')}")
        return {"id": pr["id"], "mutation": old,
                "failed": f"kept the earlier measurement -- {new.get('why')}"}
    r["mutation"] = new
    rj.write_text(json.dumps(r, indent=2))
    if not os.getenv("F2P_KEEP_IMAGES"):
        try:
            image_cache.release(image, quiet=True)
        except Exception:
            pass
    return {"id": pr["id"], "mutation": score.as_dict()}


_OUTSIDE = re.compile(
    r"\b(402|429|500|502|503|504)\b|APIConnectionError|RateLimit|ServiceUnavailable|"
    r"InternalServerError|Timeout|timed out|Connection (?:reset|refused|aborted)|"
    r"Budget has been exceeded|requires more credits", re.I)


def _outside_failure(error: str) -> bool:
    """An agent error caused by the gateway or the network rather than by the run itself."""
    return bool(_OUTSIDE.search(error or ""))


def do_pr(pr: dict, max_iterations: int, dry_run: bool,
          features: FeatureSet | None = None, no_compare: bool = False,
          out_root: Path | None = None, label: str = "",
          n_mutants: int = 0, model: str | None = None,
          provider: str | None = None, judge_model: str | None = None,
          temperature: float | None = M.DEFAULT_TEMPERATURE) -> dict:
    features = features if features is not None else FeatureSet.full()
    inst = load(pr["id"])
    repo = inst["repo"]
    test_file = V.gen_test_path(pr["id"])      # provisional; re-resolved in the box
    print(f"\n{'─' * 74}")
    print(f"  [{pr['tier']}] {pr['id']}".ljust(52) + repo.rjust(20))
    print(f"  {pr['note'][:70]}")
    if not features.default:
        print(f"  config    {features.describe()}")
    print(f"{'─' * 74}")

    # `out_root`, when given, is the exact directory for this run -- not a parent to
    # append the id to. Appending nested the id twice and, worse, left the "output" line
    # pointing at out/ where nothing had been written.
    mutation: dict | None = None
    d = out_root if out_root is not None else OUT / pr["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "pr.json").write_text(json.dumps(
        {**inst, "FAIL_TO_PASS_parsed": json.loads(inst["FAIL_TO_PASS"]),
         "PASS_TO_PASS_parsed": json.loads(inst["PASS_TO_PASS"])}, indent=2))
    (d / "fix.diff").write_text(inst["patch"])
    (d / "developer_test.diff").write_text(inst["test_patch"])
    shutil.rmtree(d / "completions", ignore_errors=True)   # counts are per run

    if dry_run:
        field("target", test_file if "repo-facts" in features else
              f"{Path(test_file).name}, in a directory the agent establishes")
        # No container in a dry run, and the runner is a property of the checkout.
        field("runner", "detected from the checkout when the container starts")
        return {"id": pr["id"], "tier": pr["tier"], "f2p": "SKIPPED"}

    image = E.image_for(pr["id"])
    if not E.have_image(image):
        # "fetching", not "pulling": the archive is tried first and a load off the disk
        # is seconds where a pull is hours. Saying "pulling" here sent someone looking
        # for a stalled download that was never happening.
        from openhands_f2p import image_cache as _c
        how = ("loading from the archive" if _c.have_archive(image)
               else "pulling from the registry (once, 1-5 GB, slow)")
        field("image", f"{image.split('.')[-1]} -- {how}")

    with flow.recording(d, f"{pr['id']}  ({repo})  config={features.slug()}"), \
            E.Sandbox(pr["id"], quiet=True,
                      # from a wheel fetched on the host; the box never has a
                      # network -- see Sandbox._install_offline
                      extra_packages=("coverage",)) as box:
        flow.record(flow.SETUP, "instance", f"{pr['note']}")
        box.strip_git()
        # Before the agent, so the diff afterwards is exactly what the agent did.
        box.snapshot_tree()
        test_file = V.gen_test_path(pr["id"], box)
        flow.record(flow.SETUP, "test path", test_file)
        field("sandbox", f"{image.split('.')[-1]}   network=none, git stripped")
        # Under --repo-search this is only what the harness *would* have chosen; the
        # line the run is judged on is `chose`, printed once the agent has decided.
        field("target", test_file if "repo-facts" in features else
              f"{Path(test_file).name}, in a directory the agent establishes "
              f"(we would have used {test_file})")

        run = run_agent(inst, box, test_file, max_iterations, d, features, n_mutants,
                        model=model, provider=provider, temperature=temperature)
        default_path = test_file

        def score(run: dict) -> tuple:
            """Resolve the test, audit the tree and decide the verdict for `run` as it
            stands. Called once, and again after a second chance."""
            # Resolved before `audit`, which flags every write that is not the test file:
            # left unresolved, the agent's own chosen path would be reported as a stray
            # write on every run of this configuration.
            #
            # In every configuration, not only when the agent chose the directory: the
            # refusal loop and the agent's own `verify` already follow the file wherever
            # it was written, and scoring a different path made them disagree.
            # django-14915 (experiments-v2) moved its test into tests/forms_tests/tests/,
            # verified it there as fail-to-pass, had its stop accepted on that file -- and
            # was scored "wrote no test" at the path it had been given.
            # `test_path_default` keeps the path the harness named.
            test_file = V.written_test_path(box, run["tool_log"], default_path)
            if "repo-facts" not in features or test_file != default_path:
                flow.record(flow.AGENT, "test path chosen", test_file)
                field("chose", f"{test_file}"
                               + ("" if test_file == default_path
                                  else f"   (the harness would have used {default_path})"))
            code = box.read(test_file)
            flow.record(flow.AGENT, "test written" if code else "no test",
                        f"{test_file} ({code.count(chr(10)) + 1} lines)" if code
                        else f"nothing at {test_file}")
            checks = audit(box, run["tool_log"], test_file)
            flow.record(flow.AUDIT, "isolation",
                        f"dns={checks['isolation']['dns_resolves']} "
                        f"git={checks['isolation']['git_present']} vcs={checks['vcs'][:40]}")
            flow.record(flow.AUDIT, "agent behaviour",
                        f"network_attempts={checks['network_attempts'] or 'none'}  "
                        f"stray_writes={checks['files_written_outside_test'] or 'none'}  "
                        f"tree_changed={checks['tree_changed'] or 'nothing but the test'}")

            starved = budget_exhausted(d) if run["actions"] == 0 else None
            if code is None and starved:
                verdict = V.Verdict(pr["id"], "BROKEN",
                                    f"the model spent its whole output budget on reasoning "
                                    f"({starved['reasoning_tokens']} of "
                                    f"{starved['completion_tokens']} tokens) and had none "
                                    f"left to call a tool -- raise max_output_tokens on this "
                                    f"model's entry in models.json")
            elif code is None and run.get("error"):
                verdict = V.Verdict(pr["id"], "BROKEN",
                                    f"the agent run failed before a test was written: "
                                    f"{run['error'][:180]}")
            elif code is None:
                verdict = V.Verdict(pr["id"], "NO",
                                    ("the agent never called a tool -- the model returned no "
                                     "tool_calls, so OpenHands read its reply as final"
                                     if run["actions"] == 0
                                     else (f"hit the {max_iterations}-action cap after "
                                           f"{run['actions']} actions without writing a test"
                                           if run.get("capped") else
                                           f"took {run['actions']} action(s) but wrote no "
                                           f"test at {test_file}" + _elsewhere(run, test_file))))
            else:
                (d / Path(test_file).name).write_text(code)
                field("test", f"{code.count(chr(10)) + 1} lines written")
                verdict = V.verify(inst, box, generated_test=code, quiet=True,
                                   test_path=test_file)
                # Cut off by something outside the agent -- the gateway ran out of credit,
                # a rate limit, a 5xx, a dropped connection. The test on disk is whatever
                # the agent had when the call failed, and the stop was never checked, so
                # scoring it records the outage as a finding about the instance.
                # experiments-v2's first pass lost 35 runs this way to an exhausted
                # OpenRouter key (22 scored NO, 13 YES) before this line existed. BROKEN is
                # what --retry-broken picks up. A context window overflow is not in this
                # list: it is the run's own length, like the action cap, and keeps its
                # verdict.
                if run.get("error") and _outside_failure(run["error"]):
                    verdict = replace(
                        verdict, f2p="BROKEN",
                        why=f"the agent was cut off after {run['actions']} actions by a "
                            f"failure outside it ({run['error'][:160]}); the test on disk "
                            f"scored {verdict.f2p}, but it is not the agent's finished answer")
                # A run stopped at the cap still has its test scored, and the verdict then
                # reads like a considered judgement with nothing to say the agent was cut
                # off mid-revision (`sphinx-10614` at 100 actions). The verdict stays what
                # the test earned; the reason says the test may not be finished.
                if run.get("capped") and verdict.f2p != "YES":
                    verdict = replace(
                        verdict,
                        why=f"{verdict.why} -- and the agent was stopped at the "
                            f"{max_iterations}-action cap, so this may be an unfinished test "
                            f"rather than a wrong one")

                def tally(o):
                    c = {}
                    for st in o.values():
                        c[st] = c.get(st, 0) + 1
                    return ", ".join(f"{k.lower()}={v}" for k, v in sorted(c.items())) \
                        or "nothing collected"
                field("verify", f"before fix: {tally(verdict.base)}"
                                f"   ->   after fix: {tally(verdict.head)}")
                cov = verdict.changed_line_coverage
                if cov.get("measured"):
                    field("coverage", f"{cov['percent']}% of the lines this PR changed "
                                      f"({cov['covered']}/{cov['executable_changed_lines']})"
                                      + (f"   missed {cov['missed'][:3]}"
                                         if cov["missed"] else ""))
                elif cov:
                    field("coverage", f"not measured: {cov['reason']}")

            # Creating files is allowed; editing one that was already here is not, and
            # this is the check that lets the first be true safely. A new file is present
            # in the before run and the after run alike, so it cannot manufacture a flip.
            # An edited one can. Outside the branch that scores a written test, so an agent
            # that wrote none and patched the library instead is caught too
            # (`scikit-learn-10297` without the guard).
            if checks["tree_altered"]:
                verdict = replace(
                    verdict, f2p="BROKEN",
                    why=f"the agent changed {len(checks['tree_altered'])} file(s) that "
                        f"already existed, so the before-the-fix run is not a fact about "
                        f"this pull request: {', '.join(checks['tree_altered'][:4])}")
                field("audit", f"VOID -- pre-existing files changed: "
                               f"{', '.join(checks['tree_altered'][:4])}")
            return test_file, code, checks, verdict

        test_file, code, checks, verdict = score(run)

        # The second chance: a restart, not a refusal (2026-09-28). A run that ended
        # without a YES, with actions left and not cut off by an outside failure, gets a
        # fresh conversation carrying the task, the record of its first attempt, the test
        # it left (unless BROKEN) and the rest of its budget -- then is scored again. The
        # first verdict is kept in `second_chance`.
        restart = None
        remaining = max_iterations - run["actions"]
        if ("second-chance" in features and verdict.f2p != "YES"
                and not (run.get("error") and _outside_failure(run["error"]))):
            restart = {"first_verdict": verdict.f2p, "first_why": verdict.why,
                       "first_actions": run["actions"], "budget": max(remaining, 0),
                       "first_tool_calls": len(run["tool_log"])}
            if remaining < MIN_USEFUL_ACTIONS:
                restart["skipped"] = f"{max(remaining, 0)} action(s) left, too few for a restart"
                flow.record(flow.AGENT, "second chance", restart["skipped"])
            else:
                note = _restart_note(run, verdict, test_file, code, max_iterations, remaining)
                field("restart", f"{verdict.f2p} after {run['actions']} actions -- starting "
                                 f"again with {remaining} left")
                again = run_agent(inst, box, default_path, remaining, d, features, n_mutants,
                                  model=model, provider=provider, temperature=temperature,
                                  restart_note=note)
                run = _joined(run, again, note)
                test_file, code, checks, verdict = score(run)
                restart["final_verdict"] = verdict.f2p
                flow.record(flow.AGENT, "second chance done",
                            f"{restart['first_verdict']} -> {verdict.f2p}")

        # Inside the sandbox, because every mutant has to be applied to the code and the
        # test run against it -- the container is gone a few lines below. After the final
        # verdict, because a test that does not flip cannot be asked what it would notice
        # about a wrong fix. And it reads the developer's test, so it belongs on this side
        # of the line with the judge, never before it. `not tree_altered` because such a
        # verdict is void anyway.
        if n_mutants and code and verdict.f2p == "YES" and not checks["tree_altered"]:
            mut = mutants.measure(inst, box, code, test_file, n_mutants,
                                  out_dir=d, quiet=True,
                                  held_out=("mutation-tool" in features))
            mutation = mut.as_dict()
            field("mutants", mutants.line(mutation))

    iso = checks["isolation"]
    field("audit", f"network {checks['network_attempts'] or 'none'}, "
                   f"stray writes {checks['files_written_outside_test'] or 'none'}, "
                   f"dns {'off' if not iso['dns_resolves'] else 'ON'}, "
                   f"git {checks['vcs']}")

    (d / "tool_log.json").write_text(json.dumps(run["tool_log"], indent=2))
    (d / "injected_messages.json").write_text(json.dumps(run.get("injected") or [], indent=2))
    (d / "before_fix.log").write_text(verdict.base_log)
    (d / "after_fix.log").write_text(verdict.head_log)
    usage = token_usage(d)
    result = {**verdict.as_dict(), "tier": pr["tier"],
              # When the agent actually ran. The file's mtime used to stand in for this
              # and was wrong the moment anything touched the file afterwards -- a
              # re-judge moved two instances a day forward in the run table.
              "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "arm": label or features.slug(),
              "features": features.as_dict(),
              # Both paths, always. A test in a directory the runner never collects from
              # fails for a reason that has nothing to do with how good the test is, and
              # without the pair on record the two are indistinguishable in the table.
              "test_path": test_file,
              "test_path_default": default_path,
              # The line of the final test that reads project source as text, or None.
              # Recorded beside the verdict, not folded into it: such a test is
              # mechanically fail-to-pass and the verdict says so. See `V.reads_source`.
              "reads_source": V.reads_source(code or ""),
              "usage": usage,
              "model": run["model"], "agent_status": run["status"],
              # None: no temperature was sent and the provider chose -- every run
              # before `--temperature` existed (absent from those results entirely).
              # Since 2026-09-26 the default is M.DEFAULT_TEMPERATURE.
              "temperature": run.get("temperature"),
              "agent_error": flow.scrub(run.get("error") or "") or None,
              # The prompt lives here rather than in its own task.txt: it is one field,
              # and keeping it means a trajectory can still be rebuilt from disk.
              "task": run["task"],
              "actions": run["actions"],
              # Parameters the model invented and the schema dropped. Before this was
              # tolerated the same calls were hard errors -- see ToolArgs.
              "invented_parameters": run.get("invented") or {},
              # Every stop require-tools refused, round by round (both conversations
              # when the run was restarted); None when none was. Before 2026-09-28 this
              # record was called `second_chance`.
              "refusals": run.get("retry"),
              # The restart: the first verdict and why, the budget it had, and the final
              # verdict; None when the second chance was off or not needed.
              "second_chance": restart,
              # Edits to files that existed at base -- the guard's subject. Scratch
              # files the agent created for itself are listed separately.
              "files_edited_outside_test": checks["preexisting_written"],
              "scratch_files": checks["scratch_files"],
              # From the tree, not the tool log: this is the one that would catch an
              # agent editing the library with the shell, which is what would make the
              # "before the fix" run a fact about something other than the pull request.
              "tree_changed": checks["tree_changed"],
              "audit": checks}
    if mutation is not None:
        # Beside the verdict, like coverage and the judge. Nothing here changes F2P.
        result["mutation"] = mutation
    # The concept check goes here and nowhere earlier: it is the only step that reads
    # the developer's test, so it must not run until the F2P verdict is settled. Its
    # answer is recorded beside the verdict, never folded into it.
    #
    # And only on a test that flipped, which is the rule coverage and the mutants have
    # always followed and this one did not. Asking whether a test checks the same
    # behaviour as the developer's presumes it checks the behaviour the change makes;
    # of the four NOs in the qwen evaluation every one was "passes before the fix too",
    # and the judge dutifully graded all four on concept, issue and readability. Those
    # are quality answers about something that has not met the bar quality is measured
    # against -- and they cost a call on the most expensive model in the registry.
    if code is not None and not no_compare and verdict.f2p == "YES":
        try:
            result["concept"] = compare.compare(
                inst, code, model=judge_model,
                completions_dir=d / "judge" / "completions")
            field("concept", compare.line(result["concept"]))
            # Counted after the fact, because `usage` above is read off the
            # agent's completions before this call has happened. Kept as its own
            # field rather than folded in: the judge is one call on a different
            # model, and a run's cost is easier to read when the two are separate.
            result["judge_usage"] = token_usage(d / "judge")
        except Exception as exc:
            result["concept"] = {"verdict": "error", "reasoning": str(exc)[:200]}
            field("concept", f"comparison failed: {str(exc)[:70]}")

    # The archive is the durable copy; Docker's is the working one. Now that the run is
    # over and the container is gone, holding both spends the space twice -- sixteen
    # images are ~36 GB in Docker against ~15 GB compressed on the host. Dropped only
    # once the archive has been read back and verified, and never while another worker
    # has claimed it. `F2P_KEEP_IMAGES=1` keeps it, which is what you want while
    # iterating on one instance: a load is minutes, and paying it every attempt is
    # worse than the disk.
    if not os.getenv("F2P_KEEP_IMAGES"):
        try:
            image_cache.release(image, quiet=True)
        except Exception as exc:          # never fail a finished run over housekeeping
            field("images", f"could not archive: {type(exc).__name__}: {exc}")

    (d / "result.json").write_text(json.dumps(result, indent=2))
    traj = trajectory.write(d)
    n_ev = len(json.loads(traj.read_text())) if traj else 0

    mark = {"YES": "F2P  YES", "NO": "F2P  NO ", "BROKEN": "BROKEN  "}[verdict.f2p]
    print()
    print(f"  {mark}   {verdict.why[:60]}")
    try:
        shown = d.relative_to(PROJECT_ROOT)
    except ValueError:
        shown = d
    field("output", f"{shown}/   "
                    f"{len(list(d.iterdir()))} files, trajectory {n_ev} events")

    return {"id": pr["id"], "tier": pr["tier"], "f2p": verdict.f2p,
            "why": verdict.why, "actions": run["actions"],
            "config": features.slug(), "label": label,
            "changed_line_coverage": verdict.changed_line_coverage,
            "usage": usage}



def build_parser() -> argparse.ArgumentParser:
    """The parser, built separately so the documentation can read it.

    `docs.py` used to scrape `add_argument` calls out of this file with a regular
    expression, which missed every flag the feature and model registries contribute and
    silently attributed one flag's help to another when a help string was an f-string.
    A parser is the only honest source for what the parser accepts.
    """
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("which", nargs="?", default="all",
                   help="1..26, an instance id, a repository prefix ('django'), "
                        "a tier ('tier5'), or 'all'")
    p.add_argument("--max-iterations", type=int, default=100,
                   help="hard cap on agent steps per PR. Observed use ranges from 12 "
                        "(sympy) to 65 (scikit-learn), so the headroom is deliberate")
    p.add_argument("--dry-run", action="store_true",
                   help="show the target path and runner command, make no LLM call")
    p.add_argument("--no-compare", action="store_true",
                   help="skip the concept judgement against the developer's test")
    p.add_argument("--mutants", type=int, default=0,
                   metavar="N", nargs="?", const=mutants.DEFAULT_MUTANTS,
                   help=f"after the verdict, mutate the lines the patch changed with "
                        f"mutmut and count how many mutants each test kills -- the "
                        f"generated one and the developer's, on the same set. Bare "
                        f"--mutants uses {mutants.DEFAULT_MUTANTS}. Deterministic and "
                        f"offline; the diffs land in <run>/<id>/mutations/. 0 is off")
    p.add_argument("--mutate-saved", action="store_true",
                   help="measure mutation on the tests already written, without "
                        "running the agent again. Adds the `mutation` field and "
                        "changes nothing else. Needs --mutants N")
    p.add_argument("--recheck", action="store_true",
                   help="re-judge the saved tests under the current harness, without "
                        "calling the model again")
    p.add_argument("--retry-broken", action="store_true",
                   help="run only instances with no result, or whose result is BROKEN. "
                        "A BROKEN verdict records that the harness or the connection "
                        "failed and says nothing about the instance, so it is worth "
                        "retrying; YES and NO are findings and are left alone")
    p.add_argument("--parallel", type=int,
                   default=int(os.getenv("F2P_MAX_PARALLEL") or 5),
                   help="how many PRs to run at once (F2P_MAX_PARALLEL, default 5)")
    p.add_argument("--out-root", default=None,
                   help="write results here instead of out/default/. `out/` is a "
                        "container of run folders -- one per run, e.g. "
                        "out/out_full_run/ -- which is how a series stays separable")
    p.add_argument("--label", default="",
                   help="a name for this run, recorded in every result. Defaults to "
                        "the configuration, e.g. no-coverage-tool")
    add_arguments(p)
    models.add_arguments(p)
    return p


def _write_summary(path: Path, results: list[dict]) -> None:
    """The series summary, merged with what is already on disk rather than replacing it.

    `RUNS.md` is rebuilt from every result in the directory, so a run over a subset
    leaves it whole. This file was written from one invocation's results alone, and the
    difference cost the seventy-instance summary: re-running five matplotlib instances
    into the same root replaced seventy entries with five, in a file sitting at the
    series root where it reads as the whole series. Nothing warned, because writing it
    is correct for the run that just happened -- it is only wrong about the series.

    Merged by instance, so the two artefacts at the root agree. This run's entry wins
    for an instance it touched; every other instance keeps the entry it had.
    """
    def key(r: dict) -> str:
        return r.get("id") or r.get("instance_id") or ""

    merged: dict[str, dict] = {}
    if path.is_file():
        try:
            for previous in json.loads(path.read_text()):
                merged[key(previous)] = previous
        except (ValueError, TypeError):
            # Unreadable or not a list. This run's results are a worse summary than a
            # complete one and a better summary than none, so it is written anyway.
            merged = {}
    # Insertion order: instances already here keep their place and are updated where
    # this run touched them, and anything new lands at the end.
    merged.update({key(r): r for r in results})
    path.write_text(json.dumps(list(merged.values()), indent=2))


def main() -> int:
    args = build_parser().parse_args()

    # Which model runs is never implicit. The registry has a `default_model`, so an
    # invocation that omitted --model used to start cleanly on whatever that happened
    # to be -- gpt-5-mini -- while the arm it was being compared against had run on
    # qwen3-coder-30b. Twenty-two of twenty-three failures converted and read as
    # variance until the model field in result.json was checked. A run is a
    # measurement against a named configuration; naming the model is part of stating
    # what was measured, so leaving it out is an error rather than a default.
    if not getattr(args, "model", None) and not args.dry_run:
        raise SystemExit(
            "  --model is required. There is no fallback for which model runs.\n"
            f"  The registry's default_model is {M.DEFAULT_MODEL!r}, but a default is "
            "not a decision -- name the model this run is measuring.")

    features = FeatureSet.from_args(args)
    # Resolved before the early-returning branches below, which all report on a series
    # and so all need to know which one.
    out_root = Path(args.out_root) if args.out_root else None
    prs = pick(args.which)

    if args.retry_broken:
        prs = [pr for pr in prs if _needs_retry((out_root or OUT) / pr["id"])]
        if not prs:
            print("  nothing to retry: every selected instance has a YES or NO result")
            return 0
        print(f"  retrying {len(prs)} instance(s) with no usable result")

    if args.mutate_saved:
        if args.mutants <= 0:
            raise SystemExit("  --mutate-saved needs --mutants N (how many per instance)")
        child = bool(os.getenv(CHILD_ENV_FLAG))
        # Filtered here, in the parent, and not left to the child to decline. A child
        # that declines writes no `result.json`, and the parent's freshness check reads
        # a file it did not write as "the child exited without producing one" -- which
        # would have replaced a real NO verdict with a BROKEN row. The child is only
        # ever given work it will do.
        if not child:
            skip, keep = [], []
            for pr in prs:
                d = (out_root or OUT) / pr["id"]
                rj = d / "result.json"
                why = ""
                if not rj.exists():
                    why = "no result to add to"
                else:
                    got = json.loads(rj.read_text()).get("f2p")
                    if got != "YES":
                        why = f"f2p is {got}, not YES"
                    elif not next((f for f in d.glob("test_f2p_*.py")), None):
                        why = "no saved test"
                (skip if why else keep).append((pr, why))
            for pr, why in skip:
                print(f"  skipping {pr['id']}: {why}")
            prs = [pr for pr, _ in keep]
            if not prs:
                print("  nothing eligible: mutation needs a YES with a saved test")
                return 0
            print(f"  measuring mutation on {len(prs)} saved test(s), "
                  f"{args.mutants} mutant(s) each")
        E.reap_orphans(quiet=False)
        if child or len(prs) == 1 or args.parallel <= 1:
            rows = [mutate_saved(pr, args.mutants,
                                 instance_dir(out_root, pr, child))
                    for pr in prs]
        else:
            # A process each, for the same reason the agent gets one: `flow._current` is
            # a module global, so two of these in one interpreter would write their step
            # logs into each other's file.
            jobs = []
            for pr in prs:
                out = (out_root or OUT) / pr["id"]
                jobs.append((pr["id"], _child_argv(pr["id"], args, features, out, ""),
                             out, ""))
            # A child that dies here must not be allowed to replace the result it was
            # only adding a field to.
            rows = _run_children(jobs, args.parallel, may_replace_result=False)
        done = [r for r in rows if (r.get("mutation") or {}).get("measured")]
        counted = sum(r["mutation"]["total"] for r in done)
        killed = sum(r["mutation"]["agent"]["killed"] for r in done)
        dev = sum(r["mutation"]["developer"]["killed"] or 0 for r in done)
        if counted:
            print(f"\n  measured {len(done)}/{len(rows)} instance(s) over {counted} "
                  f"mutant(s): the generated tests killed {killed} "
                  f"({100.0 * killed / counted:.0f}%), the developers' killed {dev} "
                  f"({100.0 * dev / counted:.0f}%)")
        else:
            print(f"\n  measured {len(done)}/{len(rows)} instance(s)")
        for r in rows:
            note = r.get("skipped") or r.get("failed")
            if note:
                print(f"    {r.get('id') or r.get('instance_id', '?')}: {note[:150]}")
        runs.main(out_root or OUT)
        return 0

    if args.recheck:
        E.reap_orphans(quiet=False)
        rows = [recheck(pr, instance_dir(out_root, pr,
                                        bool(os.getenv(CHILD_ENV_FLAG))))
                for pr in prs]
        yes = sum(1 for r in rows if r.get("f2p") == "YES")
        print(f"\n  {yes}/{len(rows)} still fail-to-pass after re-judging")
        runs.main(out_root or OUT)
        return 0

    if not os.getenv(CHILD_ENV_FLAG):
        if not args.dry_run:
            # Docker before the gateway: it is the cheaper check, and a missing daemon
            # fails every instance rather than some of them.
            for refusal in (E.daemon_refusal(), llm_config.gateway_refusal(args.model)):
                if refusal:
                    raise SystemExit(f"  {refusal}")
        E.reap_orphans(quiet=False)      # a killed run leaves its container running
    child = bool(os.getenv(CHILD_ENV_FLAG))

    # One PR, or a child doing exactly one: run it here so its output streams.
    if child or len(prs) == 1 or args.dry_run or args.parallel <= 1:
        results = [do_pr(pr, args.max_iterations, args.dry_run, features,
                         args.no_compare, instance_dir(out_root, pr, child),
                         args.label, args.mutants,
                         model=args.model, provider=args.provider,
                         judge_model=args.judge_model,
                         temperature=args.temperature)
                   for pr in prs]
    else:
        jobs = []
        for pr in prs:
            out = (out_root or OUT) / pr["id"]
            jobs.append((pr["id"],
                         _child_argv(pr["id"], args, features, out, ""),
                         out, ""))
        results = _run_children(jobs, args.parallel)

    if not args.dry_run and len(results) > 1:
        print("\n" + "-" * 74)
        for r in results:
            c = r.get("changed_line_coverage") or {}
            cov = f"{c['percent']:.0f}%" if c.get("measured") else "-"
            print(f"  {r.get('f2p','?'):<4} tier {r.get('tier','?')}  "
                  f"{r.get('id', r.get('instance_id','?')):36s} "
                  f"{r.get('actions',0):3d} actions  cov {cov:>4s}")
        yes = sum(r.get("f2p") == "YES" for r in results)
        print(f"\n{yes}/{len(results)} generated tests are fail-to-pass")
        (out_root or OUT).mkdir(parents=True, exist_ok=True)
        _write_summary((out_root or OUT) / "agent_summary.json", results)

    # RUNS.md is the index a reader opens first, so it is rewritten from the results on
    # disk at the end of every run rather than maintained by hand. Two exclusions. A
    # child skips it: it owns one directory, and twenty-six children racing on one file
    # would interleave. And a single instance skips it, because there `--out-root` names
    # that instance's own directory rather than a series -- the table would have one row
    # and sit inside it.
    series = len(prs) > 1
    if not child and not args.dry_run and series:
        runs.main(out_root or OUT)
        # The generated blocks in the design document are read out of the code, so a
        # renamed module or a new flag updates them here rather than going stale until
        # someone notices.
        docs.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(main())
