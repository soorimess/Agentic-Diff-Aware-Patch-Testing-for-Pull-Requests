# Run status, per pull request

Last run in this table: 2026-09-24 13:08 UTC.

- **70** instances across **12** repositories
- **42/66** fail-to-pass, of those that reached a verdict
- **42** measured for changed-line coverage: **mean 88%** per test, median 100%
- **70%** of the changed lines those tests were measured against (150/214, pooled)
- **30%** of every source line all 70 patches change (150/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.46 and 47.5M tokens in total
- **37** of these were sent a second-chance message after stopping with nothing to score, and **10** of them ended fail-to-pass; the other 33 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 1 | 1 | 0 | 0 | **added by the flag** |
| `collects_nothing+loop_open` | 4 | 0 | 1 | 3 | **added by the flag** |
| `loop_open` | 15 | 9 | 5 | 1 | from `require-tools` |
| `passes_at_base+loop_open` | 17 | 0 | 17 | 0 | **added by the flag** |

Of the **22** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 31 | `run` x9, `write_file` x9, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:39 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 1/3 | 3/3 | 33 | `run` x17, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 12:40 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 29 | `run` x13, `write_file` x5, `verify` x3, `coverage` x2, `run_tests` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 12:34 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 2/4 | 4/4 | 38 | `run` x22, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x2 | same | partial | poor | 2026-09-24 12:39 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 41 | `run` x20, `write_file` x6, `verify` x5, `coverage` x3, `mutation` x3, `run_tests` x1 | same | complete | acceptable | 2026-09-24 12:35 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 45 | `run` x15, `write_file` x11, `run_tests` x6, `verify` x4 | — | — | — | 2026-09-24 12:39 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | YES | 0% (0/1) | 1/1 | 1/1 | 51 | `run` x30, `write_file` x11, `verify` x3, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:43 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | BROKEN | — | — | — | 41 | `run` x24, `write_file` x8, `verify` x3, `coverage` x1, `run_tests` x1 | — | — | — | 2026-09-24 12:40 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 43 | `run` x22, `write_file` x11, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:40 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 30 | `run` x15, `write_file` x6, `verify` x4, `coverage` x2, `mutation` x1 | narrower | partial | good | 2026-09-24 12:36 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x13, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 12:33 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 45 | `run` x19, `write_file` x8, `verify` x5, `run_tests` x4, `coverage` x3, `mutation` x2 | different | misses_the_point | poor | 2026-09-24 12:41 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 51 | `run` x26, `write_file` x12, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 12:44 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | NO | — | — | — | 46 | `run` x20, `write_file` x13, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:39 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | BROKEN | — | — | — | 49 | `run` x32, `write_file` x7, `coverage` x2, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 12:40 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 43 | `run` x18, `run_tests` x7, `write_file` x6, `coverage` x3, `mutation` x2, `verify` x2  (+1 edit reverted) | narrower | partial | acceptable | 2026-09-24 12:41 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 29 | `run` x15, `write_file` x3, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-24 12:33 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 29 | `run` x15, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | unparsed | — | — | 2026-09-24 12:37 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 37 | `run` x21, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 12:35 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 42 | `run` x22, `write_file` x7, `verify` x4, `run_tests` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:40 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | BROKEN | — | — | — | 41 | `run` x23, `write_file` x8, `verify` x3, `coverage` x2  (+1 edit reverted) | — | — | — | 2026-09-24 12:36 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 32 | `run` x16, `verify` x5, `write_file` x5, `coverage` x2, `mutation` x1 | narrower | partial | good | 2026-09-24 12:39 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 32 | `run` x16, `write_file` x5, `coverage` x3, `mutation` x3, `verify` x3 | narrower | partial | poor | 2026-09-24 12:39 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 38 | `run` x19, `write_file` x8, `run_tests` x3, `verify` x3 | — | — | — | 2026-09-24 12:39 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | BROKEN | — | — | — | 39 | `run` x24, `write_file` x6, `verify` x4 | — | — | — | 2026-09-24 12:34 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 53 | `run` x21, `write_file` x13, `verify` x7, `coverage` x4, `mutation` x2 | — | — | — | 2026-09-24 12:45 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 26 | `run` x12, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 12:37 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 7/9 | 7/9 | 37 | `run` x19, `write_file` x8, `run_tests` x4, `coverage` x1, `mutation` x1, `verify` x1 | narrower | partial | poor | 2026-09-24 12:38 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 48 | `run` x16, `write_file` x11, `verify` x8, `coverage` x3, `mutation` x2 | — | — | — | 2026-09-24 12:42 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 25 | `run` x18, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | same | complete | acceptable | 2026-09-24 12:34 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 34 | `run` x20, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | broader | complete | poor | 2026-09-24 12:42 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 28 | `run` x15, `write_file` x5, `coverage` x2, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:43 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 27 | `run` x17, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1 | broader | partial | poor | 2026-09-24 12:43 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 28 | `run` x15, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:46 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 2/10 | 2/10 | 29 | `run` x15, `write_file` x6, `coverage` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 12:48 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 32 | `run` x11, `write_file` x6, `verify` x4, `coverage` x1, `run_tests` x1 | — | — | — | 2026-09-24 12:49 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 37 | `run` x18, `write_file` x8, `verify` x4 | — | — | — | 2026-09-24 12:49 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 20 | `run` x10, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 12:42 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/1 | 0/1 | 41 | `run` x16, `write_file` x6, `verify` x5, `coverage` x4, `mutation` x2 | same | partial | acceptable | 2026-09-24 12:48 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 29 | `run` x12, `write_file` x7, `run_tests` x4 | same | partial | acceptable | 2026-09-24 12:47 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 15 | `run` x7, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 12:46 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 22 | `run` x6, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 12:45 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | YES | 100% (6/6) | 1/6 | 4/6 | 39 | `run` x14, `write_file` x9, `verify` x5, `coverage` x3, `mutation` x2, `run_tests` x1  (+1 edit reverted) | narrower | partial | poor | 2026-09-24 12:54 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 25 | `run` x7, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 12:52 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 1/1 | 1/1 | 24 | `run` x6, `run_tests` x5, `write_file` x5, `verify` x4, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:48 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 19 | `run` x9, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x1 | broader | complete | poor | 2026-09-24 12:45 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 49 | `run` x21, `write_file` x12, `verify` x8, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:55 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 34 | `run` x20, `write_file` x8, `verify` x1 | — | — | — | 2026-09-24 12:51 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 24 | `run` x9, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 12:48 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 31 | `run` x12, `write_file` x6, `run_tests` x3, `verify` x2 | — | — | — | 2026-09-24 12:52 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 38 | `run` x17, `verify` x5, `write_file` x5, `coverage` x4, `mutation` x1 | — | — | — | 2026-09-24 12:51 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 26 | `run` x15, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2, `run_tests` x1 | broader | complete | acceptable | 2026-09-24 12:48 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 100% (3/3) | 2/10 | 6/10 | 35 | `run` x16, `write_file` x7, `verify` x4, `coverage` x3, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:50 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (31/54) | 1/10 | 4/10 | 34 | `run` x19, `write_file` x4, `coverage` x3, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 12:55 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 23 | `run` x10, `write_file` x4, `coverage` x2, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 12:47 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 43 | `run` x20, `write_file` x10, `verify` x6, `coverage` x2 | — | — | — | 2026-09-24 12:54 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 53 | `run` x23, `write_file` x14, `verify` x5, `run_tests` x3, `coverage` x2 | — | — | — | 2026-09-24 12:53 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 54 | `run` x24, `write_file` x10, `verify` x6, `run_tests` x5, `coverage` x1 | — | — | — | 2026-09-24 12:53 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 48 | `run` x21, `write_file` x10, `coverage` x5, `verify` x3, `mutation` x1 | — | — | — | 2026-09-24 12:56 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 43% (16/37) | 3/10 | 5/10 | 39 | `run` x23, `write_file` x5, `coverage` x3, `verify` x3, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 12:56 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 29 | `run` x15, `write_file` x4, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 12:53 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 4/5 | 5/5 | 43 | `run` x24, `write_file` x7, `run_tests` x4, `verify` x3, `coverage` x1, `mutation` x1  (+1 edit reverted) | narrower | partial | poor | 2026-09-24 12:56 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 23 | `run` x8, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3, `run_tests` x1 | narrower | complete | good | 2026-09-24 12:54 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 19 | `run` x12, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | narrower | partial | poor | 2026-09-24 12:57 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 25 | `run` x12, `verify` x3, `coverage` x2, `mutation` x2, `run_tests` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 12:55 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 37 | `run` x16, `write_file` x5, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 12:55 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 18 | `run` x5, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2, `run_tests` x1 | same | complete | acceptable | 2026-09-24 12:56 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 100% (2/2) | 0/2 | 1/2 | 24 | `run` x15, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | broader | complete | poor | 2026-09-24 13:06 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 25 | `run` x16, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | broader | complete | acceptable | 2026-09-24 13:07 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | NO | — | — | — | 37 | `run` x16, `write_file` x7, `verify` x6, `run_tests` x2 | — | — | — | 2026-09-24 13:08 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (partial)
  - Unequal Q-format VLA values are compared element-wise and reported with correct row values, counts, ratios, and report text.
- **astropy__astropy-14598** (partial)
  - A doubled single quote followed by a space and additional text is parsed as part of the value rather than causing a partial string/comment match.
- **astropy__astropy-7606** (partial)
  - UnitBase.__eq__ returning NotImplemented is not pinned: the regular-unit test only checks for an exception, and the old implementation already did not raise.
  - The changed type(self)-based subclass behavior is not tested because two ordinary UnrecognizedUnit instances pass under both the old and new implementations.
- **django__django-11477** (partial)
  - translate_url() produces the correct URL when the optional named component is absent.
  - A supplied optional named component remains captured and is translated or resolved normally.
- **django__django-13012** (partial)
  - ExpressionWrapper around a non-constant expression delegates get_group_by_cols() and preserves the wrapped expression's group-by columns.
- **django__django-13023** (partial)
  - Values that make decimal.Decimal() raise ValueError are converted to ValidationError.
- **django__django-13449** (misses_the_point)
  - SQLite Window expressions with DecimalField output, such as Lag, execute successfully by applying the numeric cast outside the OVER clause.
  - SQLite Window expressions with non-Decimal output continue using the normal Window SQL path without the DecimalField workaround.
- **django__django-14534** (partial)
  - The custom attrs ID is verified on the second choice subwidget with its `_1` suffix.
  - The no-auto_id case in which attrs has no ID and `id_for_label` must return `None`.
- **django__django-14608** (partial)
  - The initially created FormSet non-form ErrorList, including errors appended before clean() completes, uses the nonform CSS class.
  - Too-many-forms validation errors use the nonform CSS class.
  - Too-few-forms validation errors use the nonform CSS class.
- **django__django-14792** (partial)
  - An unnamed fixed-offset datetime.timezone returns its offset name, such as 'UTC+10:00'.
  - A datetime.timezone with an explicit name preserves that name.
  - A named pytz timezone returns its timezone name.
- **django__django-14915** (partial)
  - The wrapper's hash equals hash(self.value), including for equal wrappers with different instances and for the reported lookup against a dictionary keyed by the underlying value.
- **django__django-16139** (partial)
  - The corrected href is verified in the actual non-PK-to_field UserAdmin URL context and shown to resolve to the PK-based password-change URL.
- **django__django-16454** (partial)
  - Errors raised by those subparsers are rendered as management-command usage and error output rather than a traceback.
  - An explicitly supplied non-CommandParser parser class remains supported and keeps normal argparse error handling.
- **matplotlib__matplotlib-20676** (partial)
  - Exact preservation of the original lower bounds and both axes' complete bounds.
  - Initial edge-handle positions matching the relevant axis bounds.
  - The press/onmove path, including unchanged limits and updated handle positions.
- **matplotlib__matplotlib-20859** (partial)
  - The invalid-parent error path and its updated TypeError message.
- **matplotlib__matplotlib-24870** (partial)
  - The list and masked-array variants of the regular-grid cases.
  - Triangular tricontour autodetection.
  - Triangular tricontourf autodetection.
- **matplotlib__matplotlib-24970** (partial)
  - Unsigned-integer result correctness is not asserted.
  - Signed-integer result correctness is not covered.
  - Float16 and float normalization and conversion behaviour is not covered.
- **psf__requests-2931** (partial)
  - String or bytes URL parameters are normalized in `prepare_url` before `_encode_params` so query-string encoding continues to work after the pass-through change.
- **pydata__xarray-2905** (partial)
  - Pandas `Series`, `Index`, and `DataFrame` objects continue to be unwrapped through their `values` attribute.
- **pydata__xarray-4687** (partial)
  - keep_attrs=True actually copies x's attributes.
  - The false and default policies produce the intended attribute result and the default path honors the global setting.
  - The supported string and callable keep_attrs policy forms are accepted and forwarded.
- **pydata__xarray-6744** (partial)
  - center=True alignment for even and other boundary sizes, especially size 2 and the size-1 and size-7 cases exercised by the fix.
  - center=False behavior for sizes 1, 2, and 7, plus direct validation of the individual window contents rather than only their means.
- **pylint-dev__pylint-4970** (partial)
  - The user-visible disablement on actual similarity streams, demonstrated by successful execution with no duplicate-code output.
- **scikit-learn__scikit-learn-10297** (partial)
  - Fitting with store_cv_values=True creates cv_values_ with the correct shape for a one-dimensional target.
  - Fitting with store_cv_values=True creates cv_values_ with the correct shape for a multi-target target.
- **sphinx-doc__sphinx-7462** (partial)
  - The `sphinx.domains.python.unparse` path renders an empty tuple inside `Tuple[()]` as opening and closing parenthesis nodes without raising `IndexError`.
- **sphinx-doc__sphinx-7590** (partial)
  - Integer literals whose suffix begins with a built-in integer suffix and continues as a user-defined suffix.
  - Decimal floating-point literals whose suffix begins with a built-in floating-point suffix and continues as a user-defined suffix.
  - Hexadecimal floating-point literals with a user-defined suffix.
- **sympy__sympy-12489** (partial)
  - The empty/size, integer, `Cycle`, and multiple-cycle constructor routes likewise preserve the requested subclass.
  - Constructing from an instance of the same subclass with a changed size creates the resized result as that subclass.
- **sympy__sympy-14976** (partial)
  - The downstream lambdify/nsolve path preserves arbitrary precision for expressions containing rational constants.
- **sympy__sympy-16450** (partial)
  - The replacement preserves the symbol's other explicit and inferred assumptions through its complete assumptions0 set.

## Without a verdict

- **django__django-12308** — nothing collected on either side -- the file never ran
- **django__django-13794** — nothing collected on either side -- the file never ran
- **django__django-14765** — nothing collected on either side -- the file never ran
- **django__django-15569** — nothing collected on either side -- the file never ran
