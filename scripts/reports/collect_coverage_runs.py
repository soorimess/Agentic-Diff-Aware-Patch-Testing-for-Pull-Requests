"""Copy the runs behind the coverage report into one folder, with an index.

    python3 scripts/reports/collect_coverage_runs.py   (from the repository root)

new-system-final-19-prs/coverage-runs/{without-coverage-tool,with-coverage-tool}/<PR>/ hold full copies of the
run directories (raw model completions left out); README.md lists every PR with its coverage and links.
"""
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import common as C  # noqa: E402
import coverage_report as R  # noqa: E402

DEST = C.RUNS / "coverage-runs"
SIDES = {"without-coverage-tool": "base", "with-coverage-tool": "tool"}
ARM = {d: f"`{d}/`" for d in ("no-tools", "coverage-tool", "coverage-and-mutation-tools")}


def main():
    runs = R.load()
    rows = sorted(R.rows(runs), key=lambda r: -((r["tool"] or 0) - (r["base"] or 0)))
    if DEST.exists():
        shutil.rmtree(DEST)
    for side, key in SIDES.items():
        for r in rows:
            src = C.RUNS / r[f"{key}_run" if key == "tool" else "base_run"] / r["id"]
            shutil.copytree(src, DEST / side / r["id"], ignore=shutil.ignore_patterns("completions"))
    L = ["# Coverage runs: 18 PRs, without and with the coverage tool", "",
         "Each PR has one run without the coverage tool and one with it. Every folder is a full copy of the run: "
         "`trajectory.json` (the agent's steps), `flow.log` (readable step log), `tool_log.json` (tool calls and "
         "answers), the handed-in test `test_f2p_*.py` and `result.json` (verdict and coverage).", "",
         "| PR | without | with | gain | without: run | with: run |", "|---|---:|---:|---:|---|---|"]
    for r in rows:
        gain = "–" if r["tool"] is None or r["base"] is None else f'{r["tool"] - r["base"]:+.1f}'
        L.append(f'| {C.short(r["id"])} | {r["base"]:.1f}% | {r["tool"]:.1f}% | {gain} | '
                 f'[without-coverage-tool/{r["id"]}](without-coverage-tool/{r["id"]}/trajectory.json) | '
                 f'[with-coverage-tool/{r["id"]}](with-coverage-tool/{r["id"]}/trajectory.json) |')
    L += ["", "Copied from (in the folder above):", ""]
    L += [f'- {C.short(r["id"])}: without from {ARM[r["base_run"]]}, with from {ARM[r["tool_run"]]}' for r in rows]
    (DEST / "README.md").write_text("\n".join(L + [""]))
    print(DEST.relative_to(C.ROOT), sum(1 for _ in DEST.glob("*/*/trajectory.json")), "trajectories")


if __name__ == "__main__":
    main()
