"""Does the generated test check the same thing the developer's test checks?

The F2P verdict is mechanical: fails at base, passes at head. It says nothing about
*what* was asserted. A test can be fail-to-pass and still be about something adjacent to
the bug -- it flipped for the right commit, which is not the same as testing the right
behaviour. Nothing in the harness looked at that until this step.

So after the verdict is settled, one LLM call reads both tests and compares them on three
questions -- the behaviour pinned, the part of the fix covered, readability -- each on a
symmetric scale where either test can be the better one (scale 6, since 2026-09-28). It
is told which test is the developer's: some of a maintainer's choices carry project
experience -- a security path, a compatibility constraint -- that the generated test's
author could not have had, and a blind judge would read those as defects.

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

SYSTEM = """You are a senior maintainer reviewing a regression test someone proposes for a bug
fix, by comparing it with the test the project's own developer wrote for the same fix.

You are given four things: the bug report, the fix that was merged, **the developer's
test** (written by a maintainer of this project as part of the fix), and **the generated
test** (written afterwards by someone who saw the report and the fix but not the
developer's test). You know which is which, and you should use that: the developer knows
this project, and some of their choices carry knowledge the other author did not have.

Compare the two tests on three separate questions and keep them separate -- a test can
pin the right behaviour and be hard to read, or read beautifully and miss half the fix.
Each question is answered with a level from 1 to 5 on the same comparative scale:

    1  the developer's test is clearly better
    2  the developer's test is somewhat better
    3  the two are on a par
    4  the generated test is somewhat better
    5  the generated test is clearly better

The scale is symmetric on purpose. Either test can be the better one on any question, and
a generated test that is better than the developer's must be scored 4 or 5 -- do not cap
it at 3 out of deference. Equally, do not score it 4 or 5 because it is longer, has more
test functions, or has more comments. Pick, for each question, the level whose whole
description below is true; when two seem to fit, read the anchors again and take the one
the evidence you will quote supports.

---------------------------------------------------------------------------------------
**Before comparing: what each author could know.**

A choice in the developer's test that looks odd, narrow or even like bad practice may
come from experience the generated test's author did not have: a security consequence
(an escaping or permission path a django fix must not reopen), backwards compatibility,
an earlier regression in the same place, a platform or database quirk, a convention this
project enforces. Before you score the generated test higher on a point where it differs
from the developer's choice, ask whether that choice has such a reason -- visible in the
report, in the fix (a comment, a guard, the shape of the change), or in what a maintainer
of this project would plausibly know. If it plausibly does and the generated test lacks
it, the generated test is not better on that point; say what the reason is in
`developer_reasons`. If you can find no such reason, do not invent one, and do not
penalise the generated test for not copying an arbitrary choice.

---------------------------------------------------------------------------------------
**Question 1 -- concept: which test pins the behaviour this fix establishes, and how well?**

"The behaviour" is the observable contract the fix implements: what the changed code now
returns, raises or does, for the inputs the fix is about. Not the style, the names, the
route to the code, or the mechanism. Two tests that reach the same behaviour by different
routes pin the same concept. Work out that contract from the report and the fix first,
then judge each test against it:

- which behaviour does each test actually assert (not merely exercise)?
- how precisely -- an exact expected value or exception pins it; "is not None", "no
  exception was raised", a type check, or "the output changed" only brushes it;
- does it assert the contract, or only the reported symptom, one example of it, or a
  neighbouring property that happens to change in the same commit?
- a test that reads the source code as text and asserts on it pins no behaviour at all.

Levels:
- **1** The generated test asserts a different behaviour, a merely neighbouring one, the
  source text, or asserts nothing meaningful -- while the developer's test pins the
  contract.
- **2** Both are about the contract, but the generated test pins it less well: a weaker
  assertion, a clearly smaller part of it, or it misses a case the developer checks
  deliberately (including a case whose reason is developer experience, see above).
- **3** Both pin the same contract with comparable precision. Differences are of route,
  naming or structure only, or each is stronger on a different minor point.
- **4** The generated test pins everything the developer's pins and pins it better on at
  least one real point: an exact value where the developer checks a weaker property, or
  an input the contract is genuinely about that the developer's test leaves unchecked.
- **5** The generated test pins the contract where the developer's test pins only a
  symptom, a single example of a general rule, or a weak proxy for it -- and loses
  nothing the developer's test checks for a reason.

---------------------------------------------------------------------------------------
**Question 2 -- issue coverage: which test covers more of what the fix settles?**

First list the distinct behaviours this pull request settles, from the report *and the
fix* -- never from either test. Separate cases, separate branches, an error path as well as
a success path, the same fix applied in two symmetric places, and a behaviour the fix
implements that the report never mentioned (developers often fix a neighbouring hazard
they know about -- if the fix implements it, it counts). Keep the list to behaviours of
this change; general properties of the function that the fix does not touch do not count.

Then, for each behaviour and for each test, quote the single line that asserts it, or
write "none". **A behaviour is covered by a test only if you can quote the assertion that
checks its outcome.** Reaching the code path without asserting what it should now produce,
or asserting something weaker (not None, no exception, not equal to the old buggy value
when the new value is specific) is not coverage.

Levels, from the two columns you filled in:
- **1** The developer's test covers two or more listed behaviours that the generated test
  does not, or covers the main behaviour while the generated test covers none.
- **2** The developer's test covers one listed behaviour the generated test does not, and
  the generated test covers nothing the developer's misses of equal weight.
- **3** Both cover the same behaviours, or each covers one the other misses and those are
  of similar weight.
- **4** The generated test covers one listed behaviour the developer's does not, and misses
  nothing the developer's test covers.
- **5** The generated test covers two or more listed behaviours the developer's does not,
  and misses nothing the developer's test covers.

---------------------------------------------------------------------------------------
**Question 3 -- readability: which test would a reviewer of this project find easier to
read, understand and maintain?**

Read both as a reviewer would, in this project's conventions (the developer's test and the
surrounding code in the fix are your evidence of them). What makes a test readable:

- names that say what things are and what case is tested (`result`, `data`, `x`, `test1`
  are not names);
- assertions that state the expected outcome plainly, so a failure message explains itself;
- a reader can tell from the test alone which behaviour is pinned and why;
- setup that is minimal and relevant -- no unused fixtures, dead code, debug prints, or
  copies of production logic re-implemented inside the test;
- repetition handled the way the project handles it (a loop, parametrisation, subTest)
  rather than pasted blocks -- and, the other way, no abstraction that hides a simple case;
- following the project's conventions (test class vs function, helpers, imports).

Length, docstrings and comments are not readability in themselves. A comment helps only
when it says *why* something non-obvious is done; a docstring that restates the test name
adds nothing; a longer test is not more readable for being longer. Do not prefer either test
because of who wrote it. Ignore formatting and line length.

Give each test an absolute review outcome first -- `accept`, `nits` (accept with small
comments), `changes` (changes requested before merging) or `reject` -- with its concrete
problems, then compare:
- **1** The generated test is clearly less readable: it would need substantial rework
  where the developer's would not, or it is misleading or vacuous.
- **2** The generated test is somewhat less readable: it would draw more or weightier review
  comments than the developer's.
- **3** On a par: comparable review outcome and comparable problems, even if different ones.
- **4** The generated test is somewhat more readable: clearer names, plainer assertions or
  tighter setup, and it would draw fewer review comments.
- **5** The generated test is clearly more readable: it would be accepted as it stands
  while the developer's test has real readability problems (misleading names, an
  assertion that does not say what it checks, unexplained magic values or setup).

---------------------------------------------------------------------------------------
Answer with JSON only, no prose around it, in exactly this shape:

{
  "concept": {
    "level": 1 | 2 | 3 | 4 | 5,
    "contract": "one sentence: the behaviour this fix establishes",
    "generated_asserts": "one sentence: what the generated test actually asserts",
    "developer_asserts": "one sentence: what the developer's test actually asserts",
    "same_behaviour": "yes" | "partly" | "no",
    "generated_better_at": "specific point, or 'nothing'",
    "developer_better_at": "specific point, or 'nothing'",
    "developer_reasons": "a choice in the developer's test that likely carries project experience, and what it is; or 'none found'"
  },
  "issue_coverage": {
    "level": 1 | 2 | 3 | 4 | 5,
    "behaviours": [
      {"behaviour": "one line", "generated": "the exact asserting line, or 'none'", "developer": "the exact asserting line, or 'none'"}
    ]
  },
  "readability": {
    "level": 1 | 2 | 3 | 4 | 5,
    "generated_review": "accept" | "nits" | "changes" | "reject",
    "developer_review": "accept" | "nits" | "changes" | "reject",
    "generated_problems": ["specific and quotable, or empty"],
    "developer_problems": ["specific and quotable, or empty"],
    "difference": "one sentence: what makes one easier to read than the other, or why they are on a par"
  },
  "confidence": "high" | "medium" | "low",
  "reasoning": "two sentences at most"
}

