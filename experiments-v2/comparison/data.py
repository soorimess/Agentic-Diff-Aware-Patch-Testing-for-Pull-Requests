"""Every number the v2 comparison uses, pulled from the run directories. No figure is typed in.

    python experiments-v2/comparison/data.py > experiments-v2/comparison/data.json

Sources:

  experiments-v2/<arm>/            the series: one attempt per instance and arm. No
                                   best-of-two retry (decided 2026-09-26); runs an outside
                                   failure killed (the OpenRouter key limit) were rerun from
                                   scratch, which is not a retry of a verdict
  experiments/comparison/data.json v1's figures, read for the v1-vs-v2 view only

Nothing here is a model call.
"""
from __future__ import annotations

import collections
import glob
import json
import os
import statistics
import subprocess
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments-v2"
V1 = ROOT / "experiments" / "comparison" / "data.json"

ARMS = [
    ("1", "base", "+second-chance", "—"),
    ("2", "−second-chance", "no-second-chance", "the second chance"),
    ("3", "−guard", "no-guard", "the source guard"),
    ("4", "−require-tools", "no-require-tools", "the tool duty"),
    ("5", "−repo-facts", "no-repo-facts", "the testing briefing"),
    ("6", "−coverage", "no-coverage-tool", "the coverage tool"),
    ("7", "−mutation", "no-mutation-tool", "the mutation tool"),
    ("8", "−cov −mut", "no-coverage+mutation", "both instruments"),
    ("9", "−verify (×4)", "no-verify-tool", "verify, and the three that need it"),
    ("10", "−cov −mut −duty", "no-cov+mut+require", "two instruments and the duty"),
]
CONCEPT = ["different", "tangential", "narrower", "close", "equivalent"]
ISSUE = ["none", "minor only", "main only", "nearly complete", "complete"]
READ = ["reject", "poor", "acceptable", "good", "exemplary"]


def why_bucket(w: str | None) -> str:
    w = (w or "").lower()
    if "still failing" in w: return "broken"
    if "passes before" in w or "passes at base" in w: return "passes_at_base"
    if "nothing collected" in w or "collected nothing" in w: return "collects_nothing"
    if "wrote no test" in w or "never called a tool" in w: return "no_test"
    if "already existed" in w: return "voided"
    return "other"


def sign(a: int, b: int) -> float:
    """Two-sided exact sign test / McNemar on the discordant pairs."""
    n, k = a + b, min(a, b)
    return min(sum(comb(n, i) for i in range(k + 1)) / 2 ** n * 2, 1.0) if n else 1.0


def row(r: dict, log: list) -> dict:
    c = r.get("changed_line_coverage") or {}
    m = r.get("mutation") or {}
    muts = m.get("mutants") or [] if m.get("measured") else []
    dev = [x for x in muts if x.get("killed_by_developer_test")]
    con = r.get("concept") or {}
    lvl = lambda b: (b or {}).get("level") if (con.get("scale") == 5) else None
    return {
        "f2p": r.get("f2p"), "why": why_bucket(r.get("why")),
        "cov": c.get("percent") if c.get("measured") else None,
        "hit": c.get("covered") if c.get("measured") else 0,
        "tot": c.get("executable_changed_lines") if c.get("measured") else 0,
        "gated_n": len(dev), "gated_k": sum(1 for x in dev if x.get("killed_by_agent_test")),
        "raw_n": len(muts), "raw_k": sum(1 for x in muts if x.get("killed_by_agent_test")),
        "held_out": bool(m.get("held_out")),
        "actions": int(r.get("actions") or 0),
        "cost": float((r.get("usage") or {}).get("cost_usd") or 0),
        "jcost": float((r.get("judge_usage") or {}).get("cost_usd") or 0),
        "tokens": int((r.get("usage") or {}).get("total_tokens") or 0),
        "tools": collections.Counter(e.get("tool") for e in log),
        "concept": con.get("level") if con.get("scale") == 5 else None,
        "issue": lvl(con.get("issue_coverage")), "read": lvl(con.get("readability")),
        "judge_model": con.get("model"),
        "sc": r.get("second_chance") or None,
        "ran_at": r.get("ran_at"),
        "rescored": bool(r.get("rescored")),
        # verify's own coverage pointer ("some lines this pull request changed never run"),
        # which arms without the coverage tool receive too -- see the README's caveats.
        "reach_hint": sum(1 for e in log if e.get("tool") == "verify"
                          and "never run" in (e.get("shown") or "")),
    }


