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
import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import time

from dotenv import load_dotenv

from openhands_f2p import (compare, docs, flow, llm_config, prompt, runs,
                           sandbox_tools,
                           swebench_env as E, trajectory, verify as V)
from openhands_f2p.dataset import load
from openhands_f2p.prs import pick

PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUT = PROJECT_ROOT / "out"

env_file = PROJECT_ROOT / ".env"
if env_file.exists():
    load_dotenv(env_file, override=False)

# The SDK's loggers propagate to a root RichHandler set to INFO, which prints tmux pool
# setup, conversation ids and tool loading on every run. None of it says anything about
# whether the run worked. Real warnings still come through.
logging.getLogger("openhands").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)


def field(label: str, text: str) -> None:
    """One aligned line. Every status line in this file goes through here."""
    print(f"  {label:<9} {text}")


def run_agent(instance: dict, box: E.Sandbox, test_file: str, max_iterations: int,
              runner_kind: str, out_dir: Path, blind: bool = False,
              coverage_tool: bool = True) -> dict:
    from openhands.sdk import Agent, Conversation, Tool
    from openhands.sdk.event import ActionEvent, MessageEvent, ObservationEvent

    t_start = time.time()
    llm, model, proxy = llm_config.configure_llm(out_dir / "completions")
    tool_log: list = []
    # The patch reaches the tools and the prompt together, or neither: the `coverage`
    # and `verify` tools only exist because the agent is shown the change.
    patch = "" if blind else instance["patch"]
    names = sandbox_tools.register(box, instance["repo"], tool_log, patch=patch,
                                   coverage_tool=coverage_tool, gen_path=test_file,
                                   version=instance.get("version", ""))
    agent = Agent(llm=llm, tools=[Tool(name=n) for n in names])

    transcript: list[dict] = []
    counts: dict[str, int] = {}
    live = sys.stdout.isatty()

    def on_event(event) -> None:
        row = {"kind": type(event).__name__,
               "at": datetime.now(timezone.utc).isoformat()}
        if isinstance(event, ActionEvent):
            row["action"] = type(event.action).__name__
            row["detail"] = str(event.action)[:2500]
            short = {"RunAction": "run", "WriteAction": "write",
                     "TestAction": "test", "FinishAction": "finish",
                     "ThinkAction": "think"}.get(row["action"], row["action"])
            counts[short] = counts.get(short, 0) + 1
            n = sum(counts.values())
            if live:
                # One line that rewrites itself, so a 46-action run does not scroll
                # the useful output off the screen.
                print(f"\r  {'agent':<9} working... {n:2d} actions "
                      f"({', '.join(f'{v} {k}' for k, v in counts.items())})"
                      f"{' ' * 12}", end="", flush=True)
            flow.record(flow.AGENT, row["action"],
                        str(event.action).replace("\n", " ")[:110])
        elif isinstance(event, (ObservationEvent, MessageEvent)):
            row["detail"] = str(getattr(event, "observation", None)
                                or getattr(event, "llm_message", event))[:2500]
        else:
            row["detail"] = str(event)[:1200]
        transcript.append(row)

    # Assembled from prompts/, one file per instruction. See prompts/README.md.
    task = prompt.build(repo=instance["repo"], test_file=test_file,
                        problem=instance["problem_statement"], runner=runner_kind,
                        patch=patch, coverage_tool=coverage_tool,
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
    conversation = Conversation(agent=agent, workspace=str(PROJECT_ROOT / ".cache" / "ws"),
                                persistence_dir=str(PROJECT_ROOT / ".cache" / "openhands"
                                                    / instance["instance_id"]),
                                callbacks=[on_event],
                                max_iteration_per_run=max_iterations, visualizer=None)
    flow.record(flow.AGENT, "tools registered", ", ".join(names))
    flow.record(flow.AGENT, "task sent", f"{len(task)} chars, max_iter={max_iterations}")
    conversation.send_message(task)
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
    return {"status": status, "error": error, "capped": n_actions >= max_iterations,
            "transcript": transcript,
            "tool_log": tool_log, "model": model, "task": task,
            "actions": sum(1 for r in transcript if "action" in r)}


# Commands that could actually fetch something, and nothing else. The trailing
# `|https?://` this used to carry matched any URL anywhere in a command -- so an agent
# pasting the issue's own reproduction (`requests.get('http://.example.com')`) into a
# heredoc was flagged as attempting network access. Three separate runs were reported
# as suspicious for quoting the bug they were asked to reproduce. An audit that fires on
# the subject matter trains you to ignore it.
# Only in *command position* -- start of the command, or straight after a shell
# separator. The previous version allowed a match after any whitespace, and `host` and
# `dig` are ordinary English words: an agent printing `getattr(p, 'host', None)` inside a
# heredoc was flagged as attempting DNS. That is the fourth false positive this check has
# produced, each one on the repository's own subject matter, and a check that cries wolf
# four times is a check nobody reads.
NETWORK = re.compile(
    r"(?:^|[;&|`(]\s*|\n\s*|&&\s*|\|\|\s*)"
    r"(curl|wget|nc|ncat|telnet|ssh|scp|rsync|ping|host|dig|"
    r"pip\s+download|pip\s+install|"
    r"git\s+(?:clone|fetch|pull|remote|ls-remote))\b", re.I)


def audit(box: E.Sandbox, tool_log: list, test_file: str) -> dict:
    """What the agent actually did, checked rather than assumed.

    Network attempts are read off the tool log rather than the whole transcript: an
    earlier version scanned every event and flagged the test file the agent wrote,
    because in a repo about HTTP the string `requests.get("http` appears innocently.
    """
    tried_network = [e["command"] for e in tool_log
                     if e["tool"] == "run" and NETWORK.search(e.get("command", ""))]
    wrote_elsewhere = [e["path"] for e in tool_log
                       if e["tool"] == "write_file" and e.get("path") != test_file]
    dirty = box.exec("git status --porcelain 2>/dev/null || echo NO_GIT").output.strip()
    return {"network_attempts": tried_network,
            "files_written_outside_test": wrote_elsewhere,
            "isolation": box.audit_isolation(),
            "vcs": "absent" if "NO_GIT" in dirty else dirty[:300]}


def budget_exhausted(out_dir: Path) -> dict | None:
    """Did the last call end because the output budget ran out, not because the model
    had nothing to say?

    Worth separating. A reasoning model can spend its entire output allowance thinking
    and emit no tool call at all, which looks exactly like a model that cannot call
    tools -- and that misdiagnosis cost time once already, on a model that genuinely
    could not. The distinction is in the response: `finish_reason: length` with
    reasoning_tokens equal to the whole budget means raise the cap, not change the model.
    """
    files = sorted((out_dir / "completions").glob("*.json"))
    if not files:
        return None
    try:
        last = json.loads(files[-1].read_text())
    except (json.JSONDecodeError, OSError):
        return None
    choice = ((last.get("response") or {}).get("choices") or [{}])[0]
    if choice.get("finish_reason") != "length":
        return None
    u = last.get("usage_summary") or {}
    return {"completion_tokens": u.get("completion_tokens"),
            "reasoning_tokens": u.get("reasoning_tokens")}


def token_usage(out_dir: Path) -> dict:
    """Totals across every LLM call of this run, from the completion logs.

    Only meaningful because `completions/` is cleared before the run: litellm appends a
    file per call and never prunes it, so a second run on the same PR would otherwise be
    summed together with the first.
    """
    files = sorted((out_dir / "completions").glob("*.json"))
    total = {"llm_calls": len(files), "prompt_tokens": 0, "cache_read_tokens": 0,
             "completion_tokens": 0, "reasoning_tokens": 0, "cost_usd": 0.0,
             "llm_latency_sec": 0.0}
    for f in files:
        try:
            j = json.loads(f.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        u = j.get("usage_summary") or {}
        for key in ("prompt_tokens", "cache_read_tokens", "completion_tokens",
                    "reasoning_tokens"):
            total[key] += u.get(key, 0) or 0
        total["cost_usd"] += j.get("cost") or 0.0
        total["llm_latency_sec"] += j.get("latency_sec") or 0.0
    total["cost_usd"] = round(total["cost_usd"], 6)
    total["llm_latency_sec"] = round(total["llm_latency_sec"], 1)
    total["total_tokens"] = total["prompt_tokens"] + total["completion_tokens"]
    return total


def recheck(pr: dict) -> dict:
    """Re-judge a test the agent already wrote, without running the agent again.

    A harness bug that only affects the verdict or the coverage measurement -- not the
    generation -- does not need a fresh $0.06 of tokens and a fresh roll of the dice to
    correct. The saved test is the agent's answer; re-running it under the fixed harness
    asks the same question again and gets the answer we should have had the first time.
    Kept separate from `do_pr` so it cannot be mistaken for a run: nothing here calls an
    LLM, and the trajectory and token counts of the original are left untouched.
    """
    d = OUT / pr["id"]
    inst = load(pr["id"])
    saved = next((f for f in d.glob("test_f2p_*.py")), None)
    if saved is None:
        return {"id": pr["id"], "f2p": "BROKEN", "why": "no saved test to re-judge"}
    code = saved.read_text()
    print(f"  rechecking {pr['id']}  ({saved.name}, {code.count(chr(10)) + 1} lines)")

    with E.Sandbox(pr["id"], quiet=True, extra_packages=("coverage",)) as box:
        box.strip_git()
        verdict = V.verify(inst, box, generated_test=code, quiet=True)

    old = json.loads((d / "result.json").read_text())
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


def do_pr(pr: dict, max_iterations: int, dry_run: bool, blind: bool = False,
          no_compare: bool = False, coverage_tool: bool = True,
          out_root: Path | None = None, label: str = "") -> dict:
    inst = load(pr["id"])
    repo = inst["repo"]
    test_file = V.gen_test_path(repo, pr["id"])      # provisional; re-resolved in the box
    print(f"\n{'─' * 74}")
    print(f"  [{pr['tier']}] {pr['id']}".ljust(52) + repo.rjust(20))
    print(f"  {pr['note'][:70]}")
    print(f"{'─' * 74}")

    # `out_root`, when given, is the exact directory for this run -- not a parent to
    # append the id to. Appending produced out_compare_coverage/<pr>/<label>/<pr>/ and,
    # worse, left the "output" line pointing at out/ where nothing had been written.
    d = out_root if out_root is not None else OUT / pr["id"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "pr.json").write_text(json.dumps(
        {**inst, "FAIL_TO_PASS_parsed": json.loads(inst["FAIL_TO_PASS"]),
         "PASS_TO_PASS_parsed": json.loads(inst["PASS_TO_PASS"])}, indent=2))
    (d / "fix.diff").write_text(inst["patch"])
    (d / "developer_test.diff").write_text(inst["test_patch"])
    shutil.rmtree(d / "completions", ignore_errors=True)   # counts are per run

    if dry_run:
        field("target", test_file)
        field("runner", E.test_command(repo, [test_file]))
        return {"id": pr["id"], "tier": pr["tier"], "f2p": "SKIPPED"}

    image = E.image_for(pr["id"])
    if not E.have_image(image):
        field("image", f"pulling {image.split('.')[-1]} (once, 1-5 GB)")

    with flow.recording(d, f"{pr['id']}  ({repo})  arm=agent"), \
            E.Sandbox(pr["id"], quiet=True,
                      # installed on the bridge, then the network is removed and
                      # the seal re-checked -- see Sandbox._install_then_seal
                      extra_packages=("coverage",)) as box:
        flow.record(flow.SETUP, "instance", f"{pr['note']}")
        box.strip_git()
        test_file = V.gen_test_path(repo, pr["id"], box)
        flow.record(flow.SETUP, "test path", test_file)
        field("sandbox", f"{image.split('.')[-1]}   network=none, git stripped")
        field("target", test_file)

        run = run_agent(inst, box, test_file, max_iterations,
                        E.runner_for(repo)["kind"], d, blind=blind,
                        coverage_tool=coverage_tool)
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
                    f"stray_writes={checks['files_written_outside_test'] or 'none'}")

        starved = budget_exhausted(d) if run["actions"] == 0 else None
        if code is None and starved:
            verdict = V.Verdict(pr["id"], "BROKEN",
                                f"the model spent its whole output budget on reasoning "
                                f"({starved['reasoning_tokens']} of "
                                f"{starved['completion_tokens']} tokens) and had none "
                                f"left to call a tool -- raise LLM_MAX_OUTPUT_TOKENS")
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
                                       f"test at {test_file}")))
        else:
            (d / Path(test_file).name).write_text(code)
            field("test", f"{code.count(chr(10)) + 1} lines written")
            verdict = V.verify(inst, box, generated_test=code, quiet=True)
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

    iso = checks["isolation"]
    field("audit", f"network {checks['network_attempts'] or 'none'}, "
                   f"stray writes {checks['files_written_outside_test'] or 'none'}, "
                   f"dns {'off' if not iso['dns_resolves'] else 'ON'}, "
                   f"git {checks['vcs']}")

    (d / "tool_log.json").write_text(json.dumps(run["tool_log"], indent=2))
    (d / "before_fix.log").write_text(verdict.base_log)
    (d / "after_fix.log").write_text(verdict.head_log)
    usage = token_usage(d)
    result = {**verdict.as_dict(), "tier": pr["tier"],
              "arm": label or ("agent-blind" if blind else "agent"),
              "coverage_tool": coverage_tool,
              "usage": usage,
              "model": run["model"], "agent_status": run["status"],
              "agent_error": flow.scrub(run.get("error") or "") or None,
              # The prompt lives here rather than in its own task.txt: it is one field,
              # and keeping it means a trajectory can still be rebuilt from disk.
              "task": run["task"],
              "actions": run["actions"],
              "files_edited_outside_test": checks["files_written_outside_test"],
              "audit": checks}
    # The concept check goes here and nowhere earlier: it is the only step that reads
    # the developer's test, so it must not run until the F2P verdict is settled. Its
    # answer is recorded beside the verdict, never folded into it.
    if code is not None and not no_compare:
        try:
            result["concept"] = compare.compare(inst, code)
            field("concept", compare.line(result["concept"]))
        except Exception as exc:
            result["concept"] = {"verdict": "error", "reasoning": str(exc)[:200]}
            field("concept", f"comparison failed: {str(exc)[:70]}")

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
            "coverage_tool": coverage_tool, "label": label,
            "changed_line_coverage": verdict.changed_line_coverage,
            "usage": usage}


