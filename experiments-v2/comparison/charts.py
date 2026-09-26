"""The comparison's charts, as standalone SVG files. The README links them; the page inlines them.

One drawing, two hosts. Colour goes through classes whose fill is a CSS variable with a
fallback: on GitHub nothing defines the variable, so the fallback applies and a
prefers-color-scheme block inside the file switches it for a dark page; on the artifact
page the variables are defined for both themes, so the same markup follows the page's
theme toggle as well. Nothing else differs between the two.

    python experiments-v2/comparison/charts.py experiments-v2/comparison/data.json
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "charts"

# name: (light, dark). Semantic colours are separate from the one accent (base).
PALETTE = {
    "ink": ("#4a5260", "#9aa3ae"), "strong": ("#161b22", "#e8ecf1"),
    "dim": ("#8a929c", "#6b737d"), "grid": ("#dde2e8", "#2b3138"),
    "base": ("#5b4bd6", "#9d8cff"), "down": ("#c8322d", "#ff6b64"),
    "up": ("#1f7a44", "#4fcf7f"), "flat": ("#8a929c", "#59616b"),
    "sig": ("#2463c7", "#6ea8ff"), "ghost": ("#c9ced6", "#3a414a"),
    "l1": ("#c8322d", "#ff6b64"), "l2": ("#e0883a", "#f0a35a"),
    "l3": ("#c9b458", "#d9c46a"), "l4": ("#6fae7c", "#6fce8a"),
    "l5": ("#1f7a44", "#3fb970"),
    "m-broken": ("#c8322d", "#ff6b64"), "m-base": ("#c28a1a", "#e3b341"),
    "m-coll": ("#7a55d6", "#a88bff"), "m-notest": ("#8a929c", "#6b737d"),
    "m-other": ("#c9ced6", "#3a414a"), "chip": ("#ffffff", "#0e1116"),
    # Each chart paints its own ground. Without it the text colour followed the viewer's
    # system theme while the ground was whatever the host drew -- a light README preview on
    # a dark-mode machine showed near-white labels on white.
    "bg": ("#ffffff", "#151a21"),
}
FONT = "ui-sans-serif,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def style() -> str:
    light = "".join(
        f".k-{k}{{fill:var(--k-{k},{v[0]})}}.s-{k}{{stroke:var(--k-{k},{v[0]})}}"
        for k, v in PALETTE.items())
    dark = "".join(
        f".k-{k}{{fill:var(--k-{k},{v[1]})}}.s-{k}{{stroke:var(--k-{k},{v[1]})}}"
        for k, v in PALETTE.items())
    return (f"<style>svg.cmp text{{font-family:{FONT}}}{light}"
            f"@media (prefers-color-scheme: dark){{{dark}}}</style>")


def esc(s) -> str:
    return html.escape(str(s))


def svg(w: int, h: int, body: str, title: str) -> str:
    return (f"<svg class='cmp' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' "
            f"width='{w}' height='{h}' role='img' aria-label='{esc(title)}'>"
            f"<title>{esc(title)}</title>{style()}"
            f"<rect width='{w}' height='{h}' rx='8' class='k-bg'/>{body}</svg>")


def t(x, y, s, size=12, cls="ink", anchor="start", weight="normal") -> str:
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' class='k-{cls}' "
            f"text-anchor='{anchor}' font-weight='{weight}'>{esc(s)}</text>")


def r(x, y, w, h, cls, rx=2) -> str:
    return (f"<rect x='{x:.1f}' y='{y:.1f}' width='{max(w, 0):.1f}' height='{h:.1f}' "
            f"rx='{rx}' class='k-{cls}'/>")


def tb(x, y, s, size=11, cls="strong") -> str:
    """A label on a patch of the chart's own ground, so grid lines never run through it."""
    w = len(str(s)) * size * 0.6 + 6
    return (f"<rect x='{x - 3:.1f}' y='{y - size:.1f}' width='{w:.1f}' height='{size + 5}' "
            f"class='k-bg'/>" + t(x, y, s, size, cls))


