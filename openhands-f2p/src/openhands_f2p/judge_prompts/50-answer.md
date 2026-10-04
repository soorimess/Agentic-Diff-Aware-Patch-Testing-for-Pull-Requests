---
name: answer
job: The answer's shape, `meaningful` first (user, 2026-10-04). The model writes numbers and labels only; `compare.py` looks the
  level labels up and checks every question label against the lists in 20-40, so a label
  cannot drift from its definition. The levels are the judge's own decision: no rule ties
  them to the question labels (user, 2026-09-29).
---
Answer with JSON only, no prose around it, in exactly this shape. Every question takes one
label from its list, spelled exactly as listed:

{
  "meaningful": {"answer": "yes" | "no", "rests_on": "one sentence: what the generated test's flip actually rests on"},
  "concept": {
    "questions": {"C1": "<label>", "C2": "<label>", "C3": "<label>", "C4": "<label>", "C5": "<label>"},
    "level": 1 | 2 | 3 | 4 | 5,
    "contract": "one sentence: the behaviour this fix establishes",
    "generated_asserts": "one sentence: what the generated test actually asserts",
    "developer_asserts": "one sentence: what the developer's test actually asserts",
    "generated_better_at": "specific point, or 'nothing'",
    "developer_better_at": "specific point, or 'nothing'",
    "developer_reasons": "a choice in the developer's test that likely carries project experience, and what it is; or 'none found'"
  },
  "issue_coverage": {
    "questions": {"I1": "<label>", "I2": "<label>", "I3": "<label>", "I4": "<label>", "I5": "<label>"},
    "level": 1 | 2 | 3 | 4 | 5,
    "behaviours": [
      {"behaviour": "one line", "generated": "the exact asserting line, or 'none'", "developer": "the exact asserting line, or 'none'"}
    ]
  },
  "readability": {
    "questions": {"R1": "<label>", "R2": "<label>", "R3": "<label>", "R4": "<label>", "R5": "<label>"},
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

Decide each level yourself, from everything you found -- the questions, the behaviours you
quoted, the reviews. Where your evidence is thin -- a test you could not fully follow, a
fix whose intent is unclear -- say so with `confidence`, not by drifting toward 3.
