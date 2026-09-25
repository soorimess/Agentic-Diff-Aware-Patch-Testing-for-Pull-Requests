"""Hand-rolled SVG charts. No dependencies, and the colours read on light and dark."""
import json, sys, pathlib, html

# Colour is done with classes and a prefers-color-scheme block rather than fill
# attributes, because these render on GitHub against both a white and a near-black page
# and no single grey is legible on both. The hues are shared; only the greys switch.
INK, STRONG, DIM = "ink", "strong", "dim"
BASE, DOWN, UP, FLAT = "base", "down", "up", "flat"
FONT = "font-family='ui-sans-serif,-apple-system,Segoe UI,Helvetica,Arial,sans-serif'"

STYLE = """<style>
  .ink{fill:#57606a}.strong{fill:#1f2328}.dim{fill:#6e7681}
  .grid{stroke:#d0d7de}.axis{stroke:#8c959f}
  .base{fill:#8250df}.down{fill:#cf222e}.up{fill:#1a7f37}.flat{fill:#0969da}
  .s-base{stroke:#8250df}.s-grid{stroke:#d0d7de}
  .chip{fill:#ffffff}
  .c-broken{fill:#cf222e}.c-base{fill:#9a6700}.c-coll{fill:#8250df}
  .c-void{fill:#bc4c00}.c-notest{fill:#6e7681}.c-reg{fill:#8c959f}.c-other{fill:#afb8c1}
  @media (prefers-color-scheme: dark){
    .ink{fill:#8b949e}.strong{fill:#e6edf3}.dim{fill:#6e7681}
    .grid{stroke:#30363d}.axis{stroke:#484f58}
    .base{fill:#a371f7}.down{fill:#f85149}.up{fill:#3fb950}.flat{fill:#58a6ff}
    .s-base{stroke:#a371f7}.s-grid{stroke:#30363d}
    .chip{fill:#0d1117}
    .c-broken{fill:#f85149}.c-base{fill:#d29922}.c-coll{fill:#a371f7}
    .c-void{fill:#db6d28}.c-notest{fill:#6e7681}.c-reg{fill:#484f58}.c-other{fill:#30363d}
  }
</style>"""

def esc(s): return html.escape(str(s))