def pale(x, y, w, h, cls) -> str:
    """The part of a bar the retry added: same hue, lighter on either ground."""
    return (f"<rect x='{x:.1f}' y='{y:.1f}' width='{max(w, 0):.1f}' height='{h:.1f}' "
            f"rx='2' class='k-{cls}' opacity='0.42'/>")


def ln(x1, y1, x2, y2, cls="grid", w=1, dash="") -> str:
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return (f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' "
            f"class='s-{cls}' stroke-width='{w}'{d}/>")


def pfmt(p: float) -> str:
    return "p<0.001" if p < 0.001 else f"p={p:.3f}" if p < 0.01 else f"p={p:.2f}"


def name(a) -> str:
    return f"{a['num']}  {a['label']}"


# ----------------------------------------------------------------- scoreboard
def scoreboard(d) -> str:
    """The four scores on one grid: F2P as a count, the rest as paired movements."""
    arms = d["arms"]
    W, top, rh = 1000, 78, 34
    H = top + rh * len(arms) + 62
    c_name, c_f2p, c_cov, c_mut, c_jud = 16, 180, 450, 630, 800
    b = [t(c_f2p, 26, "fail-to-pass", 13, "strong", weight="600"),
         t(c_f2p, 44, "of 70 · one attempt each", 11, "dim"),
         t(c_cov + 70, 26, "coverage", 13, "strong", "middle", "600"),
         t(c_cov + 70, 44, "vs base: worse | better", 11, "dim", "middle"),
         t(c_mut + 70, 26, "mutation", 13, "strong", "middle", "600"),
         t(c_mut + 70, 44, "vs base: worse | better", 11, "dim", "middle"),
         t(c_jud, 26, "judge: concept", 13, "strong", weight="600"),
         t(c_jud, 44, "one judge, five levels", 11, "dim")]
    fx = lambda n: c_f2p + n * 3.0
    b.append(ln(fx(arms[0]["yes"]), top - 12, fx(arms[0]["yes"]), top + rh * len(arms) - 8,
                "base", 1, "3 3"))
    for k, a in enumerate(arms):
        y = top + k * rh
        b.append(t(c_name, y + 13, name(a), 12, "strong" if a["num"] == "1" else "ink",
                   weight="600" if a["num"] == "1" else "normal"))
        vs = a["vs_base"]
        cls = "base" if a["num"] == "1" else ("sig" if vs and vs["p"] <= 0.05 else "flat")
        b.append(r(c_f2p, y + 2, fx(a["first_yes"]) - c_f2p, 16, cls))
        b.append(pale(fx(a["first_yes"]), y + 2, fx(a["yes"]) - fx(a["first_yes"]), 16, cls))
        lab = f"{a['yes']}" + ("" if not vs else f"  {a['yes'] - arms[0]['yes']:+d}")
        b.append(t(max(fx(a["yes"]), fx(arms[0]["yes"])) + 6, y + 14, lab, 11, "strong"))
        for cx, key in ((c_cov, "cov_paired"), (c_mut, "mut_paired")):
            mid = cx + 70
            b.append(ln(mid, y, mid, y + 20, "grid"))
            m = a.get(key)
            if not m:
                b.append(t(mid, y + 14, "reference", 10, "dim", "middle"))
                continue
            u = 7.0
            b.append(r(mid - m["fell"] * u, y + 3, m["fell"] * u, 14, "down"))
            b.append(r(mid, y + 3, m["rose"] * u, 14, "up"))
            b.append(t(mid - m["fell"] * u - 4, y + 14, m["fell"], 10, "ink", "end"))
            b.append(t(mid + m["rose"] * u + 4, y + 14, m["rose"], 10, "ink"))
        tot = sum(a["concept"]) or 1
        x = c_jud
        for lvl in range(5):
            w = 150 * a["concept"][lvl] / tot
            b.append(r(x, y + 3, w, 14, f"l{lvl + 1}", 0))
            x += w
        b.append(t(c_jud + 156, y + 14, f"{a['judged']}", 10, "dim"))
    y = top + rh * len(arms) + 12
    lg = [("different", "l1"), ("tangential", "l2"), ("narrower", "l3"), ("close", "l4"),
          ("equivalent", "l5")]
    x = c_f2p + 330
    b.append(t(x - 8, y + 8, "judge:", 10, "dim", "end"))
    for lab, cls in lg:
        b.append(r(x, y, 9, 9, cls, 1)); b.append(t(x + 12, y + 8, lab, 10, "ink"))
        x += 13 + len(lab) * 6.2 + 12
    b.append(r(c_f2p, y, 9, 9, "sig", 1))
    b.append(t(c_f2p + 12, y + 8, "paired p ≤ 0.05 vs base", 10, "ink"))
    b.append(r(c_f2p + 150, y, 9, 9, "flat", 1))
    b.append(t(c_f2p + 162, y + 8, "not significant", 10, "ink"))
    return svg(W, H, "".join(b), "The four scores, arm by arm")


