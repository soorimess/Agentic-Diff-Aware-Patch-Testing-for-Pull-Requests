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
import sys

from openhands_f2p import sources


def _ids(src, which: str) -> list[str]:
    if which in ("", "all"):
        return [r["instance_id"] for r in json.loads(src.INSTANCES.read_text())] \
            if hasattr(src, "INSTANCES") else []
    return [w.strip() for w in which.split(",") if w.strip()]


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("action", choices=("list", "info", "prepare", "build", "validate"))
    p.add_argument("dataset", nargs="?", default="")
    p.add_argument("which", nargs="?", default="",
                   help="comma-separated instance ids, or 'all'")
    p.add_argument("--rebuild", action="store_true",
                   help="build: replace the image and its archive even if they exist")
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
        ids = None if a.which in ("", "all") else _ids(mod, a.which)
        rows = mod.prepare(ids)
        counts: dict[str, int] = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print(f"\n  {len(rows)} row(s): " + ", ".join(f"{k} {v}" for k, v in counts.items())
              + f"\n  rows: {mod.INSTANCES}")
        return 0
    ids = _ids(mod, a.which)
    if not ids:
        raise SystemExit(f"  {a.action} needs instance ids (or 'all')")
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
