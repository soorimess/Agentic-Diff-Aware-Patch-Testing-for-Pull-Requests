"""Cross-arm comparisons the base-vs-arm table cannot express."""
import json, glob, os, collections, sys
from math import comb
ROOT = sys.argv[1] if len(sys.argv) > 1 else "experiments"
def load(d):
    out = {}
    for f in glob.glob(f"{ROOT}/{d}/*/result.json"):
        r = json.load(open(f)); c = r.get("changed_line_coverage") or {}
        w = (r.get("why") or "").lower()
        out[os.path.basename(os.path.dirname(f))] = {
            "f2p": r.get("f2p"), "broken": "still failing" in w,
            "cov": c.get("percent") if c.get("measured") else None}
    return out
def sign(u, d):
    n = u + d; k = min(u, d)
    return min(sum(comb(n, i) for i in range(k + 1)) / 2 ** n * 2, 1.0) if n else 1.0
def pair(x, y):
    ids = sorted(set(x) & set(y))
    u = sum(1 for i in ids if x[i]["f2p"] != "YES" and y[i]["f2p"] == "YES")
    d = sum(1 for i in ids if x[i]["f2p"] == "YES" and y[i]["f2p"] != "YES")
    return u, d, sign(u, d)
def pair_cov(x, y):
    ids = [i for i in set(x) & set(y) if x[i]["f2p"] == "YES" == y[i]["f2p"]
           and x[i]["cov"] is not None and y[i]["cov"] is not None]
    fell = sum(1 for i in ids if y[i]["cov"] < x[i]["cov"] - 1)
    rose = sum(1 for i in ids if y[i]["cov"] > x[i]["cov"] + 1)
    return len(ids), fell, rose, sign(rose, fell)

A = {k: load(v) for k, v in {
    "base": "+second-chance", "a6": "no-coverage-tool", "a7": "no-mutation-tool",
    "a8": "no-coverage+mutation", "a9": "no-verify-tool", "a10": "no-cov+mut+require"}.items()}
out = {}
u, d, p = pair(A["a10"], A["a9"])
out["verify"] = {"up": u, "down": d, "p": round(p, 4),
                 "from": sum(1 for i in A["a10"] if A["a10"][i]["f2p"] == "YES"),
                 "to": sum(1 for i in A["a9"] if A["a9"][i]["f2p"] == "YES")}
ids = sorted(set(A["a9"]) & set(A["a10"]))
became = sum(1 for i in ids if A["a9"][i]["broken"] and not A["a10"][i]["broken"])
fixed = sum(1 for i in ids if A["a10"][i]["broken"] and not A["a9"][i]["broken"])
out["verify_broken"] = {"became": became, "fixed": fixed, "p": round(sign(became, fixed), 5),
                        "a10": sum(1 for i in ids if A["a10"][i]["broken"]),
                        "a9": sum(1 for i in ids if A["a9"][i]["broken"])}
out["coverage_reps"] = [
    {"pair": "base -> arm 6", **dict(zip(("n","fell","rose","p"), pair_cov(A["base"], A["a6"])))},
    {"pair": "arm 7 -> arm 8", **dict(zip(("n","fell","rose","p"), pair_cov(A["a7"], A["a8"])))},
    {"pair": "arm 10 -> arm 9", **dict(zip(("n","fell","rose","p"), pair_cov(A["a10"], A["a9"])))},
]
out["mutation_reps"] = [
    {"pair": "base -> arm 7", **dict(zip(("up","down","p"), pair(A["base"], A["a7"])))},
    {"pair": "arm 6 -> arm 8", **dict(zip(("up","down","p"), pair(A["a6"], A["a8"])))},
]
print(json.dumps(out, indent=2))