# --------------------------------------------------------------------- parallel
#
# Separate processes, not threads. Two pieces of module-level state make threads unsafe
# here, and both fail silently rather than loudly:
#
#   * The SDK's tool registry is a module-level dict, and `Agent._initialize` resolves
#     from it lazily -- at first run, not at construction. Two threads registering `run`
#     would leave the second one's executor in place for both, so one run would issue its
#     commands inside the other's container. Nothing would raise; the results would just
#     be wrong.
#   * `flow._current` is a module global, so two runs would interleave into one flow.log.
#
# A process per PR removes both by construction, and the work is subprocess- and
# network-bound anyway, so there is nothing to gain from sharing an interpreter.
CHILD_ENV_FLAG = "F2P_CHILD_OF"


def _child_argv(pr_id: str, args, coverage_tool: bool, out_root: Path,
                label: str) -> list[str]:
    argv = [sys.executable, "-m", "openhands_f2p.agent", pr_id,
            "--max-iterations", str(args.max_iterations),
            "--out-root", str(out_root)]
    # `--dry-run` has to reach the child, because the child is where the work happens.
    # Without it `--compare-coverage --dry-run` was not a dry run at all: the parent
    # printed nothing and forked two real runs per PR, each starting a container and
    # spending real tokens. A flag whose whole purpose is to not do the thing must not
    # be the one flag that gets dropped on the way.
    if args.dry_run:
        argv.append("--dry-run")
    if args.blind:
        argv.append("--blind")
    if args.no_compare:
        argv.append("--no-compare")
    if not coverage_tool:
        argv.append("--no-coverage-tool")
    if label:
        argv += ["--label", label]
    return argv


