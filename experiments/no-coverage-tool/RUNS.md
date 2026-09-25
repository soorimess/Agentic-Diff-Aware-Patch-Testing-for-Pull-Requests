# Run status, per pull request

Last run in this table: 2026-09-24 17:36 UTC.

- **70** instances across **12** repositories
- **43/66** fail-to-pass, of those that reached a verdict
- **43** measured for changed-line coverage: **mean 86%** per test, median 100%
- **68%** of the changed lines those tests were measured against (171/250, pooled)
- **34%** of every source line all 70 patches change (171/508) -- a fixed denominator, so this is the figure that compares across arms
- \$2.97 and 40.6M tokens in total
- **34** of these were sent a second-chance message after stopping with nothing to score, and **7** of them ended fail-to-pass; the other 36 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 4 | 0 | 0 | 4 | **added by the flag** |
| `loop_open` | 16 | 7 | 9 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 14 | 0 | 14 | 0 | **added by the flag** |

Of the **18** refused for a reason the flag itself adds, **0** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 32 | `run` x19, `write_file` x5, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 17:21 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 3/3 | 3/3 | 35 | `run` x20, `write_file` x7, `mutation` x2, `verify` x2  (+1 edit reverted) | same | misses_the_point | poor | 2026-09-24 17:20 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 29 | `run` x21, `mutation` x2, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 17:18 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 3/4 | 4/4 | 20 | `run` x9, `write_file` x4, `mutation` x2, `verify` x2 | broader | partial | acceptable | 2026-09-24 17:14 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 36 | `run` x20, `write_file` x9, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 17:20 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 38 | `run` x16, `write_file` x7, `run_tests` x4 | — | — | — | 2026-09-24 17:16 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 38 | `run` x18, `write_file` x9, `verify` x4, `run_tests` x1 | — | — | — | 2026-09-24 17:20 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 39 | `run` x25, `write_file` x6, `verify` x2 | — | — | — | 2026-09-24 17:18 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 48 | `run` x21, `write_file` x12, `verify` x6, `mutation` x1 | — | — | — | 2026-09-24 17:23 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x14, `write_file` x5, `verify` x3, `mutation` x2, `run_tests` x1 | narrower | partial | acceptable | 2026-09-24 17:17 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | BROKEN | — | — | — | 46 | `run` x28, `write_file` x7, `verify` x4, `run_tests` x1 | — | — | — | 2026-09-24 17:16 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 41 | `run` x21, `write_file` x5, `run_tests` x4, `verify` x4 | — | — | — | 2026-09-24 17:17 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 48 | `run` x21, `write_file` x13, `verify` x6, `mutation` x1 | — | — | — | 2026-09-24 17:24 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 80% (4/5) | 4/5 | 4/5 | 28 | `run` x15, `write_file` x4, `verify` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 17:18 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | NO | — | — | — | 41 | `run` x22, `write_file` x7, `run_tests` x3, `verify` x3 | — | — | — | 2026-09-24 17:16 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 36 | `run` x16, `run_tests` x6, `write_file` x5, `verify` x3, `mutation` x2 | same | partial | acceptable | 2026-09-24 17:15 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | BROKEN | — | — | — | 45 | `run` x19, `write_file` x12, `verify` x5, `mutation` x2, `run_tests` x1 | — | — | — | 2026-09-24 17:21 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 20 | `run` x11, `write_file` x3, `mutation` x2, `verify` x2 | same | complete | acceptable | 2026-09-24 17:13 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 32 | `run` x21, `write_file` x3, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 17:14 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 36 | `run` x20, `write_file` x6, `run_tests` x1, `verify` x1 | — | — | — | 2026-09-24 17:20 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 25 | `run` x18, `write_file` x2, `mutation` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 17:17 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 49 | `run` x22, `write_file` x10, `verify` x6, `run_tests` x4, `mutation` x2 | — | — | — | 2026-09-24 17:23 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 23 | `run` x13, `write_file` x3, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 17:15 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 43 | `run` x18, `write_file` x9, `verify` x6, `mutation` x3 | — | — | — | 2026-09-24 17:22 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 23 | `run` x15, `verify` x2, `write_file` x2, `mutation` x1 | broader | complete | acceptable | 2026-09-24 17:16 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 40 | `run` x20, `write_file` x10, `verify` x3, `mutation` x1 | — | — | — | 2026-09-24 17:20 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 34 | `run` x23, `write_file` x4, `mutation` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 17:18 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | BROKEN | — | — | — | 32 | `run` x14, `write_file` x6, `verify` x3, `run_tests` x2 | — | — | — | 2026-09-24 17:15 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 62% (15/24) | 3/10 | 1/10 | 24 | `run` x15, `verify` x2, `write_file` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 17:18 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 25 | `run` x18, `mutation` x2, `write_file` x2, `verify` x1 | same | complete | acceptable | 2026-09-24 17:15 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 26 | `run` x16, `write_file` x3, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 17:19 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 5/5 | 5/5 | 27 | `run` x18, `mutation` x2, `verify` x2, `write_file` x2 | narrower | complete | acceptable | 2026-09-24 17:23 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 19 | `run` x11, `write_file` x3, `verify` x2, `mutation` x1 | broader | partial | poor | 2026-09-24 17:21 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 35 | `run` x19, `write_file` x6, `verify` x3, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 17:28 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 2/10 | 2/10 | 21 | `run` x7, `write_file` x5, `run_tests` x2, `verify` x2, `mutation` x1 | different | partial | acceptable | 2026-09-24 17:25 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | YES | 100% (7/7) | 6/10 | 7/10 | 36 | `run` x13, `verify` x5, `write_file` x5, `mutation` x3, `run_tests` x3 | narrower | partial | poor | 2026-09-24 17:31 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 48 | `run` x30, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 17:27 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 26 | `run` x13, `write_file` x4, `mutation` x3, `verify` x3 | broader | complete | good | 2026-09-24 17:21 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/1 | 0/1 | 21 | `run` x13, `mutation` x2, `verify` x2, `write_file` x2 | same | partial | poor | 2026-09-24 17:22 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 26 | `run` x13, `write_file` x6, `mutation` x1, `run_tests` x1, `verify` x1 | same | misses_the_point | poor | 2026-09-24 17:26 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 3/10 | 3/10 | 18 | `run` x9, `write_file` x3, `mutation` x2, `verify` x2 | broader | complete | acceptable | 2026-09-24 17:27 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 20 | `run` x13, `mutation` x2, `verify` x1, `write_file` x1  (+2 edits reverted) | broader | complete | acceptable | 2026-09-24 17:23 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 35 | `run` x23, `write_file` x5, `mutation` x1, `run_tests` x1, `verify` x1  (+1 edit reverted) | — | — | — | 2026-09-24 17:26 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 20 | `run` x9, `write_file` x4, `mutation` x2, `verify` x2 | unparsed | — | — | 2026-09-24 17:29 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 32 | `run` x13, `verify` x6, `write_file` x6, `mutation` x1 | — | — | — | 2026-09-24 17:28 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 27 | `run` x11, `run_tests` x3, `write_file` x3, `mutation` x2, `verify` x2 | broader | complete | poor | 2026-09-24 17:25 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 50 | `run` x23, `write_file` x13, `verify` x5, `mutation` x1 | — | — | — | 2026-09-24 17:31 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 43 | `run` x15, `write_file` x12, `run_tests` x5, `verify` x4 | — | — | — | 2026-09-24 17:30 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 28 | `run` x15, `verify` x5, `write_file` x4, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 17:27 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 31 | `run` x15, `write_file` x7, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 17:31 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 38 | `run` x21, `write_file` x4, `mutation` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 17:29 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 26 | `run` x13, `run_tests` x4, `write_file` x4 | broader | complete | acceptable | 2026-09-24 17:28 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 40% (4/10) | 0/10 | 6/10 | 27 | `run` x16, `write_file` x5, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 17:27 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 55% (26/47) | 0/10 | 4/10 | 35 | `run` x23, `write_file` x5, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 17:34 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 31 | `run` x18, `write_file` x6, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 17:28 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 46 | `run` x18, `write_file` x8, `run_tests` x4, `verify` x4, `mutation` x2 | — | — | — | 2026-09-24 17:32 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 39 | `run` x19, `write_file` x10, `verify` x3 | — | — | — | 2026-09-24 17:30 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 39 | `run` x21, `write_file` x7, `verify` x3, `mutation` x1 | — | — | — | 2026-09-24 17:30 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 34 | `run` x15, `write_file` x7, `mutation` x2, `verify` x1 | — | — | — | 2026-09-24 17:33 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 40% (15/37) | 1/10 | 5/10 | 27 | `run` x11, `run_tests` x4, `write_file` x4, `verify` x3, `mutation` x2 | narrower | partial | good | 2026-09-24 17:31 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | YES | 100% (2/2) | 3/3 | 3/3 | 29 | `run` x13, `write_file` x7, `verify` x4, `mutation` x1 | same | partial | poor | 2026-09-24 17:31 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 4/5 | 5/5 | 31 | `run` x17, `verify` x4, `write_file` x4, `mutation` x2 | narrower | partial | poor | 2026-09-24 17:32 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 22 | `run` x9, `verify` x4, `write_file` x3, `run_tests` x2, `mutation` x1 | narrower | complete | poor | 2026-09-24 17:30 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 22 | `run` x13, `write_file` x3, `mutation` x2, `verify` x2 | broader | partial | acceptable | 2026-09-24 17:36 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 28 | `run` x18, `write_file` x3, `verify` x2, `mutation` x1 | broader | partial | poor | 2026-09-24 17:30 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 47 | `run` x23, `write_file` x8, `verify` x4, `mutation` x2 | — | — | — | 2026-09-24 17:34 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 21 | `run` x8, `write_file` x3, `mutation` x2, `run_tests` x2, `verify` x2 | same | complete | good | 2026-09-24 17:33 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 23 | `run` x13, `verify` x2, `write_file` x2, `mutation` x1, `run_tests` x1 | narrower | partial | poor | 2026-09-24 17:31 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 33 | `run` x19, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x1 | narrower | partial | poor | 2026-09-24 17:33 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 23 | `run` x14, `verify` x3, `mutation` x2, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 17:34 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (partial)
  - The complete expected unit for the reported scaled expression `10+3J/m/s/kpc2`, including its scale and every denominator factor, is not asserted.
  - The complete expected unit for `J/s/kpc2`, including `s` as well as `kpc2` in the denominator, is not asserted.
