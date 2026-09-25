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

import json
import re
from pathlib import Path
from typing import Any

from openhands_f2p import llm_config

SYSTEM = """You compare two Python tests that were written for the same bug report.

One was written by the library's own maintainer as part of the fix. The other was
generated. Judge it on three separate questions and keep them separate -- a test can be
about the right behaviour and still be unreadable, or read beautifully and miss half the
bug.

**1. Is it about the same thing?** "The same thing" means the same observable behaviour of
the same code path -- not the same style, the same names, or the same mechanism. Two tests
that reach the same behaviour by different routes are the same concept. A test that checks
a neighbouring behaviour which happens to change in the same commit is not.

**2. Does it cover everything the issue is about?** Read the bug report and the fix, and
work out how many distinct behaviours the pull request actually settles: separate cases,
separate branches, the same fix applied in two symmetric places, an error path as well as
a success path. Then say which of those the generated test reaches. Judge against the
*issue and the fix*, not against the maintainer's test -- the maintainer's test is
evidence of what mattered, not the definition of it. A test that covers one branch of a
two-branch fix is incomplete even if the maintainer only tested that branch too.

**3. Would you accept it in review?** Judge it as a reviewer of this project would:
whether names say what the values are (`result`, `data`, `x` for a parsed timestamp are
not names), whether the assertions state an expectation rather than merely exercising
code, whether a reader can tell from the test alone what behaviour is being pinned,
whether setup is minimal and relevant, and whether it follows the conventions visible in
the maintainer's test. Ignore formatting and line length. An assertion with no message
where the failure is self-explanatory is fine; a bare `assert result` is not.

Answer each question with a **level from 1 to 5**, using the definitions below exactly.
Levels are ordinal: pick the highest one whose whole description is true, not the one
nearest an overall impression.

**1. Concept -- is it about the same behaviour as the maintainer's test?**
- 5 `equivalent` -- the same observable behaviour, checked as fully as the maintainer's
  test does, or more.
- 4 `close` -- the same behaviour, missing only a minor case the maintainer's test checks.
- 3 `narrower` -- the same behaviour, but a clearly smaller part of what the maintainer's
  test checks.
- 2 `tangential` -- near the behaviour but not it: the same function exercised for another
  property, the reported symptom rather than the contract the fix implements, or a
  neighbouring behaviour that changes in the same commit.
- 1 `different` -- another behaviour altogether, even if it would pass and fail at the same
  commits.

**2. Issue coverage -- does it cover every behaviour the pull request settles?**
- 5 `complete` -- every distinct behaviour the pull request settles has an assertion.
- 4 `nearly complete` -- all but one minor behaviour: an edge case, or one of two symmetric
  places the same fix was applied.
- 3 `main only` -- the main behaviour is covered, and at least one other substantial
  behaviour the pull request settles is not.
- 2 `minor only` -- only a secondary behaviour is covered; the main one is not.
- 1 `none` -- none of the behaviours the pull request settles has an assertion.

**3. Readability -- would you accept it in review in this project?**
- 5 `exemplary` -- would pass review as it stands, and reads like the project's own tests.
- 4 `good` -- would pass with a nit or two.
- 3 `acceptable` -- would pass after small requested changes.
- 2 `poor` -- needs substantial rework before review would accept it.
- 1 `reject` -- misleading, vacuous or unreadable; review would turn it away.

Answer with JSON only, no prose around it, in exactly this shape. Give the number only;
the labels above are for you to read, not to write:

{
  "concept_level": 1 | 2 | 3 | 4 | 5,
  "generated_asserts": "one sentence: what the generated test actually checks",
  "developer_asserts": "one sentence: what the developer's test actually checks",
  "shared": "the behaviour both reach, or 'none'",
  "missed": "what the developer's test covers that the generated one does not, or 'nothing'",
  "issue_coverage": {
    "level": 1 | 2 | 3 | 4 | 5,
    "behaviours_in_pr": ["one line per distinct behaviour the pull request settles"],
    "covered": [{"behaviour": "...", "assertion": "the exact line from the generated test that checks it"}],
    "uncovered": ["those it does not, or empty"]
  },
  "readability": {
    "level": 1 | 2 | 3 | 4 | 5,
    "strengths": "one sentence, or 'none'",
    "problems": ["specific, quotable: a bad name, a vacuous assertion, unexplained setup"],
    "nothing_to_raise": "only when problems is empty: what you checked and found clean"
  },
  "confidence": "high" | "medium" | "low",
  "reasoning": "two sentences at most"
}

Be a strict reviewer on questions 2 and 3 and a fair one on question 1. Do not raise issue
coverage because the test passes, and do not raise readability because it works -- these
three answers are read separately and a uniformly generous one is worth nothing.

Two rules make that concrete rather than a wish.

**A behaviour is covered only if you can quote the assertion that checks it.** Every entry
in `covered` carries the exact line from the generated test that pins that behaviour. If
there is no such line -- the test reaches the code path but never asserts the outcome, or
asserts something weaker, such as that the result is not None or that the output is no
longer the symbolic form -- then the behaviour is uncovered and belongs in `uncovered`. A
test that exercises the fix without asserting what it should now produce has not covered
it.

**An empty `problems` list needs saying so.** If you raise nothing, fill
`nothing_to_raise` with what you actually checked -- names, assertions, setup, convention
-- and found clean. A readability of 4 or 5 with an empty list and no account of
what was examined is not an answer.

One thing is never a defect: a long generated test may reach you elided. Judge what you
were given, and do not report truncation, an unterminated string at the end of the
excerpt, or a missing closing bracket as a fault in the test.
"""


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
# A comma before a closing brace or bracket. Strict JSON rejects it, and the judge writes
# it now and then: matplotlib-13989 came back complete -- concept 5, issue 5 -- with
# `"reasoning": "...",` as its last line, and was recorded as unparsed. Tried only after
# the strict parse fails, so a well-formed answer is never rewritten.
TRAILING_COMMA = re.compile(r",(\s*[}\]])")


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
    for candidate in (raw, TRAILING_COMMA.sub(r"\1", raw)):
        try:
            return _levels(json.loads(candidate))
        except (json.JSONDecodeError, ValueError, TypeError, AttributeError, KeyError):
            continue
    return {"verdict": "unparsed", "reasoning": text[:400], "confidence": "low"}


