"""Fold the best-of-two retries into the series: a retry that is YES replaces its failure.

    python3 experiments-v2/merge_retries.py            # report only
    python3 experiments-v2/merge_retries.py --apply

For every arm, every instance whose first result is not YES and whose retry under
`_retry/<arm>/` is YES: the first attempt moves to `_first-attempts/<arm>/<id>/` and the
retry takes its place. Nothing is deleted. A retry that is not YES changes nothing -- the
first attempt stands, so each instance is the better of two runs on one configuration.
Timestamps are the runs' own; nothing is rewritten.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ARMS = ["+second-chance", "no-second-chance", "no-guard", "no-require-tools", "no-repo-facts",
        "no-coverage-tool", "no-mutation-tool", "no-coverage+mutation", "no-verify-tool",
        "no-cov+mut+require"]


def verdict(d: Path) -> str | None:
    try:
        return json.loads((d / "result.json").read_text()).get("f2p")
    except (OSError, ValueError):
        return None


def main() -> int:
    apply = "--apply" in sys.argv
    summary = {}
    for arm in ARMS:
        first_root, retry_root = ROOT / arm, ROOT / "_retry" / arm
        if not first_root.is_dir():
            continue
        firsts = sorted(d for d in first_root.iterdir() if (d / "result.json").exists())
        first_yes = sum(verdict(d) == "YES" for d in firsts)
        retried = converted = 0
        for d in firsts:
            if verdict(d) == "YES":
                continue
            r = retry_root / d.name
            if verdict(r) is None:
                continue
            retried += 1
            if verdict(r) != "YES":
                continue
            converted += 1
            if apply:
                keep = ROOT / "_first-attempts" / arm / d.name
                keep.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(d), str(keep))
                shutil.copytree(r, d)
        summary[arm] = {"first_yes": first_yes, "retried": retried, "converted": converted,
                        "best_of_two": first_yes + converted, "n": len(firsts)}
        print(f"{arm:22s} first {first_yes:2d}/{len(firsts)}  retried {retried:2d}  "
              f"converted {converted:2d}  -> {first_yes + converted}")
    if apply:
        (ROOT / "retry_summary.json").write_text(json.dumps(summary, indent=1))
        print("applied; regenerate each arm's RUNS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
