"""Assemble the agent's prompt from the pieces in prompts/.

One file per instruction, joined in filename order. The point is attribution: when a
result moves, you can say which instruction moved it, and a piece can be dropped for one
arm while kept for another without touching Python.

Each file carries a `---` header naming it and stating its job. The header is stripped
before anything is sent -- it is for us, not the model.

    from openhands_f2p import prompt
    text = prompt.build(repo=..., test_file=..., problem=..., runner="django")
    prompt.explain()        # what each piece is for, without building anything
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent / "prompts"
HEADER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


@dataclass
class Piece:
    path: Path
    name: str
    job: str
    body: str

    @property
    def order(self) -> str:
        return self.path.name


def _parse(path: Path) -> Piece:
    raw = path.read_text()
    m = HEADER.match(raw)
    if not m:
        raise ValueError(f"{path.name} has no `---` header naming it and its job")
    head, body = m.group(1), raw[m.end():].strip()
    fields = {}
    key = None
    for line in head.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
        elif key:                                   # a wrapped continuation line
            fields[key] += " " + line.strip()
    return Piece(path, fields.get("name", path.stem), fields.get("job", ""), body)


def pieces(runner: str = "pytest") -> list[Piece]:
    """Every piece that applies to this repository, in order.

    Runner files are named 60-runner-<kind>.md and exactly one is selected, so adding
    support for a new test runner is adding a file rather than editing a dictionary.
    """
    out = []
    for path in sorted(PROMPTS.glob("*.md")):
        if path.name == "README.md":
            continue
        if (path.name.startswith("60-runner-")
                and path.name != f"60-runner-{runner}.md"):
            continue
        out.append(_parse(path))
    return out


def build(*, repo: str, test_file: str, problem: str, runner: str = "pytest",
          patch: str = "", coverage_tool: bool = True,
          skip: set[str] | None = None) -> str:
    """The finished prompt. `skip` drops pieces by name, for arm comparisons.

    An empty `patch` drops the `change` piece automatically. That is the blind arm, and
    it is a real difference in the task rather than a formatting accident -- so it is
    made explicit here rather than left to whoever calls this.
    """
    skip = set(skip or ())
    if not patch:
        # Everything that only makes sense with the diff goes together: the diff itself,
        # the tools that read it, and the instruction to use them.
        skip |= {"change", "tools-verify", "tools-coverage",
                 "check-flips", "check-reaches"}
    elif not coverage_tool:
        # The coverage arm of --compare-coverage. The tool is not registered, so
        # describing it would send the agent after something that never answers.
        skip |= {"tools-coverage", "check-reaches"}
    used = [p for p in pieces(runner) if p.name not in skip]
    text = "\n\n".join(p.body for p in used)
    build.last_pieces = [p.name for p in used]
    return text.format(repo=repo, test_file=test_file,
                       problem=problem.strip()[:6000], patch=patch.strip()[:8000])


# The names of the pieces the last `build` call actually included. Reported rather than
# inferred: the caller used to work them out with `piece.name in task`, a substring test
# of a name against the whole prompt, which counts "tools" because the text says "You
# have these tools" and "finish" because it says "before you finish".
build.last_pieces: list[str] = []


def explain() -> str:
    lines = ["The prompt is built from these pieces, in this order:\n"]
    for p in pieces("pytest"):
        lines.append(f"  {p.path.name:22s} {p.name}")
        lines.append(f"  {'':22s} {p.job}\n")
    others = sorted(PROMPTS.glob("60-runner-*.md"))
    lines.append(f"  one runner file is chosen from: "
                 f"{', '.join(p.stem.replace('60-runner-', '') for p in others)}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if "--explain" in sys.argv:
        print(explain())
    else:
        print(build(repo="psf/requests", test_file="tests/test_f2p.py",
                    problem="<the issue text goes here>",
                    patch="<the pull request diff goes here>",
                    runner=sys.argv[1] if len(sys.argv) > 1 else "pytest"))
