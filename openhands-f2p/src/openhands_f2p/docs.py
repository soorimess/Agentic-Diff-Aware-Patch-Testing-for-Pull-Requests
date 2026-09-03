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

from openhands_f2p import prompt

PROJECT_ROOT = Path(__file__).resolve().parents[3]
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
    """The agent's flags, from the parser itself."""
    src = (PKG / "agent.py").read_text()
    rows = ["| flag | what it does |", "|---|---|"]
    pattern = re.compile(
        r'p\.add_argument\(\s*"(--[a-z-]+)".*?help=(?:\()?((?:\s*"[^"]*"\s*)+)\)?[,)]',
        re.S)
    for flag, helptext in pattern.findall(src):
        text = " ".join(re.findall(r'"([^"]*)"', helptext)).strip()
        if not text:
            continue
        rows.append(f"| `{flag}` | {text} |")
    return "\n".join(rows)


def tools() -> str:
    src = (PKG / "sandbox_tools.py").read_text()
    names = re.findall(r'name\s*=\s*"(run|write_file|run_tests|repo_info|verify|'
                       r'coverage)"', src)
    seen: list[str] = []
    for n in names:
        if n not in seen:
            seen.append(n)
    return "\n".join(f"- `{n}`" for n in seen)


def prompt_pieces() -> str:
    rows = ["| file | job |", "|---|---|"]
    for p in prompt.pieces("pytest"):
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
