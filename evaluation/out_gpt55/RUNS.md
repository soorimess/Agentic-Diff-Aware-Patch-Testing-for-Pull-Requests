# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-16 12:50 UTC.

- **10** instances across **10** repositories
- **10/10** fail-to-pass, of those that reached a verdict
- **9** measured for changed-line coverage; median 100%
- \$7.42 and 5.8M tokens in total

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | YES | 57% (53/93) | — | — | 70 | narrower | partial | acceptable | 2026-09-16 12:50 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | YES | 100% (6/6) | 7/7 | 7/7 | 25 | narrower | complete | acceptable | 2026-09-16 12:18 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 1/1 | 0/1 | 21 | broader | complete | acceptable | 2026-09-16 12:16 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | — | — | 11 | same | complete | acceptable | 2026-09-15 12:45 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 16 | narrower | partial | good | 2026-09-16 12:18 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 19 | broader | complete | good | 2026-09-16 12:17 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | YES | 100% (1/1) | 1/1 | 1/1 | 19 | same | complete | acceptable | 2026-09-16 12:15 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 100% (1/1) | 2/3 | 2/3 | 21 | same | partial | good | 2026-09-16 12:17 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | YES | 100% (8/8) | 10/10 | 10/10 | 16 | same | complete | acceptable | 2026-09-16 12:17 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | YES | — | no mutants | no mutants | 12 | broader | complete | acceptable | 2026-09-16 12:17 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-13398** (partial)
  - Refraction add/remove behaviour for AltAz.
  - Refraction add/remove behaviour for HADec.
  - Round-trip/general-vector coverage beyond the special straight-up inverse and two basis-like directions.
- **pydata__xarray-7393** (partial)
  - This dtype restoration applies to floating-point coordinates such as float32.
- **scikit-learn__scikit-learn-25232** (partial)
  - fill_value is not validated away and can be np.nan or another object accepted by SimpleImputer.

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