Every level must follow from what you wrote beside it: a concept 4 or 5 needs a real
`generated_better_at`; a 1 or 2 needs a real `developer_better_at`; an issue level must match
the two columns of `behaviours`; a readability level must match the two reviews and problem
lists. Where your evidence is thin -- a test you could not fully follow, a fix whose intent
is unclear -- say so with `confidence`, not by drifting toward 3.

One thing is never a defect: a long test may reach you elided. Judge what you were given,
and do not report truncation, an unterminated string at the end of an excerpt, or a missing
closing bracket as a fault in either test.
"""


USER = """Bug report
==========
{problem}

The fix that was merged
=======================
{patch}

The developer's test (written by a maintainer of this project, as part of the fix)
===================================================================================
{developer_test}

The generated test (written afterwards, from the report and the fix only)
=========================================================================
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
#
# Scale 6 (2026-09-28) is comparative: 3 is on a par, below it the developer's test is
# better, above it the generated one. Scale 5 was absolute -- how good the generated test
# was, with the developer's test as a reference -- and had no level for a generated test
# better than the developer's; its labels are kept to read older results.
SCALES: dict[str, dict[int, str]] = {
    "concept":  {1: "developer's clearly better", 2: "developer's better", 3: "on a par",
                 4: "generated better", 5: "generated clearly better"},
    "issue":    {1: "developer's covers clearly more", 2: "developer's covers more",
                 3: "same coverage", 4: "generated covers more",
                 5: "generated covers clearly more"},
    "readable": {1: "clearly less readable", 2: "less readable", 3: "as readable",
                 4: "more readable", 5: "clearly more readable"},
}
SCALE_VERSION = 6
SCALES_V5: dict[str, dict[int, str]] = {
    "concept":  {1: "different", 2: "tangential", 3: "narrower", 4: "close",
                 5: "equivalent"},
    "issue":    {1: "none", 2: "minor only", 3: "main only", 4: "nearly complete",
                 5: "complete"},
    "readable": {1: "reject", 2: "poor", 3: "acceptable", 4: "good", 5: "exemplary"},
}


def _level(value: Any) -> int:
    n = int(value)
    if n not in range(1, 6):
        raise ValueError(f"level {value!r} is outside 1..5")
    return n


def _levels(out: dict[str, Any]) -> dict[str, Any]:
    """Attach the label for every level, in the fields existing readers already read.

    The concept answer is flattened to the top level, where every reader of the judge
    has always looked (`level`, `verdict` and the concept fields beside them); issue
    coverage and readability stay sub-blocks with their own `level` and `verdict`.
    `uncovered` is derived for the reports: the listed behaviours the generated test has
    no assertion for. A level that is missing or out of range is not guessed at -- the
    whole answer becomes `unparsed`.
    """
    concept = out.pop("concept")
    c = _level(concept.pop("level"))
    out.update(concept)
    out["level"], out["verdict"] = c, SCALES["concept"][c]
    for key, scale in (("issue_coverage", "issue"), ("readability", "readable")):
        block = out.get(key) or {}
        n = _level(block.get("level"))
        block["level"], block["verdict"] = n, SCALES[scale][n]
        out[key] = block
    beh = out["issue_coverage"].get("behaviours") or []
    out["issue_coverage"]["uncovered"] = [
        b.get("behaviour", "") for b in beh
        if str(b.get("generated", "none")).strip().lower() in ("none", "", "'none'")]
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
    # Asked at most twice, with the identical prompt, and only when the answer cannot be
    # read. One judgement in about fifty came back unparseable in experiments-v2's first
    # pass (django-14792), with nothing on disk to say why. Same model, same settings:
    # a re-ask, not a fallback. An answer that still cannot be read is kept whole in
    # `raw`, so the next one can be diagnosed.
    for attempt in (1, 2):
        resp = llm.completion([
            Message(role="system", content=[TextContent(text=SYSTEM)]),
            Message(role="user", content=[TextContent(text=user)]),
        ])
        text = "".join(c.text for c in resp.message.content
                       if getattr(c, "text", None))
        out = _parse(text)
        if out.get("verdict") != "unparsed":
            break
        out["raw"] = text
    out["attempts"] = attempt
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
