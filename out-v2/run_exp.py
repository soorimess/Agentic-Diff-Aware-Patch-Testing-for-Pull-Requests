"""Run experiments on the laptop's 36 local instances, one folder per experiment.

    cd openhands-f2p
    uv run python ../out-v2/run_exp.py --parallel 36 base
    uv run python ../out-v2/run_exp.py --parallel 36 base base-repeat      # noise floor
    uv run python ../out-v2/run_exp.py --parallel 36 \
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

`--max-iterations 125` for every run (since 2026-10-04; it was 100). The judge does not run
by default (user, 2026-10-04): runs are scored on fail-to-pass, coverage and mutation, and
the judge is added on request, afterwards, with `--judge` -- which grades the saved test of
every YES in the named experiments and writes `concept` (and `judge/completions/`) into
each result, without running the agent again. `--with-judge` judges inside the run instead.

`--retry-broken` reruns only jobs the model or the network never let finish: no result,
or BROKEN with an outside-failure reason (gateway credit or key limit, connection, a child
that died). A BROKEN the agent caused -- nothing collected, a pre-existing file edited --
is a result like NO and is not rerun.
"""
from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Set before the harness is imported: `prs.py` and `image_cache.py` read them at import.
os.environ.setdefault("F2P_PRS_FILE", str(ROOT / "evaluation" / "local-36-prs.json"))
os.environ.setdefault("F2P_IMAGE_CACHE", "image-cache" + os.pathsep + "image-cache-evaluation")
# The server pulls from Docker Hub (~85 MB/s for one stream; a 5.3 GB image in 64 s), and
# one pull at a time would leave the last of 36 jobs waiting half an hour. Six at once.
# Irrelevant on the laptop, where every image loads from the local cache.
os.environ.setdefault("F2P_PULL_CONCURRENCY", "6")
# Archive loads at once (2026-10-04): one at a time, a 36-job launch ramped up over half an
# hour. Six pigz loads keep the disk busy without starving the running containers.
os.environ.setdefault("F2P_LOAD_CONCURRENCY", "6")

from openhands_f2p import agent as A  # noqa: E402
from openhands_f2p import runs  # noqa: E402
from openhands_f2p.features import FEATURES, FeatureSet, flag  # noqa: E402
from openhands_f2p.parallel import _child_argv, _needs_retry, _run_children  # noqa: E402
from openhands_f2p.prs import PRS  # noqa: E402

MODEL = "openrouter/qwen/qwen3-coder-30b-a3b-instruct"
MUTANTS = "20"
# The action cap for every run (user, 2026-10-04: 125, up from 100).
MAX_ITERATIONS = "125"
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


def judge_saved(names: list[str], parallel: int, only: list[str] | None) -> int:
    """Add the judge to finished runs: every YES with a saved test and no judgement.

    Nothing else in a result changes. The judge reads the issue, the patch, the developer's
    test and the saved test -- no container -- so the calls run in threads. A failed call
    is written as `{"verdict": "error"}`, as inside a run, and is retried by running this
    again (an error does not count as a judgement).
    """
    from openhands_f2p import compare
    from openhands_f2p.checks import token_usage
    from openhands_f2p.dataset import load

    todo = []
    for name in names:
        root = HERE / name
        for d in sorted(p for p in root.iterdir() if (p / "result.json").exists()):
            if only and d.name not in only:
                continue
            r = json.loads((d / "result.json").read_text())
            judged = (r.get("concept") or {}).get("verdict") not in (None, "error")
            saved = next(d.glob("test_f2p_*.py"), None)
            if r.get("f2p") == "YES" and saved is not None and not judged:
                todo.append((name, d, saved))
    print(f"judging {len(todo)} saved test(s), {parallel} at a time")

    def one(job):
        name, d, saved = job
        rj = d / "result.json"
        try:
            concept = compare.compare(load(d.name), saved.read_text(), quiet=True,
                                      completions_dir=d / "judge" / "completions")
        except Exception as exc:                                  # noqa: BLE001
            concept = {"verdict": "error", "reasoning": str(exc)[:200]}
        r = json.loads(rj.read_text())
        r["concept"] = concept
        r["judge_usage"] = token_usage(d / "judge")
        rj.write_text(json.dumps(r, indent=2))
        return name, d.name, concept.get("verdict")

    with ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
        for name, iid, verdict in pool.map(one, todo):
            print(f"  {name:24s} {iid:34s} {verdict}")
    for name in names:
        runs.main(HERE / name)
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("specs", nargs="+", help="name or name=--flag,--flag")
    # 36 on the server (since 2026-10-04: 16 CPUs, 31 GB, 287 GB disk); the laptop ran 18.
    p.add_argument("--parallel", type=int, default=36)
    p.add_argument("--only", default="", help="comma-separated instance ids, for a smoke run")
    p.add_argument("--retry-broken", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--with-judge", action="store_true",
                   help="judge each YES inside the run (off by default)")
    p.add_argument("--judge", action="store_true",
                   help="do not run the agent: judge the saved test of every YES in the "
                        "named experiments that has no judgement yet")
    a = p.parse_args()
    if a.judge:
        return judge_saved([parse_spec(s)[0] for s in a.specs], a.parallel,
                           a.only.split(",") if a.only else None)

    if len(PRS) != 36 and not a.only:
        raise SystemExit(f"  expected the 36 local instances, got {len(PRS)}")
    prs = [pr for pr in PRS if not a.only or pr["id"] in a.only.split(",")]
    parser = A.build_parser()
    per_exp = {}
    for spec in a.specs:
        name, flags = parse_spec(spec)
        args = parser.parse_args(["all", "--mutants", MUTANTS, "--model", MODEL,
                                  "--max-iterations", MAX_ITERATIONS,
                                  *([] if a.with_judge else ["--no-compare"]), *flags])
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
