# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-10 13:48 UTC.

- **26** instances across **12** repositories
- **23/24** fail-to-pass, of those that reached a verdict
- **23** measured for changed-line coverage; median 100%
- \$1.36 and 16.0M tokens in total

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES ¹ | 100% (1/1) | 4/5 | 4/5 | 30 | same | complete | good | 2026-09-10 12:16 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 38 | narrower | partial | acceptable | 2026-09-10 12:15 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | 100% (1/1) | 3/3 | 3/3 | 27 | narrower | partial | acceptable | 2026-09-10 12:16 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | YES | 100% (2/2) | 6/6 | 6/6 | 34 | same | complete | acceptable | 2026-09-10 12:17 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | YES | 100% (1/1) | no mutants | no mutants | 36 | narrower | complete | acceptable | 2026-09-10 12:17 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 100% (2/2) | 8/10 | 5/10 | 12 | broader | complete | good | 2026-09-10 12:18 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 3/3 | 3/3 | 23 | narrower | partial | acceptable | 2026-09-10 12:18 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 1/4 | 1/4 | 9 | same | complete | good | 2026-09-10 12:19 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 47 | same | complete | acceptable | 2026-09-10 12:19 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | YES | 100% (2/2) | 4/4 | 2/4 | 20 | narrower | partial | acceptable | 2026-09-10 12:20 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (3/3) | no mutants | no mutants | 14 | same | complete | acceptable | 2026-09-10 12:20 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 8/9 | 8/9 | 28 | narrower | partial | acceptable | 2026-09-10 12:20 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | NO | — | — | — | 100 | same | complete | poor | 2026-09-06 13:16 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | YES | 100% (5/5) | 10/10 | 9/10 | 72 | narrower | partial | poor | 2026-09-10 12:21 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | 1/1 | 1/1 | 7 | broader | complete | acceptable | 2026-09-10 12:58 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 6/6 | 6/6 | 10 | narrower | partial | good | 2026-09-10 13:33 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | no mutants | no mutants | 6 | same | complete | acceptable | 2026-09-10 12:22 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | 1/1 | 1/1 | 17 | narrower | partial | acceptable | 2026-09-10 12:24 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 2/5 | 2/5 | 12 | broader | complete | acceptable | 2026-09-10 12:25 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | no mutants | no mutants | 15 | narrower | partial | acceptable | 2026-09-10 12:26 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | YES | 100% (11/11) | 9/10 | 9/10 | 46 | narrower | partial | good | 2026-09-10 13:48 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | YES | 33% (2/6) | 2/4 | 3/4 | 28 | narrower | partial | acceptable | 2026-09-10 13:00 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | no mutants | no mutants | 18 | same | complete | good | 2026-09-10 13:01 UTC |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | BROKEN | — | — | — | — | — | — | — | 2026-09-07 11:50 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 4/7 | 4/7 | 22 | same | partial | acceptable | 2026-09-10 13:03 UTC |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | BROKEN | — | — | — | — | — | — | — | 2026-09-07 11:58 UTC |

¹ re-judged by `--recheck`: the same saved test run again under a later harness, with no new model call. The trajectory and token counts belong to the original run; the verdict and coverage are from the re-judgement.

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **django__django-13406** (partial)
  - A queryset assigned a pickled values_list() query uses ValuesIterable and returns values-style dict rows.
  - The same values_list() reload behaviour applies to plain, flat=True, and named=True values_list() queries.
- **django__django-15098** (partial)
  - The broadened prefix regex also supports other valid two-subtag configured language codes, such as language-region-variant and language-script-region examples beyond en-latn-us.
  - The URL-language-prefix parser still rejects longer non-language path prefixes instead of partially treating them as language codes.
- **psf__requests-6028** (partial)
  - prepend_scheme_if_needed preserves username-only userinfo in the netloc instead of dropping it during URL reconstruction
- **pylint-dev__pylint-6903** (partial)
  - The quota/period calculation path is also protected by the same `avail_cpu == 0` clamp.
  - Using `--jobs=0` with a fractional detected CPU count does not pass 0 processes to multiprocessing and crash.
- **pytest-dev__pytest-10081** (partial)
  - Under --pdb, a unittest.TestCase class skipped with @pytest.mark.skip must not have setUp or tearDown called and should be reported as skipped.
- **sphinx-doc__sphinx-10614** (partial)
  - SVG inheritance-diagram internal `refuri` links are emitted without the extra `../` prefix so cross-document class links from nested pages resolve correctly.
  - External/intersphinx URLs remain absolute and are not prefixed with `../` in diagram links.
  - PNG inheritance-diagram clickmap links continue to resolve, including external intersphinx links affected by the refname change.
- **pydata__xarray-7233** (partial)
  - DataArray.coarsen.construct keeps its original coordinates as coordinates afterwards.
- **astropy__astropy-14995** (partial)
  - When a masked NDDataRef is multiplied by a scalar/no-mask operand with handle_mask=np.bitwise_or, the existing mask is copied instead of applying bitwise_or to None.
  - When neither operand has a mask, the result mask remains None.
  - When both operands have masks, handle_mask=np.bitwise_or is still applied to combine the masks.
- **sympy__sympy-24562** (partial)
  - A non-integer denominator such as a decimal string or float must be converted independently so its numerator and denominator are combined correctly with the numerator.
  - The corrected two-argument Rational normalization must work across the affected string, float, and integer numerator/denominator combinations.
- **mwaskom__seaborn-3069** (partial)
  - Explicit user limits on a nominal x axis are preserved.
  - Explicit user limits on a nominal y axis are preserved.
- **mwaskom__seaborn-3187** (partial)
  - seaborn.objects continuous scale legends disable ScalarFormatter offset/scientific notation so large numeric legend labels show full values
- **scikit-learn__scikit-learn-10908** (partial)
  - It does not assert fixed_vocabulary_ is set to true.
  - It does not explicitly assert the exact token-to-index contents of vocabulary_.

## Without a verdict

- **matplotlib__matplotlib-26208** — child exited 1 without writing a result: failed to connect to the docker API at unix://~/.docker/run/docker.sock; check if the path is correct and if the daemon is running: dial unix ~/.docker/run/docker.sock: connect: no such file or directory
- **scikit-learn__scikit-learn-25747** — not run: the instance image was never pulled. The download was still in progress at ~0.3 MB/s (3.68 GB to go) and the run was stopped by hand. No agent was started, so this says nothing about the instance.

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

