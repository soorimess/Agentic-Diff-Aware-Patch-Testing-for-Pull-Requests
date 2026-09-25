# Run status, per pull request

Last run in this table: 2026-09-24 11:32 UTC.

- **70** instances across **12** repositories
- **41/61** fail-to-pass, of those that reached a verdict
- **41** measured for changed-line coverage: **mean 81%** per test, median 100%
- **63%** of the changed lines those tests were measured against (144/227, pooled)
- **28%** of every source line all 70 patches change (144/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.58 and 49.0M tokens in total
- **41** of these were sent a second-chance message after stopping with nothing to score, and **13** of them ended fail-to-pass; the other 29 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 7 | 3 | 0 | 4 | **added by the flag** |
| `loop_open` | 18 | 9 | 5 | 4 | from `require-tools` |
| `passes_at_base+loop_open` | 16 | 1 | 15 | 0 | **added by the flag** |

Of the **23** refused for a reason the flag itself adds, **4** ended fail-to-pass.

Every row was produced with the same configuration: **`no-guard`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 24 | `run` x10, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | same | partial | poor | 2026-09-24 11:12 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 3/3 | 3/3 | 22 | `run` x14, `write_file` x3, `coverage` x1, `mutation` x1, `verify` x1 | different | partial | poor | 2026-09-24 11:08 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 15 | `run` x7, `coverage` x2, `verify` x2, `mutation` x1, `write_file` x1 | same | partial | acceptable | 2026-09-24 11:05 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 3/4 | 4/4 | 45 | `run` x22, `write_file` x7, `coverage` x4, `verify` x3, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:18 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 43 | `run` x24, `write_file` x7, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 11:11 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | BROKEN | — | — | — | 45 | `run` x34, `write_file` x6, `verify` x1 | — | — | — | 2026-09-24 11:10 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 42 | `run` x19, `write_file` x13, `verify` x2 | — | — | — | 2026-09-24 11:13 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | BROKEN | — | — | — | 59 | `run` x32, `write_file` x14, `run_tests` x3, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 11:15 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 31 | `run` x17, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:07 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 34 | `run` x20, `write_file` x5, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 11:06 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x15, `write_file` x4, `verify` x3, `coverage` x1, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 11:04 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 49 | `run` x21, `write_file` x9, `verify` x5, `run_tests` x4, `coverage` x3, `mutation` x1 | different | misses_the_point | poor | 2026-09-24 11:17 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 32 | `run` x11, `write_file` x9, `verify` x3, `coverage` x1, `mutation` x1, `run_tests` x1 | — | — | — | 2026-09-24 11:13 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | NO | — | — | — | 46 | `run` x24, `write_file` x10, `coverage` x2, `mutation` x2, `verify` x2 | — | — | — | 2026-09-24 11:15 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | BROKEN | — | — | — | 35 | `run` x22, `write_file` x7, `run_tests` x1 | — | — | — | 2026-09-24 11:10 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 23 | `run` x13, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:09 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | YES | 25% (1/4) | 0/2 | 2/2 | 33 | `run` x19, `write_file` x8 | narrower | partial | poor | 2026-09-24 11:09 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 29 | `run` x14, `write_file` x3, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2 | narrower | complete | poor | 2026-09-24 11:09 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 50% (1/2) | no mutants | no mutants | 47 | `run` x26, `write_file` x7, `coverage` x4, `verify` x4, `mutation` x1 | different | partial | poor | 2026-09-24 11:10 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 43% (3/7) | 0/6 | 2/6 | 44 | `run` x21, `write_file` x8, `verify` x5, `run_tests` x3, `coverage` x1, `mutation` x1 | different | partial | poor | 2026-09-24 11:13 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | BROKEN | — | — | — | 35 | `run` x19, `write_file` x5, `verify` x4, `run_tests` x2, `mutation` x1 | — | — | — | 2026-09-24 11:07 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 18 | `run` x12, `verify` x2, `write_file` x2 | narrower | partial | poor | 2026-09-24 11:06 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 32 | `run` x18, `write_file` x5, `coverage` x2, `mutation` x2, `verify` x2 | broader | partial | acceptable | 2026-09-24 11:08 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 41 | `run` x14, `write_file` x9, `verify` x7, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-24 11:11 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 30 | `run` x12, `write_file` x4, `run_tests` x3, `coverage` x2, `verify` x2, `mutation` x1 | same | complete | acceptable | 2026-09-24 11:08 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | YES | 0% (0/6) | 0/1 | 1/1 | 45 | `run` x26, `write_file` x9, `verify` x4, `coverage` x1, `mutation` x1 | different | misses_the_point | poor | 2026-09-24 11:11 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 28 | `run` x17, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 11:05 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 61 | `run` x38, `write_file` x13, `coverage` x3, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 11:14 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 44% (8/18) | 1/10 | 1/10 | 46 | `run` x17, `write_file` x13, `verify` x9, `coverage` x3 | narrower | partial | acceptable | 2026-09-24 11:14 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 24 | `run` x16, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 11:05 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | BROKEN | — | — | — | 35 | `run` x17, `write_file` x8, `run_tests` x3, `verify` x2 | — | — | — | 2026-09-24 11:14 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 28 | `run` x18, `coverage` x2, `mutation` x2, `write_file` x2, `verify` x1 | narrower | partial | poor | 2026-09-24 11:15 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 32 | `run` x16, `coverage` x3, `verify` x3, `mutation` x2, `write_file` x2, `run_tests` x1 | broader | partial | poor | 2026-09-24 11:17 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | NO | — | — | — | 42 | `run` x18, `write_file` x9, `verify` x6, `coverage` x2, `mutation` x1, `run_tests` x1 | — | — | — | 2026-09-24 11:19 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 24 | `run` x9, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | narrower | partial | poor | 2026-09-24 11:18 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 44 | `run` x20, `write_file` x9, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 11:22 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 53 | `run` x27, `write_file` x8, `run_tests` x6, `verify` x5 | — | — | — | 2026-09-24 11:22 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 17 | `run` x5, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | broader | complete | acceptable | 2026-09-24 11:12 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/1 | 0/1 | 40 | `run` x13, `verify` x6, `coverage` x5, `write_file` x5, `mutation` x3, `run_tests` x1 | narrower | partial | poor | 2026-09-24 11:19 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 32 | `run` x12, `write_file` x6, `verify` x4, `coverage` x3, `run_tests` x2, `mutation` x1 | same | partial | acceptable | 2026-09-24 11:20 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 23 | `run` x9, `write_file` x5, `coverage` x3, `verify` x3, `mutation` x1 | broader | complete | acceptable | 2026-09-24 11:21 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 19 | `run` x8, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | broader | complete | acceptable | 2026-09-24 11:16 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 40 | `run` x17, `write_file` x8, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 11:21 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 13 | `run` x6, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | narrower | partial | acceptable | 2026-09-24 11:19 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | BROKEN | — | — | — | 49 | `run` x24, `write_file` x8, `run_tests` x6, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 11:23 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | BROKEN | 100% (3/3) | — | — | 23 | `run` x11, `run_tests` x3, `write_file` x3, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 11:17 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 35 | `run` x25, `write_file` x4 | narrower | partial | poor | 2026-09-24 11:19 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 40 | `run` x19, `write_file` x10, `verify` x3 | — | — | — | 2026-09-24 11:20 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 75 | `run` x52, `write_file` x8, `run_tests` x6, `verify` x1 | — | — | — | 2026-09-24 11:23 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 25 | `run` x7, `write_file` x6, `run_tests` x4 | — | — | — | 2026-09-24 11:22 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 45 | `run` x25, `write_file` x7, `verify` x4, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-24 11:24 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 19 | `run` x9, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 11:21 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 50% (5/10) | 3/10 | 6/10 | 34 | `run` x17, `write_file` x6, `coverage` x3, `verify` x3, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:22 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 64% (30/47) | 1/10 | 4/10 | 37 | `run` x16, `write_file` x5, `verify` x4, `coverage` x3, `run_tests` x3, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:26 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | BROKEN | — | — | — | 39 | `run` x27, `write_file` x5, `verify` x2 | — | — | — | 2026-09-24 11:21 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 41 | `run` x20, `write_file` x8, `verify` x4 | — | — | — | 2026-09-24 11:25 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 29 | `run` x12, `write_file` x7, `verify` x4 | — | — | — | 2026-09-24 11:22 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 46 | `run` x20, `write_file` x10, `run_tests` x5, `verify` x4 | — | — | — | 2026-09-24 11:25 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 34 | `run` x11, `write_file` x9, `verify` x7 | — | — | — | 2026-09-24 11:27 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 38% (14/37) | 1/10 | 5/10 | 36 | `run` x18, `write_file` x5, `verify` x4, `coverage` x3, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 11:26 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 34 | `run` x16, `write_file` x4, `run_tests` x3, `coverage` x2, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 11:23 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | NO | — | — | — | 46 | `run` x13, `write_file` x12, `run_tests` x5, `verify` x5, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-24 11:28 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 24 | `run` x10, `coverage` x3, `verify` x3, `write_file` x3, `mutation` x2, `run_tests` x1 | narrower | complete | poor | 2026-09-24 11:27 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 3/3 | 3/3 | 27 | `run` x16, `verify` x3, `write_file` x3, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:32 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 23 | `run` x14, `write_file` x3, `coverage` x1, `mutation` x1, `run_tests` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 11:23 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 37 | `run` x18, `write_file` x5, `run_tests` x3, `verify` x3, `coverage` x2 | — | — | — | 2026-09-24 11:27 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 23 | `run` x11, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 11:29 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 31 | `run` x12, `write_file` x4, `coverage` x3, `run_tests` x3, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 11:30 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 29 | `run` x16, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2, `run_tests` x1 | narrower | partial | poor | 2026-09-24 11:27 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 26 | `run` x17, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 11:28 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (partial)
  - It does not assert exact equivalence to the intended Unit for either reported column.
  - It does not cover the direct parser cases for unscaled chained division, explicit parenthesized denominator grouping, leading reciprocal division, or invalid mixed product/division forms.
- **astropy__astropy-14539** (partial)
  - Comparing tables with genuinely different Q-format VLA cells should report the differing rows and values correctly in the diff totals and report.
- **astropy__astropy-14598** (partial)
  - Long string Card values with doubled single quotes followed by a space and more text round-trip exactly rather than being parsed as a prefix.
- **astropy__astropy-7606** (partial)
  - UnrecognizedUnit inequality and containment/reflected comparisons involving None do not raise.
  - Comparisons between a regular Unit and an UnrecognizedUnit fall back correctly instead of being decided prematurely.
  - UnitBase.__eq__ returns NotImplemented rather than False when coercing the other operand to a Unit raises ValueError, UnitsError, or TypeError.
- **django__django-12965** (partial)
  - The public Model.objects.all().delete() path executes using that SQL.
  - The generated SQL contains no SELECT subquery at all, not merely no IN (SELECT pattern.
- **django__django-13012** (partial)
  - ExpressionWrapper delegation for non-empty group-by columns.
  - A wrapped expression with non-empty group-by columns still returns those columns.
- **django__django-13023** (partial)
  - the standard error message including the rejected value
  - the nonnumeric bytes InvalidOperation case
- **django__django-13449** (misses_the_point)
  - On SQLite, a Window expression whose output field is a DecimalField, such as Lag over a DecimalField, must compile with the numeric cast outside the OVER clause and execute without a syntax error.
  - The DecimalField Lag window query must return the correct lagged values according to the specified partitioning and ordering.
  - On SQLite, non-DecimalField Window expressions must continue to use the normal Window SQL path.
- **django__django-14534** (partial)
  - CheckboxSelectMultiple subwidgets honor a non-default form auto_id format, including the indexed suffix for each choice.
  - When a subwidget has no id in attrs, id_for_label returns None instead of inventing an id.
  - The second choice/subwidget returns its own indexed id.
- **django__django-14559** (partial)
  - bulk_update() returns the total number of rows matched by non-empty update() calls
  - the returned count is accumulated across batches
  - duplicate objects in the same batch are counted according to the single UPDATE's matched rows
- **django__django-14608** (partial)
  - When full_clean() catches a formset-level ValidationError, non_form_errors() is rebuilt with error_class='nonform' so rendered non-form errors include the nonform CSS class.
- **django__django-14725** (partial)
  - BaseModelFormSet.save() with edit_only=True skips save_new_objects(), so posted extra forms do not create model instances.
  - BaseModelFormSet.save() with edit_only=True still saves changes to existing initial forms.
  - The default/edit_only=False save path continues to save both existing and new objects.
- **django__django-14792** (partial)
  - _get_timezone_name() returns the fixed offset from tzname(None) for zoneinfo Etc/GMT zones such as Etc/GMT-10.
  - _get_timezone_name() preserves ordinary named pytz/zoneinfo time zones by falling back to str(timezone) when tzname(None) is not set.
  - _get_timezone_name() preserves the existing datetime.timezone behaviour for unnamed and explicitly named fixed offsets.
- **django__django-14915** (partial)
  - The reported dict-membership case where a ModelChoiceIteratorValue is looked up in a dict keyed by the raw underlying value.
- **django__django-16136** (misses_the_point)
  - For async views, http_method_not_allowed returns an awaitable instead of a bare HttpResponseNotAllowed.
  - Awaiting that async result yields an HttpResponseNotAllowed response.
  - For sync views, http_method_not_allowed continues to return a direct HttpResponseNotAllowed response.
- **django__django-16139** (partial)
  - That href resolves correctly when the UserAdmin change page URL uses a non-pk to_field value, so the password-change link targets the pk-based admin password-change URL rather than 404ing.
- **django__django-16560** (partial)
  - Concrete constraints pass violation_error_code through their constructors.
  - Constraint equality includes violation_error_code so constraints with different codes differ.
  - Constraint repr includes a non-None violation_error_code.
- **matplotlib__matplotlib-20676** (partial)
  - the initialized edge-handle positions correspond to the relevant current axis bounds
  - after an interactive selection move, bounds remain unchanged and edge handles reflect the selected span
- **matplotlib__matplotlib-20859** (partial)
  - The returned SubFigure legend is associated with the SubFigure via set_figure(parent).
  - An invalid Legend parent raises a TypeError whose message now refers to FigureBase.
- **matplotlib__matplotlib-24970** (partial)
  - The colormap result for index 0 remains correct for unsigned integer and normal integer scalar inputs after the unconditional astype(int).
  - The float-input branch still scales, clips, and casts float16/Python float inputs correctly after moving the astype(int) outside the float-only branch.
- **psf__requests-2931** (partial)
  - The public request preparation/body path is not exercised.
  - `prepare_url` raw string/bytes `params` handling is not actually exercised or asserted.
- **pydata__xarray-2905** (partial)
  - Pandas `Series`, `Index`, and `DataFrame` inputs should still be unwrapped to their `.values` arrays to avoid nested self-described arrays.
- **pydata__xarray-6744** (partial)
  - The iterator logic works across different window sizes beyond size 3, especially size 1 and even size 2
- **pytest-dev__pytest-6197** (partial)
  - Package discovery during collection does not mutate `sys.path` by adding unrelated package parents such as `src`.
- **sphinx-doc__sphinx-7462** (partial)
  - The Python-domain annotation parser's exact output for Tuple[()] includes the expected empty-tuple punctuation nodes.
- **sphinx-doc__sphinx-7590** (partial)
  - hexadecimal floating UDLs
  - UDL suffixes that can be confused with builtin numeric suffixes, such as uludl and fudl
  - the full set of decimal floating and integer literal spellings
- **sympy__sympy-12489** (partial)
  - No-argument or size-only subclass construction.
  - Integer subclass construction.
  - Multiple positional cycle argument construction.
- **sympy__sympy-16450** (partial)
  - The generated test does not check infinite=False or the full assumptions0 dictionary.
  - The expression test does not inspect the substituted Dummy's assumptions, so it does not verify assumption preservation inside expressions.
  - The generated test does not check preservation of any other assumptions from assumptions0.
- **sympy__sympy-19637** (partial)
  - kernS on the reported expression must still return the correct SymPy expression
- **sympy__sympy-20590** (partial)
  - It does not check that assigning a new arbitrary attribute raises `AttributeError`.
- **sympy__sympy-21596** (partial)
  - Candidate roots must still be filtered by the original base set such as Integers or Naturals0.
  - Nonlinear or otherwise unsolved imaginary-part equations should be represented with a ConditionSet.
  - Zeros of denominators in the full image expression must be excluded from the parameter set.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-11179** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: dj...
- **django__django-12308** — nothing collected on either side -- the file never ran
- **django__django-13794** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: dj...
- **django__django-14765** — nothing collected on either side -- the file never ran
- **django__django-16667** — nothing collected on either side -- the file never ran
- **pylint-dev__pylint-4970** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: py...
- **pylint-dev__pylint-7277** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: py...
- **sphinx-doc__sphinx-7757** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: sp...