# ----------------------------------------------------------------- fail-to-pass
def f2p(d) -> str:
    arms = d["arms"]
    W, top, rh, x0 = 760, 30, 30, 200
    H = top + rh * len(arms) + 40
    sx = lambda n: x0 + n * 7.2
    b = [ln(sx(v), top - 8, sx(v), top + rh * len(arms), "grid") for v in range(0, 71, 10)]
    b += [t(sx(v), top + rh * len(arms) + 16, v, 10, "dim", "middle") for v in range(0, 71, 10)]
    b.append(ln(sx(arms[0]["yes"]), top - 12, sx(arms[0]["yes"]), top + rh * len(arms),
                "base", 1.5, "4 3"))
    for k, a in enumerate(arms):
        y = top + k * rh
        vs = a["vs_base"]
        cls = "base" if not vs else ("sig" if vs["p"] <= 0.05 else "flat")
        b.append(t(16, y + 14, name(a), 12, "strong" if not vs else "ink"))
        b.append(r(x0, y + 2, sx(a["first_yes"]) - x0, 18, cls))
        b.append(pale(sx(a["first_yes"]), y + 2, sx(a["yes"]) - sx(a["first_yes"]), 18, cls))
        lab = f"{a['yes']}" if not vs else (f"{a['yes']}   {a['yes'] - arms[0]['yes']:+d}   "
                                            f"{pfmt(vs['p'])}")
        b.append(tb(max(sx(a["yes"]), sx(arms[0]["yes"])) + 8, y + 15, lab))
    b.append(t(x0, 14, "one attempt per instance · dashed line = base", 11, "dim"))
    return svg(W, H, "".join(b), "Fail-to-pass per arm")


