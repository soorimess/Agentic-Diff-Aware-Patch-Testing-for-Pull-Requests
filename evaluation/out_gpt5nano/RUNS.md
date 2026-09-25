# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-22 11:27 UTC.

- **10** instances across **10** repositories
- **7/10** fail-to-pass, of those that reached a verdict
- **7** measured for changed-line coverage; median 100%
- \$0.44 and 13.9M tokens in total
- **9** of these were sent a second-chance message after stopping with nothing to score (loop_open); the other 1 finished or failed for a reason the agent could not have seen at base

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | YES | 32% (31/96) | — | — | 48 | `run` x26, `write_file` x16, `verify` x4, `coverage` x2 | different | misses_the_point | poor | 2026-09-22 11:01 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | YES | 100% (6/6) | 5/7 | 7/7 | 88 | `run` x74, `write_file` x9, `verify` x3, `coverage` x1, `mutation` x1  (+2 edits reverted) | narrower | partial | poor | 2026-09-22 11:27 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 0/1 | 0/1 | 21 | `run` x14, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1  (+2 edits reverted) | error | — | — | 2026-09-21 14:07 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | — | — | 36 | `run` x25, `write_file` x6, `verify` x3, `coverage` x1, `mutation` x1 | error | — | — | 2026-09-21 14:07 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 21 | `run` x16, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1  (+1 edit reverted) | narrower | partial | acceptable | 2026-09-21 14:04 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 22 | `run` x11, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x1  (+2 edits reverted) | narrower | partial | acceptable | 2026-09-22 10:58 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | NO | — | — | — | 58 | `run` x53, `write_file` x3, `verify` x2 | different | misses_the_point | poor | 2026-09-22 10:59 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 100% (5/5) | 4/4 | 3/4 | 8 | `write_file` x3, `mutation` x2, `verify` x2, `coverage` x1 | broader | partial | poor | 2026-09-21 14:04 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | NO | — | — | — | 100 | `run` x98, `write_file` x1  (+1 edit reverted) | different | misses_the_point | poor | 2026-09-22 10:59 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | NO | — | — | — | 25 | `run` x20, `write_file` x3, `coverage` x1, `verify` x1 | error | — | — | 2026-09-21 14:18 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-13398** (misses_the_point)
  - Topocentric ITRS to AltAz should use the observer location and match the normal observed-coordinate route without refraction
  - Topocentric ITRS to AltAz should handle adding and removing atmospheric refraction consistently
  - AltAz transformed through topocentric ITRS should round-trip back to the same ITRS Cartesian coordinates
- **django__django-13279** (partial)
  - The sha1 legacy-format output is valid and can be decoded by the legacy decoder/older Django to recover the original session data.
  - When DEFAULT_HASHING_ALGORITHM is not 'sha1', encode() continues to use the normal signing.dumps() format.
- **pydata__xarray-7393** (partial)
  - A selected MultiIndex level created by stack preserves a narrow floating coordinate dtype such as float32 when converted to array values
  - The MultiIndex-level array conversion path now applies the dtype passed to __array__ instead of ignoring it
- **pylint-dev__pylint-7277** (partial)
  - A dot at sys.path[0] is treated as a current-directory entry and removed.
  - os.getcwd() at sys.path[0] is treated as a current-directory entry and removed.
- **pytest-dev__pytest-7982** (misses_the_point)
  - When recursive discovery scans a directory, symlinked directory entries are treated as directories and descended into.
  - As a result, normal pytest collection from a test root collects tests inside symlinked subdirectories.
- **scikit-learn__scikit-learn-25232** (partial)
  - The custom fill_value is actually used as the initial constant imputation statistic/value.
  - The default fill_value=None preserves SimpleImputer's default constant-fill behaviour.
- **sphinx-doc__sphinx-9602** (misses_the_point)
  - Literal values inside unqualified Literal[...] are rendered as literal text rather than py:class cross-references.
  - Literal values inside qualified typing.Literal[...] are rendered as literal text rather than py:class cross-references.
  - Constant values are represented with repr(), so booleans, integers, and strings display correctly, including quotes for string literals.

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

