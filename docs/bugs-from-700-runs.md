# What 700 runs showed was wrong with the harness

Read out of the ten-arm series (`experiments/`, 70 instances × 10 arms) after a rerun of
the base arm's failures recovered 11 of 28 on an unchanged configuration. The question
was whether that was variance or a defect. It was both, and the defects were found by
reading tool logs, completions and the generated tests themselves, not by counting
verdicts.

The logic that produced the ten arms is preserved on branch `final-state-of-first-runs`.
Everything below is fixed on `main` unless marked otherwise.

## Fixed

### The stop was refused once, and then never again

`conversation.run()` was called a single time after the refusal message. The agent was
told *"You cannot finish while this is the answer"*, edited the test, and called `finish`
again -- and that second stop went through, because `finish` is the SDK's own tool and
nothing guarded it.

| across runs with a verify tool (630) | |
|---|---:|
| ended on an edit never re-verified | 162 (25%) |
| of those, after the refusal had already fired | 144 |
| edited after a verify that said NOT fail-to-pass | 103 → 75 NO, 27 BROKEN, 1 YES |
| held verify + the tool duty and never called verify at all | 30, all refused once, all ignored it |

This is why the second chance converted so unevenly by reason:

| refusal reason | runs | converted |
|---|---:|---:|
| `loop_open` -- one more verify was enough | 146 | 46% |
| `collects_nothing` | 55 | 23% |
| `passes_at_base` -- needs several rewrite→verify rounds | 156 | 3% |

The agent did try: 94% of `passes_at_base` continuations rewrote the test, averaging two
writes and one verify, with a median of 6 actions spent of 68 offered. It was not refused
a second time. **Fix:** every stop is checked; up to five refusals, ending early when the
gap closes or the agent does nothing but stop twice running.

### django's runner collects only `TestCase` methods, and nobody said so

`runtests.py` is unittest discovery. A module-level `def test_x():` prints
`Ran 0 tests ... OK`, exits 0, and scores as nothing collected.

- 44 of the 50 "collected nothing" failures in the series were django; 31 of those files
  defined only bare functions.
- **127 of 127** successful django runs used a `TestCase` class. No bare-function django
  test ever passed.
- The briefing said "no `import pytest`, no fixtures", asked for "one test function per
  behaviour", and never mentioned `TestCase` or `unittest`. Its one style example for
  django was `tests/test_sqlite.py`, a settings module.

django is 27 of the 70 instances. **Fix:** `repo_facts` states the collection rule for any
labels runner (keyed on the runner kind, not the repository); style samples are files that
define a test; the goal says "one test per behaviour", in whatever form the runner collects.

### `verify`'s supporting lines contradicted its headline

The headline always applied the harness rule. Everything under it keyed on "did anything
flip": the duty line, the coverage pointer, the pointer to `mutation`, and the error flag.
`scikit-learn-14087` wrote three tests, two flipped and one still failed; it read
*"NOT fail-to-pass ... still fail after the change"* followed by *"That it flips, and what
it reaches, are two of the three questions"*, with no duty line, five times, and scored NO.
21 of 700 runs ended holding a correctly flipping test beside a failing one.

(An earlier summary of this said the tool reported "Fail-to-pass: 2 test(s)". It did not;
the headline was right and the lines beneath it were wrong.) **Fix:** one `ok` -- something
flipped and nothing still fails -- drives every line.

### A negative verdict arrived as a tool error

`is_error=not flipped`, so "your test passes at base" was delivered prefixed
`[An error occurred during execution.]`. When a refusal began there was a median of five
of these already in context. Success fell from 85% with none to 27% with six or more --
confounded, since a struggling run calls `verify` more, so no causal claim; but the framing
was wrong regardless. **Fix:** a verdict is never an error.

### Coverage was both the agent's target and the published metric

The tool ended *"100% is the target"*; `58-finish.md` said *"none of these figures is a
target"*. The percentage the agent was told to push up is the one the report publishes as
an independent quality measure, which makes arms with the tool and arms without it measure
different things. **Fix:** the agent is shown the lines it misses and asked for a test that
runs every changed line; no percentage, no target. The harness computes the figure outside.

### The trajectory hid every refusal

The refusal was sent to the model (it is in `completions/`) and logged in `flow.log`, but
`trajectory.json` was rebuilt from the opening task alone and showed one user message. This
is how the single-shot refusal stayed invisible through a whole series. **Fix:**
`injected_messages.json`, placed in the trajectory at the tool-log position it arrived.

### The guard statistic was mostly false positives

`files_edited_outside_test` compared raw path strings, so the agent's own test written as
`/testbed/tests/x.py` or `./tests/x.py` counted as a write outside the test. 296 of 700 runs
populated it. **Fix:** paths are normalised (`testbed/tests/x.py` without the slash is kept,
because it really does create a stray directory), and scratch files the agent created are
listed apart from edits to files that existed at base.

### A missing target file did not say what was written instead

`seaborn-3069` wrote `..._3269.py` -- one digit off -- and the record read *"wrote no test
at ..._3069.py"*. Correct, but it looked like the agent wrote nothing. (An earlier summary
called this a substantive NO; it was not.) **Fix:** the message names the test files it did
write.

## Not changed yet, on purpose

- **Sampling is unset.** No `temperature`, `top_p` or `seed` anywhere; four identical
  gateway calls returned three different answers. To be tested on its own before adoption.
- **A second chance that hands the agent its own failing test** with the remaining budget,
  rather than asking it to recall the file. To be tested on its own. Discarding the
  conversation, as a fresh retry does, is ruled out.

## What this does to the ten-arm results

The ten arms ran identical verdict-path code, so they remain comparable with each other.
But the refusal and django fixes change verdicts, so the new system's numbers are not
comparable with the old ones, and no conclusion should mix the two.