- **astropy__astropy-14539** (misses_the_point)
  - Identical Q-format VLA data, including comparing a file with itself, is considered identical and produces no differences.
  - Unequal Q-format VLA data is compared elementwise and reported with the correct affected rows, values, counts, and ratios.
- **astropy__astropy-14598** (partial)
  - The space-sensitive `'' xxx` case that exercises the anchored full-string regular-expression match.
- **astropy__astropy-7606** (partial)
  - The changed UnrecognizedUnit type guard for comparisons involving a different unit type or UnrecognizedUnit subclass.
- **django__django-13012** (partial)
  - An ExpressionWrapper around a nonconstant expression delegates get_group_by_cols() and preserves the wrapped expression's non-empty GROUP BY columns.
- **django__django-13590** (partial)
  - The ordinary list and tuple fallback path is not tested.
- **django__django-14534** (partial)
  - When no subwidget ID is supplied, id_for_label returns None instead of synthesizing an id_name_index value.
- **django__django-14608** (partial)
  - Built-in formset validation errors stored in the initially created non-form error list use the nonform CSS class.
- **django__django-14915** (partial)
  - The hash follows the underlying value for different values, producing different hashes for the distinct values in the regression.
  - A wrapper's hash matches the hash of a raw underlying value, allowing lookup in a dictionary keyed by that raw value.
