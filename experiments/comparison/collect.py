"""Pull every number the comparison needs out of the ten run directories."""
import json, glob, os, statistics, collections, sys
from math import comb

ROOT = sys.argv[1] if len(sys.argv) > 1 else "experiments"
ARMS = [
    ("1", "base", "+second-chance", "everything"),
    ("2", "-second-chance", "no-second-chance", "second chance"),
    ("3", "-guard", "no-guard", "guard"),
    ("4", "-require-tools", "no-require-tools", "tool duty"),
    ("5", "-repo-facts", "no-repo-facts", "testing briefing"),
    ("6", "-coverage", "no-coverage-tool", "coverage tool"),
    ("7", "-mutation", "no-mutation-tool", "mutation tool"),
    ("8", "-cov -mut", "no-coverage+mutation", "both instruments"),
    ("9", "-verify (x4)", "no-verify-tool", "all instruments + duty"),
    ("10", "-cov -mut -duty", "no-cov+mut+require", "two instruments + duty"),
]

def why_bucket(w):
    w = (w or "").lower()
    if "still failing" in w: return "broken"
    if "passes before" in w or "passes at base" in w: return "passes_at_base"
    if "nothing collected" in w: return "collects_nothing"
    if "wrote no test" in w or "never called a tool" in w: return "no_test"
    if "429" in w or "resolve reference" in w: return "registry"
    if "already existed" in w: return "voided"
    return "other"

def load(d):
    out = {}
    for f in glob.glob(f"{ROOT}/{d}/*/result.json"):
        r = json.load(open(f))
        c = r.get("changed_line_coverage") or {}
        m = r.get("mutation") or {}
        ag = (m.get("agent") or {}) if m.get("measured") else {}
        con = r.get("concept") or {}
        try:
            log = json.load(open(f.replace("result.json", "tool_log.json")))
        except Exception:
            log = []
        out[os.path.basename(os.path.dirname(f))] = {
            "f2p": r.get("f2p"),
            "why": why_bucket(r.get("why")),
            "cov": c.get("percent") if c.get("measured") else None,
            "hit": c.get("covered"), "tot": c.get("executable_changed_lines"),
            "mk": ag.get("killed"), "mn": ag.get("total"),
            "actions": int(r.get("actions") or 0),
            "cost": float((r.get("usage") or {}).get("cost_usd") or 0),
            "jcost": float((r.get("judge_usage") or {}).get("cost_usd") or 0),
            "tokens": int((r.get("usage") or {}).get("total_tokens") or 0),
            "tools": collections.Counter(e.get("tool") for e in log),
            "concept": con.get("verdict"),
            "issue": (con.get("issue_coverage") or {}).get("verdict"),
            "read": (con.get("readability") or {}).get("verdict"),
            "sc": (r.get("second_chance") or {}).get("reason"),
        }
    return out

def sign(u, d):
    n = u + d; k = min(u, d)
    return min(sum(comb(n, i) for i in range(k + 1)) / 2 ** n * 2, 1.0) if n else 1.0

data = {n: load(d) for n, _, d, _ in ARMS}
base = data["1"]

# corpus constant, from fix.diff
def changed_source_lines(diff):
    n, in_py, in_doc = 0, False, False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            in_py, in_doc = line.rstrip().endswith(".py"), False; continue
        if not in_py or not line.startswith("+") or line.startswith("+++"): continue
        b = line[1:].strip()
        if not b: continue
        q = b.count('"""') + b.count("'''")
        if in_doc:
            if q % 2: in_doc = False
            continue
        if b.startswith("#"): continue
        if b.startswith(('"""', "'''")):
            if q % 2: in_doc = True
            continue
        n += 1
    return n
CORPUS = sum(changed_source_lines(open(f, errors="replace").read())
             for f in glob.glob(f"{ROOT}/+second-chance/*/fix.diff"))

out = {"corpus_lines": CORPUS, "arms": []}
for num, label, d, removed in ARMS:
    a = data[num]
    if not a: continue
    ids = sorted(set(base) & set(a))
    up = sum(1 for i in ids if base[i]["f2p"] != "YES" and a[i]["f2p"] == "YES")
    dn = sum(1 for i in ids if base[i]["f2p"] == "YES" and a[i]["f2p"] != "YES")
    yes = [i for i in a if a[i]["f2p"] == "YES"]
    covs = [a[i]["cov"] for i in yes if a[i]["cov"] is not None]
    both = [i for i in ids if base[i]["f2p"] == "YES" == a[i]["f2p"]
            and base[i]["cov"] is not None and a[i]["cov"] is not None]
    cw = sum(1 for i in both if a[i]["cov"] < base[i]["cov"] - 1)
    cr = sum(1 for i in both if a[i]["cov"] > base[i]["cov"] + 1)
    mb = [i for i in ids if base[i]["f2p"] == "YES" == a[i]["f2p"] and base[i]["mn"] and a[i]["mn"]]
    tools = collections.Counter()
    for i in a: tools.update(a[i]["tools"])
    out["arms"].append({
        "num": num, "label": label, "removed": removed, "dir": d,
        "n": len(a),
        "yes": sum(1 for i in a if a[i]["f2p"] == "YES"),
        "no": sum(1 for i in a if a[i]["f2p"] == "NO"),
        "broken": sum(1 for i in a if a[i]["f2p"] == "BROKEN"),
        "up": up, "down": dn, "p": round(sign(up, dn), 4),
        "cov_mean": round(statistics.mean(covs), 1) if covs else None,
        "corpus_cov": round(100 * sum(a[i]["hit"] for i in yes if a[i]["hit"]) / CORPUS, 1),
        "paired_n": len(both),
        "paired_base": round(statistics.mean([base[i]["cov"] for i in both]), 1) if both else None,
        "paired_arm": round(statistics.mean([a[i]["cov"] for i in both]), 1) if both else None,
        "cov_fell": cw, "cov_rose": cr, "cov_p": round(sign(cr, cw), 3),
        "mut_n": len(mb),
        "mut_base": round(100 * statistics.mean([base[i]["mk"]/base[i]["mn"] for i in mb]), 1) if mb else None,
        "mut_arm": round(100 * statistics.mean([a[i]["mk"]/a[i]["mn"] for i in mb]), 1) if mb else None,
        "cost": round(sum(a[i]["cost"] for i in a), 2),
        "jcost": round(sum(a[i]["jcost"] for i in a), 2),
        "tokens": sum(a[i]["tokens"] for i in a),
        "actions": sum(a[i]["actions"] for i in a),
        "why": dict(collections.Counter(a[i]["why"] for i in a if a[i]["f2p"] != "YES")),
        "tools": dict(tools.most_common()),
        "judge": {k: dict(collections.Counter(a[i][k] for i in yes if a[i][k]))
                  for k in ("concept", "issue", "read")},
    })
print(json.dumps(out, indent=2))
