import json, sys, collections
from pathlib import Path
root = Path("<repo>/out-v2") / (sys.argv[1] if len(sys.argv) > 1 else "base")
c = collections.Counter(); done = []
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    rj = d / "result.json"
    if rj.exists():
        r = json.loads(rj.read_text()); done.append((d.name, r.get("f2p"), r.get("actions"))); continue
    f = d / "flow.jsonl"
    rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()] if f.exists() else []
    last = rows[-1] if rows else {}
    acts = sum(1 for r in rows if r.get("phase") == "agent" and str(r.get("event", "")).endswith("Action"))
    c[f"{last.get('phase','starting')}"] += 1
print("running by phase:", dict(c))
print(f"done {len(done)}: YES {sum(x[1]=='YES' for x in done)}  NO {sum(x[1]=='NO' for x in done)}  other {sum(x[1] not in ('YES','NO') for x in done)}")
for x in done: print("  ", *x)