- **django__django-16139** (partial)
  - The corrected href resolves correctly from a UserAdmin change URL accessed through to_field and therefore avoids the reported 404.
- **django__django-16560** (partial)
  - BaseConstraint directly accepts and stores a custom violation_error_code.
  - Constraint equality distinguishes ExclusionConstraints with different violation_error_code values.
  - UniqueConstraint repr includes a custom violation_error_code.
- **django__django-16667** (partial)
  - The form is invalid and reports the expected "Enter a valid date." error after the overflow is converted to "0-0-0".
- **matplotlib__matplotlib-20859** (partial)
  - A legend created for a SubFigure is attached to that SubFigure.
  - A parent that is neither Axes nor FigureBase is rejected with TypeError using the updated FigureBase message.
- **matplotlib__matplotlib-24870** (partial)
  - Boolean list and masked-array inputs for regular contour.
  - Boolean list and masked-array inputs for regular contourf.
  - Unfilled tricontour with boolean ndarray or list input.
- **matplotlib__matplotlib-24970** (partial)
  - Unsigned and ordinary integer inputs retain the correct colormap result after conversion before sentinel assignment.
  - Floating-point inputs retain the correct colormap result after normalization, clipping, and integer-index conversion.
- **matplotlib__matplotlib-25960** (partial)
  - The independent horizontal wspace behaviour and its expected column positions and widths.
  - The independent vertical hspace behaviour and its expected row positions and heights.