def _needs_retry(out_dir: Path) -> bool:
    """True when this instance has no result, or one that is not a real verdict.

    YES and NO are findings about a generated test and are never silently rerun --
    that would quietly turn a run into a best-of-N. BROKEN is different: it records that
    the harness or the connection failed, which says nothing about the instance. One of
    the twenty-six failed this way when the laptop lost its network mid-run.
    """
    f = out_dir / "result.json"
    if not f.exists():
        return True
    try:
        return json.loads(f.read_text()).get("f2p") not in ("YES", "NO")
    except (json.JSONDecodeError, OSError):
        return True


def _progress_line(out_dir: Path, pr_id: str, width: int = 20) -> str:
    """One line of live status for a child, read off the files it is already writing.

    No IPC needed: `flow.jsonl` is flushed per step and `result.json` appears at the end,
    so the parent can just read them. Children capture their own stdout into child.log,
    which is why a parallel run otherwise showed nothing at all for twenty minutes.
    """
    rj = out_dir / "result.json"
    if rj.exists():
        try:
            r = json.loads(rj.read_text())
        except (json.JSONDecodeError, OSError):
            return f"  {pr_id[:34]:34s} done"
        c = r.get("changed_line_coverage") or {}
        cov = f"cov {c['percent']:.0f}%" if c.get("measured") else "cov --"
        return (f"  {pr_id[:34]:34s} {'done':7s} {r.get('f2p','?'):4s} {cov:8s} "
                f"{r.get('actions', 0):3d} actions")

    fj = out_dir / "flow.jsonl"
    if not fj.exists():
        return f"  {pr_id[:34]:34s} {'starting':7s}"
    try:
        rows = [json.loads(l) for l in fj.read_text().splitlines() if l.strip()]
    except (json.JSONDecodeError, OSError):
        rows = []
    if not rows:
        return f"  {pr_id[:34]:34s} {'starting':7s}"
    last = rows[-1]
    acts = sum(1 for r in rows if r.get("phase") == "agent"
               and str(r.get("event", "")).endswith("Action"))
    detail = str(last.get("event") or "")[:width]
    return (f"  {pr_id[:34]:34s} {last.get('phase','')!s:7s} "
            f"{acts:3d} actions  {detail:{width}s} {last.get('t', 0):5.0f}s")


