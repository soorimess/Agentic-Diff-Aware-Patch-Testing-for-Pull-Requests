"""Oracle sweep: run the developer's own test through our verifier, on every PR.

That test is fail-to-pass by construction. Any instance where we do not reproduce it is
a defect in the harness, the runner table or the output parser -- never a result about a
model. Running this before any agent exists is what stops a broken measurement from
being read later as a bad model result.

    uv run python -m openhands_f2p.oracle          # all five
    uv run python -m openhands_f2p.oracle 3        # just django
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from openhands_f2p.layout import OUT
from openhands_f2p import swebench_env as E
from openhands_f2p import verify as V
from openhands_f2p.dataset import load
from openhands_f2p.prs import f2p_is_consistent, pick




def check(pr: dict, save: bool = True) -> dict:
    inst = load(pr["id"])
    print(f"\n=== [{pr['tier']}] {pr['id']}  ({inst['repo']})")
    print(f"    build={pr['build']:8s} localise={pr['localise']:7s} runner={pr['runner']}")

    # Before running anything: is the instance internally consistent? An id naming a
    # test its own patch never adds cannot be verified, and without this check it
    # reports as "the test does not exercise the change" -- a verdict about a test,
    # for a dataset problem.
    inconsistent = f2p_is_consistent(inst)
    if inconsistent:
        print(f"    SKIPPED  : FAIL_TO_PASS names {inconsistent[:1]}, which this "
              f"instance's own test patch never adds -- a dataset artefact, not a "
              f"result. Not verifiable.")
        row = {"id": pr["id"], "tier": pr["tier"], "repo": inst["repo"],
               "env_ok": False, "env_checked": 0, "env_seen": 0, "oracle_ok": False,
               "isolated": False, "f2p": "UNVERIFIABLE",
               "why": f"FAIL_TO_PASS id absent from test_patch: {inconsistent[:2]}",
               "f2p_nodes": [], "checked_at": datetime.now(timezone.utc).isoformat()}
        if save:
            d = OUT / pr["id"]
            d.mkdir(parents=True, exist_ok=True)
            (d / "oracle.json").write_text(json.dumps(row, indent=2))
        return row

    env = E.verify_environment(inst, quiet=True)
    print(f"    env gate : {env['checked']} PASS_TO_PASS checked, {env['seen']} seen, "
          f"ok={env['ok']}" + (f", failed={env['failed'][:2]}" if not env["ok"] else ""))

    with E.Sandbox(pr["id"], quiet=True) as box:
        before = box.audit_isolation()
        box.strip_git()
        after = box.audit_isolation()
        print(f"    isolation: dns={before['dns_resolves']} "
              f"git_before={before['git_present']} git_after={after['git_present']}")
        # The same verify() an agent run uses. If the oracle passed through different
        # code, it would not be testing the thing it claims to test.
        verdict = V.verify(inst, box, use_gold_test=True, quiet=True)

    for n in verdict.f2p_nodes[:2]:
        print(f"    F2P      : flipped  {n[-58:]!r}")
    isolated = not before["dns_resolves"] and not after["git_present"]
    ok = verdict.ok and env["ok"]
    print(f"    verdict  : {verdict.line()}")
    print(f"    ORACLE   : {'OK' if ok else 'MISMATCH'}")

    row = {"id": pr["id"], "tier": pr["tier"], "repo": inst["repo"],
           "env_ok": env["ok"], "env_checked": env["checked"], "env_seen": env["seen"],
           "oracle_ok": verdict.ok, "isolated": isolated,
           "f2p": verdict.f2p, "why": verdict.why,
           "f2p_nodes": verdict.f2p_nodes,
           "checked_at": datetime.now(timezone.utc).isoformat()}
    if save:
        d = OUT / pr["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "oracle.json").write_text(json.dumps(row, indent=2))
        (d / "oracle_before_fix.log").write_text(verdict.base_log)
        (d / "oracle_after_fix.log").write_text(verdict.head_log)
        print(f"    wrote    : out/{pr['id']}/oracle.json")
    return row


def main() -> int:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    results = [check(pr) for pr in pick(which)]
    print("\n" + "-" * 74)
    for r in results:
        good = r["oracle_ok"] and r["env_ok"] and r["isolated"]
        print(f"  {'OK  ' if good else 'BAD '} tier {r['tier']}  {r['id']:36s} "
              f"env={r['env_ok']} oracle={r['oracle_ok']} isolated={r['isolated']}")
    good = sum(r["oracle_ok"] and r["env_ok"] and r["isolated"] for r in results)
    print(f"\n{good}/{len(results)} instances are ready to develop against")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "oracle_summary.json").write_text(json.dumps(results, indent=2))
    print("wrote out/oracle_summary.json")
    return 0 if good == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
