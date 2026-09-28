"""Run experiments on the laptop's 36 local instances, one folder per experiment.

    cd openhands-f2p
    uv run python ../out-v2/run_exp.py --parallel 18 base
    uv run python ../out-v2/run_exp.py --parallel 18 base base-repeat      # noise floor
    uv run python ../out-v2/run_exp.py --parallel 18 \
        no-mutation=--add-verify-tool,--add-coverage-tool,--add-guard,--add-require-tools,--add-second-chance

Each spec is `name` or `name=--flag,--flag`. A bare name runs the base configuration --
every input shown, every add-on added except variants (`BASE_FLAGS`); a name with flags runs exactly those
flags and nothing implied, so what an experiment has is written in its command. The folder
`out-v2/<name>/` gets one directory per instance, `agent_summary.json` and `RUNS.md`,
exactly as `agent all` writes them. The name says what changed in the system or the
configuration for that experiment.

Everything else is fixed here so experiments differ only by what their names say: the
36 instances cached locally (`evaluation/local-36-prs.json` -- 26 development, 10
evaluation), both image caches, the model, `--mutants 20`, the default temperature.
Several specs run as one job pool, instance-major, so an image is loaded once for every
experiment that needs it.

`--retry-broken` reruns only jobs the model or the network never let finish: no result,
or BROKEN with an outside-failure reason (gateway credit or key limit, connection, a child
that died). A BROKEN the agent caused -- nothing collected, a pre-existing file edited --
is a result like NO and is not rerun.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Set before the harness is imported: `prs.py` and `image_cache.py` read them at import.
os.environ.setdefault("F2P_PRS_FILE", str(ROOT / "evaluation" / "local-36-prs.json"))
os.environ.setdefault("F2P_IMAGE_CACHE", "image-cache" + os.pathsep + "image-cache-evaluation")

from openhands_f2p import agent as A  # noqa: E402
from openhands_f2p import runs  # noqa: E402
from openhands_f2p.features import FEATURES, FeatureSet, flag  # noqa: E402
from openhands_f2p.parallel import _child_argv, _needs_retry, _run_children  # noqa: E402
from openhands_f2p.prs import PRS  # noqa: E402

MODEL = "openrouter/qwen/qwen3-coder-30b-a3b-instruct"
MUTANTS = "20"
# The base configuration: every add-on added, except variants of another add-on
# (`require-tools-with-score-report` is require-tools with scores, an experiment of its
# own). Read off the registry, so an add-on added later is in base without anyone
# editing this list.
BASE_FLAGS = [flag(f.name) for f in FEATURES if f.added and not f.implies]

# Reasons the harness writes when a run never finished for reasons outside it.
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


def parse_spec(spec: str) -> tuple[str, list[str]]:
    name, eq, flags = spec.partition("=")
    if not name or "/" in name:
        raise SystemExit(f"  bad experiment name {name!r}")
    return name, ([f for f in flags.split(",") if f] if eq else list(BASE_FLAGS))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("specs", nargs="+", help="name or name=--flag,--flag")
    p.add_argument("--parallel", type=int, default=18)
    p.add_argument("--only", default="", help="comma-separated instance ids, for a smoke run")
    p.add_argument("--retry-broken", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()

    if len(PRS) != 36 and not a.only:
        raise SystemExit(f"  expected the 36 local instances, got {len(PRS)}")
    prs = [pr for pr in PRS if not a.only or pr["id"] in a.only.split(",")]
    parser = A.build_parser()
    per_exp = {}
    for spec in a.specs:
        name, flags = parse_spec(spec)
        args = parser.parse_args(["all", "--mutants", MUTANTS, "--model", MODEL, *flags])
        per_exp[name] = (args, FeatureSet.from_args(args))

    jobs = []
    for pr in prs:                                   # instance-major
        for name, (args, features) in per_exp.items():
            d = HERE / name / pr["id"]
            if a.retry_broken and not _outside_broken(d):
                continue
            jobs.append((pr["id"], _child_argv(pr["id"], args, features, d, ""), d, name))
    print(f"{len(jobs)} jobs over {len(per_exp)} experiment(s) x {len(prs)} instances, "
          f"{a.parallel} at a time")
    for name, (_, features) in per_exp.items():
        argv = next((j[1] for j in jobs if j[3] == name), None)
        print(f"  {name:24s} {features.slug():30s} {' '.join(argv[3:]) if argv else ''}")
    if a.dry_run or not jobs:
        return 0

    for refusal in (A.E.daemon_refusal(), A.llm_config.gateway_refusal(MODEL)):
        if refusal:
            raise SystemExit(f"  {refusal}")
    A.E.reap_orphans(quiet=False)
    t0 = time.time()
    rows = _run_children(jobs, a.parallel)
    print(f"\nfinished {len(rows)} jobs in {(time.time() - t0) / 3600:.1f} h")
    for name in per_exp:
        root = HERE / name
        mine = [r for r, j in zip(rows, jobs, strict=True) if j[3] == name]
        print(f"  {name:24s} {sum(r.get('f2p') == 'YES' for r in mine)}/{len(mine)} YES")
        root.mkdir(parents=True, exist_ok=True)
        A._write_summary(root / "agent_summary.json", mine)
        runs.main(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