def svg(w, h, body, title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-label="{esc(title)}">\n{STYLE}\n{body}\n</svg>\n')

def text(x, y, s, size=12, cls=INK, anchor="start", weight="normal"):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" class="{cls}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {FONT}>{esc(s)}</text>')

def rect(x, y, w, h, cls, rx=2, op=1.0):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{h:.1f}" class="{cls}" rx="{rx}" opacity="{op}"/>'

def line(x1, y1, x2, y2, cls="grid", w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" stroke-width="{w}"{d}/>'


def chart_f2p(arms, path):
    """Fail-to-pass per arm, base marked, significance called out."""
    rows = len(arms); rh, gap, top, left, right = 26, 8, 46, 172, 74
    w = 810; h = top + rows * (rh + gap) + 40
    right = 140
    plot = w - left - right
    mx = 46
    b = [text(12, 22, "Fail-to-pass out of 70", 14, STRONG, weight="600"),
         text(12, 38, "bar length is tests that flipped; the dashed line is the base", 11, DIM)]
    x0 = left
    basex = x0 + plot * 42 / mx
    b.append(line(basex, top - 8, basex, top + rows * (rh + gap), "s-base", 1, "4 3"))
    b.append(text(basex, top - 14, "base 42", 10, BASE, "middle", "600"))
    labx = x0 + plot + 14
    for i, a in enumerate(arms):
        y = top + i * (rh + gap)
        net = a["yes"] - 42
        sig = a["p"] <= 0.05
        col = BASE if a["num"] == "1" else (DOWN if net < 0 else UP if net > 0 else FLAT)
        if not sig and a["num"] != "1":
            col = DOWN if net < 0 else UP if net > 0 else FLAT
        op = 1.0 if (sig or a["num"] == "1") else 0.45
        b.append(text(x0 - 10, y + 17, f'{a["num"]}  {a["label"]}', 12,
                      STRONG if sig or a["num"] == "1" else INK, "end",
                      "600" if sig else "normal"))
        b.append(rect(x0, y, plot * a["yes"] / mx, rh, col, 3, op))
        b.append(text(x0 + plot * a["yes"] / mx - 8, y + 17, str(a["yes"]), 11,
                      "chip", "end", "700"))
        if a["num"] != "1":
            lab = f'{net:+d}   p={a["p"]:.2f}' + ("  \u2605" if sig else "")
            b.append(text(labx, y + 17, lab, 11,
                          STRONG if sig else DIM, weight="600" if sig else "normal"))
    b.append(text(x0, h - 10, "★ clears p ≤ 0.05 against the base (McNemar, paired on all 70)", 10, DIM))
    return pathlib.Path(path).write_text(svg(w, h, "\n".join(b), "Fail-to-pass per arm"))


def chart_failures(arms, path):
    """What the failures were, as a share of all 70."""
    order = [("broken", "c-broken", "test fails after the fix too"),
             ("passes_at_base", "c-base", "test passes on unfixed code"),
             ("collects_nothing", "c-coll", "file never ran"),
             ("voided", "c-void", "voided: edited the tree"),
             ("no_test", "c-notest", "no test written"),
             ("registry", "c-reg", "image never pulled"),
             ("other", "c-other", "other")]
    rows = len(arms); rh, gap, top, left = 26, 8, 92, 172
    w = 810; h = top + rows * (rh + gap) + 30
    plot = w - left - 56
    b = [text(12, 22, "How the failures failed", 14, STRONG, weight="600"),
         text(12, 38, "every instance that did not flip, as a share of 70", 11, DIM)]
    lx, ly = 12, 52
    for key, col, lab in order:
        wdt = 13 + len(lab) * 4.9 + 14
        if lx + wdt > w - 12:
            lx, ly = 12, ly + 15
        b.append(rect(lx, ly - 8, 9, 9, col, 2))
        b.append(text(lx + 13, ly, lab, 9, DIM))
        lx += wdt
    for i, a in enumerate(arms):
        y = top + i * (rh + gap)
        b.append(text(left - 10, y + 17, f'{a["num"]}  {a["label"]}', 12, INK, "end"))
        x = left
        for key, col, _ in order:
            v = a["why"].get(key, 0)
            if not v: continue
            wdt = plot * v / 70
            b.append(rect(x, y, wdt, rh, col, 2))
            if wdt > 17:
                b.append(text(x + wdt / 2, y + 17, str(v), 10, "chip", "middle", "700"))
            x += wdt
        b.append(text(x + 8, y + 17, f'{70 - a["yes"]} failed', 10, DIM))
    return pathlib.Path(path).write_text(svg(w, h, "\n".join(b), "Failure modes per arm"))


def chart_cost(arms, path):
    """What each arm cost against what it produced."""
    w, h = 810, 420; left, bot, top, right = 70, 62, 56, 30
    pw, ph = w - left - right, h - top - bot
    xs = [a["cost"] + a["jcost"] for a in arms]; ys = [a["yes"] for a in arms]
    x0, x1 = 1.8, 4.9; y0, y1 = 26, 46
    px = lambda v: left + pw * (v - x0) / (x1 - x0)
    py = lambda v: top + ph - ph * (v - y0) / (y1 - y0)
    b = [text(12, 22, "What each arm cost, against what it produced", 14, STRONG, weight="600"),
         text(12, 38, "total dollars per 70-instance run, agent plus judge", 11, DIM)]
    for gy in range(y0, y1 + 1, 4):
        b.append(line(left, py(gy), left + pw, py(gy), "grid", 1))
        b.append(text(left - 8, py(gy) + 4, str(gy), 10, DIM, "end"))
    for gx in [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]:
        b.append(line(px(gx), top, px(gx), top + ph, "grid", 1))
        b.append(text(px(gx), top + ph + 16, f"${gx:.1f}", 10, DIM, "middle"))
    b.append(text(left + pw / 2, h - 12, "cost of the run", 11, DIM, "middle"))
    b.append(f'<text transform="translate(18,{top + ph/2:.0f}) rotate(-90)" font-size="11" '
             f'class="dim" text-anchor="middle" {FONT}>fail-to-pass</text>')
    for a in arms:
        x, y = px(a["cost"] + a["jcost"]), py(a["yes"])
        sig = a["p"] <= 0.05
        col = BASE if a["num"] == "1" else (DOWN if sig else FLAT)
        b.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{7 if a["num"]=="1" else 5.5}" class="{col}" opacity="{1 if sig or a["num"]=="1" else .75}"/>')
        dx, dy = 10, 4
        if a["num"] in ("8",): dy = -10          # arm 8 and arm 10 share a point
        if a["num"] in ("10",): dx, dy = -10, 16
        if a["num"] == "1": dx, dy = -12, -10    # the base marker sits under its own label
        # anything in the right third would run off the edge
        if x > left + pw * 0.66 and a["num"] not in ("1", "10"): dx = -10
        b.append(text(x + dx, y + dy, f'{a["num"]} {a["label"]}', 10,
                      STRONG if sig or a["num"] == "1" else INK,
                      "end" if dx < 0 else "start"))
    return pathlib.Path(path).write_text(svg(w, h, "\n".join(b), "Cost against fail-to-pass"))


def chart_coverage(arms, path):
    """Paired changed-line coverage: which way did it move, on instances that passed in both."""
    arms = [a for a in arms if a["num"] != "1" and a["paired_n"]]
    rows = len(arms); rh, gap, top, left = 24, 10, 62, 172
    w = 760; h = top + rows * (rh + gap) + 40
    mid = left + (w - left - 80) / 2
    half = (w - left - 80) / 2
    mx = 8
    b = [text(12, 22, "Changed-line coverage, paired", 14, STRONG, weight="600"),
         text(12, 38, "instances that passed in BOTH arms; left = coverage fell without the feature", 11, DIM),
         text(mid - 6, 54, "fell", 10, DOWN, "end"), text(mid + 6, 54, "rose", 10, UP)]
    for i, a in enumerate(arms):
        y = top + i * (rh + gap)
        b.append(text(left - 10, y + 16, f'{a["num"]}  {a["label"]}', 12, INK, "end"))
        b.append(line(mid, y - 3, mid, y + rh + 3, "axis", 1))
        b.append(rect(mid - half * a["cov_fell"] / mx, y, half * a["cov_fell"] / mx, rh, DOWN, 2, .9))
        b.append(rect(mid, y, half * a["cov_rose"] / mx, rh, UP, 2, .9))
        note = f'{a["paired_base"]}%→{a["paired_arm"]}%  p={a["cov_p"]:.2f}'
        b.append(text(w - 72, y + 16, note, 10, STRONG if a["cov_p"] <= .05 else DIM))
    return pathlib.Path(path).write_text(svg(w, h, "\n".join(b), "Paired coverage movement"))


if __name__ == "__main__":
    data = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    arms = data["arms"]
    chart_f2p(arms, out / "f2p.svg")
    chart_failures(arms, out / "failures.svg")
    chart_cost(arms, out / "cost.svg")
    chart_coverage(arms, out / "coverage.svg")
    print("wrote", ", ".join(p.name for p in sorted(out.glob("*.svg"))))
