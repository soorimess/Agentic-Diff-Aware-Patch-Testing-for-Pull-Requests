"""Plausible wrong versions of the change, for the agent's feedback (2026-10-24, user).

`mutmut`'s operators flip a comparison or replace a literal; a weak model reads
"`x < y   ->   x <= y`" and does not turn it into an assertion. A wrong version written the
way a developer might get the change wrong -- "writes the JSON to stdout instead of the
file", "drops every format after the first" -- names a behaviour, which is what a test
asserts. One model call per pull request, before the agent starts, cached in the run
directory; never part of the measurement (`mutants.measure` stays deterministic), only of
what `verify` shows the agent. Every version is gated: its text must be found verbatim in
the fixed code, the result must parse, and it must not compile to the fix's own bytecode.
"""
from __future__ import annotations

import ast
import difflib
import json
import re
from pathlib import Path
from typing import Any

SYSTEM = (
    "You write plausible WRONG implementations of a code change, the kind of mistake a "
    "developer could make while implementing it. Each one must change observable "
    "behaviour of the feature the change adds or fixes -- what a function returns, "
    "writes, prints or raises -- not just style, logging or messages. Each must keep the "
    "file importable. Answer with JSON only.")

USER = """This pull request changes the code as shown in the diff below.

<problem>
{problem}
</problem>

<diff>
{patch}
</diff>

Write {n} different wrong versions of this change. For each, pick 1 to 8 CONSECUTIVE lines
of the code AFTER the change (lines starting with `+` in the diff, or unchanged context
lines around them; copy them EXACTLY, with their indentation, without the leading `+` or
space) and give the lines that replace them.

Answer with a JSON list, nothing else:
[{{"file": "path/in/the/repo.py", "find": "exact lines from the changed code",
   "replace": "the wrong lines", "why": "one short sentence: what this version gets wrong, as behaviour"}}]
"""


def generate(instance: dict[str, Any], out_dir: Path | None = None, n: int = 6,
             model: str | None = None) -> list[dict]:
    """The model's wrong versions for one pull request, cached as `wrong_fixes.json`."""
    cache = out_dir / "wrong_fixes.json" if out_dir else None
    if cache is not None and cache.exists():
        try:
            return json.loads(cache.read_text())
        except ValueError:
            pass
    from openhands.sdk.llm import Message, TextContent

    from openhands_f2p import llm_config
    from openhands_f2p import models as M
    from openhands_f2p.prompt import clip_marked
    llm, model, _ = llm_config.configure_llm(
        usage_id="f2p-wrong-fixes",
        completions_dir=(out_dir / "wrong_fixes" / "completions") if out_dir else None,
        model=model or M.DEFAULT_JUDGE, timeout=M.DEFAULT_JUDGE_TIMEOUT)
    user = USER.format(problem=clip_marked(instance["problem_statement"].strip(), 8000),
                       patch=clip_marked(instance["patch"], 20000), n=n)
    got: list[dict] = []
    for _ in (1, 2):
        resp = llm.completion([Message(role="system", content=[TextContent(text=SYSTEM)]),
                               Message(role="user", content=[TextContent(text=user)])])
        text = "".join(c.text for c in resp.message.content if getattr(c, "text", None))
        m = re.search(r"\[.*\]", text, re.S)
        try:
            raw = json.loads(m.group(0)) if m else []
        except ValueError:
            raw = []
        got = [w for w in raw if isinstance(w, dict) and w.get("file") and w.get("find")
               and isinstance(w.get("replace"), str)]
        if got:
            break
    if cache is not None:
        cache.write_text(json.dumps(got, indent=2))
    return got


def build(box, entries: list[dict]):
    """`mutants.Mutant`s from the model's entries, read against the code as it stands --
    call with the change applied. Entries whose text is not found verbatim, that do not
    parse, or that compile to the same bytecode as the fix are dropped."""
    from openhands_f2p import mutants as M
    out = []
    for k, w in enumerate(entries):
        path = w["file"].lstrip("./").removeprefix("a/").removeprefix("b/")
        head = box.read(path)
        find, repl = w["find"].strip("\n"), w["replace"].strip("\n")
        if head is None or not find.strip() or find not in head or find == repl:
            continue
        source = head.replace(find, repl, 1)
        try:
            ast.parse(source)
        except SyntaxError:
            continue
        if M.same_bytecode(head, source, path):
            continue
        line = head[:head.index(find)].count("\n") + 1
        out.append(M.Mutant(
            name=f"wrong-{k + 1}", file=path, line=line,
            operator=(w.get("why") or "a wrong version of the change").strip(),
            source=source,
            diff="".join(difflib.unified_diff(head.splitlines(keepends=True),
                                              source.splitlines(keepends=True),
                                              fromfile=f"a/{path}", tofile=f"b/{path}", n=1))))
    return out
