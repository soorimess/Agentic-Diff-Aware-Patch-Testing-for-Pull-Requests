"""Refresh the generated blocks in `docs/system-design.md`.

The prose in that document is written by hand and stays that way. The parts that drift --
the module inventory, the CLI surface, the tools the agent is given, the prompt pieces --
are read out of the code here and written between markers, so a renamed file or a new
flag cannot leave the document quietly wrong.

    uv run python -m openhands_f2p.docs

Runs automatically at the end of every non-child agent run, next to `runs.py`.
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

from openhands_f2p.layout import PROJECT_ROOT
from openhands_f2p import prompt


PKG = Path(__file__).resolve().parent
DOC = PROJECT_ROOT / "docs" / "system-design.md"

BLOCK = "<!-- generated:{name} -->"
END = "<!-- /generated:{name} -->"


def _summary(path: Path) -> str:
    """First sentence of a module's docstring."""
    try:
        tree = ast.parse(path.read_text())
    except SyntaxError:
        return ""
    doc = ast.get_docstring(tree) or ""
    first = doc.strip().split("\n\n")[0].replace("\n", " ").strip()
    return first[:150]


def modules() -> str:
    rows = ["| module | lines | what it is |", "|---|---|---|"]
    for f in sorted(PKG.glob("*.py")):
        if f.name == "__init__.py":
            continue
        n = len(f.read_text().splitlines())
        rows.append(f"| `{f.name}` | {n} | {_summary(f)} |")
    return "\n".join(rows)


def cli() -> str:
    """Every flag the parser accepts, read off the parser.

    Including the ones `features.py` and `models.py` contribute, which a scrape of
    `agent.py` could never see. Grouped the way `--help` groups them, and the default is
    shown where there is one worth knowing, because "what happens if I leave it out" is
    the question a flag table is usually consulted for.
    """
    import argparse

    from openhands_f2p.agent import build_parser

    parser = build_parser()
    # Which argparse group each action belongs to, so the table reads like `--help`.
    group_of = {}
    for g in parser._action_groups:
        for a in g._group_actions:
            group_of[id(a)] = g.title or ""
    order, rows = [], {}
    for a in parser._actions:
        if isinstance(a, argparse._HelpAction):
            continue
        title = group_of.get(id(a), "options")
        title = {"positional arguments": "the instances to run",
                 "options": "the run"}.get(title, title)
        if title not in rows:
            order.append(title)
            rows[title] = []
        flag = ", ".join(f"`{o}`" for o in a.option_strings) or f"`{a.dest}`"
        help_text = " ".join((a.help or "").split())
        tail = help_text.rstrip()
        sep = "" if tail.endswith((".", "!", "?")) else "."
        if a.choices:
            help_text = tail + sep + " Choices: " + ", ".join(f"`{c}`" for c in a.choices) + "."
            tail, sep = help_text, ""
        shown = a.default
        if shown not in (None, False) and "default" not in help_text.lower():
            help_text = tail + sep + f" Default: `{shown}`."
        rows[title].append(f"| {flag} | {help_text} |")
    out = []
    for title in order:
        out.append(f"\n**{title}**\n")
        out.append("| flag | what it does |")
        out.append("|---|---|")
        out.extend(rows[title])
    return "\n".join(out).strip()


def tools() -> str:
    """Every tool `sandbox_tools.py` defines, discovered rather than listed.

    This used to match against a hardcoded alternation of the five tools that existed
    when it was written, so `mutation` was added and the generated block stayed at five
    -- and `--check` passed, because the generator agreed with its own stale output. A
    documentation generator with an allow-list of the things it may document is not
    generating anything.

    Which of these a given run registers depends on the feature set; `features.py` owns
    that, and the configuration table below says which go with which.
    """
    src = (PKG / "sandbox_tools.py").read_text()
    seen: list[str] = []
    for n in re.findall(r'^\s+name="([a-z_]+)",$', src, re.M):
        if n not in seen:
            seen.append(n)
    if not seen:                       # the declaration style moved; say so loudly
        raise SystemExit("  docs.tools(): no tool names found in sandbox_tools.py")
    return "\n".join(f"- `{n}`" for n in seen)


def prompt_pieces() -> str:
    rows = ["| file | job |", "|---|---|"]
    for p in prompt.pieces():
        job = " ".join((p.job or "").split())
        rows.append(f"| `{p.path.name}` | {job[:160]} |")
    return "\n".join(rows)


SECTIONS = {"modules": modules, "cli": cli, "tools": tools,
            "prompts": prompt_pieces}


def refresh(check: bool = False) -> int:
    if not DOC.exists():
        print(f"{DOC} does not exist", file=sys.stderr)
        return 1
    text = original = DOC.read_text()
    for name, fn in SECTIONS.items():
        start, end = BLOCK.format(name=name), END.format(name=name)
        if start not in text or end not in text:
            print(f"  no {name} block in {DOC.name}", file=sys.stderr)
            continue
        head, _, rest = text.partition(start)
        _, _, tail = rest.partition(end)
        text = f"{head}{start}\n{fn()}\n{end}{tail}"
    if text == original:
        print(f"{DOC.relative_to(PROJECT_ROOT)} already current")
        return 0
    if check:
        print(f"{DOC.relative_to(PROJECT_ROOT)} is out of date -- run "
              f"`python -m openhands_f2p.docs`", file=sys.stderr)
        return 1
    DOC.write_text(text)
    print(f"updated {DOC.relative_to(PROJECT_ROOT)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="fail instead of writing, for CI")
    return refresh(check=ap.parse_args().check)


if __name__ == "__main__":
    sys.exit(main())
