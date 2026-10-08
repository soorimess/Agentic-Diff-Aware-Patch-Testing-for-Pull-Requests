import json, sys, collections
from pathlib import Path
root = Path("<repo>/out-v2") / sys.argv[1]
print(f"{'instance':34s} f2p  act  cov  magt mdev  ver cov mut  refusals -> restart  f2pH")
for d in sorted(p for p in root.iterdir() if (p / "result.json").exists()):
    r = json.loads((d / "result.json").read_text())
    c = r.get("changed_line_coverage") or {}
    m = r.get("mutation") or {}
    pct = lambda k: (f"{(m.get(k) or {}).get('percent'):.0f}" if (m.get(k) or {}).get("percent") is not None else "--")
    t = json.loads((d / "tool_log.json").read_text()) if (d / "tool_log.json").exists() else []
    tc = collections.Counter(x.get("tool") for x in t)
    rs = [x.get("reason") for x in ((r.get("refusals") or {}).get("rounds") or [])]
    rsc = collections.Counter(rs)
    sc = r.get("second_chance") or {}
    h = r.get("f2p_history") or {}
    print(f"{d.name:34s} {r.get('f2p'):4s} {r.get('actions') or 0:3d} "
          f"{(str(round(c['percent'])) if c.get('measured') else '--'):>4s} {pct('agent'):>4s} {pct('developer'):>4s}  "
          f"{tc['verify']:3d} {tc['coverage']:3d} {tc['mutation']:3d}  "
          f"{','.join(f'{k}x{v}' for k,v in rsc.items()) or '-'}"
          f"{' | SC '+str(sc.get('first_verdict'))+'->'+str(sc.get('final_verdict') or sc.get('skipped')) if sc else ''}"
          f"  vf={h.get('verified_f2p')} worse={h.get('made_worse')}"
          f"{'  excl='+str(len((m.get('developer') or {}).get('excluded') or [])) if (m.get('developer') or {}).get('excluded') else ''}"
          f"{'  mwhy='+str(m.get('why'))[:60] if m.get('why') else ''}")