# The three scales. The model writes only the number; the label is looked up here, so
# a label can never be spelled two ways or drift from its definition in SYSTEM. Kept in
# the order the prompt defines them, and read by the reports for their legend.
SCALES: dict[str, dict[int, str]] = {
    "concept":  {1: "different", 2: "tangential", 3: "narrower", 4: "close",
                 5: "equivalent"},
    "issue":    {1: "none", 2: "minor only", 3: "main only", 4: "nearly complete",
                 5: "complete"},
    "readable": {1: "reject", 2: "poor", 3: "acceptable", 4: "good", 5: "exemplary"},
}
SCALE_VERSION = 5


def _level(value: Any) -> int:
    n = int(value)
    if n not in range(1, 6):
        raise ValueError(f"level {value!r} is outside 1..5")
    return n


def _levels(out: dict[str, Any]) -> dict[str, Any]:
    """Attach the label for every level, in the fields existing readers already read.

    `verdict` stays the concept label and each sub-block keeps a `verdict` label, so
    everything that consumed the three-category judge still finds a word where it
    looked for one; the number sits beside it as `level`. A level that is missing or out
    of range is not guessed at -- the whole answer becomes `unparsed`.
    """
    c = _level(out.pop("concept_level"))
    out["level"], out["verdict"] = c, SCALES["concept"][c]
    for key, scale in (("issue_coverage", "issue"), ("readability", "readable")):
        block = out.get(key) or {}
        n = _level(block.get("level"))
        block["level"], block["verdict"] = n, SCALES[scale][n]
        out[key] = block
    out["scale"] = SCALE_VERSION
    return out


def shown(block: dict[str, Any] | None, key: str = "verdict") -> str:
    """How a judge answer is printed: `narrower (3)`. Older three-category answers,
    which carry no level, print as the bare word they always were."""
    block = block or {}
    label = block.get(key, "—")
    return f"{label} ({block['level']})" if block.get("level") else str(label)


def compare(instance: dict[str, Any], generated: str,
            quiet: bool = False, model: str | None = None,
            completions_dir: "Path | None" = None) -> dict[str, Any]:
    """Judge one generated test against the developer's. Never call before scoring."""
    from openhands.sdk.llm import Message, TextContent

    from openhands_f2p import models as M

    # Deliberately a stronger model than the agent's. This call has to read two tests
    # and decide whether they check the same thing -- a judgement, not a search -- and
    # it happens once per instance rather than thirty times.
    # `completions_dir`, so the judge's own tokens are on disk like the agent's.
    # Without it the judge was the one call in a run that cost money and left no
    # record, and every per-run cost we reported was the agent's alone.
    llm, model, _ = llm_config.configure_llm(
        usage_id="f2p-compare", completions_dir=completions_dir,
        model=model or M.DEFAULT_JUDGE, timeout=M.DEFAULT_JUDGE_TIMEOUT)
    user = USER.format(
        # 12000 for the generated test, not 3000. At 3000 one test in four arrived cut
        # off mid-file and the judge marked it down for exactly that -- "truncated at
        # `Test that even wi`, leaving an unterminated docstring and a syntactically
        # invalid test file" was written about a test that ran and passed. The readability
        # answer was measuring our own truncation. The rest are raised more modestly: only
        # one developer test in seventy exceeded 3000 characters.
        problem=instance["problem_statement"].strip()[:4000],
        patch=instance["patch"][:6000],
        developer_test=added_lines(instance["test_patch"])[:8000],
        generated=generated[:12000])
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
    """One terminal line. All three answers, because reading only the first is how a
    test that is 'same' and unreadable and half-complete looks like a success."""
    uncovered = (result.get("issue_coverage") or {}).get("uncovered") or []
    tail = f"  misses: {uncovered[0][:52]}" if uncovered else ""
    return (f"concept {shown(result)} | issue {shown(result.get('issue_coverage'))} | "
            f"readable {shown(result.get('readability'))} "
            f"({result.get('confidence', '?')} conf){tail}")
