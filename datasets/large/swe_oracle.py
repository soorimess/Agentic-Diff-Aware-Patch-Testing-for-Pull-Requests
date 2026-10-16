"""Oracle check (run on the server from openhands-f2p/) for one SWE-bench instance: the gold test through the harness's verify.

    F2P_DATASET=../data/swebench_full.json uv run python swe_oracle.py <instance_id> <out.jsonl>
"""
import json
import sys
import time

from openhands_f2p import sources, swebench_env as E, verify as V

sources.select("swebench")
iid, out = sys.argv[1:3]
t0 = time.time()
rec = {"id": iid}
try:
    inst = sources.load(iid)
    with E.Sandbox(iid, quiet=True, extra_packages=("coverage",)) as box:
        v = V.verify(inst, box, use_gold_test=True, quiet=True)
    rec.update(f2p=v.f2p, why=v.why[:300],
               expected=len(json.loads(inst["FAIL_TO_PASS"])), flipped=len(v.f2p_nodes))
except BaseException as e:
    rec.update(f2p="ERROR", why=f"{type(e).__name__}: {e}"[:300])
rec["secs"] = round(time.time() - t0)
with open(out, "a") as f:
    f.write(json.dumps(rec) + "\n")
print(json.dumps(rec))
