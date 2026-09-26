"""Run several arms of the ten-arm series at once, instance-major, as one job pool.

    cd openhands-f2p
    F2P_PRS_FILE=... F2P_NO_ARCHIVE=1 F2P_KEEP_IMAGES=1 \\
      uv run python ../experiments-v2/run_arms.py --parallel 70 +second-chance no-second-chance ...

Why not one `agent all --parallel N` per arm: each of those walks the instance list on its
own, so N workers per arm hold N different images, and an instance image is ~5 GB on the
server. Here every (arm, instance) job goes into one list ordered instance by instance --
all arms of instance 1, then all arms of instance 2 -- and `parallel._run_children` takes
them in that order. With ten arms, 70 workers hold about seven instances, so about seven
images, and an image is used by every arm while it is loaded.

Each child is launched exactly as `agent all` would launch it: the argv comes from
`parallel._child_argv` over arguments parsed by the agent's own parser, and the job runner,
`child.log`, BROKEN handling and budget stop are the harness's. Afterwards each arm gets its
`agent_summary.json` and `RUNS.md` the way `agent all` writes them.

`--retry-broken` reruns only jobs the model or the network never let finish: no result,
or BROKEN with an outside-failure reason (gateway credit or key limit, connection, a child
that died). A BROKEN the agent caused -- nothing collected, a pre-existing file edited --
is a result like NO and is left for the best-of-two pass, so it gets no extra attempt.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

from openhands_f2p import agent as A
from openhands_f2p import runs
from openhands_f2p.features import FeatureSet
from openhands_f2p.parallel import _child_argv, _needs_retry, _run_children
from openhands_f2p.prs import PRS

MODEL = "openrouter/qwen/qwen3-coder-30b-a3b-instruct"
# The series' flags, arm by arm (experiments/comparison/data.py ARMS). Every arm but
# no-second-chance carries --second-chance; --mutants 10 everywhere.
ARMS = {
    "+second-chance":       ["--second-chance"],
    "no-second-chance":     [],
    "no-guard":             ["--second-chance", "--no-guard"],
    "no-require-tools":     ["--second-chance", "--no-require-tools"],
    "no-repo-facts":        ["--second-chance", "--no-repo-facts"],
    "no-coverage-tool":     ["--second-chance", "--no-coverage-tool"],
    "no-mutation-tool":     ["--second-chance", "--no-mutation-tool"],
    "no-coverage+mutation": ["--second-chance", "--no-coverage-tool", "--no-mutation-tool"],
    "no-verify-tool":       ["--second-chance", "--no-verify-tool"],
    "no-cov+mut+require":   ["--second-chance", "--no-coverage-tool", "--no-mutation-tool",
                             "--no-require-tools"],
}


# Reasons the harness writes when the run never finished for reasons outside it.
OUTSIDE = ("cut off after", "the agent run failed before a test was written",
           "not started: the gateway budget", "child exited", "without writing a result")


def _outside_broken(d: Path) -> bool:
    if _needs_retry(d) is False:
        return False
    f = d / "result.json"
    if not f.exists():
        return True
    try:
        why = json.loads(f.read_text()).get("why") or ""
    except (OSError, ValueError):
        return True
    return any(k in why for k in OUTSIDE)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arms", nargs="+", choices=list(ARMS))
    p.add_argument("--out", default=str(Path(__file__).resolve().parent),
                   help="series root; each arm writes to <out>/<arm>")
    p.add_argument("--parallel", type=int, required=True)
    p.add_argument("--retry-broken", action="store_true")
    p.add_argument("--failures-of", default=None,
                   help="best-of-two retry pass: only (arm, instance) whose result under "
                        "<this root>/<arm> is not YES; results go to --out")
    p.add_argument("--dry-run", action="store_true",
                   help="print the job list and one argv per arm; start nothing")
    a = p.parse_args()

    if not os.getenv("F2P_PRS_FILE"):
        raise SystemExit("F2P_PRS_FILE is not set -- the default list is the 26-instance "
                         "set, not the series corpus")
    out = Path(a.out).resolve()
    parser = A.build_parser()
    per_arm = {}
    for arm in a.arms:
        args = parser.parse_args(["all", "--mutants", "10", "--model", MODEL, *ARMS[arm]])
        per_arm[arm] = (args, FeatureSet.from_args(args))

    jobs = []
    for pr in PRS:                                   # instance-major
        for arm in a.arms:
            args, features = per_arm[arm]
            d = out / arm / pr["id"]
            if a.retry_broken and not _outside_broken(d):
                continue
            if a.failures_of:
                first = Path(a.failures_of) / arm / pr["id"] / "result.json"
                if not first.exists() or json.loads(first.read_text()).get("f2p") == "YES":
                    continue
            jobs.append((pr["id"], _child_argv(pr["id"], args, features, d, ""), d, arm))
    print(f"{len(jobs)} jobs over {len(a.arms)} arm(s) x {len(PRS)} instances, "
          f"{a.parallel} at a time")
    for arm in a.arms:
        argv = next((j[1] for j in jobs if j[3] == arm), None)
        if argv:
            print(f"  {arm:22s} {' '.join(argv[3:])}")
    if a.dry_run or not jobs:
        return 0

    for refusal in (A.E.daemon_refusal(), A.llm_config.gateway_refusal(MODEL)):
        if refusal:
            raise SystemExit(f"  {refusal}")
    A.E.reap_orphans(quiet=False)
    t0 = time.time()
    rows = _run_children(jobs, a.parallel)
    print(f"\nfinished {len(rows)} jobs in {(time.time() - t0) / 3600:.1f} h")

    for arm in a.arms:
        root = out / arm
        mine = [r for r, j in zip(rows, jobs, strict=True) if j[3] == arm]
        yes = sum(r.get("f2p") == "YES" for r in mine)
        print(f"  {arm:22s} {yes}/{len(mine)} YES this pass")
        root.mkdir(parents=True, exist_ok=True)
        A._write_summary(root / "agent_summary.json", mine)
        runs.main(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