def _run_children(jobs: list[tuple], parallel: int) -> list[dict]:
    """Each job is (pr_id, argv, out_dir, label). Returns whatever the children wrote."""
    import subprocess
    import threading
    from concurrent.futures import ThreadPoolExecutor      # threads only wait on procs

    env = dict(os.environ, **{CHILD_ENV_FLAG: "1"})
    labels = [f"{pid}{f' [{lab}]' if lab else ''}" for pid, _, _, lab in jobs]
    print(f"  {len(jobs)} job(s), {parallel} at a time. "
          f"Full output per job in its child.log.\n")

    live = sys.stdout.isatty()
    stop = threading.Event()

    def paint(first: bool = False) -> None:
        lines = [_progress_line(out, lab)
                 for (_, _, out, _), lab in zip(jobs, labels, strict=True)]
        if not first:
            sys.stdout.write(f"\033[{len(lines)}A")
        sys.stdout.write("".join(f"{l:<98}\n" for l in lines))
        sys.stdout.flush()

    def redraw() -> None:
        paint(first=True)
        while not stop.is_set():
            stop.wait(2.0)
            paint()

    def one(idx_job):
        idx, (pr_id, argv, out_dir, label) = idx_job
        # A ceiling, not a schedule. Nothing here should take two hours -- the longest
        # real run was twenty minutes plus a pull -- but a child that wedges on a socket
        # used to hold the parent open indefinitely, and three of them once sat silent
        # for fifty-one minutes after a laptop sleep before being killed by hand.
        limit = float(os.getenv("F2P_CHILD_TIMEOUT") or 7200)
        try:
            proc = subprocess.run(argv, capture_output=True, text=True, env=env,
                                  timeout=limit)
        except subprocess.TimeoutExpired as exc:
            def text_of(v):
                return v.decode(errors="replace") if isinstance(v, bytes) else (v or "")
            proc = subprocess.CompletedProcess(
                argv, 124, text_of(exc.stdout),
                text_of(exc.stderr) + f"\nkilled after {limit:.0f}s")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "child.log").write_text(
            proc.stdout + ("\n--- stderr ---\n" + proc.stderr
                           if proc.stderr.strip() else ""))
        rj = out_dir / "result.json"
        row = json.loads(rj.read_text()) if rj.exists() else {
            "instance_id": pr_id, "f2p": "BROKEN",
            "why": f"child exited {proc.returncode} without writing a result"}
        row["label"] = label
        if not live:                       # piped output: one line per finish
            print(f"  {row.get('f2p', '?'):6s} {labels[idx]}", flush=True)
        return row

    painter = threading.Thread(target=redraw, daemon=True) if live else None
    if painter:
        painter.start()
    try:
        with ThreadPoolExecutor(max_workers=max(1, parallel)) as ex:
            rows = list(ex.map(one, enumerate(jobs)))
    finally:
        stop.set()
        if painter:
            painter.join(timeout=3)
            paint()                        # end on the finished state
    return rows


