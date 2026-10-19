"""Build the ChaCo base vs base-coverage compare page from the two run folders."""
import html
import json
from pathlib import Path

ROOT = Path("<repo>")
OUTS = ROOT / "chaco-outs"
GROUPS = json.loads((ROOT / "datasets/chaco/pr-groups.json").read_text())
NB = GROUPS["not_behavioural"]["ids"]
NP = GROUPS["not_python"]["ids"]
OUT = Path(__file__).parent / "chaco-coverage-tool.html"


def load(arm):
    return {f.parent.name: json.loads(f.read_text()) for f in sorted((OUTS / arm).glob("*/result.json"))}


A, B = load("base"), load("base-coverage")
# Compared: the behavioural PRs only (user, 2026-10-13). The not-behavioural PRs were run
# but are left out of every figure; the Rust PRs were never run. Both are listed at the end.
ids = sorted((i for i in A if i not in NB),
             key=lambda i: (i.split("__")[0].lower(), int(i.rsplit("-", 1)[1])))
import re
SWALLOW = re.compile(r"except(\s+(Exception|BaseException))?\s*(as \w+)?\s*:\s*\n(\s*#[^\n]*\n)*\s*pass\b")


def swallows(arm, i):
    return any(SWALLOW.search(f.read_text(errors="replace"))
               for f in (OUTS / arm / i).glob("test_f2p_*.py"))


def cov(r):
    c = r.get("changed_line_coverage") or {}
    return c if r.get("f2p") == "YES" and c.get("measured") else None


def mut(r):
    m = r.get("mutation") or {}
    a = m.get("agent") or {}
    return (a.get("killed"), m.get("total")) if m.get("measured") and m.get("total") else None


def short(i):
    repo, num = i.split("__")[0], i.rsplit("-", 1)[1]
    return {"scipy": "SciPy", "pandas-dev": "pandas", "Qiskit": "Qiskit"}[repo] + " " + num


both = [i for i in ids if cov(A[i]) and cov(B[i])]


def pooled(R, xs):
    h = sum(cov(R[i])["covered"] for i in xs)
    t = sum(cov(R[i])["executable_changed_lines"] for i in xs)
    return h, t


ha, ta = pooled(A, both)
hb, tb = pooled(B, both)
pmean = lambda R: sum(cov(R[i])["percent"] for i in both) / len(both)
pm_a, pm_b = pmean(A), pmean(B)
diffs = [(i, cov(A[i])["percent"], cov(B[i])["percent"]) for i in both]
higher_a = sum(1 for _, x, y in diffs if x > y)
higher_b = sum(1 for _, x, y in diffs if y > x)
same = sum(1 for _, x, y in diffs if x == y)
yes_a = sum(A[i]["f2p"] == "YES" for i in ids)
yes_b = sum(B[i]["f2p"] == "YES" for i in ids)
n = len(ids)
sw_a = sum(swallows("base", i) for i in ids)
sw_b = sum(swallows("base-coverage", i) for i in ids)
own = lambda R: [cov(R[i])["percent"] for i in ids if cov(R[i])]
mean_a, mean_b = sum(own(A)) / len(own(A)), sum(own(B)) / len(own(B))
cost = lambda R: sum((R[i].get("usage") or {}).get("cost_usd") or 0 for i in ids)
acts = lambda R: sum(R[i].get("actions") or 0 for i in ids)
mk = lambda R: (sum(mut(R[i])[0] for i in both if mut(A[i]) and mut(B[i])),
                sum(mut(R[i])[1] for i in both if mut(A[i]) and mut(B[i])))
(ma, mt), (mb, _) = mk(A), mk(B)
pct = lambda h, t: f"{100 * h / t:.1f}%"

