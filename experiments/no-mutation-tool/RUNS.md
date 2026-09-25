# Run status, per pull request

Last run in this table: 2026-09-24 20:00 UTC.

- **70** instances across **12** repositories
- **40/66** fail-to-pass, of those that reached a verdict
- **40** measured for changed-line coverage: **mean 88%** per test, median 100%
- **85%** of the changed lines those tests were measured against (107/126, pooled)
- **21%** of every source line all 70 patches change (107/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.41 and 46.7M tokens in total
- **42** of these were sent a second-chance message after stopping with nothing to score, and **12** of them ended fail-to-pass; the other 28 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 4 | 1 | 0 | 3 | **added by the flag** |
| `loop_open` | 21 | 9 | 12 | 0 | from `require-tools` |
| `no_test` | 1 | 1 | 0 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 16 | 1 | 14 | 1 | **added by the flag** |

Of the **20** refused for a reason the flag itself adds, **2** ended fail-to-pass.

Every row was produced with the same configuration: **`no-mutation-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 30 | `run` x9, `write_file` x9, `verify` x7 | — | — | — | 2026-09-24 19:37 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 0% (0/1) | 0/7 | 7/7 | 29 | `run` x13, `write_file` x8, `verify` x4, `coverage` x1 | different | misses_the_point | poor | 2026-09-24 19:33 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 21 | `run` x12, `coverage` x2, `verify` x2, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 19:33 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 5/9 | 9/9 | 21 | `run` x11, `coverage` x2, `verify` x2, `write_file` x2, `run_tests` x1 | broader | partial | acceptable | 2026-09-24 19:33 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 53 | `run` x30, `write_file` x9, `run_tests` x5, `verify` x3 | — | — | — | 2026-09-24 19:35 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | BROKEN | — | — | — | 29 | `run` x14, `write_file` x6, `verify` x4  (+1 edit reverted) | — | — | — | 2026-09-24 19:31 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | YES | 100% (1/1) | 2/2 | 2/2 | 39 | `run` x23, `write_file` x6, `coverage` x3, `verify` x3, `run_tests` x1 | narrower | partial | acceptable | 2026-09-24 19:36 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 53 | `run` x24, `write_file` x11, `run_tests` x6, `verify` x6 | — | — | — | 2026-09-24 19:39 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | BROKEN | — | — | — | 33 | `run` x16, `write_file` x8, `verify` x1 | — | — | — | 2026-09-24 19:32 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 25 | `run` x16, `write_file` x3, `coverage` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 19:28 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 24 | `run` x10, `write_file` x4, `coverage` x3, `verify` x3 | narrower | partial | good | 2026-09-24 19:32 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/10 | 8/10 | 41 | `run` x17, `write_file` x9, `verify` x5, `coverage` x4 | different | misses_the_point | poor | 2026-09-24 19:40 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 36 | `run` x18, `write_file` x9, `verify` x5 | — | — | — | 2026-09-24 19:35 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | BROKEN | — | — | — | 39 | `run` x22, `write_file` x9, `verify` x2 | — | — | — | 2026-09-24 19:34 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 32 | `run` x13, `write_file` x6, `run_tests` x4, `coverage` x3, `verify` x3 | narrower | partial | acceptable | 2026-09-24 19:35 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 42 | `run` x28, `write_file` x5, `verify` x3, `coverage` x2 | narrower | partial | acceptable | 2026-09-24 19:34 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 46 | `run` x26, `write_file` x9, `verify` x3, `run_tests` x2 | — | — | — | 2026-09-24 19:31 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 0% (0/1) | 6/6 | 6/6 | 48 | `run` x24, `write_file` x9, `coverage` x3, `verify` x3 | same | complete | acceptable | 2026-09-24 19:36 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 25 | `run` x14, `write_file` x3, `coverage` x2, `run_tests` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 19:33 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 41 | `run` x21, `write_file` x7, `verify` x3, `run_tests` x1 | — | — | — | 2026-09-24 19:37 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 24 | `run` x14, `verify` x3, `write_file` x3, `coverage` x1, `run_tests` x1 | broader | complete | good | 2026-09-24 19:30 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 1/2 | 2/2 | 26 | `run` x17, `write_file` x3, `coverage` x1, `verify` x1 | narrower | partial | acceptable | 2026-09-24 19:34 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 0/1 | 1/1 | 26 | `run` x15, `write_file` x5, `coverage` x1, `verify` x1 | narrower | partial | acceptable | 2026-09-24 19:34 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 55 | `run` x24, `write_file` x15, `coverage` x4, `verify` x4 | — | — | — | 2026-09-24 19:42 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 38 | `run` x28, `write_file` x4, `verify` x2, `coverage` x1 | same | complete | good | 2026-09-24 19:34 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 48 | `run` x23, `write_file` x9, `verify` x6, `coverage` x2 | — | — | — | 2026-09-24 19:38 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 2/2 | 2/2 | 20 | `run` x12, `verify` x2, `write_file` x2, `coverage` x1 | narrower | partial | poor | 2026-09-24 19:30 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 9/10 | 9/10 | 48 | `run` x25, `write_file` x11, `verify` x4, `coverage` x2 | narrower | partial | poor | 2026-09-24 19:42 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 46 | `run` x15, `write_file` x12, `verify` x6, `coverage` x5, `run_tests` x1 | — | — | — | 2026-09-24 19:40 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 30 | `run` x14, `write_file` x5, `run_tests` x4, `coverage` x2, `verify` x2 | same | complete | acceptable | 2026-09-24 19:34 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 40 | `run` x23, `write_file` x10, `verify` x2, `coverage` x1 | narrower | partial | poor | 2026-09-24 19:37 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | NO | — | — | — | 44 | `run` x25, `write_file` x7, `verify` x3 | — | — | — | 2026-09-24 19:43 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 27 | `run` x20, `coverage` x1, `verify` x1, `write_file` x1 | same | partial | acceptable | 2026-09-24 19:37 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 24 | `run` x10, `coverage` x3, `verify` x3, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 19:41 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 1/10 | 20 | `run` x9, `verify` x3, `write_file` x3, `coverage` x2 | narrower | partial | poor | 2026-09-24 19:40 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 45 | `run` x21, `verify` x8, `write_file` x8, `coverage` x2 | — | — | — | 2026-09-24 19:48 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 53 | `run` x23, `write_file` x12, `verify` x10 | — | — | — | 2026-09-24 19:45 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 23 | `run` x13, `verify` x3, `write_file` x3, `coverage` x2 | broader | complete | good | 2026-09-24 19:37 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/2 | 0/2 | 48 | `run` x16, `verify` x10, `write_file` x10, `coverage` x6 | same | partial | acceptable | 2026-09-24 19:45 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 100% (2/2) | 1/1 | 0/1 | 35 | `run` x19, `write_file` x6, `verify` x4, `coverage` x2 | broader | partial | acceptable | 2026-09-24 19:46 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 22 | `run` x13, `write_file` x3, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 19:43 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 21 | `run` x11, `verify` x3, `write_file` x3, `coverage` x2 | broader | complete | acceptable | 2026-09-24 19:42 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 37 | `run` x16, `verify` x8, `write_file` x8, `coverage` x1 | — | — | — | 2026-09-24 19:46 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 21 | `run` x9, `write_file` x5, `verify` x3, `coverage` x2 | narrower | partial | acceptable | 2026-09-24 19:45 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 38 | `run` x21, `write_file` x7, `verify` x5 | — | — | — | 2026-09-24 19:48 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 7/7 | 7/7 | 21 | `run` x12, `coverage` x2, `verify` x2, `write_file` x2 | broader | complete | poor | 2026-09-24 19:43 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 41 | `run` x19, `write_file` x9, `verify` x6 | — | — | — | 2026-09-24 19:48 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | YES | 100% (1/1) | 1/2 | 2/2 | 31 | `run` x19, `write_file` x6, `verify` x2, `coverage` x1 | narrower | partial | poor | 2026-09-24 19:44 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 42 | `run` x21, `run_tests` x6, `write_file` x6, `coverage` x2, `verify` x2 | — | — | — | 2026-09-24 19:45 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | YES | 100% (2/2) | 2/2 | 0/2 | 34 | `run` x16, `write_file` x8, `verify` x4, `coverage` x2 | different | misses_the_point | poor | 2026-09-24 19:49 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 28 | `run` x16, `write_file` x3, `run_tests` x2, `verify` x2, `coverage` x1 | — | — | — | 2026-09-24 19:44 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 20 | `run` x15, `coverage` x1, `verify` x1, `write_file` x1 | narrower | partial | acceptable | 2026-09-24 19:43 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | NO | — | — | — | 41 | `run` x14, `write_file` x12, `verify` x8, `coverage` x2 | — | — | — | 2026-09-24 19:49 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | NO | — | — | — | 39 | `run` x18, `write_file` x9, `verify` x8 | — | — | — | 2026-09-24 19:47 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 28 | `run` x16, `coverage` x3, `write_file` x3, `verify` x2 | — | — | — | 2026-09-24 19:45 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 46 | `run` x25, `write_file` x9, `verify` x4, `coverage` x3 | — | — | — | 2026-09-24 19:52 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 48 | `run` x27, `write_file` x10, `verify` x6 | — | — | — | 2026-09-24 19:48 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 46 | `run` x25, `write_file` x10, `verify` x3, `coverage` x2 | — | — | — | 2026-09-24 19:52 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 29 | `run` x9, `write_file` x6, `verify` x5, `coverage` x1, `run_tests` x1 | — | — | — | 2026-09-24 19:48 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | NO | — | — | — | 33 | `run` x11, `run_tests` x8, `write_file` x7, `verify` x1 | — | — | — | 2026-09-24 19:48 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 36 | `run` x19, `write_file` x8, `verify` x3, `coverage` x2 | — | — | — | 2026-09-24 19:50 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 10/10 | 10/10 | 39 | `run` x24, `write_file` x8, `verify` x2, `coverage` x1 | narrower | partial | poor | 2026-09-24 19:50 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 20 | `run` x10, `write_file` x3, `coverage` x2, `verify` x2 | narrower | complete | good | 2026-09-24 19:50 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 16 | `run` x8, `verify` x2, `write_file` x2, `coverage` x1, `run_tests` x1 | broader | partial | acceptable | 2026-09-24 20:00 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 37 | `run` x24, `write_file` x5, `coverage` x2, `verify` x2 | broader | complete | acceptable | 2026-09-24 19:50 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 44 | `run` x26, `write_file` x6, `verify` x4, `coverage` x2 | — | — | — | 2026-09-24 19:53 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 19 | `run` x10, `coverage` x2, `verify` x2, `write_file` x2 | same | complete | acceptable | 2026-09-24 19:53 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 28 | `run` x16, `verify` x3, `write_file` x3, `coverage` x2 | narrower | partial | poor | 2026-09-24 19:51 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 45 | `run` x26, `write_file` x9, `verify` x5, `coverage` x2 | different | misses_the_point | poor | 2026-09-24 19:55 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 32 | `run` x17, `write_file` x7, `verify` x3, `coverage` x2 | narrower | partial | acceptable | 2026-09-24 19:52 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (misses_the_point)
  - Q-format VLA columns are compared through the VLA-specific comparison path rather than the generic array comparison.
  - Different values in Q-format VLA cells are reported with the correct rows, values, count, ratio, and report text.
  - Identical files containing Q-format VLA columns, including a file compared with itself, are reported as identical.
- **astropy__astropy-14598** (partial)
  - Preserve doubled single quotes followed by a space and then additional value text, as in the developer test value "x" * 100 + "'' xxx".
- **astropy__astropy-7606** (partial)
  - The changed UnitBase.__eq__ NotImplemented protocol is not pinned: the regular-unit false result would also have passed before the fix.
  - The type(self) subclass distinction in UnrecognizedUnit.__eq__ is not tested.
- **django__django-11477** (partial)
  - translate_url() produces a translated URL without an erroneous optional suffix when that argument is absent.
  - An optional suffix that is present remains in the translated URL.
- **django__django-13012** (partial)
  - An ExpressionWrapper whose inner expression has non-empty group-by columns returns those inner group-by columns.
- **django__django-13023** (partial)
  - Values that make Decimal(value) raise ValueError are not tested.
- **django__django-13449** (misses_the_point)
  - On SQLite, a Window containing Lag over a DecimalField executes successfully instead of raising the near "OVER" syntax error and returns the correct lagged values.
  - On SQLite, Window expressions whose output is not a DecimalField continue through the ordinary Window SQL path without the Decimal-specific cast.
- **django__django-13794** (partial)
  - Two lazy integer proxies can be added to produce the numeric sum 9.
- **django__django-14534** (partial)
  - When no ID is present in the subwidget attrs, id_for_label returns None rather than generating a fallback ID.
- **django__django-14608** (partial)
  - The initially created _non_form_errors ErrorList is tagged with the nonform class.
  - A max_num violation produces a non-form error rendered with the nonform class.
  - A min_num violation produces a non-form error rendered with the nonform class.
- **django__django-14792** (partial)
  - An unnamed fixed-offset datetime.timezone returns its offset name, such as 'UTC+10:00'.
  - A named datetime.timezone preserves its explicit name, such as 'Etc/GMT-10'.
  - A named pytz timezone preserves its timezone name, such as 'Europe/Madrid'.
- **django__django-14915** (partial)
  - Wrappers with different underlying values produce different hashes.
- **django__django-16139** (partial)
  - The generated link is resolved from a to_field-based UserAdmin change URL and reaches the canonical password-change endpoint.
- **django__django-16454** (partial)
  - The actual user-facing nested CLI output, including the correct usage/program prefix and precise argument diagnostic rather than only generic error substrings.
  - Propagation to an explicitly supplied CommandParser subclass.
  - Preservation of standard argparse behaviour for an explicitly supplied non-CommandParser such as argparse.ArgumentParser.
- **django__django-16667** (partial)
  - Form validation is explicitly asserted to be invalid with the exact error {"my_date": ["Enter a valid date."]}.
- **matplotlib__matplotlib-20859** (partial)
  - An unsupported parent still raises TypeError with the updated FigureBase wording.
- **matplotlib__matplotlib-24870** (partial)
  - A boolean input to `tricontour` defaults to the single level `[0.5]`.
  - A boolean input to `tricontourf` defaults to `[0, 0.5, 1]`.
- **matplotlib__matplotlib-24970** (partial)
  - The actual colormap output and lookup-index correctness for uint8, int, float16, and float inputs are never asserted.
  - The generated test does not check non-empty unsigned-integer inputs or distinguish the expected under, over, and bad lookup results.
- **psf__requests-2931** (partial)
  - String or bytes supplied as URL parameters are converted to a native string before query-string assembly.
- **pydata__xarray-2905** (partial)
  - pandas Index inputs continue to be converted to their values arrays.
  - pandas DataFrame inputs continue to be converted to their values arrays.
- **pydata__xarray-4075** (partial)
  - The direct sum_of_weights() result is numeric and counts True weights rather than collapsing their dot product to boolean True.
- **pydata__xarray-6744** (partial)
  - The center=False trailing/right-aligned iteration branch.
  - The actual values and contents of the yielded windows for the even-size and edge-case tests; those tests assert only NaN positions.
  - The broader window-size cases covered by the maintainer test, especially sizes 1, 2, and 7.
- **pytest-dev__pytest-6202** (partial)
  - The collection-level getmodpath() result, including its class-qualified path, is not asserted directly.
  - The vscode-python test-discovery behaviour is not exercised.
- **scikit-learn__scikit-learn-13124** (misses_the_point)
  - With shuffle=True, changing random_state must change the class-wise fold memberships rather than merely reorder an otherwise identical collection of folds.
- **scikit-learn__scikit-learn-9288** (partial)
  - The fitted labels_ arrays are exactly equal between the serial and parallel runs.
- **sympy__sympy-14976** (partial)
  - The affected `nsolve` path evaluates rational constants at the requested arbitrary precision.
- **sympy__sympy-16450** (partial)
  - Preservation of additional assumptions such as integer=True on a symbol that posify actually replaces.
- **sympy__sympy-19637** (partial)
  - Returning the correctly parsed expression 2*x/(x-1), rather than merely returning any non-None value.
- **sympy__sympy-20590** (misses_the_point)
  - Slotted Symbol/Basic instances do not expose a __dict__.
  - Assigning an undeclared attribute to such an instance raises AttributeError.
- **sympy__sympy-21596** (partial)
  - The complete reported intersection is exactly FiniteSet(-1, 1), including both valid roots and no others.
  - Factored imaginary-part conditions are solved and filtered correctly for the additional Integers and Naturals0 cases.
  - An unsolved nonlinear imaginary-part condition is represented with a ConditionSet.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-11179** — nothing collected on either side -- the file never ran
- **django__django-12965** — nothing collected on either side -- the file never ran
- **django__django-13590** — nothing collected on either side -- the file never ran
