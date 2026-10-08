import json, re
from pathlib import Path
R = Path("<repo>/out-v2")
print(f"{'run':20s} f2p  act  cov    body   mutants  restart   ref  approach")
for f in [f"rand-astropy-{a}-{n}" for a in ("base", "nsc") for n in (1, 2, 3)]:
    d = R / f / "astropy__astropy-13398"
    r = json.loads((d / "result.json").read_text())
    c = r.get("changed_line_coverage") or {}
    b = c.get("excluding_import_time") or {}
    m = r.get("mutation") or {}
    sc = r.get("second_chance") or {}
    t = next(d.glob("test_f2p_*.py"), None)
    code = t.read_text() if t else ""
    appr = "calls transforms" if re.search(r"transform_to\(|AltAz|HADec", code) else "attribute only"
    rr = len((r.get("refusals") or {}).get("rounds") or [])
    cov = f"{c.get('percent')}%" if c.get("measured") else "--"
    body = f"{b.get('percent')}%" if b.get("percent") is not None else "--"
    mut = f"{(m.get('agent') or {}).get('killed')}/{m.get('total')}" if m.get("measured") else "--"
    rs = f"{sc.get('first_verdict')}->{sc.get('final_verdict')}" if sc else "-"
    why = (r.get("why") or "")[:55]
    print(f"{f:20s} {r['f2p']:4s} {r['actions']:3d}  {cov:6s} {body:6s} {mut:8s} {rs:9s} {rr:3d}  {appr} | {why}")
