"""Judge a hand-written test with the harness's own verify (same path as agent recheck).

    uv run python hand_verify.py <instance_id> <test_path_in_repo> <local_test_file>
"""
import sys
from openhands_f2p import sources, swebench_env as E, verify as V

sources.select("chaco")
iid, rel, local = sys.argv[1:4]
inst = sources.load(iid)
code = open(local).read()
with E.Sandbox(iid, quiet=True, extra_packages=("coverage",)) as box:
    box.strip_git()
    v = V.verify(inst, box, generated_test=code, test_path=rel, quiet=False)
print("F2P:", v.f2p, "|", v.why)
print("base:", v.base)
print("head:", v.head)
if "-v" in sys.argv:
    print("---- base log tail\n", v.base_log[-3000:], "\n---- head log tail\n", v.head_log[-3000:])
cov = v.changed_line_coverage or {}
print("coverage:", cov.get("percent"), cov.get("reason", ""))
