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
            # The spaces before an inline opener are the sentence's, not the block's:
            # "If you did, {?verify-tool}the checks...{/verify-tool}" rendered as
            # "If you did,the checks" (ChaCo audit, 2026-10-11).
            space = m.group(0)[:len(m.group(0)) - len(m.group(0).lstrip(" \t"))]
            if not keep:
                return space + tail
            lead = "\n" if m.string[m.start(2) - 1] == "\n" else ""
            mid = "\n" if m.string[m.end(2)] == "\n" else ""
            return space + lead + m.group(2) + mid + tail
        return f"{m.group(2)}\n" if keep else ""
    while True:
        resolved = BLOCK.sub(one, body)
        if resolved == body:
            return resolved
        body = resolved


# Tools that no longer exist in any configuration: coverage and mutation are reports of
# `verify` since 2026-10-19 (user), and a piece naming them as tools sends the agent to
# call something it does not have.
RETIRED_TOOLS = {"coverage", "mutation"}


def _check_no_absent_tools(text: str, features: FeatureSet) -> None:
    absent = set(features.absent_tools) | RETIRED_TOOLS
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


# How much of the issue and the fix the prompt carries. 6000 and 8000 until 2026-10-05,
# cut without a word: astropy-13398's fix (13,883 characters) reached the agent as
# `@@ -0,0 +1,145 @@ +i` -- the whole new module it adds reduced to one letter -- and the
# agent then argued for four refusals that the module "does not exist"; matplotlib-22719
# lost 4,173 characters of its issue. Every one of the 36 fits now; a longer text is cut
# with a line saying so.
ISSUE_CHARS = 20000
# 60000 since 2026-10-11. Every SWE-bench patch fits in 30000; ChaCo's scipy-21700 is
# 142,019 characters, and a plain cut at 30000 hid the class the PR adds (`Mixture`,
# from character 68,330) while saying "read the files in the repository for the rest"
# -- of a repository that is at base and has none of it. Longer ones: `clip_patch`.
PATCH_CHARS = 60000


def clip_marked(text: str, limit: int) -> str:
    """`text` up to `limit` characters, and a line saying how much was left out if any."""
    if len(text) <= limit:
        return text
    return (text[:limit] + f"\n[... {len(text) - limit} more characters not shown here -- "
            f"read the files in the repository for the rest ...]")


_COMMENTISH = ("#", '"""', "'''")


def _hunks(chunk: str) -> tuple[str, list[str]]:
    """A file's diff split into its header and its hunks."""
    parts = re.split(r"(?m)^(?=@@ )", chunk)
    return parts[0], parts[1:]


def clip_patch(patch: str, limit: int) -> str:
    """The patch, or -- when it is longer than `limit` -- the part that says most about it.

    Always the list of every file the change touches, with its added and removed line
    counts. Then whole hunks, those adding the most code first (removed docstrings and
    reformatting last), shown in their original order, until the budget is spent. The
    note names what is left out and says plainly that the repository is at base, so the
    missing new code is not there to be read.
    """
    if len(patch) <= limit:
        return patch
    chunks = [c for c in re.split(r"(?m)^(?=diff --git )", patch)
              if c.startswith("diff --git ")]
    summary, hunks = [], []                  # (key, file index, header, hunk, score)
    for fi, chunk in enumerate(chunks):
        path = chunk.split("\n", 1)[0].split(" b/", 1)[-1]
        head, hs = _hunks(chunk)
        lines = chunk.splitlines()
        adds = sum(ln.startswith("+") and not ln.startswith("+++") for ln in lines)
        dels = sum(ln.startswith("-") and not ln.startswith("---") for ln in lines)
        summary.append(f"  {path} (+{adds}/-{dels})")
        for hi, h in enumerate(hs):
            code = sum(1 for ln in h.splitlines()[1:]
                       if ln.startswith("+") and ln[1:].strip()
                       and not ln[1:].lstrip().startswith(_COMMENTISH))
            hunks.append(((fi, hi), fi, head, h, code))
    intro = ("This change touches these files (lines added/removed):\n"
             + "\n".join(summary) + "\n\n")
    budget = limit - len(intro) - 400
    chosen: set = set()
    for key, _fi, head, h, _score in sorted(hunks, key=lambda t: -t[4]):
        cost = len(h) + (0 if any(k[0] == key[0] for k in chosen) else len(head))
        if cost <= budget:
            chosen.add(key)
            budget -= cost
    out, shown_files, left = [], set(), []
    for key, fi, head, h, _ in hunks:
        if key in chosen:
            if fi not in shown_files:
                out.append(head)
                shown_files.add(fi)
            out.append(h)
        else:
            left.append(fi)
    missing = sorted({chunks[fi].split("\n", 1)[0].split(" b/", 1)[-1] for fi in left})
    note = (f"\n[... {len(left)} of the {len(hunks)} hunks are not shown, to keep this "
            f"short: they are in {', '.join(missing[:12])}"
            f"{' and others' if len(missing) > 12 else ''}. The repository is at the "
            f"commit BEFORE this change, so it does not contain the code those hunks add; "
            f"the file list above is complete.]")
    return intro + "".join(out).rstrip("\n") + note


def build(*, repo: str, test_file: str, problem: str = "", repo_facts: str = "",
          patch: str = "", features: FeatureSet | None = None,
          skip: object = None) -> str:
    """The finished prompt. `skip` drops pieces by name, for ablations by hand."""
    features = features if features is not None else FeatureSet.full()
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
        problem=clip_marked(problem.strip(), ISSUE_CHARS),
        patch=clip_patch(patch.strip(), PATCH_CHARS))
    _check_no_absent_tools(text, features)
    build.last_pieces = used
    return text


# The names of the pieces the last `build` call actually included. Reported rather than
# inferred: the caller used to work them out with `piece.name in task`, a substring test
# of a name against the whole prompt, which counts "tools" because the text says "You
# have these tools" and "finish" because it says "before you finish".
build.last_pieces: list[str] = []


def explain(features: FeatureSet | None = None) -> str:
    features = features if features is not None else FeatureSet.full()
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
    import argparse

    from openhands_f2p.features import add_arguments
    ap = argparse.ArgumentParser(description="Print the prompt a configuration assembles.")
    ap.add_argument("--explain", action="store_true")
    add_arguments(ap)
    cli = ap.parse_args()
    fs = FeatureSet.from_args(cli)
    if cli.explain:
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
