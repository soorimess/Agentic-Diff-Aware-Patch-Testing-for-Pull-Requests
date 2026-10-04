# The judge's prompt

The judge (`compare.py`) compares a generated test with the developer's test on three
subjects -- concept, issue coverage, readability. Its system prompt is assembled from the
numbered pieces here, in order; `user.md` is the user turn. Each piece has a header naming
it and saying what it is for, the same convention as the agent's `prompts/`.

| piece | what it does |
|---|---|
| `00-role.md` | who the judge is, what it is given, the comparative 1-5 scale |
| `10-context.md` | what each author could know (developer experience); the developer's test is added lines, the generated one a whole file; the judge cannot run either |
| `15-meaningful.md` | the first label and the only absolute one: is the generated test meaningful at all, `yes`/`no`, no questions (user, 2026-10-04) |
| `20-concept.md` | concept: questions C1-C5 with their labels, and the level anchors |
| `30-issue.md` | issue coverage: the behaviour list, questions I1-I5, and the level anchors |
| `40-readability.md` | readability: review outcomes, questions R1-R5, and the level anchors |
| `50-answer.md` | the JSON answer |
| `user.md` | the user turn: report, fix, developer's test, generated test |

**Questions are read from the pieces.** A line of the form

    - **C1** <question> Labels: `a` · `b` · `c`

defines a question and its labels; `compare.QUESTIONS` is parsed from these lines at
import, and every answer's labels are checked against it. Change a question's labels here
and the check follows; there is no second list in the code.

**The levels are the judge's own decision.** The questions are answered first and weighed,
but no rule ties a level to them (user, 2026-09-29): the judge answers both.

To see the assembled prompt: `uv run python -m openhands_f2p.compare --show`.
