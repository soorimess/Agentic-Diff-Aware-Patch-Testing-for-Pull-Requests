"""The coverage A/B: every pull request twice, with the tool and without.

The harness measures changed-line coverage in *both* arms. That is the whole point --
without a number for the arm that had no coverage tool there is nothing to compare
against, and any claim that the tool helps would rest on a single run of the arm that
had it.
"""
from __future__ import annotations

import json

from openhands_f2p.layout import PROJECT_ROOT
from openhands_f2p.parallel import _child_argv, _run_children



def compare_coverage(prs: list[dict], args) -> int:
    """Run every PR twice -- with the coverage tool and without -- and contrast them.

    The harness measures changed-line coverage in *both* arms. That is the whole point:
    without a number for the arm that had no coverage tool there is nothing to compare
    against, and any claim that the tool helps would rest on a single run of the arm that
    had it.
    """
    root = PROJECT_ROOT / "out_compare_coverage"
    jobs = []
    for pr in prs:
        for on, label in ((True, "with_coverage_tool"), (False, "without_coverage_tool")):
            out = root / pr["id"] / label
            jobs.append((pr["id"], _child_argv(pr["id"], args, on, out, label),
                         out, label))
    # Two runs per PR, so the cap is doubled -- the configured number is PRs in flight.
    rows = _run_children(jobs, args.parallel * 2)

    print("\n" + "=" * 78)
    print(f"{'instance':32s} {'tool':4s} {'F2P':5s} {'changed-line cov':>17s} {'act':>4s}")
    by_id: dict[str, dict] = {}
    for r in rows:
        by_id.setdefault(r["instance_id"], {})[r["label"]] = r
    for iid, pair in sorted(by_id.items()):
        for label, mark in (("with_coverage_tool", "on "),
                            ("without_coverage_tool", "off")):
            r = pair.get(label)
            if not r:
                print(f"{iid[:32]:32s} {mark:4s} {'--':5s} {'no result':>17s}")
                continue
            c = r.get("changed_line_coverage") or {}
            cov = (f"{c['percent']:.1f}% ({c['covered']}/"
                   f"{c['executable_changed_lines']})" if c.get("measured")
                   else "not measured")
            print(f"{iid[:32]:32s} {mark:4s} {r.get('f2p','?'):5s} {cov:>17s} "
                  f"{r.get('actions', 0):4d}")
        print()
    # The per-instance table is evidence; this is the answer. Both arms are summarised
    # over the instances where *both* produced a number, because an arm that failed on a
    # different subset would otherwise be compared on easier work.
    paired = [(a, b) for a, b in
              ((pair.get("with_coverage_tool"), pair.get("without_coverage_tool"))
               for pair in by_id.values()) if a and b]
    aggregate = {"instances": len(by_id), "paired": len(paired), "arms": {}}
    print("=" * 78)
    print(f"{'':22s} {'F2P':>10s} {'mean cov':>10s} {'median cov':>11s} {'actions':>9s}")
    for label, key in (("with coverage tool", "with_coverage_tool"),
                       ("without", "without_coverage_tool")):
        arm = [r for r in (pair.get(key) for pair in by_id.values()) if r]
        yes = sum(1 for r in arm if r.get("f2p") == "YES")
        covs = sorted(c["percent"] for r in arm
                      if (c := r.get("changed_line_coverage") or {}).get("measured"))
        mean = sum(covs) / len(covs) if covs else None
        med = covs[len(covs) // 2] if covs else None
        acts = [r.get("actions", 0) for r in arm]
        aggregate["arms"][key] = {
            "runs": len(arm), "f2p_yes": yes, "measured": len(covs),
            "mean_coverage": round(mean, 1) if mean is not None else None,
            "median_coverage": med,
            "mean_actions": round(sum(acts) / len(acts), 1) if acts else None}
        print(f"{label:22s} {f'{yes}/{len(arm)}':>10s} "
              f"{(f'{mean:.1f}%' if mean is not None else '-'):>10s} "
              f"{(f'{med:.1f}%' if med is not None else '-'):>11s} "
              f"{(sum(acts) / len(acts) if acts else 0):>9.1f}")
    if len(paired) < len(by_id):
        print(f"\n  {len(by_id) - len(paired)} instance(s) produced a result in only one "
              f"arm; the means above are over each arm's own runs, so read them "
              f"alongside the per-instance table rather than as a paired difference.")

    (root / "summary.json").write_text(
        json.dumps({"aggregate": aggregate, "runs": rows}, indent=2))
    print("\nwrote out_compare_coverage/summary.json")
    return 0
