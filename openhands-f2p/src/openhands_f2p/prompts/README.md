# The agent's prompt, in pieces

The prompt is assembled at run time from the numbered files in this directory, in
filename order. Each one is a separate file so that a change can be attributed: if a
result moves, you can see which instruction moved it, and a piece can be removed for one
arm and kept for another without editing Python.

Every file has a `---` header giving its name and what job it does. **The header is
stripped before the prompt is sent** — the model sees only the body.

| file | job |
|---|---|
| `10-situation.md` | where the model is, and that the bug is still present |
| `20-goal.md` | the one deliverable, and what fail-to-pass means |
| `30-issue.md` | the bug report, verbatim from the dataset |
| `40-tools.md` | the always-present tools, that `run_tests` builds the command, and to read neighbouring tests first |
| `45-tools-verify.md` | `verify`, which needs the diff |
| `46-tools-coverage.md` | `coverage`, and what it is for |
| `50-rules.md` | the constraints, and why each exists |
| `55-check-runs.md` | check one: does the file run |
| `56-check-flips.md` | check two: does it fail before and pass after |
| `57-check-reaches.md` | check three: does it reach the changed lines |
| `58-finish.md` | when to stop |
| `60-runner-*.md` | per-repo advice, one file per test runner |

The four `5x` checks are separate files because the arms have different tools. `--blind`
drops `56` and `57` along with the diff; `--compare-coverage` drops `57` in one arm. A
step that named a tool the agent had not been given would send it after something that
never answers.

## Placeholders

`{repo}`, `{test_file}`, `{problem}` are filled in by `prompt.py`. A brace that is meant
literally must be doubled — `{{` — or formatting will fail.

## A note on what belongs here

Some of these instructions are load-bearing for the *measurement*, not for the model's
convenience. `50-rules.md` forbidding edits outside the test file is the clearest case:
without it an agent can make any test pass by changing the library, and then the
"before the fix" run is not a fact about the pull request.

Others are hints about workflow — the `5x` checks hand over a sequence the agent might
not have arrived at alone, which is a thumb on the scale for the agentic arm. They are
kept in their own files precisely so they can be dropped when that matters.

The wording of those files is load-bearing in a second way. An earlier version told the
agent to iterate until coverage answered well, which is an instruction to maximise the
number we score by: a high figure would then be evidence that the agent followed an
instruction, not that the test is good. The correction is to make *asking* mandatory and
say nothing about raising the answer — the checks are described as diagnostics, and
`57-check-reaches.md` says outright that adding a call with no assertion behind it to
raise the figure is not acceptable.
