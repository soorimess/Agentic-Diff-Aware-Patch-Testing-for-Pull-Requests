# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-23 23:58 UTC.

- **10** instances across **10** repositories
- **6/9** fail-to-pass, of those that reached a verdict
- **6** measured for changed-line coverage; median 100%
- \$0.50 and 6.8M tokens in total
- **7** of these were sent a second-chance message after stopping with nothing to score (collects_nothing+loop_open, loop_open, passes_at_base+loop_open); the other 3 finished or failed for a reason the agent could not have seen at base

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | YES | 32% (31/96) | — | — | 39 | `run` x16, `write_file` x8, `verify` x7, `coverage` x2, `mutation` x2 | different | partial | acceptable | 2026-09-23 23:58 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | BROKEN | — | — | — | 42 | `run` x17, `write_file` x11, `verify` x6 | — | — | — | 2026-09-23 23:54 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 0/1 | 0/1 | 30 | `run` x11, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x2 | same | partial | acceptable | 2026-09-23 23:54 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | — | — | 24 | `run` x11, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | broader | complete | acceptable | 2026-09-23 23:50 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 20 | `run` x10, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-23 23:52 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 23 | `run` x11, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x1 | broader | complete | poor | 2026-09-23 23:51 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | NO | — | — | — | 41 | `run` x19, `write_file` x10, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-23 23:56 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 100% (5/5) | 2/4 | 3/4 | 35 | `run` x15, `write_file` x5, `verify` x4, `coverage` x3, `run_tests` x3, `mutation` x2 | narrower | partial | poor | 2026-09-23 23:55 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | NO | — | — | — | 38 | `run` x11, `write_file` x10, `run_tests` x6, `verify` x3 | — | — | — | 2026-09-23 23:55 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | NO | — | — | — | 34 | `run` x18, `write_file` x5, `verify` x4, `coverage` x1 | — | — | — | 2026-09-23 23:54 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-13398** (partial)
  - Direct ITRS to AltAz transformations agree with the normal observed-coordinate route without refraction
  - Direct ITRS to AltAz transformations correctly add and remove refraction
  - AltAz to ITRS round-trips preserve the ITRS Cartesian position
- **matplotlib__matplotlib-22719** (partial)
  - Updating categorical unit data with empty data should not log the informational message about strings being parsable as floats or dates.
- **scikit-learn__scikit-learn-25232** (partial)
  - It does not test `np.nan` as a `fill_value`.
  - It does not assert that the internal `SimpleImputer` receives or uses the custom `fill_value`.

## Without a verdict

- **django__django-13279** — nothing collected on either side -- the file never ran

## What is in each directory

| file | what it holds |
|---|---|
| `result.json` | the verdict, the coverage, token usage, the audit |
| `flow.log` | every step in order: container, commands, both test runs, verdict |
| `flow.jsonl` | the same, one JSON object per step |
| `trajectory.json` | the agent's events, for the OpenHands visualizer |
| `tool_log.json` | one entry per tool call, as it reached the container |
| `test_f2p_*.py` | the test the agent wrote |
| `before_fix.log`, `after_fix.log` | the two runs the verdict is read from |
| `fix.diff` | the pull request's change, which the agent is shown |
| `developer_test.diff` | the maintainer's test, which it is **not** |
| `pr.json` | the full SWE-bench row |
| `child.log` | the child process's stdout, under `--parallel` |

`completions/` (raw prompt and response bytes per model call) is written on every run and git-ignored, being the largest thing a run produces. It is the only place the exact bytes sent to the model can be read back; the trajectory records the parsed events, which is a summary of them.

