"""Build COVERAGE_REPORT.md and coverage.html from the final experiment's runs.

    python3 scripts/reports/coverage_report.py   (from the repository root)
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import common as C  # noqa: E402

E = C.E
WITH = ["coverage-tool", "coverage-and-mutation-tools"]   # arms that have the coverage tool
WITHOUT = ["no-tools"]
OUT = C.RUNS / "coverage.html"
MD = C.RUNS / "COVERAGE_REPORT.md"
# sympy-13091 is left out: the run without the tool wrote no fail-to-pass test there.
PRS = [i for i in C.FINAL if i != "sympy__sympy-13091"]


def load():
    runs = {}
    for d in WITH + WITHOUT:
        for i in C.FINAL:
            f = C.RUNS / d / i / "result.json"
            if f.exists():
                runs[(d, i)] = json.loads(f.read_text())
    return runs


def pick(runs, i, dirs, best):
    vals = [(C.covp(runs.get((d, i))), d) for d in dirs if C.covp(runs.get((d, i))) is not None]
    if not vals:
        return None, None, sum((d, i) in runs for d in dirs)
    v, d = (max if best else min)(vals)
    return v, d, sum((d2, i) in runs for d2 in dirs)


def rows(runs):
    out = []
    for i in PRS:
        t, td, tn = pick(runs, i, WITH, True)
        b, bd, bn = pick(runs, i, WITHOUT, False)
        out.append({"id": i, "tool": t, "tool_run": td, "tool_n": tn, "base": b, "base_run": bd, "base_n": bn})
    return out


def stats(rs):
    both = [r for r in rs if r["tool"] is not None and r["base"] is not None]
    tool = [r["tool"] for r in rs if r["tool"] is not None]
    base = [r["base"] for r in rs if r["base"] is not None]
    mean = lambda v: sum(v) / len(v) if v else None
    return {
        "both": len(both),
        "tool_mean": mean([r["tool"] for r in both]), "base_mean": mean([r["base"] for r in both]),
        "tool_full": sum(v >= 99.5 for v in tool), "base_full": sum(v >= 99.5 for v in base),
        "tool_80": sum(v >= 80 for v in tool), "base_80": sum(v >= 80 for v in base),
        "tool_low": sum(v < 20 for v in tool), "base_low": sum(v < 20 for v in base),
        "tool_yes": len(tool), "base_yes": len(base),
        "wins": sum(r["tool"] - r["base"] >= 1 for r in both),
        "ties": sum(abs(r["tool"] - r["base"]) < 1 for r in both),
        "losses": sum(r["base"] - r["tool"] >= 1 for r in both),
    }


def gain(r):
    return "–" if r["tool"] is None or r["base"] is None else f'{r["tool"] - r["base"]:+.0f}'


def build():
    runs = load()
    rs = rows(runs)
    s = stats(rs)
    n = len(PRS)
    order = sorted(rs, key=lambda r: -((r["tool"] or 0) - (r["base"] or 0)))
    dot_rows = [(C.short(r["id"]), f'{C.LINES[r["id"]]} lines', {"A": r["base"], "B": r["tool"]}, None) for r in order]
    fmt = lambda v: "–" if v is None else f"{v:.0f}%"
    trs = "".join(
        f'<tr><td><span class="pr">{E(C.short(r["id"]))}</span></td><td class=num>{C.LINES[r["id"]]}</td>'
        f'<td class=num>{fmt(r["base"])}</td><td class=num>{fmt(r["tool"])}</td>'
        f'<td class="num a-B">{gain(r)}</td></tr>'
        for r in order)
    css = C.CSS.read_text()
    key = '<span class="key k-A"><i></i>without the coverage tool</span> &nbsp; <span class="key k-B"><i></i>with the coverage tool</span>'
    figs = "".join([
        C.fig("Mean changed-line coverage", [("A", f'{s["base_mean"]:.0f}%'), ("B", f'{s["tool_mean"]:.0f}%')], f"{n} PRs"),
        C.fig("PRs at 100% coverage", [("A", str(s["base_full"])), ("B", str(s["tool_full"]))], f"of {n}"),
        C.fig("PRs at 80% or more", [("A", str(s["base_80"])), ("B", str(s["tool_80"]))], f"of {n}"),
        C.fig("PRs under 20%", [("A", str(s["base_low"])), ("B", str(s["tool_low"]))], f"of {n}"),
    ])
    return f"""<title>How Far Coverage Goes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{css}</style>
