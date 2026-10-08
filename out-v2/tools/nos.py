import json, sys
from pathlib import Path
root = Path("<repo>/out-v2") / sys.argv[1]
for d in sorted(root.iterdir()):
    f = d / "result.json"
    if not f.exists(): continue
    r = json.loads(f.read_text())
    if r.get("f2p") == "YES": continue
    rs = [x.get("reason") for x in (r.get("refusals") or {}).get("rounds", [])]
    sc = r.get("second_chance") or {}
    print(d.name, r.get("f2p"), r.get("actions"), "|", (r.get("why") or "")[:110])
    print("   refusals:", rs, "| restart:", sc.get("first_verdict"), "->", sc.get("final_verdict"), sc.get("skipped") or "")
