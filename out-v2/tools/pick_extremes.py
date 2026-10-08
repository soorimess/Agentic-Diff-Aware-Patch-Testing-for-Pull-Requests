"""Best base against worst arms: the largest effect each flag can show (user, 2026-10-06).

    python3 out-v2/tools/pick_extremes.py

For every PR, picks one run from all runs of the *same system and configuration* -- the
best for base, the worst for an arm -- and links it (relative symlink) into
`out-v2/extreme-<name>/<pr>`, with a PICKED.md saying where each run came from.

Best:  YES over NO, then higher coverage, then more mutants caught.
Worst: NO over YES, then lower coverage, then fewer mutants caught.
Ties keep the official run (listed first), so as little is picked as possible.

Candidate pools are the runs made on the current system with that configuration: the
official folder and the 8-PR rerun (`rerun8-*`).
Excluded: runs replaced because a fix changed what the agent saw (`*-second-runs/`,
`fix-check*/`), and `base-temp0` (another temperature).
"""
from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent          # out-v2/

# The astropy-13398 randomness runs left the pools on 2026-10-06: they ran before the
# `252dd3aa` text fixes (astropy's header hid the failure reason), so they are another
# system now. `rerun8-*` saw none of the fixed texts (`replay_texts.py`) and stays.
# Base takes its best run per PR; every other arm of the plan that has run takes its worst
# (user, 2026-10-06/07). An arm with a single run per PR keeps it.
ARMS = ["no-second-chance", "no-require-tools", "no-second-chance-no-require-tools", "no-guard",
        "require-tools-with-score", "no-verify", "no-coverage", "no-mutation",
        "no-coverage-no-mutation", "no-coverage-no-mutation-no-require-tools"]
POOLS = {"base-best": ("best", ["base", "rerun8-base"])}
for _arm in ARMS:
    if (HERE / _arm).is_dir():
        POOLS[f"{_arm}-worst"] = ("worst", [_arm] + ([f"rerun8-{_arm}"]
                                                   if (HERE / f"rerun8-{_arm}").is_dir() else []))


def score(r: dict) -> tuple:
    c = r.get("changed_line_coverage") or {}
    m = r.get("mutation") or {}
    yes = r.get("f2p") == "YES"
    cov = c.get("percent") if yes and c.get("measured") else None
    k, t = (m.get("agent") or {}).get("killed"), m.get("total")
    mut = k / t if yes and m.get("measured") and t and k is not None else None
    # Unmeasured counts as neither good nor bad: it only breaks ties among measured ones.
    return (yes, -1 if cov is None else cov, -1 if mut is None else mut)


def label(r: dict) -> str:
    c = r.get("changed_line_coverage") or {}
    m = r.get("mutation") or {}
    s = r.get("f2p", "?")
    if (r.get("second_chance") or {}).get("first_verdict") and s == "YES":
        s += " (rescued)"
    if s.startswith("YES"):
        s += f", coverage {c['percent']:.0f}%" if c.get("measured") else ", coverage --"
        if m.get("measured") and m.get("total"):
            s += f", mutants {(m.get('agent') or {}).get('killed')}/{m['total']}"
    return s


def main() -> None:
    ids = sorted(p.parent.name for p in (HERE / "base").glob("*/result.json"))
    for name, (mode, pool) in POOLS.items():
        dest = HERE / f"extreme-{name}"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir()
        lines = [f"# Picked runs: {name}", "",
                 f"Per PR, the **{mode}** run among every run of the same system and "
                 f"configuration (user, 2026-10-06), to show the largest effect a flag can make "
                 f"-- base's best against an arm's worst. Not a fair one-sample comparison.", "",
                 f"Pool, in order (ties keep the first): {', '.join(f'`{p}`' for p in pool)}. "
                 "Best: YES over NO, then higher coverage, then more mutants; worst the reverse.",
                 "Each PR folder here is a link to the run it names.", "",
                 "| PR | picked | from | runs considered |", "|---|---|---|---|"]
        changed = 0
        for i in ids:
            cands = [(p, json.loads((HERE / p / i / "result.json").read_text()))
                     for p in pool if (HERE / p / i / "result.json").is_file()]
            pick = cands[0]
            for c in cands[1:]:
                better = score(c[1]) > score(pick[1])
                if (better if mode == "best" else score(c[1]) < score(pick[1])):
                    pick = c
            changed += pick[0] != pool[0]
            os.symlink(os.path.relpath(HERE / pick[0] / i, dest), dest / i)
            seen = "; ".join(f"`{p}`: {label(r)}" for p, r in cands)
            lines.append(f"| `{i}` | {label(pick[1])} | `{pick[0]}` | {seen} |")
        lines += ["", f"{changed} of {len(ids)} PRs take a run other than the official one."]
        (dest / "PICKED.md").write_text("\n".join(lines) + "\n")
        print(f"{name}: {changed} picked away from `{pool[0]}`")


if __name__ == "__main__":
    main()