# ----------------------------------------------------------------- v1 against v2
def v1v2(d) -> str:
    """Each arm's fail-to-pass in v1 (first attempt, and best of two) and in v2 (one attempt)."""
    arms = d["arms"]
    W, top, rh, x0 = 760, 46, 28, 200
    H = top + rh * len(arms) + 34
    sx = lambda n: x0 + (n - 20) * 12.0
    b = [ln(sx(v), top - 8, sx(v), top + rh * len(arms), "grid") for v in range(20, 61, 10)]
    b += [t(sx(v), top + rh * len(arms) + 16, v, 10, "dim", "middle") for v in range(20, 61, 10)]
    lg = [("v1 first attempt", "ghost"), ("v1 best of two", "flat"), ("v2, one attempt", "base")]
    x = x0
    ring = lambda cx, cy, r: (f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r}' class='k-bg s-strong' "
                              f"stroke-width='2'/>")
    for lab, cls in lg:
        b.append(ring(x + 5, 17, 5) if cls == "flat" else
                 f"<circle cx='{x + 5:.1f}' cy='17' r='5' class='k-{cls}'/>")
        b.append(t(x + 14, 21, lab, 11, "ink"))
        x += 30 + len(lab) * 6.2
    for k, a in enumerate(arms):
        y = top + k * rh + 10
        v1 = d["v1"].get(a["dir"], {})
        b.append(t(16, y + 4, name(a), 12, "strong" if a["num"] == "1" else "ink"))
        xs = [sx(v1.get("first_yes", a["yes"])), sx(v1.get("yes", a["yes"])), sx(a["yes"])]
        b.append(ln(min(xs), y, max(xs), y, "grid", 2))
        for xx, cls in zip(xs, ("ghost", "flat", "base")):
            b.append(ring(xx, y, 6) if cls == "flat" else
                     f"<circle cx='{xx:.1f}' cy='{y:.1f}' r='6' class='k-{cls}'/>")
        b.append(tb(max(xs) + 12, y + 4, f"{v1.get('first_yes', '?')} · {v1.get('yes', '?')} · "
                                         f"{a['yes']}", 11))
    return svg(W, H, "".join(b), "Fail-to-pass, v1 against v2")


# ----------------------------------------------------------------- failure modes
MODES = [("broken", "still fails after the fix", "m-broken"),
         ("passes_at_base", "passes before the fix", "m-base"),
         ("collects_nothing", "collects nothing", "m-coll"),
         ("no_test", "wrote no test", "m-notest"),
         ("other", "other", "m-other")]


def failures(d) -> str:
    arms = d["arms"]
    W, top, rh, x0 = 760, 44, 26, 200
    H = top + rh * len(arms) + 30
    sx = lambda n: n * 12.0
    b = []
    x = x0
    for key, lab, cls in MODES:
        b.append(r(x, 12, 10, 10, cls, 1)); b.append(t(x + 14, 21, lab, 11, "ink"))
        x += 20 + len(lab) * 5.6
    for k, a in enumerate(arms):
        y = top + k * rh
        b.append(t(16, y + 13, name(a), 12, "ink"))
        x = x0
        for key, _, cls in MODES:
            n = a["why"].get(key, 0) + (a["why"].get("voided", 0) if key == "other" else 0)
            if n:
                b.append(r(x, y + 2, sx(n), 16, cls, 0))
                if n >= 2:
                    b.append(t(x + sx(n) / 2, y + 14, n, 10, "chip", "middle"))
                x += sx(n)
    return svg(W, H, "".join(b), "What the failures were")


# ----------------------------------------------------------------- the corpus
def patches(d) -> str:
    s = d["patch_sizes"]
    W, H, x0, y0 = 760, 200, 40, 160
    bw = (W - x0 - 20) / len(s)
    mx = max(s)
    b = [ln(x0, y0, W - 20, y0, "grid")]
    for i, v in enumerate(s):
        h = 130 * v / mx
        b.append(r(x0 + i * bw + 1, y0 - h, bw - 2, h, "base" if i < 5 else "flat", 1))
    b.append(t(x0, 18, f"executable lines each of the 70 fixes adds, largest first — "
               f"{d['corpus_lines']} in all", 11, "dim"))
    top5 = sum(s[:5])
    lx = x0 + 5 * bw + 60
    b.append(ln(x0 + 5 * bw, 62, lx - 6, 62, "grid", 1))
    b.append(t(lx, 66, f"the five largest: {top5} lines, "
               f"{round(100 * top5 / d['corpus_lines'])}% of the corpus", 11, "strong"))
    b.append(t(x0, y0 + 16, "one bar per pull request", 10, "dim"))
    return svg(W, H, "".join(b), "The corpus is lopsided")


