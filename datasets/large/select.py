"""Pick the two large-PR sets (user, 2026-10-14): 35 SWE-bench and 35 ChaCo pull requests.

    python3 datasets/large/select.py <swebench_full.json>

"Large" = code lines the patch adds to non-test Python source (blank and comment lines not
counted), at least 50. Python only: a patch touching C, C++, Cython or Rust source is out.
Repos as varied as the pool allows. Writes swebench-35.json and chaco-35.json (run lists,
F2P_PRS_FILE format) and sizes.json beside this file.
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
MIN_LINES = 50
MAX_PATCH_CHARS = 60000            # the prompt shows up to 60k of the diff unclipped
SKIP_SUFFIX = (".py", ".rst", ".md", ".txt", ".yaml", ".yml", ".toml", ".cfg", ".ini",
               ".build", ".json", ".in")


def is_test(p):
    return bool(re.search(r"(^|/)(tests?|testing)(/|$)|(^|/)test_[^/]*\.py$|_tests?\.py$"
                          r"|conftest\.py$", p))


def size(patch):
    added = 0
    nonpy = []
    f = None
    for ln in patch.splitlines():
        if ln.startswith("diff --git "):
            path = ln.split(" b/", 1)[1]
            if (not path.endswith(SKIP_SUFFIX)
                    and not path.startswith(("doc", "releasenotes", ".github"))):
                nonpy.append(path)
            f = path if (path.endswith(".py") and not is_test(path)
                         and not path.startswith(("doc", "benchmarks/", "asv_bench/"))) else None
            continue
        if not f or ln.startswith(("+++", "---")):
            continue
        body = ln[1:].strip()
        if body and not body.startswith("#") and ln.startswith("+"):
            added += 1
    return added, nonpy


# ---- SWE-bench: the full test split; Verified first, then a seeded draw, per repo.
QUOTA = {"mwaskom/seaborn": 1, "pallets/flask": 1, "psf/requests": 2, "pylint-dev/pylint": 3,
         "pytest-dev/pytest": 3, "astropy/astropy": 3, "matplotlib/matplotlib": 3,
         "sphinx-doc/sphinx": 3, "pydata/xarray": 4, "django/django": 4,
         "scikit-learn/scikit-learn": 4, "sympy/sympy": 4}
# Replacements after the oracle check found the gold test does not flip here.
SWE_DROPPED: dict[str, str] = {}


def swebench(full_path):
    rows = json.loads(Path(full_path).read_text())
    verified = {r["instance_id"] for r in json.loads((ROOT / "data/swebench_verified.json").read_text())}
    rng = random.Random(14)
    picked, sizes = [], {}
    for repo, n in QUOTA.items():
        pool = []
        for r in rows:
            if r["repo"] != repo or r["instance_id"] in SWE_DROPPED:
                continue
            a, nonpy = size(r["patch"])
            if a >= MIN_LINES and not nonpy and len(r["patch"]) <= MAX_PATCH_CHARS:
                pool.append((r["instance_id"] in verified, rng.random(), r["instance_id"], a))
        pool.sort(key=lambda t: (not t[0], t[1]))
        for v, _, iid, a in pool[:n]:
            picked.append({"id": iid, "tier": 0,
                           "note": f"large set, {repo}, {a} added code lines"
                                   + (", Verified" if v else "")})
            sizes[iid] = a
    return picked, sizes


# ---- ChaCo: its 145-PR list; every Python-only PR of 50+ lines but those left out below.
CHACO_OUT = {
    "scipy__scipy-21485": "not behavioural: refactor into `_bary_rational`",
    "pandas-dev__pandas-59555": "refactor that de-duplicates methods; no developer test",
    "pandas-dev__pandas-58792": "refactor that breaks up a function; no developer test",
    "scipy__scipy-23028": "maintenance: a module moved to solve a circular import",
    "Qiskit__qiskit-13343": "speed-up; its only observable change is `__slots__`",
}


def chaco():
    rows = json.loads((ROOT / "datasets/chaco/instances.json").read_text())
    picked, sizes = [], {}
    for r in rows:
        a, nonpy = size(r["patch"])
        if a >= MIN_LINES and not nonpy and r["instance_id"] not in CHACO_OUT:
            picked.append({"id": r["instance_id"], "tier": 0,
                           "note": f"large set, {r['repo']}, {a} added code lines"})
            sizes[r["instance_id"]] = a
    picked.sort(key=lambda p: (p["id"].split("__")[0].lower(), -sizes[p["id"]]))
    return picked, sizes


if __name__ == "__main__":
    swe, swe_sizes = swebench(sys.argv[1])
    ch, ch_sizes = chaco()
    (HERE / "swebench-35.json").write_text(json.dumps(swe, indent=1) + "\n")
    (HERE / "chaco-35.json").write_text(json.dumps(ch, indent=1) + "\n")
    (HERE / "sizes.json").write_text(json.dumps({"swebench": swe_sizes, "chaco": ch_sizes,
                                                 "chaco_left_out": CHACO_OUT,
                                                 "swebench_dropped": SWE_DROPPED}, indent=1) + "\n")
    print(f"swebench {len(swe)}  chaco {len(ch)}")
