"""`out/RUNS.md` -- the state of every instance, for someone who has just cloned this.

`out/` holds one directory per instance and each one holds a dozen files. That is the
right shape for reading a single run in detail and the wrong shape for the first
question anyone asks, which is "what is in here and when was it produced". This writes
the index that answers it: one row per pull request, its verdict, its coverage, when it
last ran, and the directory to open next.

Written from `result.json` and the file timestamps rather than kept by hand, so it
cannot drift from what is actually on disk. Regenerate any time:

    uv run python -m openhands_f2p.runs
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from openhands_f2p.layout import OUT
from openhands_f2p.prs import PRS



VERDICT_NOTE = {
    "YES": "fails at base, passes after the fix",
    "NO": "ran, but is not fail-to-pass",
    "BROKEN": "no usable result -- see `why`",
}


def _row(pr: dict) -> dict:
    d = OUT / pr["id"]
    f = d / "result.json"
    if not f.exists():
        return {**pr, "f2p": "—", "when": "", "cov": None, "actions": None,
                "why": "never run", "judge": "—", "rechecked": False}
    r = json.loads(f.read_text())
    c = r.get("changed_line_coverage") or {}
    when = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
    return {**pr, "f2p": r.get("f2p", "?"),
            "when": when.strftime("%Y-%m-%d %H:%M UTC"),
            "cov": c.get("percent") if c.get("measured") else None,
            "covered": c.get("covered"), "total": c.get("executable_changed_lines"),
            "actions": r.get("actions"), "why": (r.get("why") or "").strip(),
            "judge": (r.get("concept") or {}).get("verdict", "—"),
            "issue": ((r.get("concept") or {}).get("issue_coverage")
                      or {}).get("verdict", "—"),
            "readable": ((r.get("concept") or {}).get("readability")
                         or {}).get("verdict", "—"),
            "uncovered": ((r.get("concept") or {}).get("issue_coverage")
                          or {}).get("uncovered") or [],
            "rechecked": bool(r.get("rechecked")),
            "tokens": (r.get("usage") or {}).get("total_tokens") or 0,
            "cost": (r.get("usage") or {}).get("cost_usd") or 0.0}


def build() -> str:
    rows = [_row(pr) for pr in PRS]
    decided = [r for r in rows if r["f2p"] in ("YES", "NO")]
    yes = [r for r in rows if r["f2p"] == "YES"]
    covs = [r["cov"] for r in rows if r["cov"] is not None]
    stamps = sorted(r["when"] for r in rows if r["when"])

    out = ["# Run status, per pull request", "",
           f"Generated from `result.json` by `python -m openhands_f2p.runs`. "
           f"Last run in this table: {stamps[-1] if stamps else 'none'}.", ""]

    out += [f"- **{len(rows)}** instances across "
            f"**{len({r['id'].split('__')[0] for r in rows})}** repositories",
            f"- **{len(yes)}/{len(decided)}** fail-to-pass, of those that reached a "
            f"verdict",
            f"- **{len(covs)}** measured for changed-line coverage; "
            f"median {sorted(covs)[len(covs) // 2]:.0f}%" if covs else "",
            f"- ${sum(r['cost'] for r in rows):.2f} and "
            f"{sum(r['tokens'] for r in rows) / 1e6:.1f}M tokens in total",
            ""]

    out += ["Coverage is measured only for tests that are fail-to-pass; for anything "
            "else the question does not apply. A `—` in that column means not "
            "measured, not zero.", "",
            "`concept`, `issue` and `readable` are three separate answers from one "
            "judgement call by a stronger model that wrote none of these tests: whether "
            "the test is about the same behaviour as the maintainer's, whether it "
            "reaches every behaviour the pull request settles, and whether it would pass "
            "review. None of them feeds the F2P verdict.", "",
            "| instance | version | verdict | coverage | actions | concept | issue | "
            "readable | last run |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        cov = (f"{r['cov']:.0f}% ({r['covered']}/{r['total']})"
               if r["cov"] is not None else "—")
        out.append(f"| [`{r['id']}`](./{r['id']}/) | {r['version']} | "
                   f"{r['f2p']}{' ¹' if r['rechecked'] else ''} | {cov} | "
                   f"{r['actions'] if r['actions'] is not None else '—'} | "
                   f"{r['judge']} | {r['issue']} | {r['readable']} | "
                   f"{r['when'] or '—'} |")
    if any(r["rechecked"] for r in rows):
        out += ["", "¹ re-judged by `--recheck`: the same saved test run again under a "
                    "later harness, with no new model call. The trajectory and token "
                    "counts belong to the original run; the verdict and coverage are "
                    "from the re-judgement."]

    gaps = [r for r in rows if r["uncovered"]]
    if gaps:
        out += ["", "## Behaviours the judge says are not covered", "",
                "Read alongside the coverage column: these come from reading the issue "
                "and the fix, not from line execution, so the two disagree in useful "
                "ways.", ""]
        for r in gaps:
            out.append(f"- **{r['id']}** ({r['issue']})")
            for u in r["uncovered"][:3]:
                out.append(f"  - {u}")

    unresolved = [r for r in rows if r["f2p"] not in ("YES", "NO")]
    if unresolved:
        out += ["", "## Without a verdict", ""]
        for r in unresolved:
            out.append(f"- **{r['id']}** — {r['why'] or 'never run'}")

    out += ["", "## What is in each directory", "",
            "| file | what it holds |", "|---|---|",
            "| `result.json` | the verdict, the coverage, token usage, the audit |",
            "| `flow.log` | every step in order: container, commands, both test runs, "
            "verdict |",
            "| `flow.jsonl` | the same, one JSON object per step |",
            "| `trajectory.json` | the agent's events, for the OpenHands visualizer |",
            "| `tool_log.json` | one entry per tool call, as it reached the container |",
            "| `test_f2p_*.py` | the test the agent wrote |",
            "| `before_fix.log`, `after_fix.log` | the two runs the verdict is read from |",
            "| `fix.diff` | the pull request's change, which the agent is shown |",
            "| `developer_test.diff` | the maintainer's test, which it is **not** |",
            "| `pr.json` | the full SWE-bench row |",
            "| `child.log` | the child process's stdout, under `--parallel` |", "",
            "`completions/` (raw prompt and response bytes per model call) is not "
            "committed: 43 MB across these instances. Set `LLM_LOG_COMPLETIONS=1` and "
            "rerun to regenerate it locally.", ""]
    return "\n".join(line for line in out if line is not None) + "\n"


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "RUNS.md"
    path.write_text(build())
    print(f"wrote {path.relative_to(Path(__file__).resolve().parents[3])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
