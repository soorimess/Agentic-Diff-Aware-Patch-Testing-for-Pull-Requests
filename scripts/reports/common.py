"""Shared pieces of the final-experiment reports (scripts/reports/*.py)."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "swe-bench-outs" / "new-system-final-19-prs"
CSS = Path(__file__).with_name("report.css")
POOL = json.loads((ROOT / "datasets/large/swebench.json").read_text())
# Executable changed lines per PR, from the pool's notes.
LINES = {p["id"]: int(p["note"].split(" executable")[0].split()[-1]) for p in POOL}
E = html.escape

FINAL = ["astropy__astropy-14295", "astropy__astropy-7008", "django__django-16092",
         "django__django-11991", "matplotlib__matplotlib-25515", "matplotlib__matplotlib-19743",
         "matplotlib__matplotlib-20693", "pydata__xarray-6971", "pydata__xarray-7444",
         "pylint-dev__pylint-4551", "pytest-dev__pytest-5787", "scikit-learn__scikit-learn-14012",
         "sphinx-doc__sphinx-7590", "sphinx-doc__sphinx-7234", "sphinx-doc__sphinx-7380",
         "sympy__sympy-13091", "sympy__sympy-17512", "sympy__sympy-14085", "sympy__sympy-13236"]


def short(iid):
    repo, num = iid.split("__")[1].rsplit("-", 1)
    return f"{repo} {num}"


def cov(r):
    c = (r or {}).get("changed_line_coverage") or {}
    return c if c.get("measured") else None


def covp(r):
    c = cov(r) if r and r.get("f2p") == "YES" else None
    return c["percent"] if c else None


def fig(label, vals, foot):
    v = "".join(f'<span class="a-{k}">{E(x)}</span>' for k, x in vals)
    return f'<div class="fig"><div class="label">{E(label)}</div><div class="vals">{v}</div><div class="foot">{foot}</div></div>'


def dots_svg(rows, label, ceiling_name=None):
    """One row per PR: a dot per arm on a 0-100% axis, plus an optional developer mark."""
    w, left, right, rowh = 640, 150, 24, 30
    plot = w - left - right
    h = 24 + rowh * len(rows) + 26
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{E(label)} per pull request, arms A, B and C">']
    for k in range(5):
        x = left + plot * k / 4
        parts.append(f'<line x1="{x:.1f}" y1="18" x2="{x:.1f}" y2="{h - 26}" class="grid"/>'
                     f'<text x="{x:.1f}" y="{h - 8}" class="tick" text-anchor="middle">{25 * k}%</text>')
    for r, (name, sub, vals, dev) in enumerate(rows):
        y = 24 + r * rowh + 12
        parts.append(f'<text x="{left - 12}" y="{y + 1}" class="lab" text-anchor="end">{E(name)}</text>'
                     f'<text x="{left - 12}" y="{y + 12}" class="sub" text-anchor="end">{E(sub)}</text>')
        xs = [left + plot * v / 100 for v in vals.values() if v is not None]
        if len(xs) > 1:
            parts.append(f'<line x1="{min(xs):.1f}" y1="{y - 4}" x2="{max(xs):.1f}" y2="{y - 4}" class="span"/>')
        if dev is not None:
            x = left + plot * dev / 100
            parts.append(f'<path d="M{x:.1f} {y - 13} v18" class="dev"><title>{name}, {ceiling_name}: {dev:.0f}%</title></path>')
        if not xs:
            parts.append(f'<text x="{left + 6}" y="{y}" class="sub">pending</text>')
        for key, v in vals.items():
            if v is None:
                continue
            x = left + plot * v / 100
            parts.append(f'<circle cx="{x:.1f}" cy="{y - 4}" r="5.5" class="arm-{key}"><title>{name}, arm {key}: {v:.0f}%</title></circle>')
    parts.append("</svg>")
    return "".join(parts)
