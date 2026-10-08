"""Which changed lines does an EMPTY test already hit? No model calls."""
import json, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from openhands_f2p import swebench_env as E
from openhands_f2p.dataset import load
from openhands_f2p import coverage_metric as C
from openhands_f2p.runners import runner_for
# The empty test IS the environment: with the subtraction on, it would always score 0.
C.environment_lines = lambda box, targets: {}
R = Path("../out-v2")
ids = [p["id"] for p in json.load(open("../evaluation/local-36-prs.json"))]
def one(iid):
    r = json.loads((R / "base" / iid / "result.json").read_text())
    rel = r.get("test_path") or ""
    path = str(Path(rel).parent / "test_f2p_baseline_empty.py")
    inst = load(iid)
    try:
        with E.Sandbox(iid, quiet=True, extra_packages=("coverage",)) as box:
            box.write(path, C._EMPTY_CLASS if runner_for(box)["args"] == "labels" else C._EMPTY_FUNCTION)
            base = E.base_texts(box, inst["patch"])
            box.apply_patch(inst["patch"])
            cov = E.changed_line_coverage(box, [path], inst["patch"], base)
            box.apply_patch(inst["patch"], revert=True)
        return iid, cov.get("measured"), cov.get("hit") or [], cov.get("executable_changed_lines"), cov.get("reason"), cov.get("test_run_returncode")
    except Exception as exc:
        return iid, None, [], None, f"ERROR {type(exc).__name__}: {exc}"[:150], None
with ThreadPoolExecutor(int(sys.argv[1]) if len(sys.argv) > 1 else 12) as ex:
    rows = list(ex.map(one, ids))
json.dump(rows, open(sys.argv[2] if len(sys.argv) > 2 else "/root/baseline_probe.json", "w"), indent=1)
for iid, m, hit, tot, why, rc in rows:
    print(f"{iid:36s} measured={m} env_hits={len(hit):3d}/{tot} rc={rc} {why or ''} {hit[:4]}")