# ---- dumbbell chart: coverage per PR YES in both, sorted by gap
rows = sorted(diffs, key=lambda d: d[1] - d[2], reverse=True)
W, left, right, top, rowh = 640, 132, 24, 34, 30
H = top + rowh * len(rows) + 30
x = lambda p: left + (W - left - right) * p / 100
svg = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Changed-line coverage per pull request, with and without the coverage tool">']
for t in (0, 25, 50, 75, 100):
    svg.append(f'<line x1="{x(t):.1f}" y1="{top - 10}" x2="{x(t):.1f}" y2="{H - 26}" class="grid"/>')
    svg.append(f'<text x="{x(t):.1f}" y="{H - 8}" class="tick" text-anchor="middle">{t}%</text>')
for k, (i, a, b) in enumerate(rows):
    y = top + rowh * k + rowh / 2
    lines = cov(A[i])["executable_changed_lines"]
    svg.append(f'<text x="{left - 12}" y="{y + 4:.1f}" class="lab" text-anchor="end">{short(i)}</text>')
    svg.append(f'<text x="{left - 12}" y="{y + 15:.1f}" class="sub" text-anchor="end">{lines} lines</text>')
    svg.append(f'<line x1="{x(min(a, b)):.1f}" y1="{y:.1f}" x2="{x(max(a, b)):.1f}" y2="{y:.1f}" class="bar"/>')
    svg.append(f'<circle cx="{x(b):.1f}" cy="{y:.1f}" r="6" class="dot-b"><title>{short(i)} without the tool: {b:.0f}%</title></circle>')
    svg.append(f'<circle cx="{x(a):.1f}" cy="{y:.1f}" r="6" class="dot-a"><title>{short(i)} with the tool: {a:.0f}%</title></circle>')
svg.append("</svg>")
chart = "\n".join(svg)


def verdict(r):
    v = r.get("f2p", "?")
    rescued = (r.get("second_chance") or {}).get("first_verdict") and v == "YES"
    cls = {"YES": "yes", "NO": "no"}.get(v, "broken")
    return f'<span class="pill {cls}">{v}</span>' + ('<span class="note" title="YES after the restart">rescued</span>' if rescued else "")


def cell_cov(r):
    c = cov(r)
    return f'{c["percent"]:.0f}%' if c else '<span class="dim">–</span>'


def cell_mut(r):
    m = mut(r)
    return f"{m[0]}/{m[1]}" if m and r.get("f2p") == "YES" else '<span class="dim">–</span>'


table = []
for i in ids:
    tag = ""
    differ = A[i]["f2p"] != B[i]["f2p"]
    table.append(
        f'<tr class="{"differ" if differ else ""}"><td><span class="pr">{short(i)}</span>{tag}</td>'
        f"<td>{verdict(A[i])}</td><td class=num>{cell_cov(A[i])}</td><td class=num>{cell_mut(A[i])}</td>"
        f"<td>{verdict(B[i])}</td><td class=num>{cell_cov(B[i])}</td><td class=num>{cell_mut(B[i])}</td></tr>")

flips = [i for i in ids if A[i]["f2p"] != B[i]["f2p"]]
flip_rows = "".join(
    f"<tr><td><span class=pr>{short(i)}</span></td><td>{verdict(A[i])}</td><td>{verdict(B[i])}</td>"
    f"<td>{html.escape((B[i] if B[i]['f2p'] != 'YES' else A[i]).get('why', '')[:80])}</td></tr>" for i in flips)
to_b = sum(1 for i in flips if B[i]["f2p"] == "YES")
to_a = len(flips) - to_b
nb_rows = "".join(f"<li><span class=pr>{short(i)}</span> {html.escape(n)}</li>" for i, n in NB.items())

