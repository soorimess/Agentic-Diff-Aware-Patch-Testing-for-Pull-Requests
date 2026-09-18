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
# `out/` is a container of run folders, not a run folder. One run per subdirectory:
# `out/out_full_run/` is the twenty-six tuned-against instances, `out/out_compare_repo_search/`
# is an arm comparison, and a run with no `--out-root` lands in `out/default/` rather than
# scattering instance directories among them. A dozen sibling `out_*` folders at the project
# root is what this replaced.
OUT = PROJECT_ROOT / "out" / "default"
CACHE = PROJECT_ROOT / "cache" if (PROJECT_ROOT / "cache").exists() \
    else PROJECT_ROOT / ".cache"

_env = PROJECT_ROOT / ".env"
if _env.exists():
    load_dotenv(_env, override=False)
