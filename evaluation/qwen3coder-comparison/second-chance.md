# qwen3-coder: control against `--second-chance`

Two runs of the evaluation ten, identical except for the flag. `qwen3-coder-30b-a3b-instruct`,
`full` configuration, `--mutants 10`, `--parallel 10`, 2026-09-24.

| | folder | fail-to-pass | cost | actions | LLM calls |
|---|---|---|---|---|---|
| **control** | [`out_qwen3coder`](../out_qwen3coder/) | **5/10** | \$0.54 | 358 | 358 |
| **`--second-chance`** | [`out_qwen3coder_secondchance`](../out_qwen3coder_secondchance/) | **6/10** | \$0.50 | 326 | 327 |

The flag refuses the agent's first stop when the run ended with nothing a judge could score
and the reason is one the agent could have found itself. It continues in the same
conversation on what is left of the budget, once. It cost nothing extra: the arm ran 32
fewer actions and four cents cheaper than its control.

## Verdict, coverage, mutants

`mutants` is the held-out half of the pool, agent test against developer test on the same
set. A `—` is not measured, not zero: coverage, mutants and the judge run only on a test
that flipped, because each is a question about a test that has already met the bar.

| instance | ctl | sc | ctl coverage | sc coverage | ctl mutants | sc mutants |
|---|---|---|---|---|---|---|
| `astropy-13398` | NO | **YES** | — | 32% (31/96) | — | 0/0 |
| `django-13279` | NO | **BROKEN** | — | — | — | — |
| `matplotlib-22719` | YES | YES | 100% (2/2) | 100% (2/2) | 0/1 · 0/1 | 0/1 · 0/1 |
| `psf-requests-1766` | YES | YES | 100% (1/1) | 100% (1/1) | 0/0 · 0/0 | 0/0 · 0/0 |
| `xarray-7393` | YES | YES | 100% (3/3) | 100% (3/3) | 3/3 · 3/3 | 3/3 · 3/3 |
| `pylint-7277` | YES | YES | 100% (3/3) | 100% (3/3) | 3/3 · 3/3 | 3/3 · 3/3 |
| `pytest-7982` | NO | NO | — | — | — | — |
| `sklearn-25232` | YES | YES | 100% (5/5) | 100% (5/5) | 2/4 · 3/4 | 2/4 · 3/4 |
| `sphinx-9602` | NO | NO | — | — | — | — |
| `sympy-21612` | NO | NO | — | — | — | — |

Mutant scores are identical on every instance both arms scored. The one new entry,
`astropy-13398`, had no mutants in its held-out half, so it says nothing either way.

`astropy-13398` is also the only test in either run below 100% changed-line coverage, at
32%. It flipped on one of seven behaviours the pull request settles — a YES by the
definition, and the weakest one here.

## The judge

`concept` / `issue coverage` / `readability`, one call by a stronger model that wrote
neither test. None of it feeds the verdict.

| instance | control | `--second-chance` |
|---|---|---|
| `astropy-13398` | — | different / partial / acceptable |
| `matplotlib-22719` | same / partial / acceptable | same / partial / acceptable |
| `psf-requests-1766` | same / complete / acceptable | **broader** / complete / acceptable |
| `xarray-7393` | same / **partial** / acceptable | broader / **complete** / acceptable |
| `pylint-7277` | broader / complete / poor | broader / complete / poor |
| `sklearn-25232` | narrower / partial / poor | narrower / partial / poor |

One genuine movement: `xarray-7393` goes `partial` to `complete` on issue coverage, on an
instance already YES in both arms. The judge notes the arm's test covers several integer
and float dtypes where the control's covered one. The flag did not cause that — `xarray`
was never refused a stop — so it is run-to-run variation, and it shows the size of
variation this corpus produces on an unchanged configuration.

## Which runs were refused, and what they did with it

Budget is what remained of `--max-iterations` at the first stop; the flag neither raises
nor resets it.

| instance | reason given | budget left | actions after | outcome |
|---|---|---|---|---|
| `astropy-13398` | `loop_open` | 68 | 7 | NO → **YES** |
| `django-13279` | `collects_nothing` + `loop_open` | 66 | 8 | NO → **BROKEN** |
| `matplotlib-22719` | `loop_open` | 75 | 5 | YES → YES |
| `pytest-7982` | `passes_at_base` + `loop_open` | 71 | 12 | NO → NO |
| `sklearn-25232` | `loop_open` | 76 | 11 | YES → YES |
| `sphinx-9602` | `passes_at_base` + `loop_open` | 68 | 6 | NO → NO |
| `sympy-21612` | `passes_at_base` + `loop_open` | 67 | 1 | NO → NO |
| `psf-requests-1766` | *not refused* | | | YES |
| `xarray-7393` | *not refused* | | | YES |
| `pylint-7277` | *not refused* | | | YES |

