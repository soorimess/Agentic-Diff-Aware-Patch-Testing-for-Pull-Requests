"""The datasets, and getting one ready to run.

    uv run python -m openhands_f2p.sources list
    uv run python -m openhands_f2p.sources info chaco
    uv run python -m openhands_f2p.sources prepare chaco [id,id,... | all]
    uv run python -m openhands_f2p.sources build chaco id[,id...]
    uv run python -m openhands_f2p.sources validate chaco id[,id...]

`prepare` makes the standard rows (no Docker), `build` makes the images, `validate` runs
the developer's tests in them to derive FAIL_TO_PASS and marks a row runnable when the
oracle reproduces it. A run then names the dataset:

    uv run python -m openhands_f2p.agent --dataset chaco <id> --model ...
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys

from openhands_f2p import sources


def _ids(mod, which: str, buildable: bool = False) -> list[str]:
    """Instance ids from `which`: ids, a list name of the dataset (`ablation`), or `all`
    (every prepared row). `buildable` keeps only rows that have an image to build."""
    rows = {r["instance_id"]: r for r in json.loads(mod.INSTANCES.read_text())} \
        if mod.INSTANCES.exists() else {}
    out: list[str] = []
    for w in (x.strip() for x in (which or "all").split(",") if x.strip()):
        if w == "all":
            out += list(rows)
        elif w in getattr(mod, "LISTS", {}):
            out += [mod.instance_id(r, n) for r, n in mod.benchmark(w)]
        else:
            out.append(w)
    out = list(dict.fromkeys(out))
    if buildable:
        out = [i for i in out if rows.get(i, {}).get("status", "unsupported") != "unsupported"]
    return out


def _fan_out(action: str, dataset: str, ids: list[str], parallel: int,
             extra: list[str]) -> int:
    """One process per instance, `parallel` at a time; each one's output in its own log
    under `.cache/builds/<action>-<id>.log`. Processes, not threads: `Sandbox` and the
    image claims are per process."""
    from concurrent.futures import ThreadPoolExecutor
    from openhands_f2p.image_build import BUILDS
    BUILDS.mkdir(parents=True, exist_ok=True)

    def one(iid: str) -> tuple[str, int]:
        log = BUILDS / f"{action}-{iid}.log"
        with log.open("w") as fh:
            rc = subprocess.run([sys.executable, "-m", "openhands_f2p.sources", action,
                                 dataset, iid, *extra], stdout=fh,
                                stderr=subprocess.STDOUT).returncode
        tail = log.read_text(errors="replace").strip().splitlines()[-1:] or [""]
        print(f"  {action:8s} {iid:32s} exit {rc}  {tail[0][:110]}", flush=True)
        return iid, rc

    with ThreadPoolExecutor(max_workers=max(1, parallel)) as pool:
        results = list(pool.map(one, ids))
    bad = [i for i, rc in results if rc]
    print(f"\n  {action}: {len(ids) - len(bad)}/{len(ids)} ok"
          + (f"; failed: {', '.join(bad)}" if bad else ""))
    return 1 if bad else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=("list", "info", "prepare", "build", "validate"))
    p.add_argument("dataset", nargs="?", default="")
    p.add_argument("which", nargs="?", default="",
                   help="comma-separated instance ids, or 'all'")
    p.add_argument("--rebuild", action="store_true",
                   help="build: replace the image and its archive even if they exist")
    p.add_argument("--parallel", type=int, default=1,
                   help="build/validate: this many instances at once, a process each")
    a = p.parse_args()

    if a.action == "list":
        active = sources.active_name()
        for name in sources.names():
            s = sources.get(name).summary()
            mark = "*" if name == active else " "
            extra = (f"prepared {s['prepared']}, " + ", ".join(
                f"{k} {v}" for k, v in sorted(s["status"].items()))
                if "prepared" in s else s.get("file", ""))
            print(f" {mark} {name:9s} {s['instances']:4d} instances  images {s['images']:6s}"
                  f"  {extra}")
        print(f"\n  * = active ({sources.DATASET_ENV}, or --dataset on a run)")
        return 0

    if not a.dataset:
        raise SystemExit(f"  {a.action} needs a dataset: {', '.join(sources.names())}")
    src = sources.select(a.dataset)
    mod = sys.modules[type(src).__module__]

    if a.action == "info":
        s = src.summary()
        print(json.dumps(s, indent=2))
        if hasattr(mod, "INSTANCES") and mod.INSTANCES.exists():
            for r in json.loads(mod.INSTANCES.read_text()):
                f2p = len(json.loads(r.get("FAIL_TO_PASS") or "[]"))
                print(f"  {r.get('status', '?'):<16} {r['instance_id']:32s} f2p={f2p:<3d} "
                      f"{(r.get('why') or '')[:80]}")
        return 0

    if not hasattr(src, "recipe"):
        raise SystemExit(f"  {a.dataset} has nothing to {a.action}: its rows and images "
                         f"come ready-made")
    if a.action == "prepare":
        ids = None if a.which in ("", "all") else \
            [w.strip() for w in a.which.split(",") if w.strip()]
        rows = mod.prepare(ids)
        counts: dict[str, int] = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print(f"\n  {len(rows)} row(s): " + ", ".join(f"{k} {v}" for k, v in counts.items())
              + f"\n  rows: {mod.INSTANCES}")
        return 0
    ids = _ids(mod, a.which, buildable=True)
    if not ids:
        raise SystemExit(f"  {a.action}: nothing to do for {a.which!r}")
    if len(ids) > 1 and a.parallel > 1:
        return _fan_out(a.action, a.dataset, ids, a.parallel,
                        ["--rebuild"] if a.rebuild else [])
    if a.action == "build":
        from openhands_f2p import image_build
        from openhands_f2p import image_cache
        for iid in ids:
            image = src.image_for(iid)
            if a.rebuild:
                image_cache.archive_for(image).unlink(missing_ok=True)
            image_build.build(image, force=a.rebuild)
        return 0
    bad = 0
    for iid in ids:
        bad += mod.validate(iid).get("status") != "runnable"
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
