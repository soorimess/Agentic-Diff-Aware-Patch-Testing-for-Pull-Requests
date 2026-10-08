import json, sys, subprocess
from pathlib import Path
from openhands_f2p import verify as V
root = Path(sys.argv[1])
out = {}
for d in sorted(root.iterdir()):
    if not (d / "result.json").exists(): continue
    r = json.loads((d/"result.json").read_text()); rel = r.get("test_path")
    log = json.loads((d/"tool_log.json").read_text())
    notes = []
    for i, e in enumerate(log):
        if e.get("tool") == "mutation" and "not fail-to-pass" in (e.get("error") or ""):
            if V.verify_settled(log[:i], rel): notes.append(f"mutation gate @{i}: refused -> now allowed")
        if e.get("tool") == "verify":
            b, a = e.get("before") or {}, e.get("after") or {}
            inv = [n for n in a if b.get(n) == "PASSED" and a[n] in ("FAILED", "ERROR")]
            if inv and e.get("flipped"): notes.append(f"verify @{i}: flipped+backwards (headline changes)")
    if notes: out[d.name] = notes
for k, v in out.items(): print(k, v)