# ----------------------------------------------------------------- coverage, three ways
def coverage3(d) -> str:
    arms = d["arms"]
    W, top, rh, x0 = 760, 44, 30, 200
    H = top + rh * len(arms) + 30
    sx = lambda p: x0 + p * 4.6
    keys = [("cov_mean", "mean per test", "flat"), ("cov_pooled", "pooled", "sig"),
            ("cov_share", f"share of all {d['corpus_lines']}", "base")]
    b = []
    x = x0
    for _, lab, cls in keys:
        b.append(r(x, 12, 10, 10, cls, 1)); b.append(t(x + 14, 21, lab, 11, "ink"))
        x += 30 + len(lab) * 6.2
    b += [ln(sx(v), top - 6, sx(v), top + rh * len(arms), "grid") for v in range(0, 101, 20)]
    b += [t(sx(v), top + rh * len(arms) + 14, f"{v}%", 10, "dim", "middle")
          for v in range(0, 101, 20)]
    for k, a in enumerate(arms):
        y = top + k * rh
        b.append(t(16, y + 16, name(a), 12, "ink"))
        for j, (key, _, cls) in enumerate(keys):
            v = a[key] or 0
            b.append(r(x0, y + 2 + j * 8, sx(v) - x0, 7, cls, 1))
    return svg(W, H, "".join(b), "Three coverage numbers that do not rank the arms alike")


# ----------------------------------------------------------------- paired movement
def paired(d, key: str, title: str, what: str) -> str:
    arms = [a for a in d["arms"] if a[key]]
    W, top, rh = 760, 40, 28
    H = top + rh * len(arms) + 30
    mid, u = 470, 18.0
    b = [t(mid - 10, 22, f"← {what} fell", 11, "down", "end"),
         t(mid + 10, 22, f"{what} rose →", 11, "up"),
         ln(mid, top - 8, mid, top + rh * len(arms), "strong", 1)]
    b.append(t(W - 16, 22, "pairs · p", 11, "dim", "end"))
    for k, a in enumerate(arms):
        y = top + k * rh
        m = a[key]
        b.append(t(16, y + 14, name(a), 12, "ink"))
        b.append(r(mid - m["fell"] * u, y + 2, m["fell"] * u, 16, "down"))
        b.append(r(mid, y + 2, m["rose"] * u, 16, "up"))
        if m["fell"]:
            b.append(t(mid - m["fell"] * u - 5, y + 14, m["fell"], 11, "strong", "end"))
        if m["rose"]:
            b.append(t(mid + m["rose"] * u + 5, y + 14, m["rose"], 11, "strong"))
        b.append(t(W - 16, y + 14, f"{m['n']} · {pfmt(m['p'])}", 11,
                   "sig" if m["p"] <= 0.05 else "dim", "end"))
    return svg(W, H, "".join(b), title)


