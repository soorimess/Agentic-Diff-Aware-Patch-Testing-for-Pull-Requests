"""Pick the two large-PR sets (user, 2026-10-14): 35 SWE-bench and 35 ChaCo pull requests.

    python3 datasets/large/select.py <swebench_full.json>

"Large" = at least 50 executable changed lines: the library Python lines the patch adds
that start an executable statement, the figure every run's coverage is measured over
(user, 2026-10-14; measured beforehand by measure.py into executable.json). Candidates
for measuring: 50+ added code lines (a superset). Python only: a patch touching C, C++,
Cython or Rust source is out.
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
TOTAL = 35
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
SWE_DROPPED: dict[str, str] = {
    # Real failures of the oracle check (the gold test through verify), after the two
    # harness fixes of 2026-10-14: SWE-bench ids cut at a space, and django runs that
    # cannot start before the fix. Three PRs with a few gold tests that never print
    # (xarray-7179 1344/1351, sklearn-25363 489/496, sklearn-10483 114/122 flip, none
    # still failing) are kept.
    "psf__requests-2678": "oracle NO: 6 of 7 gold tests still fail after the fix",
    "astropy__astropy-13398": "oracle NO: 1 of 4 gold tests still fails after the fix",
    "pydata__xarray-7052": "oracle NO: the gold tests pass before the fix too",
    "pydata__xarray-3733": "oracle: 1325 of 1630 gold tests never appear in the output",
    "pytest-dev__pytest-8055": "oracle BROKEN: nothing collected on either side",
    "pytest-dev__pytest-7122": "oracle: 85 of 145 gold tests never appear in the output",
    "scikit-learn__scikit-learn-12983": "oracle: 122 of 132 gold tests never appear in the output",
}


EXEC = json.loads((HERE / "executable.json").read_text())


def swebench(full_path):
    rows = json.loads(Path(full_path).read_text())
    verified = {r["instance_id"] for r in json.loads((ROOT / "data/swebench_verified.json").read_text())}
    rng = random.Random(14)
    pools = {}
    for r in rows:
        a, nonpy = size(r["patch"])
        if a < MIN_LINES or nonpy:
            continue
        # The draw is made for every candidate before any filter or drop, so dropping a
        # PR only promotes the next one in its repo and leaves every other pick in place.
        key = (r["instance_id"] not in verified, rng.random())
        ex = EXEC["swebench"][r["instance_id"]]["executable"]
        if ex >= MIN_LINES and r["instance_id"] not in SWE_DROPPED:
            pools.setdefault(r["repo"], []).append((key, r["instance_id"], ex))
    for pool in pools.values():
        pool.sort()
    # As even as the pools allow: raise a common cap until 35 fit, then take the excess
    # back from the smallest pools at the cap.
    cap = 0
    while sum(min(len(p), cap) for p in pools.values()) < TOTAL:
        cap += 1
    quota = {repo: min(len(p), cap) for repo, p in pools.items()}
    excess = sum(quota.values()) - TOTAL
    for repo in sorted(pools, key=lambda r: len(pools[r])):
        if excess and quota[repo] == cap:
            quota[repo] -= 1
            excess -= 1
    picked, sizes = [], {}
    for repo in sorted(pools):
        for (unverified, _), iid, ex in pools[repo][:quota[repo]]:
            picked.append({"id": iid, "tier": 0,
                           "note": f"large set, {repo}, {ex} executable changed lines"
                                   + ("" if unverified else ", Verified")})
            sizes[iid] = ex
    return picked, sizes


# ---- ChaCo: its 145-PR list; every Python-only PR of 50+ lines but those left out below.
CHACO_OUT = {
    "scipy__scipy-21485": "not behavioural: refactor into `_bary_rational`",
    "pandas-dev__pandas-59555": "refactor that de-duplicates methods; no developer test",
    "pandas-dev__pandas-58792": "refactor that breaks up a function; no developer test",
    "scipy__scipy-23028": "maintenance: a module moved to solve a circular import",
    "Qiskit__qiskit-13343": "speed-up; its only observable change is `__slots__`",
    "scipy__scipy-20789": "validate: oracle-mismatch (verify finds the developer tests broken)",
}


def chaco():
    rows = json.loads((ROOT / "datasets/chaco/instances.json").read_text())
    picked, sizes = [], {}
    for r in rows:
        iid = r["instance_id"]
        ex = (EXEC["chaco"].get(iid) or {}).get("executable", 0)
        if ex >= MIN_LINES and iid not in CHACO_OUT:
            picked.append({"id": iid, "tier": 0,
                           "note": f"large set, {r['repo']}, {ex} executable changed lines"})
            sizes[iid] = ex
    picked.sort(key=lambda p: (p["id"].split("__")[0].lower(), -sizes[p["id"]]))
    return picked, sizes


if __name__ == "__main__":
    swe, swe_sizes = swebench(sys.argv[1])
    ch, ch_sizes = chaco()
    (HERE / "swebench.json").write_text(json.dumps(swe, indent=1) + "\n")
    (HERE / "chaco.json").write_text(json.dumps(ch, indent=1) + "\n")
    (HERE / "sizes.json").write_text(json.dumps({"swebench": swe_sizes, "chaco": ch_sizes,
                                                 "chaco_left_out": CHACO_OUT,
                                                 "swebench_dropped": SWE_DROPPED}, indent=1) + "\n")
    print(f"swebench {len(swe)}  chaco {len(ch)}")
