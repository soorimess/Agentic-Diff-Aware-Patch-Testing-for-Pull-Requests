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
| `16-explore.md` | what to establish about the checkout, when the briefing is withheld |
| `20-goal.md` | the one deliverable, and what fail-to-pass means |
| `30-issue.md` | the bug report, verbatim from the dataset |
| `40-tools.md` | the always-present tools, that `run_tests` builds the command, and to read neighbouring tests first |
| `45-tools-verify.md` | `verify`, which needs the diff |
| `46-tools-coverage.md` | `coverage`, and what it is for |
| `47-tools-mutation.md` | `mutation`, and how to read a survivor without gaming it |
| `50-rules.md` | the constraints, and why each exists |
| `55-check-runs.md` | check one: does the file run |
| `56-check-flips.md` | check two: does it fail before and pass after |
| `57-check-reaches.md` | check three: does it reach the changed lines |
| `57b-check-notices.md` | check four: would it notice a wrong fix |
| `58-finish.md` | when to stop, and to re-run the checks after changing the test |

The `5x` checks are separate files because configurations have different tools. A step
that named a tool the agent had not been given would send it after something that never
answers.

There were also `60-runner-*.md` files, one per test runner, carrying per-repository
advice. They were deleted: right for the twelve repositories someone had looked at and
silently absent for the thirteenth. `15-repo.md` replaced them, read off the checkout by
`repo_facts` with no model involved.

`16-explore.md` is that piece's opposite number, included only with `--repo-search`. It
asks the same questions and answers none of them: naming an answer — that tests live in a
directory called `tests` — would put the deleted per-repository advice straight back.

## How a piece knows whether it applies

Two mechanisms, because dropping whole instructions is not enough on its own.

**`needs:` in the header** drops the piece. `35-change.md` *is* the diff, so with
`--no-patch` there is nothing left of it to include.

```
---
name: change
needs: patch
job: ...
---
```

A name can be negated. `needs: !repo-facts` keeps the piece only while that feature is
*off*, which is how a withheld component gets a substitute instruction instead of leaving
a hole. `16-explore.md` is the only piece that uses it so far, and it is the reason the
form exists: withholding the briefing on how a project tests has to *add* the instruction
to work it out, or the run measures a missing instruction rather than a missing input.

**`{?feature} ... {/feature}` in the body** drops a paragraph. Most pieces are not
all-or-nothing: `20-goal.md` still has a job when the diff is withheld, but the clause
about "what it will do *after* the change" describes something the agent can no longer
see. Same for the multi-check framing in `55-check-runs.md` — "work through these in
order" describes nothing when one check is left.

A block can also sit inside a paragraph, opener right after the text it follows:
`...rather than passing it.{?guard} This is checked after every action...{/guard}` keeps or
drops that one sentence and leaves the paragraph break after it alone. `50-rules.md` does
this for the guard's "any such edit is reverted" and `57-check-reaches.md` for the
coverage duty's "it will be sent back": an arm without the feature must not be told it is
enforced.

Feature names come from `FEATURES` in `openhands_f2p/features.py`. A name that is not in
that registry raises when the piece is parsed, so a typo fails loudly instead of silently
including or excluding text.

**The guarantee:** after assembling, `prompt.build` scans the finished text for the names
of tools that were not registered and raises, naming the piece to fix. The pieces backtick
tool names consistently, which is what makes the scan precise — `` `coverage` `` is the
tool, "changed-line coverage" is prose. Check any configuration:

```bash
uv run python -m openhands_f2p.prompt --explain --no-patch
uv run python -m openhands_f2p.prompt --no-coverage-tool
uv run python -m openhands_f2p.prompt --repo-search
```

## Placeholders

`{repo}`, `{test_file}`, `{problem}` are filled in by `prompt.py`. A brace that is meant
literally must be doubled — `{{` — or formatting will fail.

## `followups/`

A subdirectory, because `pieces()` globs `prompts/*.md` and joins everything it finds into
the opening prompt. What lives one level down is a message sent as its own turn, later in
the same conversation, and only in the configurations that ask for one.

| file | job |
|---|---|
| `second-chance.md` | refuses the agent's first stop, when the run ended with nothing a judge could score. Sent by `--second-chance`. Says only what the agent could have established at base -- never that the test failed against the fix, which exists only in the head run |

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