<main>
<header>
  <div class="eyebrow">{n} held-out large SWE-bench PRs · qwen3-coder-30b</div>
  <h1>How far can the coverage tool raise coverage?</h1>
  <p class="lede">With the coverage tool the agent is told which changed lines its test misses and may not stop until
  it reaches them. Mean changed-line coverage goes from <b class="a-A">{s["base_mean"]:.0f}%</b> to
  <b class="a-B">{s["tool_mean"]:.0f}%</b>: <b>{s["tool_mean"] - s["base_mean"]:+.0f} points</b>, higher on {s["wins"]} of {s["both"]} PRs.</p>
</header>

<section aria-label="Headline figures">
  <div class="figures">{figs}</div>
  <p class="small">{key}</p>
</section>

<section>
  <h2>Coverage per pull request</h2>
  <p>Largest gain first. {key}</p>
  <div class="chart">{C.dots_svg(dot_rows, "Changed-line coverage")}</div>
</section>

<section>
  <h2>Every pull request</h2>
  <div class="tablewrap"><table>
    <thead><tr><th>PR</th><th>lines</th><th class="grp k-A">without</th><th class="grp k-B">with</th><th>gain</th></tr></thead>
    <tbody>{trs}</tbody></table></div>
</section>

<section>
  <h2>How this was measured</h2>
  <ul class="small">
    <li>{n} large SWE-bench PRs (50 to 160 executable changed lines), none used while the tools were built or tuned.
    Same harness, model and settings in every run: qwen3-coder-30b, temperature 0.3, at most 125 actions; the agent must
    call <code>verify</code> itself, and a guard undoes any edit outside the test file.</li>
    <li>Coverage is measured after the run on the handed-in test with the change applied, over the executable lines
    the PR adds. Only fail-to-pass tests are counted.</li>
  </ul>
</section>
</main>
"""


def build_md():
    runs = load()
    rs = rows(runs)
    s = stats(rs)
    n = len(PRS)
    order = sorted(rs, key=lambda r: -((r["tool"] or 0) - (r["base"] or 0)))
    fmt = lambda v: "–" if v is None else f"{v:.1f}%"
    L = ["# How far can the coverage tool raise coverage?", "",
         f"{n} held-out large SWE-bench PRs, qwen3-coder-30b. Charts: [coverage.html](coverage.html).", "",
         f"Mean changed-line coverage goes from **{s['base_mean']:.1f}%** without the coverage tool to "
         f"**{s['tool_mean']:.1f}%** with it (**{s['tool_mean'] - s['base_mean']:+.1f} points**), higher on {s['wins']} "
         f"of {s['both']} PRs.", "",
         "| | without the tool | with the tool |", "|---|---:|---:|",
         f"| Mean changed-line coverage | {s['base_mean']:.1f}% | {s['tool_mean']:.1f}% |",
         f"| PRs at 100% | {s['base_full']} | {s['tool_full']} |",
         f"| PRs at 80% or more | {s['base_80']} | {s['tool_80']} |",
         f"| PRs under 20% | {s['base_low']} | {s['tool_low']} |", "",
         "## Every pull request", "",
         "| PR | lines | without | with | gain |", "|---|---:|---:|---:|---:|"]
    for r in order:
        gap = (r["tool"] - r["base"]) if r["tool"] is not None and r["base"] is not None else None
        L.append(f"| {C.short(r['id'])} | {C.LINES[r['id']]} | {fmt(r['base'])} | {fmt(r['tool'])} | "
                 f"{'–' if gap is None else f'{gap:+.1f}'} |")
    L += ["", "## How this was measured", "",
          f"- {n} large SWE-bench PRs (50 to 160 executable changed lines), none used while the tools were built or "
          "tuned. Same harness, model and settings in every run: qwen3-coder-30b, temperature 0.3, at most 125 "
          "actions; the agent must call `verify` itself, and a guard undoes any edit outside the test file.",
          "- Coverage is measured after the run on the handed-in test with the change applied, over the executable "
          "lines the PR adds. Only fail-to-pass tests are counted.", ""]
    return "\n".join(L)


if __name__ == "__main__":
    OUT.write_text(build())
    MD.write_text(build_md())
    print(OUT.relative_to(C.ROOT))
    print(MD.relative_to(C.ROOT))
