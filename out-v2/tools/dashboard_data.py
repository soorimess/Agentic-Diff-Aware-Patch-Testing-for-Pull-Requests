"""Experiment documents for the comparison page (Artifact "F2P Flag Ablations").

    python3 out-v2/tools/dashboard_data.py [arm ...]

The page shows, per PR, base's best run and every other arm's worst (user, 2026-10-07):
the runs `tools/pick_extremes.py` links into `extreme-base-best/` and
`extreme-<arm>-worst/`. Run that first. Each document is filed under the arm's own name
(`out-v2/dashboard/<arm>.json`): its flags (from each run's `features.on`) and, per PR,
verdict, first-attempt verdict, coverage lines, mutants, actions, cost. Upload with
`ArtifactData` `set` (collection `experiments`, doc id = arm, `file_path`); the page
computes every comparison itself, so a new arm is one more document.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # out-v2/
OUT = HERE / "dashboard"

# Shown order and names, as in the plan.
KNOWN = {
    "base": ("Base", "arm", 1),
    "no-second-chance": ("No second chance", "arm", 2),
    "no-require-tools": ("No require-tools", "arm", 3),
    "no-second-chance-no-require-tools": ("No second chance, no require-tools", "arm", 4),
    "no-guard": ("No guard", "arm", 5),
    "require-tools-with-score": ("Require-tools with scores", "arm", 6),
    "no-verify": ("No verify", "arm", 7),
    "no-coverage": ("No coverage tool", "arm", 8),
    "no-mutation": ("No mutation tool", "arm", 9),
    "no-coverage-no-mutation": ("No coverage, no mutation", "arm", 10),
    "no-coverage-no-mutation-no-require-tools": ("No coverage, no mutation, no require-tools", "arm", 11),
}


def source(arm: str) -> str:
    """The folder of picked runs this arm's document is built from."""
    return "extreme-base-best" if arm == "base" else f"extreme-{arm}-worst"


FLAGS = ["verify-tool", "coverage-tool", "mutation-tool", "guard", "require-tools",
         "require-tools-with-score-report", "second-chance"]


def run_row(r: dict) -> dict:
    c = r.get("changed_line_coverage") or {}
    m = r.get("mutation") or {}
    sc = r.get("second_chance") or {}
    yes = r.get("f2p") == "YES"
    row = {"v": r.get("f2p") or "?", "first": sc.get("first_verdict") or r.get("f2p") or "?",
           "a": r.get("actions") or 0,
           "c": round(((r.get("usage") or {}).get("cost_usd") or 0), 4),
           "w": (r.get("why") or "")[:110]}
    if yes and c.get("measured"):
        row["ch"], row["ct"] = c["covered"], c["executable_changed_lines"]
    k = (m.get("agent") or {}).get("killed")
    if yes and m.get("measured") and m.get("total") and k is not None:
        row["mk"], row["mt"] = k, m["total"]
    return row


def build(arm: str) -> dict:
    root = HERE / source(arm)
    results = {p.parent.name: json.loads(p.read_text())
               for p in sorted(root.glob("*/result.json"))}
    on: set[str] = set()
    temps = set()
    for r in results.values():
        on |= set((r.get("features") or {}).get("on") or [])
        temps.add(str(r.get("temperature")))
    label, kind, order = KNOWN.get(arm, (arm, "arm", 50))
    return {"label": label, "kind": kind, "order": order,
            "flags": {f: f in on for f in FLAGS},
            "temperature": ",".join(sorted(temps)),
            "prs": len(results),
            "runs": {i: run_row(r) for i, r in results.items()}}


def main(folders: list[str]) -> None:
    OUT.mkdir(exist_ok=True)
    for f in folders or [k for k in KNOWN if (HERE / source(k)).is_dir()]:
        doc = build(f)
        (OUT / f"{f}.json").write_text(json.dumps(doc, indent=1))
        yes = sum(r["v"] == "YES" for r in doc["runs"].values())
        print(f"{f}: {yes}/{doc['prs']} YES -> dashboard/{f}.json")


if __name__ == "__main__":
    main(sys.argv[1:])
