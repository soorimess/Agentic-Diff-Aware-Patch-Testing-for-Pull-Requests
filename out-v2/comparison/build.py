"""The comparison page as Markdown: `out-v2/comparison/README.md`, `data.json`, `charts/`.

    python3 out-v2/comparison/build.py

Reads the same experiment documents the page "F2P Flag Ablations" shows
(`out-v2/dashboard/<arm>.json`, built by `tools/pick_extremes.py` + `tools/dashboard_data.py`)
and computes the same figures the page computes: the scoreboard, each experiment against base
(with per-PR line charts), what each flag does, and every PR.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
DASH = HERE.parent / "dashboard"
CHARTS = HERE / "charts"

FLAG_COLS = [("verify-tool", "verify"), ("coverage-tool", "coverage"), ("mutation-tool", "mutation"),
             ("guard", "guard"), ("require-tools", "require-tools"),
             ("require-tools-with-score-report", "scores shown"), ("second-chance", "second chance")]
PAIRS = [
    ("Second chance", "require-tools on", "base", "no-second-chance"),
    ("Second chance", "require-tools off", "no-require-tools", "no-second-chance-no-require-tools"),
    ("Require-tools", "second chance on", "base", "no-require-tools"),
    ("Require-tools", "second chance off", "no-second-chance", "no-second-chance-no-require-tools"),
    ("Require-tools", "without coverage and mutation", "no-coverage-no-mutation",
     "no-coverage-no-mutation-no-require-tools"),
    ("Guard", "everything else on", "base", "no-guard"),
    ("Scores shown", "everything else on", "require-tools-with-score", "base"),
    ("Verify (and coverage, mutation, require-tools)", "guard and second chance on", "base", "no-verify"),
    ("Coverage tool", "everything else on", "base", "no-coverage"),
    ("Mutation tool", "everything else on", "base", "no-mutation"),
    ("Coverage and mutation tools", "everything else on", "base", "no-coverage-no-mutation"),
]


def yes(r): return bool(r) and r["v"] == "YES"
def rescued(r): return yes(r) and r["first"] != "YES"
def short(i): return i.split("__", 1)[1]
def pct(h, t): return f"{100 * h / t:.1f}%" if t else "–"
def mean(xs): return sum(xs) / len(xs) if xs else None
def fmt(x): return "–" if x is None else f"{x:.1f}%"


def summary(e):
    rs = list(e["runs"].values())
    return {"yes": sum(map(yes, rs)), "n": len(rs), "first": sum(r["first"] == "YES" for r in rs),
            "rescued": sum(map(rescued, rs)),
            "cov": mean([100 * r["ch"] / r["ct"] for r in rs if yes(r) and r.get("ct")]),
            "covN": sum(1 for r in rs if yes(r) and r.get("ct")),
            "mut": mean([100 * r["mk"] / r["mt"] for r in rs if yes(r) and r.get("mt")]),
            "mutN": sum(1 for r in rs if yes(r) and r.get("mt")),
            "actions": sum(r["a"] for r in rs), "cost": sum(r["c"] for r in rs)}


def quality(A, B, kh, kt):
    """Pooled over the PRs YES in both with the measure in both; plus the PR that moves the gap
    most, when one does (the page's leave-one-out row)."""
    ids = [i for i in A["runs"] if i in B["runs"] and yes(A["runs"][i]) and yes(B["runs"][i])
           and A["runs"][i].get(kt) and A["runs"][i].get(kt) == B["runs"][i].get(kt)]

    def pool(xs):
        return (sum(A["runs"][i][kh] for i in xs), sum(B["runs"][i][kh] for i in xs),
                sum(A["runs"][i][kt] for i in xs))
    full = pool(ids)
    gap = lambda p: (p[1] - p[0]) / p[2] if p[2] else 0
    drop, rest, best = None, None, 1e-9
    if len(ids) > 1:
        for i in ids:
            r = pool([j for j in ids if j != i])
            if abs(gap(full) - gap(r)) > best:
                best, drop, rest = abs(gap(full) - gap(r)), i, r
    return {"n": len(ids), "full": full, "drop": drop, "rest": rest}


def svg_chart(cats, series, title):
    """A line chart, 0-100%, fixed colours on a white ground (renders the same on GitHub's
    light and dark themes)."""
    W, H, L, R, T, B = 800, 300, 84, 16, 48, 96
    pw, ph, n = W - L - R, H - T - B, len(cats)
    x = lambda i: L + (pw / 2 if n == 1 else i * pw / (n - 1))
    y = lambda v: T + ph * (1 - v / 100)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="Menlo, monospace">', f'<rect width="{W}" height="{H}" fill="#ffffff"/>',
           f'<text x="{L - 70}" y="18" font-size="13" font-weight="600" fill="#18212b" '
           f'font-family="Helvetica, Arial, sans-serif">{title}</text>']
    for v in (0, 25, 50, 75, 100):
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(v):.1f}" y2="{y(v):.1f}" stroke="#dbe1e7"/>'
                   f'<text x="{L - 6}" y="{y(v) + 3.5:.1f}" font-size="10.5" fill="#5d6977" '
                   f'text-anchor="end">{v}%</text>')
    for i, c in enumerate(cats):
        ty = H - B + 14
        out.append(f'<text x="{x(i):.1f}" y="{ty}" font-size="10.5" fill="#5d6977" text-anchor="end" '
                   f'transform="rotate(-40 {x(i):.1f} {ty})">{c}</text>')
    lx = L - 70
    for name, color, dash, vals in series:
        pts = [(x(i), y(v)) for i, v in enumerate(vals) if v is not None]
        d = " ".join(("M" if k == 0 else "L") + f"{px:.1f},{py:.1f}" for k, (px, py) in enumerate(pts))
        out.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2"'
                   + (' stroke-dasharray="5 4"' if dash else "") + "/>")
        out += [f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{color}" stroke="#ffffff" '
                f'stroke-width="1.5"/>' for px, py in pts]
        out.append(f'<rect x="{lx}" y="31" width="16" height="3" fill="{color}"/>'
                   f'<text x="{lx + 22}" y="36" font-size="11" fill="#5d6977" '
                   f'font-family="Helvetica, Arial, sans-serif">{name}</text>')
        lx += 22 + 7 * len(name) + 24
    out.append("</svg>")
    return "\n".join(out)


