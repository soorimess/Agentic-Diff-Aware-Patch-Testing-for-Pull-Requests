"""How does the generated test compare with the developer's, on concept, issue coverage and readability?

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

# The prompt lives in judge_prompts/, one file per part, like the agent's in prompts/
# (2026-09-29): numbered pieces joined in order into the system prompt, `user.md` the
# user turn. See judge_prompts/README.md.
JUDGE_PROMPTS = Path(__file__).resolve().parent / "judge_prompts"
_HEADER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def _body(path: Path) -> str:
    raw = path.read_text()
    m = _HEADER.match(raw)
    if not m:
        raise ValueError(f"{path.name} has no `---` header naming it and its job")
    return raw[m.end():].strip()


def pieces() -> list[Path]:
    return sorted(JUDGE_PROMPTS.glob("[0-9][0-9]-*.md"))


SYSTEM = "\n\n".join(_body(p) for p in pieces())
USER = _body(JUDGE_PROMPTS / "user.md") + "\n"

# The questions of each subject and their labels, read off the pieces: a bullet
# `- **C1** <question> Labels: `a` · `b`` (possibly wrapped) defines one. The prompt text
# is the only list, so a label cannot be allowed here and absent there.
_QUESTION = re.compile(r"^- \*\*([CIR]\d)\*\* ")
_SUBJECT = {"C": "concept", "I": "issue_coverage", "R": "readability"}


def _questions() -> dict[str, dict[str, dict]]:
    out: dict[str, dict[str, dict]] = {v: {} for v in _SUBJECT.values()}
    for path in pieces():
        lines = path.read_text().splitlines()
        for k, line in enumerate(lines):
            m = _QUESTION.match(line)
            if not m:
                continue
            text = line[m.end():]
            for more in lines[k + 1:]:
                if not more.startswith("  ") or more.lstrip().startswith("- "):
                    break
                text += " " + more.strip()
            ask, sep, labels = text.partition("Labels:")
            if not sep:
                raise ValueError(f"{path.name}: {m.group(1)} has no `Labels:`")
            out[_SUBJECT[m.group(1)[0]]][m.group(1)] = {
                "question": ask.strip(), "labels": re.findall(r"`([a-z][a-z/-]*)`", labels)}
    return out


QUESTIONS = _questions()


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
# The questions under each level (judge_prompts/, 2026-09-29). Same scale 6 levels, so the
# levels stay comparable; `rubric` says whether the questions were asked.
RUBRIC = "questions-v2"     # v2 (2026-10-04): + `meaningful`, yes/no, first
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


def _labels(block: dict, subject: str) -> dict[str, str]:
    """The block's question labels, every one present and spelled as its piece lists it."""
    got = block.get("questions") or {}
    for qid, q in QUESTIONS[subject].items():
        if got.get(qid) not in q["labels"]:
            raise ValueError(f"{qid}={got.get(qid)!r} is not one of {q['labels']}")
    return {qid: got[qid] for qid in QUESTIONS[subject]}


def _levels(out: dict[str, Any]) -> dict[str, Any]:
    """Attach the label for every level, in the fields existing readers already read.

    The concept answer is flattened to the top level, where every reader of the judge
    has always looked (`level`, `verdict`, `questions` and the concept fields beside
    them); issue coverage and readability stay sub-blocks with their own `level`,
    `verdict` and `questions`. `uncovered` is derived for the reports: the listed
    behaviours the generated test has no assertion for. A level or question label that
    is missing or not on its list is not guessed at -- the whole answer becomes
    `unparsed`.
    """
    # The first label (user, 2026-10-04): absolute, yes or no, read before anything else.
    # Required like every other field -- a missing or misspelled answer makes the whole
    # judgement `unparsed` and re-asked, never a guessed "yes".
    meaningful = out.pop("meaningful")
    answer = str(meaningful.get("answer", "")).strip().lower()
    if answer not in ("yes", "no"):
        raise ValueError(f"meaningful={meaningful.get('answer')!r} is not yes or no")
    concept = out.pop("concept")
    c = _level(concept.pop("level"))
    concept["questions"] = _labels(concept, "concept")
    out.update(concept)
    out["level"], out["verdict"] = c, SCALES["concept"][c]
    for key, scale in (("issue_coverage", "issue"), ("readability", "readable")):
        block = out.get(key) or {}
        n = _level(block.get("level"))
        block["questions"] = _labels(block, key)
        block["level"], block["verdict"] = n, SCALES[scale][n]
        out[key] = block
    beh = out["issue_coverage"].get("behaviours") or []
    out["issue_coverage"]["uncovered"] = [
        b.get("behaviour", "") for b in beh
        if str(b.get("generated", "none")).strip().lower() in ("none", "", "'none'")]
    out["meaningful"] = {"answer": answer, "rests_on": meaningful.get("rests_on", "")}
    out["scale"] = SCALE_VERSION
    out["rubric"] = RUBRIC
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
    # The levels are the judge's own decision (user, 2026-09-29): no rule ties them to
    # the question labels, so an answer is re-asked only when it cannot be read.
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
    meaningful = (result.get("meaningful") or {}).get("answer", "?")
    return (f"meaningful {meaningful} | "
            f"concept {shown(result)} | issue {shown(result.get('issue_coverage'))} | "
            f"readable {shown(result.get('readability'))} "
            f"({result.get('confidence', '?')} conf){tail}")


if __name__ == "__main__":
    import sys
    if "--show" in sys.argv:
        print(SYSTEM)
        print("\n" + "=" * 30 + " user turn " + "=" * 30 + "\n")
        print(USER)
    else:
        for subject, qs in QUESTIONS.items():
            print(subject)
            for qid, q in qs.items():
                print(f"  {qid}  {q['question']}\n      {' | '.join(q['labels'])}")
