"""Where the project is on disk, and the environment it runs with.

Five modules had each worked out the repository root for themselves with the same
`Path(__file__).resolve().parents[3]`, which is four copies of one fact and four places to
be wrong if the package ever moves. It lives here once.

Importing this loads `.env`, without overriding anything already set in the environment --
so a variable given on the command line still wins.
"""
from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

# src/openhands_f2p/layout.py -> src/openhands_f2p -> src -> openhands-f2p -> the root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
# Results live per dataset (2026-10-09): everything run on SWE-bench under
# `swe-bench-outs/` (out/, out-v2/, experiments*/, evaluation/), and a dataset added later
# under `<dataset>-outs/` -- `chaco-outs/`. Inside, `out/` is a container of run folders,
# not a run folder: one run per subdirectory, and a SWE-bench run with no `--out-root`
# lands in `swe-bench-outs/out/default/` rather than scattering instance directories among
# them.
SWEBENCH_OUTS = PROJECT_ROOT / "swe-bench-outs"
OUT = SWEBENCH_OUTS / "out" / "default"


def outs_for(dataset: str) -> Path:
    """Where a dataset's runs go: `swe-bench-outs/` or `<dataset>-outs/`."""
    return SWEBENCH_OUTS if dataset == "swebench" else PROJECT_ROOT / f"{dataset}-outs"


def default_out(dataset: str) -> Path:
    """Where a run with no `--out-root` writes."""
    return OUT if dataset == "swebench" else outs_for(dataset) / "default"
CACHE = PROJECT_ROOT / "cache" if (PROJECT_ROOT / "cache").exists() \
    else PROJECT_ROOT / ".cache"

_env = PROJECT_ROOT / ".env"
if _env.exists():
    load_dotenv(_env, override=False)