def load(arm_dir: str) -> dict[str, dict]:
    out = {}
    for f in glob.glob(str(EXP / arm_dir / "*" / "result.json")):
        r = json.load(open(f))
        try:
            log = json.load(open(f.replace("result.json", "tool_log.json")))
        except (OSError, json.JSONDecodeError):
            log = []
        out[os.path.basename(os.path.dirname(f))] = row(r, log)
    return out


def changed_source_lines(diff: str) -> int:
    """Executable source lines the fix adds, counted from fix.diff alone (see README)."""
    n, in_py, in_doc = 0, False, False
    for line in diff.splitlines():
        if line.startswith("diff --git "):
            in_py, in_doc = line.rstrip().endswith(".py"), False
            continue
        if not in_py or not line.startswith("+") or line.startswith("+++"):
            continue
        b = line[1:].strip()
        if not b:
            continue
        q = b.count('"""') + b.count("'''")
        if in_doc:
            if q % 2: in_doc = False
            continue
        if b.startswith("#"):
            continue
        if b.startswith(('"""', "'''")):
            if q % 2: in_doc = True
            continue
        n += 1
    return n


def paired_f2p(x: dict, y: dict) -> dict:
    ids = sorted(set(x) & set(y))
    up = sum(1 for i in ids if x[i]["f2p"] != "YES" and y[i]["f2p"] == "YES")
    dn = sum(1 for i in ids if x[i]["f2p"] == "YES" and y[i]["f2p"] != "YES")
    return {"up": up, "down": dn, "p": round(sign(up, dn), 4)}


def paired_cov(x: dict, y: dict) -> dict:
    ids = [i for i in set(x) & set(y) if x[i]["f2p"] == "YES" == y[i]["f2p"]
           and x[i]["cov"] is not None and y[i]["cov"] is not None]
    fell = sum(1 for i in ids if y[i]["cov"] < x[i]["cov"] - 1)
    rose = sum(1 for i in ids if y[i]["cov"] > x[i]["cov"] + 1)
    return {"n": len(ids), "fell": fell, "rose": rose, "p": round(sign(fell, rose), 3)}


def paired_mut(x: dict, y: dict) -> dict:
    ids = [i for i in set(x) & set(y) if x[i]["f2p"] == "YES" == y[i]["f2p"]
           and x[i]["gated_n"] and y[i]["gated_n"]]
    rate = lambda r: r["gated_k"] / r["gated_n"]
    fell = sum(1 for i in ids if rate(y[i]) < rate(x[i]) - 1e-9)
    rose = sum(1 for i in ids if rate(y[i]) > rate(x[i]) + 1e-9)
    return {"n": len(ids), "fell": fell, "rose": rose, "same": len(ids) - fell - rose,
            "p": round(sign(fell, rose), 3)}


def paired_judge(x: dict, y: dict) -> dict:
    ids = [i for i in set(x) & set(y) if x[i]["concept"] and y[i]["concept"]]
    fell = sum(1 for i in ids if y[i]["concept"] < x[i]["concept"])
    rose = sum(1 for i in ids if y[i]["concept"] > x[i]["concept"])
    return {"n": len(ids), "fell": fell, "rose": rose, "p": round(sign(fell, rose), 3)}


