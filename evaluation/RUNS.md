# Evaluation set — four models, same ten pull requests

Ten SWE-bench Verified instances, one per repository, seeded and never looked at while
the prompts were written. The 26 in `out/` are the tuned-against set; these answer the
one question that set cannot — whether the system works on instances nobody saw.

Each model's own `RUNS.md` sits beside this file with the per-instance detail.

## Headline

| model | fail-to-pass | coverage (of YES) | issue complete | cost | per instance |
|---|---|---|---|---|---|
| `gpt-5.5` | **10/10** | 95% mean, 8/9 at 100% | 7/10 | $7.42 | $0.742 |
| `gpt-5-mini` | **10/10** | 92% mean, 8/9 at 100% | 4/10 | $0.89 | $0.089 |
| `gpt-5-nano` | **6/10** | 94% mean, 5/6 at 100% | 3/10 | $0.34 | $0.034 |
| `gpt-oss-20b` | **2/10** | 100% mean, 2/2 at 100% | 2/10 | $0.24 | $0.024 |

The two strongest models are indistinguishable on the headline: both pass all ten. They
separate on `issue complete` — whether the test reaches *every* behaviour the pull request
settles — where gpt-5.5 is 7/10 against mini's 4/10, for 8x the money.

Below mini the fall is steep and it is not gradual: 10 → 6 → 2.

## Per instance

`YES` / `NO` / `BRK` = broken. Coverage shown for passes.

| instance | tier | changed lines | gpt-5.5 | gpt-5-mini | gpt-5-nano | gpt-oss-20b |
|---|---|---|---|---|---|---|
| `astropy__astropy-13398` | 4 | 93 | **YES** 57% | **YES** 32% | NO | NO |
| `django__django-13279` | 3 | 6 | **YES** 100% | **YES** 100% | NO | NO |
| `matplotlib__matplotlib-22719` | 2 | 2 | **YES** 100% | **YES** 100% | **YES** 100% | NO |
| `psf__requests-1766` | 2 | 1 | **YES** 100% | **YES** 100% | **YES** 100% | **YES** 100% |
| `pydata__xarray-7393` | 3 | 3 | **YES** 100% | **YES** 100% | **YES** 100% | NO |
| `pylint-dev__pylint-7277` | 2 | 3 | **YES** 100% | **YES** 100% | **YES** 66% | BRK |
| `pytest-dev__pytest-7982` | 2 | 1 | **YES** 100% | **YES** 100% | **YES** 100% | **YES** 100% |
| `scikit-learn__scikit-learn-25232` | 2 | 1 | **YES** 100% | **YES** 100% | **YES** 100% | NO |
| `sphinx-doc__sphinx-9602` | 3 | 8 | **YES** 100% | **YES** 100% | NO | NO |
| `sympy__sympy-21612` | 3 | — | **YES** | **YES** | BRK | NO |

Every instance a weaker model passes, every stronger model passes too — the ordering is
clean, with no inversions. That is worth as much as the counts: it says the set grades
models rather than sampling noise.

## Where the weak models actually fail

The counts hide the interesting part. The two weak models fail in different ways, and
only one of those ways is about writing bad tests.

| failure | gpt-5-nano | gpt-oss-20b |
|---|---|---|
| never wrote a test file | 0 | 6 |
| wrote a test that does not flip | 2 | 1 |
| wrote a file that would not run | 1 | 0 |
| hit the 100-action cap | 1 | 0 |
| timed out / infrastructure | 0 | 1 |

**gpt-oss-20b mostly never produces a file at all.** Six of its eight failures are
*wrote no test* — it takes actions, explores, and stops without ever calling `write_file`,
once after a single action. It is not writing weak tests; it is not writing tests.

**gpt-5-nano does produce files, and they are usually right.** Its failures are ordinary
ones: a test that passes before the fix too, one that never ran, one cap-hit. And on the
six it passes, five are at 100% changed-line coverage — when nano succeeds, it succeeds
properly.

That difference matters for the tooling question. A tool that reports on a test can only
help a model that writes one.

## Quality of the tests that did pass

Only counting instances where the model produced a fail-to-pass test, so the weak models
are judged on their successes rather than penalised twice for their failures.

| model | n | judge `same` | issue `complete` | mutants = developer |
|---|---|---|---|---|
| `gpt-5.5` | 10 | 4 | 7 | 10/10 |
| `gpt-5-mini` | 10 | 4 | 4 | 9/10 |
| `gpt-5-nano` | 6 | 3 | 2 | 4/6 |
| `gpt-oss-20b` | 2 | 2 | 2 | 2/2 |

The shape holds: of the tests it does manage to write, gpt-oss's are not obviously worse
than nano's. The models differ in *how often they get there*, far more than in the quality
of what they produce when they do.

## Reading these numbers

**`BROKEN` is not a clean category here.** It is meant for a harness or connection
failure, and `--retry-broken` treats it as retryable. But nano's `sympy-21612` is recorded
`BROKEN` for *"nothing collected on either side — the file never ran"*, which is a fact
about the model's output, not the harness: the agent finished normally in 35 actions and
left a file with a syntax or import error. gpt-oss's `pylint-7277` is a genuine one — a
7200-second timeout. Folding the first kind into `BROKEN` would quietly flatter weak
models, so both are shown as `BRK` above and counted as failures, never as passes.

**The runs are not perfectly matched.** gpt-5.5 and gpt-5-mini were taken before two
prompt changes that gpt-5-nano and gpt-oss-20b had (`50-rules.md` write-early,
`20-goal.md` one-function-per-behaviour). The gap between 10/10 and 2/10 is far larger
than any prompt effect measured so far, but a few points either way is not attributable
to the model alone.

**Coverage means less as the pass rate drops.** gpt-oss's "100% mean" is two instances,
both one-line patches. Read the denominator, not the percentage.

## What this settles

The system is not the limiting factor at the top: two models pass all ten held-out
instances, and the remaining gap between them is behavioural breadth, not anything
mechanical. Below mini there is a great deal of headroom — which is where a tool can
show its value, since at the top there is nothing left for one to find.

The ladder to use for that: **gpt-5-nano is the right rung.** It fails often enough to
leave room for improvement (6/10) but writes real tests when it runs, so coverage and
mutation feedback have something to act on. **gpt-oss-20b is too weak to measure tooling
with** — six of its eight failures never reach the point where any tool could speak.