- **psf__requests-2931** (partial)
  - URL parameters are normalized in `prepare_url` before being passed to `_encode_params`.
- **pydata__xarray-2905** (misses_the_point)
  - The assigned HasValues object is stored as the object itself rather than being coerced to its values attribute.
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their values arrays.
- **scikit-learn__scikit-learn-10297** (partial)
  - With store_cv_values=True and cv=None, fitting one-dimensional targets produces cv_values_ with shape (n_samples, 1, n_alphas).
  - With store_cv_values=True and cv=None, fitting two-dimensional targets produces cv_values_ with shape (n_samples, n_targets, n_alphas).
- **scikit-learn__scikit-learn-14087** (partial)
  - The multinomial coefficient-path branch.
  - The elasticnet branch that computes and stores selected l1 ratios.
  - The explicit l1_ratio_ is None postcondition for non-elasticnet penalties.
- **sphinx-doc__sphinx-7462** (partial)
  - The Python domain unparser produces the expected punctuation-node structure for `Tuple[()]`; `assert result is not None` is too weak to pin this behaviour.
- **sphinx-doc__sphinx-7590** (partial)
  - A successful parse is not pinned to an expected AST or mangled ID; assert result is not None is weaker than checking the parsed literal.
  - Hexadecimal floating-point UDLs are not tested.
  - Character UDLs, including prefixed character forms, are not tested.
- **sympy__sympy-12489** (partial)
  - Cycle, multi-argument, and sequence/list constructor paths use the calling subclass rather than base Permutation.
  - Construction from an existing subclass instance, including resizing, preserves the calling subclass.
  - The internal _af_new constructor creates the class on which it is invoked.
- **sympy__sympy-13551** (partial)
  - The reported product evaluates to the exact correct value 15/2 when n=2; assert result != 9/2 permits any other incorrect value.
- **sympy__sympy-14976** (partial)
  - The complete exact Rational printer output, including mpmath.mpf wrapping of both numerator and denominator.
  - Full-precision nsolve behaviour for an expression containing a rational constant.
- **sympy__sympy-16450** (partial)
  - Retention of an additional assumption such as integer=True on a symbol that is actually replaced; in test_posify_preserves_multiple_assumptions, positive=True prevents posify from taking the replacement path.
- **sympy__sympy-16766** (partial)
  - Exact single-index output is not asserted; `assert "p[0]" in result` allows additional output.
  - Exact multi-index output is not asserted; `assert "q[0, 1]" in result` allows additional output.
- **sympy__sympy-19637** (partial)
  - The no-space input must successfully return the parsed expression 2*x/(x-1).
- **sympy__sympy-20590** (partial)
  - Slotted SymPy objects reject assignment of undeclared attributes with AttributeError.
- **sympy__sympy-21596** (partial)
  - The alternative factored imaginary-part cases over Integers and Naturals0, including filtering out non-domain roots.
  - The unresolved imaginary equation represented by a ConditionSet.
  - Denominator and pole exclusion cases, including retaining valid values and producing EmptySet when none remain.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-13023** — nothing collected on either side -- the file never ran
- **django__django-14559** — nothing collected on either side -- the file never ran
- **django__django-16454** — nothing collected on either side -- the file never ran
