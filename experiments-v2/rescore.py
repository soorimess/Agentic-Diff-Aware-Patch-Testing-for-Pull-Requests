"""Re-score every experiments-v2 result from its saved logs with the fixed django parser.

    cd openhands-f2p && uv run python ../experiments-v2/rescore.py [--apply]

The agent is not run again and nothing is measured again: the before/after logs the run
saved are parsed with `runners.parse_output` as fixed after the v2 audit (a django status
printed on a later line than its test name was dropped), and the verdict is recomputed by
the harness's own `verify._decide`. Only a run whose verdict changes is rewritten; it keeps
its old verdict in `rescored_from` and says why in `rescored`. Coverage, mutation and the
judge are measured only for YES, inside the container, so a run that becomes YES here has
none of them (`not measured: rescored offline`), and one that stops being YES keeps them
under `superseded_*` rather than in the fields the reports read.
"""
import json
import sys
from pathlib import Path

from openhands_f2p import verify as V
from openhands_f2p.runners import parse_output

ROOT = Path(__file__).resolve().parent
ARMS = ["+second-chance", "no-second-chance", "no-guard", "no-require-tools", "no-repo-facts",
        "no-coverage-tool", "no-mutation-tool", "no-coverage+mutation", "no-verify-tool",
        "no-cov+mut+require"]
NOTE = ("verdict recomputed from the saved logs after the django parser fix (a status "
        "printed on a later line than its test name had been dropped)")


def main() -> int:
    apply = "--apply" in sys.argv
    changed = 0
    for arm in ARMS:
        for rj in sorted((ROOT / arm).glob("*/result.json")):
            r = json.loads(rj.read_text())
            if r.get("f2p") not in ("YES", "NO"):
                continue                 # BROKEN: no test ran on one side, nothing to re-read
            d = rj.parent
            try:
                blog, hlog = (d / "before_fix.log").read_text(), (d / "after_fix.log").read_text()
            except FileNotFoundError:
                continue
            base, head = parse_output(blog), parse_output(hlog)
            v = V._decide(r["instance_id"], "", base, head, r.get("targets") or [], None,
                          blog, hlog)
            if v.f2p == r["f2p"]:
                continue
            changed += 1
            print(f"{arm:22s} {d.name:34s} {r['f2p']} -> {v.f2p}   {v.why[:80]}")
            if not apply:
                continue
            r.update({"rescored_from": {"f2p": r["f2p"], "why": r["why"]},
                      "rescored": NOTE, "f2p": v.f2p, "why": v.why,
                      "f2p_nodes": v.f2p_nodes, "base": base, "head": head})
            if v.f2p == "YES":
                for k in ("changed_line_coverage", "mutation", "concept"):
                    r[k] = {"measured": False, "why": "not measured: rescored offline"} \
                        if k != "concept" else {"verdict": "not measured: rescored offline"}
            else:
                for k in ("changed_line_coverage", "mutation", "concept"):
                    if k in r:
                        r["superseded_" + k] = r.pop(k)
            rj.write_text(json.dumps(r, indent=2))
    print(f"{changed} verdict(s) change" + ("" if apply else " (dry run; --apply to write)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