def compare_coverage(prs: list[dict], args) -> int:
    """Run every PR twice -- with the coverage tool and without -- and contrast them.

    The harness measures changed-line coverage in *both* arms. That is the whole point:
    without a number for the arm that had no coverage tool there is nothing to compare
    against, and any claim that the tool helps would rest on a single run of the arm that
    had it.
    """
    root = PROJECT_ROOT / "out_compare_coverage"
    jobs = []
    for pr in prs:
        for on, label in ((True, "with_coverage_tool"), (False, "without_coverage_tool")):
            out = root / pr["id"] / label
            jobs.append((pr["id"], _child_argv(pr["id"], args, on, out, label),
                         out, label))
    # Two runs per PR, so the cap is doubled -- the configured number is PRs in flight.
    rows = _run_children(jobs, args.parallel * 2)

    print("\n" + "=" * 78)
    print(f"{'instance':32s} {'tool':4s} {'F2P':5s} {'changed-line cov':>17s} {'act':>4s}")
    by_id: dict[str, dict] = {}
    for r in rows:
        by_id.setdefault(r["instance_id"], {})[r["label"]] = r
    for iid, pair in sorted(by_id.items()):
        for label, mark in (("with_coverage_tool", "on "),
                            ("without_coverage_tool", "off")):
            r = pair.get(label)
            if not r:
                print(f"{iid[:32]:32s} {mark:4s} {'--':5s} {'no result':>17s}")
                continue
            c = r.get("changed_line_coverage") or {}
            cov = (f"{c['percent']:.1f}% ({c['covered']}/"
                   f"{c['executable_changed_lines']})" if c.get("measured")
                   else "not measured")
            print(f"{iid[:32]:32s} {mark:4s} {r.get('f2p','?'):5s} {cov:>17s} "
                  f"{r.get('actions', 0):4d}")
        print()
    # The per-instance table is evidence; this is the answer. Both arms are summarised
    # over the instances where *both* produced a number, because an arm that failed on a
    # different subset would otherwise be compared on easier work.
    paired = [(a, b) for a, b in
              ((pair.get("with_coverage_tool"), pair.get("without_coverage_tool"))
               for pair in by_id.values()) if a and b]
    aggregate = {"instances": len(by_id), "paired": len(paired), "arms": {}}
    print("=" * 78)
    print(f"{'':22s} {'F2P':>10s} {'mean cov':>10s} {'median cov':>11s} {'actions':>9s}")
    for label, key in (("with coverage tool", "with_coverage_tool"),
                       ("without", "without_coverage_tool")):
        arm = [r for r in (pair.get(key) for pair in by_id.values()) if r]
        yes = sum(1 for r in arm if r.get("f2p") == "YES")
        covs = sorted(c["percent"] for r in arm
                      if (c := r.get("changed_line_coverage") or {}).get("measured"))
        mean = sum(covs) / len(covs) if covs else None
        med = covs[len(covs) // 2] if covs else None
        acts = [r.get("actions", 0) for r in arm]
        aggregate["arms"][key] = {
            "runs": len(arm), "f2p_yes": yes, "measured": len(covs),
            "mean_coverage": round(mean, 1) if mean is not None else None,
            "median_coverage": med,
            "mean_actions": round(sum(acts) / len(acts), 1) if acts else None}
        print(f"{label:22s} {f'{yes}/{len(arm)}':>10s} "
              f"{(f'{mean:.1f}%' if mean is not None else '-'):>10s} "
              f"{(f'{med:.1f}%' if med is not None else '-'):>11s} "
              f"{(sum(acts) / len(acts) if acts else 0):>9.1f}")
    if len(paired) < len(by_id):
        print(f"\n  {len(by_id) - len(paired)} instance(s) produced a result in only one "
              f"arm; the means above are over each arm's own runs, so read them "
              f"alongside the per-instance table rather than as a paired difference.")

    (root / "summary.json").write_text(
        json.dumps({"aggregate": aggregate, "runs": rows}, indent=2))
    print("\nwrote out_compare_coverage/summary.json")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("which", nargs="?", default="all",
                   help="1..23, an instance id, a repository prefix ('django'), "
                        "a tier ('tier5'), or 'all'")
    p.add_argument("--max-iterations", type=int, default=100,
                   help="hard cap on agent steps per PR. Observed use ranges from 12 "
                        "(sympy) to 65 (scikit-learn), so the headroom is deliberate")
    p.add_argument("--dry-run", action="store_true",
                   help="show the target path and runner command, make no LLM call")
    p.add_argument("--blind", action="store_true",
                   help="withhold the PR diff. Harder task, comparable to TDD-Bench "
                        "baselines; drops the coverage and verify tools with it")
    p.add_argument("--no-compare", action="store_true",
                   help="skip the concept judgement against the developer's test")
    p.add_argument("--compare-coverage", action="store_true",
                   help="run each PR twice, with and without the coverage tool, into "
                        "out_compare_coverage/<pr>/{with,without}_coverage_tool/")
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
                   help="how many PRs to run at once (F2P_MAX_PARALLEL, default 5). "
                        "Doubled in --compare-coverage, since each PR is two runs")
    # set by the parent when it forks a child; not for people
    p.add_argument("--no-coverage-tool", action="store_true", help=argparse.SUPPRESS)
    p.add_argument("--out-root", default=None, help=argparse.SUPPRESS)
    p.add_argument("--label", default="", help=argparse.SUPPRESS)
    args = p.parse_args()

    prs = pick(args.which)

    if args.retry_broken:
        root = Path(args.out_root) if args.out_root else OUT
        prs = [pr for pr in prs if _needs_retry(root / pr["id"])]
        if not prs:
            print("  nothing to retry: every selected instance has a YES or NO result")
            return 0
        print(f"  retrying {len(prs)} instance(s) with no usable result")

    # Refused rather than run: with --blind there is no diff, so the coverage tool is
    # never registered in either arm and the prompts come out byte-identical. The
    # comparison would be a thing against itself, and the noise between two runs of the
    # same configuration would read as an effect of the tool.
    if args.recheck:
        E.reap_orphans(quiet=False)
        rows = [recheck(pr) for pr in prs]
        yes = sum(1 for r in rows if r.get("f2p") == "YES")
        print(f"\n  {yes}/{len(rows)} still fail-to-pass after re-judging")
        runs.main()
        return 0

    if args.compare_coverage and args.blind:
        raise SystemExit(
            "--compare-coverage and --blind cannot be combined. The coverage tool needs "
            "the diff, so under --blind neither arm has it and both arms are identical. "
            "Run --compare-coverage without --blind to measure the tool, or --blind on "
            "its own to measure the harder task.")

    if not os.getenv(CHILD_ENV_FLAG):
        if not args.dry_run:
            refusal = llm_config.gateway_refusal()
            if refusal:
                raise SystemExit(f"  {refusal}")
        E.reap_orphans(quiet=False)      # a killed run leaves its container running
    out_root = Path(args.out_root) if args.out_root else None
    child = bool(os.getenv(CHILD_ENV_FLAG))

    if args.compare_coverage and not child:
        return compare_coverage(prs, args)

    # One PR, or a child doing exactly one: run it here so its output streams.
    if child or len(prs) == 1 or args.dry_run or args.parallel <= 1:
        results = [do_pr(pr, args.max_iterations, args.dry_run, args.blind,
                         args.no_compare, not args.no_coverage_tool, out_root,
                         args.label) for pr in prs]
    else:
        jobs = []
        for pr in prs:
            out = (out_root or OUT) / pr["id"]
            jobs.append((pr["id"],
                         _child_argv(pr["id"], args, not args.no_coverage_tool, out, ""),
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
        ((out_root or OUT) / "agent_summary.json").write_text(json.dumps(results, indent=2))

    # out/RUNS.md is the index a reader opens first, so it is rewritten from the results
    # on disk at the end of every run rather than maintained by hand. A child skips it:
    # it owns one directory, and twenty-six children racing on one file would interleave.
    if not child and not args.dry_run and out_root is None:
        runs.main()
        # The generated blocks in the design document are read out of the code, so a
        # renamed module or a new flag updates them here rather than going stale until
        # someone notices.
        docs.refresh()
    return 0


if __name__ == "__main__":
    sys.exit(main())
