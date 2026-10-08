import json, sys
d = sys.argv[1]
t = json.load(open(f"{d}/tool_log.json")); inj = json.load(open(f"{d}/injected_messages.json"))
marks = {m["at_tool"]: m for m in inj}
last = None; seen = {}
for i, e in enumerate(t):
    if i in marks:
        m = marks[i]; print("   >>> refusal", m.get("reason"), "| last-round note:", "did not change the test" in (m.get("text") or ""))
    x = e["tool"]
    if x == "write_file" and "test_f2p" in e.get("path", ""):
        sha = (e.get("sha") or "")[:6]
        tag = "(same as last)" if sha == last else ("(back to %s)" % seen[sha] if sha in seen else "")
        print(i, "write", sha, tag); last = sha; seen.setdefault(sha, i)
    elif x == "mutation":
        print(i, "mutation", e.get("error") or "%s/%s survived=%s" % (e.get("killed"), e.get("total"), len(e.get("survived") or [])), "content", last)
    elif x == "verify":
        still = sum(v in ("FAILED", "ERROR") for v in (e.get("after") or {}).values())
        print(i, "verify flipped=%d still=%d" % (len(e.get("flipped") or []), still))