def main() -> None:
    data = {n: load(d) for n, _, d, _ in ARMS}
    base = data["1"]
    sizes = {}
    for f in glob.glob(str(EXP / "+second-chance" / "*" / "fix.diff")):
        sizes[os.path.basename(os.path.dirname(f))] = changed_source_lines(
            open(f, errors="replace").read())
    corpus = sum(sizes.values())

    out = {"corpus_lines": corpus, "patch_sizes": sorted(sizes.values(), reverse=True),
           "patch_sizes_by_id": sizes, "arms": [], "pairs": {}}
    for num, label, d, removed in ARMS:
        a = data[num]
        yes = [i for i in a if a[i]["f2p"] == "YES"]
        covs = [a[i]["cov"] for i in yes if a[i]["cov"] is not None]
        hit_sum = sum(a[i]["hit"] or 0 for i in yes)
        measured_tot = sum(a[i]["tot"] or 0 for i in yes if a[i]["cov"] is not None)
        gated = [i for i in yes if a[i]["gated_n"]]
        tools = collections.Counter()
        for i in a:
            tools.update(a[i]["tools"])
        judged = [i for i in yes if a[i]["concept"]]
        big5 = sorted(sizes, key=sizes.get, reverse=True)[:5]
        out["arms"].append({
            "num": num, "label": label, "dir": d, "removed": removed, "n": len(a),
            "yes": len(yes), "no": sum(1 for i in a if a[i]["f2p"] == "NO"),
            "broken_verdict": sum(1 for i in a if a[i]["f2p"] == "BROKEN"),
            "first_yes": len(yes), "retried": 0, "converted": 0,
            "rescored": sum(1 for i in a if a[i]["rescored"]),
            "reach_hint_runs": sum(1 for i in a if a[i]["reach_hint"]),
            "reach_hint_calls": sum(a[i]["reach_hint"] for i in a),
            "vs_base": paired_f2p(base, a) if num != "1" else None,
            "why": dict(collections.Counter(a[i]["why"] for i in a if a[i]["f2p"] != "YES")),
            "cov_mean": round(statistics.mean(covs), 1) if covs else None,
            "cov_pooled": round(100 * hit_sum / measured_tot, 1) if measured_tot else None,
            "cov_lines": hit_sum, "cov_share": round(100 * hit_sum / corpus, 1),
            "big5_lines": sum(a[i]["hit"] or 0 for i in big5 if i in yes),
            "big5_yes": sum(1 for i in big5 if i in yes),
            "cov_paired": paired_cov(base, a) if num != "1" else None,
            "mut_scored": len(gated),
            "mut_gated_n": sum(a[i]["gated_n"] for i in gated),
            "mut_gated_k": sum(a[i]["gated_k"] for i in gated),
            "mut_rate": round(100 * sum(a[i]["gated_k"] for i in gated)
                              / max(1, sum(a[i]["gated_n"] for i in gated)), 1),
            "mut_raw": round(100 * sum(a[i]["raw_k"] for i in yes)
                             / max(1, sum(a[i]["raw_n"] for i in yes)), 1),
            "mut_held_out": any(a[i]["held_out"] for i in yes),
            "mut_paired": paired_mut(base, a) if num != "1" else None,
            "judged": len(judged),
            "judge_models": dict(collections.Counter(a[i]["judge_model"] for i in judged)),
            "concept": [sum(1 for i in judged if a[i]["concept"] == k) for k in range(1, 6)],
            "issue": [sum(1 for i in judged if a[i]["issue"] == k) for k in range(1, 6)],
            "read": [sum(1 for i in judged if a[i]["read"] == k) for k in range(1, 6)],
            "judge_paired": paired_judge(base, a) if num != "1" else None,
            "cost_final": round(sum(a[i]["cost"] for i in a), 2),
            "cost_replaced": 0.0,
            "cost_retry_failed": 0.0,
            "jcost": round(sum(a[i]["jcost"] for i in a), 2),
            "tokens": sum(a[i]["tokens"] for i in a),
            "actions": sum(a[i]["actions"] for i in a),
            "tools": dict(tools.most_common()),
            "sc_refused": sum(1 for i in a if a[i]["sc"]),
            "sc_reasons": dict(collections.Counter(
                (a[i]["sc"] or {}).get("reason") for i in a if a[i]["sc"])),
            "sc_yes": sum(1 for i in a if a[i]["sc"] and a[i]["f2p"] == "YES"),
            # Refused for something only --second-chance checks (the test passes at base,
            # collects nothing, or was never written), as against `loop_open`, which the
            # tool duty raises whether or not the second chance is on.
            "sc_own": sum(1 for i in a if a[i]["sc"] and a[i]["sc"].get("reason", "") != "loop_open"
                          and any(k in a[i]["sc"].get("reason", "") for k in
                                  ("passes_at_base", "collects_nothing", "no_test"))),
            "sc_own_yes": sum(1 for i in a if a[i]["sc"] and a[i]["f2p"] == "YES"
                              and any(k in a[i]["sc"].get("reason", "") for k in
                                      ("passes_at_base", "collects_nothing", "no_test"))),
            "sc_pab": sum(1 for i in a if a[i]["sc"] and "passes_at_base" in a[i]["sc"].get("reason", "")),
            "sc_pab_yes": sum(1 for i in a if a[i]["sc"] and a[i]["f2p"] == "YES"
                              and "passes_at_base" in a[i]["sc"].get("reason", "")),
        })
        for arm in out["arms"]:
            arm["spend"] = round(arm["cost_final"] + arm["cost_replaced"]
                                 + arm["cost_retry_failed"] + arm["jcost"], 2)

    # The same removal asked a second time, and the one isolation of verify.
    D = {n: data[n] for n in data}
    out["pairs"] = {
        "verify_f2p": paired_f2p(D["10"], D["9"]),
        "coverage_reps": {k: paired_cov(D[x], D[y]) for k, (x, y) in
                          {"base→6": ("1", "6"), "7→8": ("7", "8"), "base→4": ("1", "4"),
                           "8→10": ("8", "10")}.items()},
        "mutation_reps": {k: paired_f2p(D[x], D[y]) for k, (x, y) in
                          {"base→7": ("1", "7"), "6→8": ("6", "8")}.items()},
        "verify_cov": paired_cov(D["10"], D["9"]), "verify_mut": paired_mut(D["10"], D["9"]),
        "verify_judge": paired_judge(D["10"], D["9"]),
    }
    ids = sorted(set(D["9"]) & set(D["10"]))
    br = lambda r: r["f2p"] != "YES" and r["why"] == "broken"
    became = sum(1 for i in ids if br(D["9"][i]) and not br(D["10"][i]))
    fixed = sum(1 for i in ids if br(D["10"][i]) and not br(D["9"][i]))
    out["pairs"]["verify_broken"] = {"a10": sum(br(D["10"][i]) for i in ids),
                                     "a9": sum(br(D["9"][i]) for i in ids),
                                     "became": became, "fixed": fixed,
                                     "p": round(sign(became, fixed), 5)}
    # Between-arm churn: how many instances change verdict between two arms at all.
    churn = []
    for x in D:
        for y in D:
            if x < y:
                pf = paired_f2p(D[x], D[y]); churn.append(pf["up"] + pf["down"])
    out["churn"] = [min(churn), max(churn)]
    # What the second chance's refusals in the base arm were worth: were they right, and
    # did the agent act on them. Read from the run directories, not from `row`.
    own = {"passes_at_base", "collects_nothing", "no_test"}
    refused, correct, writes, verifies, diag = 0, 0, [], [], 0
    for f in sorted(glob.glob(str(EXP / "+second-chance" / "*" / "result.json"))):
        r = json.load(open(f))
        rounds = (r.get("second_chance") or {}).get("rounds") or []
        if not any(set(x["reason"].split("+")) & own for x in rounds):
            continue
        refused += 1
        correct += "passes before the fix" in (r.get("why") or "") or r.get("f2p") == "YES"
        d = os.path.dirname(f)
        inj = json.load(open(os.path.join(d, "injected_messages.json")))
        tl = json.load(open(os.path.join(d, "tool_log.json")))
        after = tl[inj[0]["at_tool"]:]
        writes.append(sum(e.get("tool") == "write_file" for e in after))
        verifies.append(sum(e.get("tool") == "verify" for e in after))
        diag += any("**It does" in m["text"] for m in inj)
    out["second_chance_base"] = {
        "refused": refused, "ended_pab_or_yes": correct, "with_diagnosis": diag,
        "writes_min": min(writes or [0]), "writes_max": max(writes or [0]),
        "writes_median": statistics.median(writes or [0]),
        "verified_after": sum(1 for v in verifies if v)}
    # v1, for the side-by-side only: its first attempts and its best-of-two.
    v1 = json.load(open(V1))
    out["v1"] = {a["dir"]: {"first_yes": a["first_yes"], "yes": a["yes"],
                            "vs_base": a["vs_base"], "cov_paired": a["cov_paired"]}
                 for a in v1["arms"]}
    json.dump(out, sys.stdout, indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
