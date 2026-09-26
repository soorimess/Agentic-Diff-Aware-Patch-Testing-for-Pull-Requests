"""Assemble the agent's prompt from the pieces in prompts/.

One file per instruction, joined in filename order. The point is attribution: when a
result moves, you can say which instruction moved it, and a piece can be dropped for one
configuration while kept for another without touching Python.

Each file carries a `---` header naming it and stating its job. The header is stripped
before anything is sent -- it is for us, not the model.

    from openhands_f2p import prompt
    text = prompt.build(repo=..., test_file=..., problem=..., features=...)
    prompt.explain()        # what each piece is for, without building anything

Configuration reaches the text two ways, because dropping whole instructions is not
enough on its own:

* **`needs:` in the header** drops the piece. `35-change.md` *is* the diff, so without
  the `patch` feature there is nothing left of it to include. A name can be negated:
  `needs: !repo-facts` keeps the piece only while that feature is *off*, which is how a
  withheld component gets a substitute instruction. Without it, withholding the briefing
  on how a project tests would leave a hole where it used to be, and the run would
  measure a missing instruction rather than a missing input.
* **`{?feature} ... {/feature}`** in the body drops a sentence or a paragraph. Most
  pieces are not all-or-nothing: `20-goal.md` still has a job to do when the diff is
  withheld, but the clause telling the agent to work out "what it will do after the
  change" describes something it can no longer see.

Both are checked. An unknown feature name in either place raises, and the finished
prompt is scanned for the names of tools that were not registered -- so a piece cannot
quietly send the agent after a tool that does not exist. That last check is the one that
matters: the failure it prevents is silent, and the agent's own transcript is where you
would find out, several runs later.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from openhands_f2p.features import BY_NAME, FeatureSet

PROMPTS = Path(__file__).resolve().parent / "prompts"
HEADER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
# {?patch} ... {/patch}  -- kept only while that feature is on; {?!patch} for the
# inverse. Non-greedy and name-matched, so two blocks in one file cannot swallow each
# other, and the backreference makes a mismatched closing tag simply not match.
BLOCK = re.compile(r"[ \t]*\{\?(!?[a-z][a-z0-9-]*)\}\n?(.*?)\n?[ \t]*\{/\1\}\n?",
                   re.S)
# A tool the prompt refers to. The pieces always backtick tool names, which is what
# makes this precise: `coverage` is a tool, "changed-line coverage" is prose.
TOOL_REF = re.compile(r"`([a-z_]+)`")


def holds(name: str, features: FeatureSet) -> bool:
    """Is the condition `name` satisfied? `f` means f is on, `!f` means f is off."""
    return name[1:] not in features if name.startswith("!") else name in features


def _label(name: str) -> str:
    return f"no {name[1:]}" if name.startswith("!") else name


@dataclass
class Piece:
    path: Path
    name: str
    job: str
    body: str
    needs: tuple[str, ...] = ()
    blocks: tuple[str, ...] = field(default_factory=tuple)
    """Features this piece gates a paragraph on -- reported so `explain` can show a
    piece that survives in a reduced form rather than only which ones vanish."""

    @property
    def order(self) -> str:
        return self.path.name


def _parse(path: Path) -> Piece:
    raw = path.read_text()
    m = HEADER.match(raw)
    if not m:
        raise ValueError(f"{path.name} has no `---` header naming it and its job")
    head, body = m.group(1), raw[m.end():].strip()
    fields: dict[str, str] = {}
    key = None
    for line in head.splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
        elif key:                                   # a wrapped continuation line
            fields[key] += " " + line.strip()

    needs = tuple(n.strip() for n in fields.get("needs", "").split(",") if n.strip())
    blocks = tuple(dict.fromkeys(m.group(1) for m in BLOCK.finditer(body)))
    for name in (*needs, *blocks):
        if name.lstrip("!") not in BY_NAME:
            where = "needs:" if name in needs else "a {?...} block"
            raise ValueError(
                f"{path.name}: {where} names {name!r}, which is not a feature. "
                f"Known: {', '.join(BY_NAME)}")
    return Piece(path, fields.get("name", path.stem), fields.get("job", ""),
                 body, needs, blocks)


def pieces() -> list[Piece]:
    """Every piece, in order.

    Every piece applies to every repository. There used to be `60-runner-<kind>.md`
    files carrying per-project advice -- where django puts its tests, that sympy has no
    pytest -- and they were removed on purpose: they were right for the twelve
    repositories someone had looked at and silently absent for the thirteenth, which
    capped the system at our own knowledge rather than at what it could work out. That
    knowledge now comes from `15-repo.md`, which is read off the checkout at run
    time by `repo_facts` with no model involved.
    """
    return [_parse(path) for path in sorted(PROMPTS.glob("*.md"))
            if path.name != "README.md"]


def _resolve_blocks(body: str, features: FeatureSet) -> str:
    """Keep the inside of `{?f}` blocks whose feature is on, drop the rest.

    Innermost first, repeatedly, because the blocks nest. `58-finish.md` states one
    condition per instrument inside a single `{?require-tools}` wrapper, and the
    conjunction is the point -- the coverage line belongs in the prompt only when the
    requirement is on *and* the tool exists. `BLOCK` is non-greedy, so one pass matches
    the inner pair and leaves the outer opener stranded for `.format()` to choke on:
    `KeyError: '?verify-tool'`. Looping until the text stops changing resolves inner
    pairs first and the wrapper last.
    """
    def one(m: re.Match) -> str:
        keep = holds(m.group(1), features)
        # Inline -- the opener follows text on its line, as when one sentence of a
        # paragraph belongs to a feature. The match ate the newline after the closer, and
        # that newline is the paragraph's, so it goes back whichever way the block goes.
        # (Returning "" would join the next paragraph onto this one.)
        # Newlines just inside the tags were eaten the same way and belong to the text
        # being kept, so a kept inline block reads exactly as if it had no tags.
        if m.start() > 0 and m.string[m.start() - 1] != "\n":
            tail = "\n" if m.group(0).endswith("\n") else ""
            if not keep:
                return tail
            lead = "\n" if m.string[m.start(2) - 1] == "\n" else ""
            mid = "\n" if m.string[m.end(2)] == "\n" else ""
            return lead + m.group(2) + mid + tail
        return f"{m.group(2)}\n" if keep else ""
    while True:
        resolved = BLOCK.sub(one, body)
        if resolved == body:
            return resolved
        body = resolved


def _check_no_absent_tools(text: str, features: FeatureSet) -> None:
    absent = set(features.absent_tools)
    if not absent:
        return
    named = sorted(absent & set(TOOL_REF.findall(text)))
    if named:
        raise AssertionError(
            f"the assembled prompt refers to {', '.join('`' + n + '`' for n in named)}, "
            f"which will not be registered for this configuration "
            f"({features.describe()}). Gate that text with a `needs:` header or a "
            f"{{?feature}} block in the piece that mentions it.")


def followup(name: str, **fields: object) -> str:
    """A message sent *after* the task, from `prompts/followups/`.

    These live in a subdirectory because `pieces()` globs `prompts/*.md` and joins
    everything it finds into the opening prompt. A follow-up is not part of that -- it is
    a separate turn, sent only in the configurations that ask for one -- so putting it
    one level down is what keeps it out, rather than a name the glob has to remember to
    skip.

    Same header convention as a piece, and the header is stripped the same way.
    """
    body = _parse(PROMPTS / "followups" / f"{name}.md").body
    return body.strip().format(**fields)


def build(*, repo: str, test_file: str, problem: str = "", repo_facts: str = "",
          patch: str = "", features: FeatureSet | None = None,
          skip: object = None) -> str:
    """The finished prompt. `skip` drops pieces by name, for ablations by hand."""
    features = features if features is not None else FeatureSet.of()
    skip = set(skip or ())

    used, text_parts = [], []
    for p in pieces():
        if p.name in skip or any(not holds(n, features) for n in p.needs):
            continue
        body = _resolve_blocks(p.body, features).strip()
        if not body:                        # every paragraph of it was gated away
            continue
        used.append(p.name)
        text_parts.append(body)

    text = "\n\n".join(text_parts).format(
        repo=repo, test_file=test_file, repo_facts=repo_facts,
        problem=problem.strip()[:6000], patch=patch.strip()[:8000])
    _check_no_absent_tools(text, features)
    build.last_pieces = used
    return text


# The names of the pieces the last `build` call actually included. Reported rather than
# inferred: the caller used to work them out with `piece.name in task`, a substring test
# of a name against the whole prompt, which counts "tools" because the text says "You
# have these tools" and "finish" because it says "before you finish".
build.last_pieces: list[str] = []


def explain(features: FeatureSet | None = None) -> str:
    features = features if features is not None else FeatureSet.of()
    lines = [f"Prompt pieces, in order. Configuration: {features.describe()}\n"]
    for p in pieces():
        dropped = [n for n in p.needs if not holds(n, features)]
        gated = [n for n in p.blocks if not holds(n, features)]
        if dropped:
            mark = f"DROPPED (needs {', '.join(_label(n) for n in dropped)})"
        elif gated:
            mark = f"reduced (no {', '.join(_label(n) for n in gated)})"
        else:
            mark = ""
        lines.append(f"  {p.path.name:22s} {p.name:14s} {mark}")
        lines.append(f"  {'':22s} {p.job}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    from openhands_f2p.features import FEATURES
    alias = {a: f.name for f in FEATURES for a in f.aliases}
    off = [alias.get(a) or a[len("--no-"):] for a in sys.argv[1:]
           if a.startswith("--no-") or a in alias]
    fs = FeatureSet.of(off)
    if "--explain" in sys.argv:
        print(explain(fs))
    else:
        # The bare filename when the briefing is withheld, because that is what
        # `run_agent` passes then -- the directory is the agent's to establish, and a
        # preview showing a path would contradict the piece that says so.
        print(build(repo="psf/requests",
                    test_file="tests/test_f2p.py" if "repo-facts" in fs
                              else "test_f2p.py",
                    problem="<the issue text goes here>",
                    patch="<the pull request diff goes here>",
                    repo_facts="<what repo_facts read off the checkout>",
                    features=fs))