**Seven of ten refused. One NO became a YES. One NO became a BROKEN.**

`loop_open` belongs to `require-tools`, which is on by default and fires in the control
too. `passes_at_base` and `collects_nothing` are what this flag adds — four of the seven
refusals carried one, and every one of those four was a correct statement about the tree.

Every refused run acted on the message: 1 to 12 further actions, never zero. The mechanism
is not being ignored. It is being acted on and mostly not converting.

Budget was never the constraint. The smallest remaining budget was 66 actions and the
largest continuation spent 12. Nothing here failed for want of room, which rules out the
first explanation for the five that did not convert.

`django-13279` is the row to read before assuming the flag is free. It was told
`collects_nothing`, which was true, spent eight more actions, and finished with a file that
still collected nothing — a BROKEN where the control had recorded a NO. Correct diagnosis,
worse outcome.

## Tool use

Every call each arm made.

| instance | control | `--second-chance` |
|---|---|---|
| `astropy-13398` | `run` x8, `write_file` x6, `run_tests` x5, `verify` x4 | `run` x16, `write_file` x8, `verify` x7, `coverage` x2, `mutation` x2 |
| `django-13279` | `run` x20, `write_file` x10, `verify` x6, `coverage` x2, `run_tests` x1, `mutation` x1 | `run` x17, `write_file` x11, `verify` x6 |
| `matplotlib-22719` | `run` x10, `write_file` x7, `verify` x3, `coverage` x1, `mutation` x1 | `run` x11, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x2 |
| `psf-requests-1766` | `run` x10, `write_file` x6, `run_tests` x5, `verify` x1, `coverage` x1, `mutation` x1 | `run` x11, `write_file` x4, `verify` x2, `coverage` x2, `mutation` x2 |
| `xarray-7393` | `run` x7, `write_file` x3, `run_tests` x2, `verify` x2, `coverage` x2, `mutation` x2 | `run` x10, `write_file` x2, `verify` x2, `coverage` x2, `mutation` x2 |
| `pylint-7277` | `run` x14, `write_file` x7, `run_tests` x2, `verify` x2, `coverage` x2, `mutation` x2 | `run` x11, `write_file` x3, `verify` x3, `coverage` x2, `mutation` x1 |
| `pytest-7982` | `run` x18, `write_file` x15, `verify` x5, `coverage` x1, `mutation` x1 | `run` x19, `write_file` x10, `verify` x4, `coverage` x1, `mutation` x1 |
| `sklearn-25232` | `run` x25, `write_file` x3, `verify` x3, `mutation` x3, `run_tests` x2, `coverage` x2 | `run` x15, `write_file` x5, `verify` x4, `run_tests` x3, `coverage` x3, `mutation` x2 |
| `sphinx-9602` | `run` x23, `write_file` x8, `verify` x4, `coverage` x1, `mutation` x1 | `run` x11, `write_file` x10, `run_tests` x6, `verify` x3 |
| `sympy-21612` | `run` x14, `write_file` x10, `verify` x5, `coverage` x2, `mutation` x1 | `run` x18, `write_file` x5, `verify` x4, `coverage` x1 |

Every run in both arms called `verify`, 1 to 7 times, median 3.5.

The two refused runs that moved show opposite shapes. `astropy-13398` went from 4 `verify`
calls to 7 and reached `coverage` and `mutation` it never got to in the control — and
flipped. `django-13279` spent its eight extra actions and reached neither, having never
produced a collectable file.

`run` dominates both arms: 152 of 358 control actions and 139 of 326. The agent still
spends most of its budget in the shell rather than on the instruments.

## What this says

**5/10 against 6/10 is not a result.** Ten instances, one repeat, on a set that has
returned 4, 5 and 6 across recent configurations. One instance is inside the noise, and the
`xarray` judge movement on an untouched instance is direct evidence of how wide that noise
is.

**The machinery is sound.** Seven refusals, seven correct diagnoses, seven responses, none
blocked by budget. If this flag does not pay, it will not be because it failed to fire or
failed to be heard.

**The failure it cannot fix is the common one.** Three of the five persistent NOs were told
`passes_at_base` — the test runs, collects, and passes on unfixed code. They were told
exactly what was wrong, had 67 to 71 actions left, and still could not write a test that
distinguishes the two versions. That is a capability limit, not a prompting one, and no
message closes it.

**What would settle it.** Three repeats of both arms before reading a one-instance
difference. Failing that, size the arm at the population it can reach: only four of ten
runs here carried a reason this flag adds, so a corpus-level effect is bounded by that
fraction before it starts.
