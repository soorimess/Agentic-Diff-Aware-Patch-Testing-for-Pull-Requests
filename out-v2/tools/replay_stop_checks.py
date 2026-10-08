"""Which runs would the current stop logic have steered differently? Replays verify_gap/duty_gap
at every recorded refusal (reason + text) and at the end of every conversation (accept vs refuse)."""
import json, sys, re
from pathlib import Path
from openhands_f2p import verify as V, agent as A
root = Path(sys.argv[1])
INSTR = ("coverage", "mutation")
def gap(log, rel, inj):
    # `rewound` as agent.py passes it: after a rewind, a lower score is an ordinary attempt.
    rew = {d for d in INSTR if any(V.rewind_said(d) in (m.get("text") or "") for m in inj)}
    return V.verify_gap(log, rel) or V.duty_gap(log, INSTR, rel, refused=A._first_refusals(inj),
                                                 last_refused=A._last_refusals(inj), rewound=rew)
def body(text):
    b = (text or "").split("\n\nWhat you have done so far", 1)[0]
    return "\n\n".join(x for x in b.strip().split("\n\n") if not x.startswith("Stop refused"))
changed = {}
for d in sorted(root.iterdir()):
    if not (d / "result.json").exists(): continue
    r = json.loads((d/"result.json").read_text()); rel = r.get("test_path")
    log = json.loads((d/"tool_log.json").read_text())
    inj = json.loads((d/"injected_messages.json").read_text()) if (d/"injected_messages.json").exists() else []
    cuts = [m["at_tool"] for m in inj if m.get("reason") == "restart"]
    convs = [(0, cuts[0] if cuts else len(log))] + ([(cuts[0], len(log))] if cuts else [])
    notes = []
    for lo, hi in convs:
        sub = log[lo:hi]
        mine = [dict(m, at_tool=m["at_tool"] - lo) for m in inj if lo <= m["at_tool"] < hi and m.get("reason") != "restart"] if lo == 0 else \
               [dict(m, at_tool=m["at_tool"] - lo) for m in inj if lo < m["at_tool"] <= hi and m.get("reason") != "restart"]
        for k, m in enumerate(mine):
            reason = m.get("reason") or ""
            if not ("verify_open" in reason or "duties_open" in reason): continue
            g = gap(sub[:m["at_tool"]], rel, mine[:k])
            if not g: notes.append(f"@{m['at_tool']+lo} {reason} -> NONE")
            elif g[0] != reason.replace("+reads_source", ""): notes.append(f"@{m['at_tool']+lo} {reason} -> {g[0]}")
            elif g[1].strip() not in body(m.get("text")) : notes.append(f"@{m['at_tool']+lo} {reason}: text differs")
        # end of conversation: old accepted (no refusal at end) -> does new refuse?
        # A conversation that ended at the cap could not be refused whatever the gap.
        # (Refusals need 3 actions left; out-v2 runs have a cap of 125.)
        capped = hi == len(log) and (r.get("actions") or 0) >= 125 - 2
        if V.verify_settled(sub, rel) and not capped:
            g = gap(sub, rel, mine)
            if g: notes.append(f"end conv@{hi}: accepted -> now {g[0]}")
    # reach diagnosis: subprocess hedge
    if any("**It does not reach the change.**" in (m.get("text") or "") for m in inj):
        tests = [e.get("content") or "" for e in log if e.get("tool") == "write_file" and V.wrote_to(e.get("path",""), rel)]
        if any(V.starts_process(t) for t in tests): notes.append("does-not-reach sent; test spawns a process (subprocess hedge may apply)")
    # deleted-line mutant labels shown
    for e in log:
        if e.get("tool") == "mutation" and any(l.rstrip().endswith("->") for l in (e.get("shown") or "").splitlines()):
            notes.append("mutation tool showed an empty label"); break
    if notes: changed[d.name] = notes
for k, v in changed.items():
    print(k); [print("   ", n) for n in v]
print("affected:", len(changed))
