# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-11 11:37 UTC.

- **24** instances across **12** repositories
- **24/24** fail-to-pass, of those that reached a verdict
- **24** measured for changed-line coverage; median 100%
- $1.57 and 18.2M tokens in total

Every row was produced with the same configuration: **`no-repo-facts`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES | 100% (1/1) | 4/5 | 4/5 | 28 | same | complete | acceptable | 2026-09-11 11:07 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 40 | narrower | partial | acceptable | 2026-09-11 11:11 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | 100% (1/1) | 3/3 | 3/3 | 42 | narrower | partial | acceptable | 2026-09-11 11:15 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | YES | 100% (2/2) | 6/6 | 6/6 | 24 | same | complete | acceptable | 2026-09-11 11:12 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | YES | 100% (1/1) | no mutants | no mutants | 56 | narrower | complete | poor | 2026-09-11 11:21 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 50% (1/2) | 3/10 | 5/10 | 32 | narrower | partial | acceptable | 2026-09-11 11:12 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 3/3 | 3/3 | 16 | narrower | partial | acceptable | 2026-09-11 11:07 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 1/4 | 1/4 | 10 | same | complete | good | 2026-09-11 11:09 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 69 | same | complete | acceptable | 2026-09-11 11:17 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | YES | 100% (2/2) | 3/4 | 2/4 | 19 | narrower | partial | acceptable | 2026-09-11 11:11 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (3/3) | no mutants | no mutants | 13 | same | complete | poor | 2026-09-11 11:07 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 8/9 | 8/9 | 42 | narrower | partial | poor | 2026-09-11 11:17 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 100% (3/3) | 10/10 | 10/10 | 49 | narrower | complete | acceptable | 2026-09-11 11:20 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | YES | 80% (4/5) | 8/10 | 9/10 | 97 | narrower | partial | poor | 2026-09-11 11:37 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | 1/1 | 1/1 | 12 | same | complete | acceptable | 2026-09-11 11:15 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 5/6 | 6/6 | 15 | narrower | partial | acceptable | 2026-09-11 11:17 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | no mutants | no mutants | 13 | broader | complete | acceptable | 2026-09-11 11:16 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | 1/1 | 1/1 | 28 | narrower | partial | acceptable | 2026-09-11 11:20 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 2/5 | 2/5 | 25 | broader | complete | poor | 2026-09-11 11:20 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | no mutants | no mutants | 18 | narrower | partial | acceptable | 2026-09-11 11:19 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | YES | 100% (11/11) | 9/10 | 9/10 | 46 | narrower | partial | poor | 2026-09-11 11:26 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | YES | 100% (6/6) | 3/4 | 3/4 | 48 | same | complete | acceptable | 2026-09-11 11:30 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | no mutants | no mutants | 17 | same | complete | good | 2026-09-11 11:21 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 4/7 | 4/7 | 16 | narrower | partial | acceptable | 2026-09-11 11:24 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **django__django-13406** (partial)
  - A pickled values_list() query assigned to a normal queryset reloads as values-style dictionaries.
  - Pickled values_list(flat=True) and values_list(named=True) queries assigned to a normal queryset reload as values-style dictionaries.
- **django__django-15098** (partial)
  - Exact resolution of /en-latn-us/ and /en-Latn-US/ to those same language codes.
  - Other three-subtag forms affected by the same regexp change, such as de-ch-1901 and nan-hani-tw.
  - Unsupported prefixes and overlong hyphenated paths returning None.
- **psf__requests-1142** (partial)
  - A prepared HEAD request with no body omits Content-Length instead of sending Content-Length: 0.
  - A prepared request using methods other than GET or HEAD with no body still receives Content-Length: 0.
- **psf__requests-6028** (partial)
  - prepend_scheme_if_needed must preserve username-only auth in the URL netloc
- **pylint-dev__pylint-6903** (partial)
  - `_query_cpu()` also coerces any other computed `avail_cpu == 0`, including a fractional quota/period calculation, to 1.
  - `--jobs=0` no longer causes pylint to pass 0 processes to multiprocessing and crash.
- **pytest-dev__pytest-10081** (partial)
  - It does not cover method-level skipped unittest.TestCase tests.
  - It does not cover @pytest.mark.skip on the class.
  - It does not explicitly prove that setUp was not called or that the run had no other error.
- **sphinx-doc__sphinx-10614** (partial)
  - SVG inheritance diagrams with normal internal refuri links should use the builder-provided URI without adding '../'.
  - PNG image-map inheritance diagrams should still produce valid local hrefs and unprefixed absolute intersphinx hrefs after the shared refuri-key change.
  - The generated SVG hrefs from actual root and subdirectory pages resolve to existing output files.
- **pydata__xarray-7233** (partial)
  - Dataset Coarsen.construct preserves a non-dimensional coordinate that depends on the coarsened dimension after it is reshaped.
  - DataArray Coarsen.construct preserves its original coordinates as coordinates after constructing the coarsened dimension.
- **astropy__astropy-14995** (partial)
  - No-mask operands with handle_mask=np.bitwise_or still produce no result mask.
  - A masked NDDataRef multiplied by an unmasked NDDataRef with handle_mask=np.bitwise_or copies the existing mask instead of calling bitwise_or with None.
  - Two masked operands still combine integer bitmasks using the supplied handle_mask function.
- **sympy__sympy-24562** (partial)
  - A non-integer numerator with a fractional non-integer denominator, including string and float forms, computes the mathematical quotient rather than corrupting or repeating the raw denominator.
  - An integer numerator with a fractional non-integer denominator still computes the mathematical quotient.
- **mwaskom__seaborn-3069** (partial)
  - Gridlines are disabled on nominal axes for both x and y.
  - User-specified limits on nominal x and y axes are honored.
  - The tweaks apply to inferred Nominal scales.
- **scikit-learn__scikit-learn-10908** (partial)
  - It does not verify the complete vocabulary_ mapping.
  - It does not verify fixed_vocabulary_ is set to true.
  - It does not cover a supplied mapping vocabulary.

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

`completions/` (raw prompt and response bytes per model call) is not committed: 43 MB across these instances. Set `LLM_LOG_COMPLETIONS=1` and rerun to regenerate it locally.

