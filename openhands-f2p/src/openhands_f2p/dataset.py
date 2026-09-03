"""Where the SWE-bench Verified rows come from, and how they are found.

Lifted out of `oracle.py` for two reasons. The first is a dependency direction that had
gone backwards: `agent.py` imported `load` from `oracle`, so running the agent pulled in
the oracle sweep and everything it imports, for one function that has nothing to do with
oracles.

The second is portability, and it was a real defect. The path was written relative to a
sibling directory outside this project -- it resolved only because both happened to sit
under one parent on the machine they were written on, so a clone of this repository alone
could not load a single instance. The search order below stays inside the project.
"""
from __future__ import annotations

import functools
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# In order of preference. `F2P_DATASET` overrides both.
CANDIDATES = (
    PROJECT_ROOT / "data" / "swebench_verified.json",
    PROJECT_ROOT / ".cache" / "swebench_verified.json",
)

HOW_TO_FETCH = """The dataset is not in the repository -- it is 8 MB of someone else's
data and it is a download, not a source file. Fetch it once:

    uv run python -c "from datasets import load_dataset; import json; \\
      rows = list(load_dataset('princeton-nlp/SWE-bench_Verified', split='test')); \\
      json.dump(rows, open('data/swebench_verified.json','w'))"

or point F2P_DATASET at a copy you already have."""


def dataset_path() -> Path:
    override = os.getenv("F2P_DATASET")
    if override:
        p = Path(override).expanduser()
        if not p.exists():
            raise SystemExit(f"F2P_DATASET={override} does not exist")
        return p
    for p in CANDIDATES:
        if p.exists():
            return p
    looked = "\n".join(f"  {p}" for p in CANDIDATES)
    raise SystemExit(f"no SWE-bench Verified dataset found. Looked in:\n{looked}\n\n"
                     f"{HOW_TO_FETCH}")


@functools.lru_cache(maxsize=1)
def _rows() -> dict[str, dict]:
    """Every instance, keyed by id.

    Cached: the file is 8 MB of JSON and `load` used to re-read and re-parse all of it
    for each instance, which is half a second per PR spent finding one dictionary.
    """
    return {r["instance_id"]: r
            for r in json.loads(dataset_path().read_text())}


def load(instance_id: str) -> dict:
    rows = _rows()
    if instance_id not in rows:
        raise SystemExit(f"{instance_id} is not in {dataset_path()}")
    return rows[instance_id]