page = f"""<title>Coverage Tool on ChaCo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@500;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: one reading column; a figures strip, a dot chart, then the evidence tables. */
:root {{
  --bg: #f6f7f9; --surface: #ffffff; --ink: #1b2330; --muted: #5d6878; --rule: #dde2ea;
  --with: #2f5d9e; --without: #c27a1a; --yes: #1f7a4d; --yes-bg: #e3f3ea; --no: #a8352b; --no-bg: #f8e5e2;
  --chip: #eef1f6; --flag: #fff7e6;
  --display: "Schibsted Grotesk", "Helvetica Neue", Arial, sans-serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  --mono: "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #9aa5b5; --rule: #2c3442;
  --with: #7aa7e8; --without: #e6a650; --yes: #6fd19c; --yes-bg: #173327; --no: #f08a7e; --no-bg: #3a1f1c;
  --chip: #252d39; --flag: #2e2716; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --bg: #12161d; --surface: #1a2029; --ink: #e5e9f0; --muted: #9aa5b5; --rule: #2c3442;
  --with: #7aa7e8; --without: #e6a650; --yes: #6fd19c; --yes-bg: #173327; --no: #f08a7e; --no-bg: #3a1f1c;
  --chip: #252d39; --flag: #2e2716; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font: 17px/1.55 var(--body); margin: 0; }}
main {{ max-width: 860px; margin: 0 auto; padding-inline: 20px; padding-block: 40px 64px; display: grid; gap: 40px; }}
h1, h2 {{ font-family: var(--display); text-wrap: balance; margin: 0; line-height: 1.15; }}
h1 {{ font-size: 2.1rem; }}
h2 {{ font-size: 1.3rem; }}
p {{ margin: 0; max-width: 66ch; }}
section {{ display: grid; gap: 14px; min-width: 0; }}
.eyebrow {{ font: 600 .78rem/1 var(--mono); letter-spacing: .08em; text-transform: uppercase; color: var(--muted); }}
.lede {{ font-size: 1.12rem; }}
.key {{ display: inline-flex; align-items: center; gap: 6px; font-weight: 600; white-space: nowrap; }}
.key i {{ width: 11px; height: 11px; border-radius: 50%; display: inline-block; }}
.key.a i {{ background: var(--with); }} .key.b i {{ background: var(--without); }}
.figures {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1px; background: var(--rule); border: 1px solid var(--rule); border-radius: 10px; overflow: hidden; }}
.fig {{ background: var(--surface); padding: 16px 18px; display: grid; gap: 6px; align-content: start; }}
.fig .label {{ font-size: .86rem; color: var(--muted); }}
.fig .vals {{ font: 600 1.35rem/1.2 var(--mono); font-variant-numeric: tabular-nums; display: flex; gap: 10px; align-items: baseline; flex-wrap: wrap; }}
.fig .vals .a {{ color: var(--with); }} .fig .vals .b {{ color: var(--without); }} .fig .vals .vs {{ font-size: .8rem; color: var(--muted); font-weight: 400; }}
.fig .foot {{ font-size: .82rem; color: var(--muted); }}
.chart {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; padding: 14px 10px 6px; overflow-x: auto; }}
.chart svg {{ width: 100%; min-width: 520px; height: auto; display: block; }}
.chart .grid {{ stroke: var(--rule); stroke-width: 1; }}
.chart .tick {{ fill: var(--muted); font: 11px var(--mono); }}
.chart .lab {{ fill: var(--ink); font: 600 13px var(--body); }}
.chart .sub {{ fill: var(--muted); font: 10.5px var(--mono); }}
.chart .bar {{ stroke: var(--muted); stroke-width: 2; opacity: .45; }}
.chart .dot-a {{ fill: var(--with); }} .chart .dot-b {{ fill: var(--without); }}
.callout {{ background: var(--flag); border-left: 3px solid var(--without); padding: 12px 16px; border-radius: 0 8px 8px 0; }}
.tablewrap {{ overflow-x: auto; background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; }}
table {{ border-collapse: collapse; width: 100%; font-size: .93rem; }}
th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid var(--rule); white-space: nowrap; }}
th {{ font: 600 .74rem/1.2 var(--mono); letter-spacing: .05em; text-transform: uppercase; color: var(--muted); }}
th.grp-a {{ color: var(--with); }} th.grp-b {{ color: var(--without); }}
tr:last-child td {{ border-bottom: 0; }}
td.num {{ font-family: var(--mono); font-variant-numeric: tabular-nums; }}
tr.differ td:first-child {{ box-shadow: inset 3px 0 0 var(--without); }}
tr.excluded td {{ background: var(--chip); }}
.pr {{ font-family: var(--mono); font-weight: 600; font-size: .9rem; }}
.pill {{ font: 600 .74rem/1 var(--mono); padding: 4px 7px; border-radius: 4px; }}
.pill.yes {{ color: var(--yes); background: var(--yes-bg); }} .pill.no {{ color: var(--no); background: var(--no-bg); }}
.note {{ margin-left: 6px; font-size: .74rem; color: var(--muted); }}
.chip {{ margin-left: 8px; font-size: .72rem; padding: 2px 7px; border-radius: 99px; background: var(--chip); color: var(--muted); }}
.dim {{ color: var(--muted); }}
ul {{ margin: 0; padding-left: 20px; display: grid; gap: 4px; }}
.small {{ font-size: .9rem; color: var(--muted); }}
@media (max-width: 480px) {{ h1 {{ font-size: 1.7rem; }} body {{ font-size: 16px; }} }}
</style>
<main>
<header style="display:grid;gap:14px">
  <div class="eyebrow">ChaCo ablation set · {n} behavioural pull requests · qwen3-coder-30b</div>
  <h1>Does the coverage tool raise coverage?</h1>
  <p class="lede">We ran the ChaCo pull requests to measure what the <code>coverage</code> tool adds
  to our system. With the tool (<span class="key a"><i></i>base</span>), the agent's tests ran
  <b>{pct(ha, ta)}</b> of the changed lines on the {len(both)} PRs both runs passed. Without it
  (<span class="key b"><i></i>base-coverage</span>) they ran <b>{pct(hb, tb)}</b>. Per PR, the
  average coverage was <b>{pm_a:.1f}%</b> with the tool and <b>{pm_b:.1f}%</b> without, and the
  tool's tests covered more on {higher_a} of those PRs against {higher_b}. Fail-to-pass barely moves:
  {yes_a} of {n} with the tool, {yes_b} without.</p>
</header>

<section aria-label="Headline figures">
<div class="figures">
  <div class="fig"><div class="label">Changed lines covered, PRs YES in both</div>
    <div class="vals"><span class="a">{pct(ha, ta)}</span><span class="vs">vs</span><span class="b">{pct(hb, tb)}</span></div>
    <div class="foot">{ha} vs {hb} of {ta} lines, {len(both)} PRs</div></div>
  <div class="fig"><div class="label">Mean coverage per PR, PRs YES in both</div>
    <div class="vals"><span class="a">{pm_a:.1f}%</span><span class="vs">vs</span><span class="b">{pm_b:.1f}%</span></div>
    <div class="foot">each run's own YES PRs: {mean_a:.1f}% ({len(own(A))}) vs {mean_b:.1f}% ({len(own(B))})</div></div>
  <div class="fig"><div class="label">Fail-to-pass</div>
    <div class="vals"><span class="a">{yes_a}/{n}</span><span class="vs">vs</span><span class="b">{yes_b}/{n}</span></div>
    <div class="foot">{n} behavioural pull requests</div></div>
  <div class="fig"><div class="label">Which side covered more, per PR</div>
    <div class="vals"><span class="a">{higher_a}</span><span class="vs">to</span><span class="b">{higher_b}</span></div>
    <div class="foot">of {len(both)} PRs YES in both; {same} tied</div></div>
</div>
</section>

<section>
  <h2>Coverage per pull request</h2>
  <p>The {len(both)} PRs where both runs wrote a fail-to-pass test, sorted by how much the tool helped.
  <span class="key a"><i></i>with the tool</span> &nbsp; <span class="key b"><i></i>without</span></p>
  <div class="chart">{chart}</div>
  <p class="small">The first figure above pools lines, so a large PR counts for more: SciPy 21700 adds a
  whole module (156 changed lines), and the tool took its test from 38% to 83%. The mean counts every PR
  once.</p>
</section>

<section>
  <h2>The same switch on SWE-bench</h2>
  <p>On the 36 SWE-bench PRs, removing the tool took pooled coverage from <b>81.8%</b> to <b>52.0%</b>
  over the 25 PRs both runs passed, and the per-PR mean from <b>94.7%</b> to <b>90.5%</b>, with
  fail-to-pass 29 against 28. ChaCo repeats the pattern on another dataset: coverage drops without the
  tool, and fail-to-pass does not.</p>
</section>

<section>
  <h2>Other measures</h2>
  <div class="tablewrap"><table>
    <thead><tr><th></th><th class="grp-a">base</th><th class="grp-b">base-coverage</th></tr></thead>
    <tbody>
      <tr><td>Mutants caught, pooled over PRs YES in both</td><td class=num>{pct(ma, mt)} ({ma}/{mt})</td><td class=num>{pct(mb, mt)} ({mb}/{mt})</td></tr>
      <tr><td>Agent actions, all {n} PRs</td><td class=num>{acts(A)}</td><td class=num>{acts(B)}</td></tr>
      <tr><td>Model cost, all {n} PRs</td><td class=num>${cost(A):.2f}</td><td class=num>${cost(B):.2f}</td></tr>
      <tr><td>Tests that swallow every error (<code>except Exception: pass</code>)</td><td class=num>{sw_a}</td><td class=num>{sw_b}</td></tr>
    </tbody></table></div>
</section>

<section>
  <h2>Verdicts that differ ({len(flips)})</h2>
  <p>{to_b} PRs passed only without the tool and {to_a} only with it. Each PR was run once per
  configuration.</p>
  <div class="tablewrap"><table>
    <thead><tr><th>PR</th><th class="grp-a">base</th><th class="grp-b">base-coverage</th><th>why the NO side failed</th></tr></thead>
    <tbody>{flip_rows}</tbody></table></div>
</section>

<section>
  <h2>Every pull request</h2>
  <p class="small">Coverage and mutants are shown for YES runs only. A stripe marks a verdict that differs.</p>
  <div class="tablewrap"><table>
    <thead><tr><th rowspan="2">PR</th><th colspan="3" class="grp-a">base (with tool)</th><th colspan="3" class="grp-b">base-coverage (without)</th></tr>
    <tr><th>verdict</th><th>coverage</th><th>mutants</th><th>verdict</th><th>coverage</th><th>mutants</th></tr></thead>
    <tbody>{''.join(table)}</tbody></table></div>
</section>

<section>
  <h2>Pull requests left out</h2>
  <p>ChaCo's ablation list has 30 pull requests. Seven are left out of this comparison:</p>
  <p><b>Not behavioural (5).</b> {html.escape(GROUPS['not_behavioural']['why'])} They were run, but no
  test of them can say anything about coverage, so they are not compared.</p>
  <ul>{nb_rows}</ul>
  <p><b>Not Python (2).</b> Qiskit 13704 and 12495 change Rust code. The image builds the Rust extension
  once, so the harness cannot apply and revert the change, and they were not run.</p>
</section>

<section>
  <h2>How this was measured</h2>
  <ul class="small">
    <li>Both runs use the same harness and model (qwen3-coder-30b, temperature 0.3, 125 actions, 20 mutants), the same pull requests and one run per PR. The only difference is the <code>coverage</code> tool, which lists the changed lines the agent's test never runs.</li>
    <li>Coverage is measured by the harness after the run, on the agent's final test with the change applied, over the executable lines the PR changed.</li>
    <li>The pooled figure divides covered lines by all changed lines on the PRs both runs passed, so both sides share one denominator. The mean averages each PR's percentage over the same PRs.</li>
    <li>Every trajectory of both runs was read before this comparison; no run was dropped or rerun for its result.</li>
  </ul>
</section>
</main>
"""
OUT.write_text(page)
print(OUT, len(page))
