"""Download the SWE-bench rows the runs read into data/ (git-ignored).

    uv run --project openhands-f2p --with datasets python scripts/fetch_swebench.py          # both
    uv run --project openhands-f2p --with datasets python scripts/fetch_swebench.py verified # one

verified -> data/swebench_verified.json (500 rows): the default dataset of the agent.
full     -> data/swebench_full.json (2294 rows): the large-PR sets and the final experiment,
            run with F2P_DATASET=../data/swebench_full.json.
"""
import argparse
import json
from pathlib import Path

from datasets import load_dataset

SETS = {"verified": ("princeton-nlp/SWE-bench_Verified", "swebench_verified.json"),
        "full": ("princeton-nlp/SWE-bench", "swebench_full.json")}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("which", nargs="?", choices=(*SETS, "both"), default="both")
    p.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data"))
    a = p.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for name in (SETS if a.which == "both" else [a.which]):
        repo, file = SETS[name]
        rows = list(load_dataset(repo, split="test"))
        (out / file).write_text(json.dumps(rows))
        print(f"{out / file}: {len(rows)} rows")


if __name__ == "__main__":
    main()
