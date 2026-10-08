"""SWE-bench Verified: the dataset the harness was built on, read as it always was.

Its rows are already the standard shape, so this adapter only finds the dump and adds the
three fields every adapter adds. The images are published by SWE-bench and pulled.

Moved here from `dataset.py` (2026-10-08) when a second dataset arrived; the search order
and the error text are unchanged.
"""
from __future__ import annotations

import functools
import json
import os
from pathlib import Path

from openhands_f2p.layout import PROJECT_ROOT

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

IMAGE = "swebench/sweb.eval.x86_64.{tag}:latest"


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


class SweBench:
    name = "swebench"
    description = ("SWE-bench Verified (princeton-nlp/SWE-bench_Verified, 500 rows); "
                   "prepared images pulled from Docker Hub (swebench/sweb.eval.*)")

    def load(self, instance_id: str) -> dict:
        rows = _rows()
        if instance_id not in rows:
            raise SystemExit(f"{instance_id} is not in {dataset_path()}")
        return {**rows[instance_id], "dataset": self.name,
                "image": self.image_for(instance_id), "image_source": "pull"}

    def prs(self) -> list[dict] | None:
        return None             # the built-in twenty-six in prs.py, or F2P_PRS_FILE

    def image_for(self, instance_id: str) -> str:
        """swebench uses `_1776_` where the instance id has `__`."""
        return IMAGE.format(tag=instance_id.replace("__", "_1776_"))

    def owns_image(self, image: str) -> bool:
        return image.startswith("swebench/")

    def summary(self) -> dict:
        try:
            n = len(_rows())
            where = str(dataset_path())
        except SystemExit:
            n, where = 0, "not downloaded"
        return {"name": self.name, "description": self.description,
                "instances": n, "file": where, "images": "pulled"}


SOURCE = SweBench()
