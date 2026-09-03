"""Does the generated test check the same thing the developer's test checks?

The F2P verdict is mechanical: fails at base, passes at head. It says nothing about
*what* was asserted. A test can be fail-to-pass and still be about something adjacent to
the bug -- it flipped for the right commit, which is not the same as testing the right
behaviour. Nothing in the harness looked at that until this step.

So after the verdict is settled, one LLM call reads both tests and answers a single
question: are these two tests about the same thing?

Three rules this step lives by.

**It runs last, always.** The developer's test is the answer to the task. Anything that
reads it must run after the generated test is finalised and scored, or the measurement
is void. Ordering is the whole safety property here, and it is enforced by where the
call sites are, not by a flag.

**It is a plain completion, not an agent.** No tools, no repository access, no
iteration. It sees two pieces of text and returns a judgement. That keeps it cheap and
keeps its failure modes small.

**Its answer is not the score.** F2P remains the number. This is a second, softer
reading, recorded alongside -- useful precisely where the two disagree. A test that is
F2P but `different` is the interesting case, and so is one that is `same` but not F2P.
"""
from __future__ import annotations

import os

import json
import re
from typing import Any

from openhands_f2p import llm_config

SYSTEM = """You compare two Python tests that were written for the same bug report.

One was written by the library's own maintainer as part of the fix. The other was
generated. Judge whether they test the same thing.

"The same thing" means the same observable behaviour of the same code path -- not the
same style, the same names, or the same mechanism. Two tests that reach the same
behaviour by different routes are the same concept. A test that checks a neighbouring
behaviour that happens to change in the same commit is not.

Answer with JSON only, no prose around it, in exactly this shape:

{
  "verdict": "same" | "narrower" | "broader" | "different",
  "generated_asserts": "one sentence: what the generated test actually checks",
  "developer_asserts": "one sentence: what the developer's test actually checks",
  "shared": "the behaviour both reach, or 'none'",
  "missed": "what the developer's test covers that the generated one does not, or 'nothing'",
  "confidence": "high" | "medium" | "low",
  "reasoning": "two sentences at most"
}

Use "narrower" when the generated test checks a real subset of the developer's -- the
right behaviour, fewer cases. Use "broader" when it checks that and more. Use
"different" when it is about another behaviour, even if it would pass and fail at the
same commits."""

USER = """Bug report
==========
{problem}

The fix that was applied
========================
{patch}

The maintainer's test
=====================
{developer_test}

The generated test
==================
{generated}
"""

FENCE = re.compile(r"```(?:json)?\s*\n(.*?)```", re.S)


def added_lines(diff: str) -> str:
    """The test the developer added, without the diff noise around it."""
    out = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            out.append(line[1:])
    return "\n".join(out)


def _parse(text: str) -> dict[str, Any]:
    blocks = FENCE.findall(text)
    raw = blocks[0] if blocks else text
    start, end = raw.find("{"), raw.rfind("}")
    if start >= 0 and end > start:
        raw = raw[start:end + 1]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"verdict": "unparsed", "reasoning": text[:400],
                "confidence": "low"}


def compare(instance: dict[str, Any], generated: str,
            quiet: bool = False) -> dict[str, Any]:
    """Judge one generated test against the developer's. Never call before scoring."""
    from openhands.sdk.llm import Message, TextContent

    # Deliberately a stronger model than the agent's. This call has to read two tests
    # and decide whether they check the same thing -- a judgement, not a search -- and
    # it happens once per instance rather than thirty times.
    llm, model, _ = llm_config.configure_llm(
        usage_id="f2p-compare",
        model=os.getenv("LLM_JUDGE_MODEL") or "litellm_proxy/gpt-5.5",
        timeout=int(os.getenv("LLM_JUDGE_TIMEOUT") or 180))
    user = USER.format(
        problem=instance["problem_statement"].strip()[:3000],
        patch=instance["patch"][:3000],
        developer_test=added_lines(instance["test_patch"])[:3000],
        generated=generated[:3000])
    resp = llm.completion([
        Message(role="system", content=[TextContent(text=SYSTEM)]),
        Message(role="user", content=[TextContent(text=user)]),
    ])
    text = "".join(c.text for c in resp.message.content
                   if getattr(c, "text", None))
    out = _parse(text)
    out["model"] = model
    return out


def line(result: dict[str, Any]) -> str:
    v = result.get("verdict", "?")
    conf = result.get("confidence", "?")
    return f"{v} ({conf} confidence) -- {result.get('reasoning', '')[:90]}"