# ----------------------------------------------------------------- the judge
def judge(d) -> str:
    arms = d["arms"]
    W, top, rh = 1000, 70, 26
    H = top + rh * len(arms) + 24
    cols = [("concept", "concept", 190), ("issue", "issue coverage", 460),
            ("read", "readability", 730)]
    labels = {"concept": ["different", "tangential", "narrower", "close", "equivalent"],
              "issue": ["none", "minor", "main only", "nearly", "complete"],
              "read": ["reject", "poor", "acceptable", "good", "exemplary"]}
    b = []
    for key, lab, x in cols:
        b.append(t(x, 22, lab, 13, "strong", weight="600"))
        # Two rows of legend, so five labels fit under a 250-wide column.
        for i, l in enumerate(labels[key]):
            lx = x + (i % 3) * 84
            ly = 34 + (i // 3) * 14
            b.append(r(lx, ly, 8, 8, f"l{i + 1}", 1)); b.append(t(lx + 11, ly + 8, f"{i + 1} {l}", 9, "ink"))
    for k, a in enumerate(arms):
        y = top + k * rh
        b.append(t(16, y + 13, name(a), 12, "ink"))
        for key, _, x in cols:
            tot = sum(a[key]) or 1
            xx = x
            for i in range(5):
                w = 250 * a[key][i] / tot
                b.append(r(xx, y + 2, w, 15, f"l{i + 1}", 0))
                if a[key][i] and w > 14:
                    b.append(t(xx + w / 2, y + 13, a[key][i], 9, "chip", "middle"))
                xx += w
    return svg(W, H, "".join(b), "Judge verdicts, five levels, one judge")


# ----------------------------------------------------------------- cost
def cost(d) -> str:
    arms = d["arms"]
    W, H, x0, y0 = 760, 380, 60, 310
    xs = [a["spend"] for a in arms]
    lo, hi = min(xs) * 0.9, max(xs) * 1.05
    sx = lambda v: x0 + (v - lo) / (hi - lo) * (W - x0 - 40)
    sy = lambda n: y0 - (n - 34) / (58 - 34) * (y0 - 30)   # v2 spans 38..54
    b = []
    for n in range(35, 59, 5):
        b += [ln(x0, sy(n), W - 30, sy(n), "grid"), t(x0 - 8, sy(n) + 4, n, 10, "dim", "end")]
    step = 0.5
    v = round(lo / step) * step
    while v <= hi:
        b += [t(sx(v), y0 + 16, f"${v:.2f}", 10, "dim", "middle")]
        v += step
    b.append(t(x0, 16, "fail-to-pass against total spend per arm, agent and judge", 11, "dim"))
    # Numbers, not names, beside the dots: three arms sit at 51 within fifty cents of each
    # other and a name long enough to read lands next to the wrong dot. The key below
    # names them.
    dots = [(sx(a["spend"]), sy(a["yes"])) for a in arms]
    placed: list[tuple[float, float]] = []
    for a, (x, y) in zip(arms, dots):
        cls = "base" if a["num"] == "1" else "sig" if (a["vs_base"] or {}).get("p", 1) <= 0.05 else "flat"
        b.append(f"<circle cx='{x:.1f}' cy='{y:.1f}' r='6' class='k-{cls}'/>")
    for a, (x, y) in zip(arms, dots):
        for lx, ly in ((x + 9, y + 4), (x - 9 - 7 * len(a["num"]), y + 4), (x - 3, y - 10),
                       (x - 3, y + 18)):
            if all(abs(lx - px) > 16 or abs(ly - py) > 11 for px, py in placed) and \
               all(abs(lx + 4 - dx) > 9 or abs(ly - 4 - dy) > 9 for dx, dy in dots):
                break
        placed.append((lx, ly))
        b.append(t(lx, ly, a["num"], 11, "strong", weight="600"))
    names = [f"{a['num']} {a['label']}" for a in arms]
    b.append(t(x0, y0 + 36, "  ·  ".join(names[:5]), 10, "dim"))
    b.append(t(x0, y0 + 50, "  ·  ".join(names[5:]), 10, "dim"))
    return svg(W, H, "".join(b), "What each arm cost against what it produced")


CHARTS = {
    "scoreboard.svg": scoreboard, "f2p.svg": f2p, "v1v2.svg": v1v2,
    "failures.svg": failures, "patches.svg": patches, "coverage3.svg": coverage3,
    "cov_paired.svg": lambda d: paired(d, "cov_paired", "Coverage, paired against the base",
                                       "coverage"),
    "mut_paired.svg": lambda d: paired(d, "mut_paired", "Mutation, paired against the base",
                                       "kill rate"),
    "judge.svg": judge, "cost.svg": cost,
}


def main() -> None:
    d = json.load(open(sys.argv[1]))
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for fname, fn in CHARTS.items():
        (OUT / fname).write_text(fn(d))
    print(f"wrote {len(CHARTS)} charts to {OUT}")


if __name__ == "__main__":
    main()