def pair_chart(A, B, kh, kt, title, path):
    ids = [i for i in A["runs"] if i in B["runs"] and yes(A["runs"][i]) and yes(B["runs"][i])
           and A["runs"][i].get(kt) and B["runs"][i].get(kt)]
    if not ids:
        return None
    v = lambda R, i: 100 * R["runs"][i][kh] / R["runs"][i][kt]
    ids.sort(key=lambda i: (-v(A, i), i))
    path.write_text(svg_chart([short(i) for i in ids], [
        (A["label"], "#0f6e7a", False, [v(A, i) for i in ids]),
        (B["label"], "#b7791f", True, [v(B, i) for i in ids])], title))
    return path


def main():
    exps = {p.stem: json.loads(p.read_text()) for p in sorted(DASH.glob("*.json"))}
    order = sorted(exps, key=lambda k: exps[k].get("order", 99))
    base = exps["base"]
    ids = sorted({i for e in exps.values() for i in e["runs"]})
    CHARTS.mkdir(exist_ok=True)
    (HERE / "data.json").write_text(json.dumps(exps, indent=1))

    md = ["# F2P Flag Ablations", "",
          "An agent writes a test that must fail before a SWE-bench fix and pass after it. Each "
          "experiment runs the same 36 pull requests with one set of add-ons, and this page compares "
          "what they produced.", "",
          "PRs **36** · model **qwen3-coder-30b-a3b** · temperature **0.3** · action cap **125** · "
          "mutants **20**, scored on the held-out half · per PR: base's best run, each other "
          "experiment's worst", "",
          "## Scoreboard", ""]
    flags_h = " | ".join(lbl for _, lbl in FLAG_COLS)
    md += [f"| Experiment | {flags_h} | YES | first attempt | after restart | coverage, pooled over PRs "
           f"YES in both with base | coverage, mean | mutants caught, mean | actions | cost |",
           "|---|" + "---|" * len(FLAG_COLS) + "---:|---:|---:|---:|---:|---:|---:|---:|"]
    for k in order:
        e = exps[k]
        s = summary(e)
        dots = " | ".join("●" if e["flags"].get(f) else "○" for f, _ in FLAG_COLS)
        if k == "base":
            pooled = "reference"
        else:
            q = quality(base, e, "ch", "ct")
            ha, hb, t = q["full"]
            pooled = f"{pct(hb, t)} (base {pct(ha, t)}, {q['n']} PRs)" if t else "–"
        md.append(f"| **{e['label']}** | {dots} | **{s['yes']}/{s['n']}** | {s['first']} | "
                  f"{s['rescued'] or '–'} | {pooled} | {fmt(s['cov'])} ({s['covN']}) | "
                  f"{fmt(s['mut'])} ({s['mutN']}) | {s['actions']:,} | ${s['cost']:.2f} |")
    md += ["", "● on · ○ off. Means: the per-PR figures averaged over the experiment's own YES PRs. "
           "Pooled: covered lines over all changed lines on the PRs YES in both the experiment and base.", ""]

    md += ["## Each experiment against base", ""]
    for k in order:
        if k == "base":
            continue
        A, B = base, exps[k]
        sa, sb = summary(A), summary(B)
        cov, mut = quality(A, B, "ch", "ct"), quality(A, B, "mk", "mt")
        both = sum(1 for i in A["runs"] if i in B["runs"] and yes(A["runs"][i]) and yes(B["runs"][i]))
        md += [f"### Base vs {B['label']}", "",
               f"| | Base | {B['label']} |", "|---|---:|---:|",
               f"| fail-to-pass | {sa['yes']}/{sa['n']} | {sb['yes']}/{sb['n']} |",
               f"| first attempt | {sa['first']} | {sb['first']} |",
               f"| YES after the restart | {sa['rescued'] or '–'} | {sb['rescued'] or '–'} |",
               f"| coverage, mean of per-PR over own YES | {fmt(sa['cov'])} | {fmt(sb['cov'])} |",
               f"| mutants caught, mean of per-PR over own YES | {fmt(sa['mut'])} | {fmt(sb['mut'])} |"]
        for lab, q in (("changed-line coverage", cov), ("mutants caught", mut)):
            ha, hb, t = q["full"]
            md.append(f"| {lab}, pooled over {q['n']} PRs YES in both | {pct(ha, t)} ({ha}/{t}) | "
                      f"{pct(hb, t)} ({hb}/{t}) |")
            if q["drop"]:
                ra, rb, rt = q["rest"]
                md.append(f"| &nbsp;&nbsp;without `{short(q['drop'])}`, the PR that moves the gap most "
                          f"| {pct(ra, rt)} | {pct(rb, rt)} |")
        md += [f"| actions | {sa['actions']:,} | {sb['actions']:,} |",
               f"| model cost | ${sa['cost']:.2f} | ${sb['cost']:.2f} |", "",
               f"{both} PRs are YES in both.", ""]
        flips = [i for i in A["runs"] if i in B["runs"] and A["runs"][i]["v"] != B["runs"][i]["v"]]
        if flips:
            md += [f"Verdicts that differ ({len(flips)}): " + ", ".join(
                f"`{short(i)}` {A['runs'][i]['v']}→{B['runs'][i]['v']}" for i in sorted(flips)), ""]
        for kh, kt, what in (("ch", "ct", "coverage"), ("mk", "mt", "mutants")):
            p = pair_chart(A, B, kh, kt, f"{'Coverage' if what == 'coverage' else 'Mutants caught'} per PR, "
                           f"PRs YES in both: Base vs {B['label']}", CHARTS / f"base-vs-{k}-{what}.svg")
            if p:
                md += [f"![{what} per PR, base vs {B['label']}](charts/{p.name})", ""]

    md += ["## What each flag does", "",
           "Each row compares two experiments that differ only by that flag. The means are over each "
           "experiment's own YES PRs; the detail columns pool lines and mutants over the PRs YES in both.", "",
           "| Flag | Other flags | YES, on vs off | coverage mean | mutants mean | detail: lines covered, "
           "PRs YES in both | detail: mutants caught, PRs YES in both | cost |",
           "|---|---|---:|---:|---:|---:|---:|---:|"]
    for flag, ctx, on, off in PAIRS:
        if on not in exps or off not in exps:
            continue
        A, B = exps[on], exps[off]
        sa, sb = summary(A), summary(B)
        cells = []
        for q in (quality(A, B, "ch", "ct"), quality(A, B, "mk", "mt")):
            ha, hb, t = q["full"]
            c = f"{pct(ha, t)} vs {pct(hb, t)} · {q['n']} PRs"
            if q["drop"]:
                ra, rb, rt = q["rest"]
                c += f"<br>without {short(q['drop'])}: {pct(ra, rt)} vs {pct(rb, rt)}"
            cells.append(c)
        d = sa["yes"] - sb["yes"]
        md.append(f"| {flag} | {ctx} | {sa['yes']} vs {sb['yes']} ({d:+d}) | {fmt(sa['cov'])} vs "
                  f"{fmt(sb['cov'])} | {fmt(sa['mut'])} vs {fmt(sb['mut'])} | {cells[0]} | {cells[1]} | "
                  f"${sa['cost']:.2f} vs ${sb['cost']:.2f} |")

    md += ["", "## Every PR", "",
           "Each cell: the verdict and, for a YES, changed-line coverage. ↻ marks a YES reached after "
           "the restart.", "",
           "| PR | " + " | ".join(exps[k]["label"] for k in order) + " |",
           "|---|" + "---:|" * len(order)]
    for i in ids:
        cells = []
        for k in order:
            r = exps[k]["runs"].get(i)
            if not r:
                cells.append("–")
            elif yes(r):
                cells.append(("↻ " if rescued(r) else "") + (f"{round(100 * r['ch'] / r['ct'])}%"
                                                            if r.get("ct") else "YES"))
            else:
                cells.append("NO")
        md.append(f"| `{short(i)}` | " + " | ".join(cells) + " |")
    (HERE / "README.md").write_text("\n".join(md) + "\n")
    print(f"wrote README.md, data.json and {len(list(CHARTS.glob('*.svg')))} charts")


if __name__ == "__main__":
    main()
