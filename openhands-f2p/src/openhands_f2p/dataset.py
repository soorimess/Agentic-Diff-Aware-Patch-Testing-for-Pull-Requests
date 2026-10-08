"""One instance, from whichever dataset this run is over.

`load(instance_id)` is what the agent, the oracle and the mutation sweep call. It used to
read the SWE-bench Verified dump directly; since 2026-10-08 it asks the active dataset
(`--dataset`, `openhands_f2p.sources`), and the SWE-bench file lookup lives in
`sources/swebench.py` with its search order and error text unchanged.
"""
from __future__ import annotations

from openhands_f2p.sources import load
from openhands_f2p.sources.swebench import CANDIDATES, HOW_TO_FETCH, dataset_path

__all__ = ["load", "dataset_path", "CANDIDATES", "HOW_TO_FETCH"]
