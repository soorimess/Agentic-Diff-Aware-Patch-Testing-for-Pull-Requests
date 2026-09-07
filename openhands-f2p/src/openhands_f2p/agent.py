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
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import time

from openhands_f2p import (arms, compare, docs, flow, llm_config, prompt, runs,
                           sandbox_tools, swebench_env as E, trajectory, verify as V)
from openhands_f2p.checks import audit, budget_exhausted, token_usage
from openhands_f2p.dataset import load
from openhands_f2p.layout import CACHE, OUT, PROJECT_ROOT
from openhands_f2p.parallel import (CHILD_ENV_FLAG, _child_argv, _needs_retry,
                                    _run_children)
from openhands_f2p.prs import pick


def field(label: str, text: str) -> None:
    """One aligned line. Every status line in this file goes through here."""
    print(f"  {label:<9} {text}")


def run_agent(instance: dict, box: E.Sandbox, test_file: str, max_iterations: int,
              out_dir: Path, blind: bool = False,
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
                                   coverage_tool=coverage_tool, gen_path=test_file)
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
                        repo_facts=E.repo_facts(box, test_file),
                        problem=instance["problem_statement"], patch=patch, coverage_tool=coverage_tool,
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
    conversation = Conversation(agent=agent, workspace=str(CACHE / "ws"),
                                persistence_dir=str(CACHE / "openhands"
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
    test_file = V.gen_test_path(pr["id"])      # provisional; re-resolved in the box
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
        # No container in a dry run, and the runner is a property of the checkout.
        field("runner", "detected from the checkout when the container starts")
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
        test_file = V.gen_test_path(pr["id"], box)
        flow.record(flow.SETUP, "test path", test_file)
        field("sandbox", f"{image.split('.')[-1]}   network=none, git stripped")
        field("target", test_file)

        run = run_agent(inst, box, test_file, max_iterations, d, blind=blind,
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
              # When the agent actually ran. The file's mtime used to stand in for this
              # and was wrong the moment anything touched the file afterwards -- a
              # re-judge moved two instances a day forward in the run table.
              "ran_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
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
        return arms.compare_coverage(prs, args)

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
