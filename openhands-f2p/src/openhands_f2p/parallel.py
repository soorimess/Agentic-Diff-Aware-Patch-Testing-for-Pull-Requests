"""Running several pull requests at once, as separate processes.

Processes rather than threads, because the SDK's tool registry is a process-global
resolved lazily when the agent is constructed -- two agents in one process would share it.
The threads here only wait on subprocesses.

That choice makes every shared resource a hazard, and the two that bit are handled
elsewhere: image pulls are serialised behind a lock in `images`, and container reaping
goes by owning process id rather than by name.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path

from openhands_f2p.features import FeatureSet, child_flags



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


def _child_argv(pr_id: str, args, features: FeatureSet, out_root: Path,
                label: str) -> list[str]:
    """The command line that reproduces this run for one instance.

    Everything that changes what the agent is given has to be forwarded, because the
    child is where the work happens. `--dry-run` was once dropped here and the parent
    printed nothing while forking real runs that started containers and spent real
    tokens. The feature flags come from `features.child_flags`, generated from the
    registry, so a new switch cannot be added and forgotten on this line.
    """
    argv = [sys.executable, "-m", "openhands_f2p.agent", pr_id,
            "--max-iterations", str(args.max_iterations),
            "--out-root", str(out_root)]
    if args.dry_run:
        argv.append("--dry-run")
    if args.no_compare:
        argv.append("--no-compare")
    if getattr(args, "mutants", 0):
        argv += ["--mutants", str(args.mutants)]
    # No `--second-chance`: it is a feature since 2026-09-28, forwarded with the others
    # as `--add-second-chance` when present.
    # Which model answers is part of what the run *is*, so it has to reach the child.
    # Left off, a parallel run would quietly use the default while the header said
    # otherwise -- the same class of mistake as dropping --dry-run, which once forked
    # real runs that started containers and spent real tokens.
    for flag in ("model", "judge_model", "provider"):
        value = getattr(args, flag, None)
        if value:
            argv += [f"--{flag.replace('_', '-')}", str(value)]
    # Tested against None, not for truth: 0.0 is a real temperature, and the loop above
    # would drop it -- the children would sample at the provider's default while the
    # parent recorded 0.
    if getattr(args, "temperature", None) is not None:
        argv += ["--temperature", repr(args.temperature)]
    if getattr(args, "mutate_saved", False):
        argv.append("--mutate-saved")
    # The environment carries it too (sources.select); on the command line as well so
    # the child's argv, which is logged, says what it ran over.
    if getattr(args, "dataset", None):
        argv += ["--dataset", args.dataset]
    argv += child_flags(features)
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


def _run_children(jobs: list[tuple], parallel: int,
                  may_replace_result: bool = True) -> list[dict]:
    """Each job is (pr_id, argv, out_dir, label). Returns whatever the children wrote.

    `may_replace_result` is about what a *failed* child means. For a run that produces
    the verdict, a child that writes nothing has produced nothing, and recording BROKEN
    is the honest answer. For a pass that only adds a field to a result already on disk
    -- `--mutate-saved` -- it is the opposite: the child failing says nothing about the
    verdict sitting in that file, and overwriting it destroys a real result.

    That is not hypothetical. Three instances whose images had no local archive tried to
    pull, the registry timed out, their children died before writing anything, and three
    genuine YES verdicts were replaced by BROKEN rows. They were recoverable only
    because the older file is kept as `result.stale.json`.
    """
    import subprocess
    from concurrent.futures import ThreadPoolExecutor      # threads only wait on procs

    env = dict(os.environ, **{CHILD_ENV_FLAG: "1"})
    labels = [f"{pid}{f' [{lab}]' if lab else ''}" for pid, _, _, lab in jobs]
    print(f"  {len(jobs)} job(s), {parallel} at a time. "
          f"Full output per job in its child.log.\n")

    live = sys.stdout.isatty()
    # Set by the first child that dies of an exhausted gateway budget. Every remaining
    # job would meet the same wall: the retry inside the SDK backs off for twenty minutes
    # first, so five instances took an hour and forty to all fail the same way. A budget
    # is terminal for the run, not for one instance.
    spent = threading.Event()
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
        if spent.is_set():
            out_dir.mkdir(parents=True, exist_ok=True)
            row = {"instance_id": pr_id, "f2p": "BROKEN", "label": label,
                   "why": "not started: the gateway budget was exhausted earlier in "
                          "this run. Top the key up and use --retry-broken."}
            rj = out_dir / "result.json"
            if rj.exists():             # an older verdict is kept, never overwritten
                rj.replace(out_dir / "result.stale.json")
            rj.write_text(json.dumps(row, indent=2))
            return row
        # A ceiling, not a schedule. Nothing here should take two hours -- the longest
        # real run was twenty minutes plus a pull -- but a child that wedges on a socket
        # used to hold the parent open indefinitely, and three of them once sat silent
        # for fifty-one minutes after a laptop sleep before being killed by hand.
        #
        # Six hours since 2026-09-30, above what the model-call retries can spend (60,
        # see `models.BUILTIN`). At two hours django-17029 rode out the proxy outage on
        # its retries, carried on working, and was killed by this ceiling instead -- the
        # retries only moved the failure.
        limit = float(os.getenv("F2P_CHILD_TIMEOUT") or 21600)
        # Stamped before launch so a result.json left by an *earlier* run is not read
        # back as this child's answer. One instance died when the docker socket vanished
        # mid-pull and the parent reported the previous day's row -- wrong cause, wrong
        # date -- because the file merely existed.
        started = time.time()
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
        # OpenRouter's own wording when the key's credit is gone. ten-arms-70-prs-take-two's first
        # pass met it and, not recognising it, started every remaining job anyway.
        if any(m in (proc.stdout + proc.stderr)
               for m in ("Budget has been exceeded", "requires more credits")):
            spent.set()
        rj = out_dir / "result.json"
        fresh = rj.exists() and rj.stat().st_mtime >= started
        if fresh:
            row = json.loads(rj.read_text())
        else:
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()
            why = (f"child exited {proc.returncode} without writing a result"
                   + (f": {tail[-1][:300]}" if tail else ""))
            row = {"instance_id": pr_id, "f2p": "BROKEN", "why": why}
            if may_replace_result:
                if rj.exists():         # keep the older verdict, but stop reporting it
                    rj.replace(out_dir / "result.stale.json")
                rj.write_text(json.dumps(row | {"label": label}, indent=2))
            else:
                # Reported to the caller, written nowhere. The file on disk is a result
                # this pass was only going to annotate.
                row = {"instance_id": pr_id, "failed": why}
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
