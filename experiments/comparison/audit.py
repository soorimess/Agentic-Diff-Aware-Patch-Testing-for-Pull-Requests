"""Every way a run could have gone wrong, counted across all ten arms.

Run before reading the comparison. A number in that document is only worth as much as the
runs behind it, and "the agent did badly" and "the harness fell over" produce the same
verdict unless someone checks.
"""
import json, glob, os, re, collections, sys

R = sys.argv[1] if len(sys.argv) > 1 else "experiments"
ARMS = ["+second-chance", "no-second-chance", "no-guard", "no-require-tools",
        "no-repo-facts", "no-coverage-tool", "no-mutation-tool",
        "no-coverage+mutation", "no-verify-tool", "no-cov+mut+require"]
TRACE = re.compile(r"Traceback \(most recent call last\)")

print("%-24s %5s %6s %7s %6s %7s %7s %8s %7s %7s" % (
    "arm", "runs", "dupes", "agtErr", "0act", "notFin", "judErr", "toolErr", "tracebk", "capped"))
print("-" * 104)
grand = collections.Counter()
tool_msgs = collections.Counter()
for arm in ARMS:
    dirs = sorted(glob.glob(f"{R}/{arm}/*/"))
    a = collections.Counter()
    ids = []
    for d in dirs:
        rj = os.path.join(d, "result.json")
        if not os.path.exists(rj):
            a["no_result"] += 1
            continue
        ids.append(os.path.basename(d.rstrip("/")))
        r = json.load(open(rj))
        a["runs"] += 1
        a["agent_error"] += bool(r.get("agent_error"))
        st = str(r.get("agent_status") or "")
        a["not_finished"] += bool(st and "FINISHED" not in st)
        a["zero_actions"] += (r.get("actions", 0) == 0)
        a["judge_error"] += ((r.get("concept") or {}).get("verdict") == "error")
        a["capped"] += ("cap" in (r.get("why") or "").lower())
        try:
            log = json.load(open(os.path.join(d, "tool_log.json")))
        except Exception:
            log = []
        for e in log:
            if not isinstance(e, dict):
                continue
            res = e.get("result")
            if ("error" in e) or (isinstance(res, dict) and res.get("is_error")):
                a["tool_errors"] += 1
                tool_msgs[f'{e.get("tool")}: ' + str(e.get("error") or "")[:80]] += 1
        for name in ("child.log", "flow.log"):
            p = os.path.join(d, name)
            if os.path.exists(p) and TRACE.search(open(p, errors="replace").read()):
                a["traceback"] += 1
    grand.update(a)
    print("%-24s %5d %6d %7d %6d %7d %7d %8d %7d %7d" % (
        arm, a["runs"], len(ids) - len(set(ids)), a["agent_error"], a["zero_actions"],
        a["not_finished"], a["judge_error"], a["tool_errors"], a["traceback"], a["capped"]))

calls = err = empty = 0
prov = collections.Counter()
for arm in ARMS:
    for f in glob.glob(f"{R}/{arm}/*/completions/*.json"):
        try:
            d = json.load(open(f))
        except Exception:
            err += 1
            continue
        calls += 1
        resp = d.get("response") or {}
        err += bool(resp.get("error"))
        if resp.get("provider"):
            prov[resp["provider"]] += 1
        for ch in (resp.get("choices") or []):
            m = ch.get("message") or {}
            if not (m.get("content") or m.get("tool_calls") or m.get("reasoning")):
                empty += 1
print()
print("model calls %d | transport errors %d | empty replies %d | providers %s"
      % (calls, err, empty, dict(prov)))
sets = {a: {os.path.basename(os.path.dirname(f)) for f in glob.glob(f"{R}/{a}/*/result.json")}
        for a in ARMS}
base = sets[ARMS[0]]
diff = {a: sorted(s ^ base) for a, s in sets.items() if s != base}
print("instance sets differing from the base:", diff or "none")
if tool_msgs:
    print()
    print("tool errors, by message (these are refusals by design, not faults):")
    for m, n in tool_msgs.most_common(6):
        print("  %3d  %s" % (n, m))
