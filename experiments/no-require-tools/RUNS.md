# Run status, per pull request

Last run in this table: 2026-09-24 13:48 UTC.

- **70** instances across **12** repositories
- **37/65** fail-to-pass, of those that reached a verdict
- **37** measured for changed-line coverage: **mean 91%** per test, median 100%
- **81%** of the changed lines those tests were measured against (123/152, pooled)
- **24%** of every source line all 70 patches change (123/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.19 and 43.8M tokens in total
- **28** of these were sent a second-chance message after stopping with nothing to score, and **5** of them ended fail-to-pass; the other 42 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 8 | 3 | 0 | 5 | **added by the flag** |
| `no_test` | 2 | 1 | 1 | 0 | from `require-tools` |
| `passes_at_base` | 18 | 1 | 17 | 0 | **added by the flag** |

Of the **26** refused for a reason the flag itself adds, **4** ended fail-to-pass.

Every row was produced with the same configuration: **`no-require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 31 | `run` x11, `write_file` x8, `run_tests` x3, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 13:33 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | NO | — | — | — | 30 | `run` x14, `write_file` x6, `verify` x3, `mutation` x2, `coverage` x1 | — | — | — | 2026-09-24 13:29 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 24 | `run` x17, `write_file` x5 | narrower | partial | acceptable | 2026-09-24 13:28 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 2/4 | 4/4 | 26 | `run` x14, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | same | partial | poor | 2026-09-24 13:26 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 37 | `run` x21, `write_file` x7, `verify` x3, `run_tests` x1 | — | — | — | 2026-09-24 13:28 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 43 | `run` x16, `write_file` x12, `verify` x5, `run_tests` x3 | — | — | — | 2026-09-24 13:28 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 47 | `run` x26, `write_file` x10, `verify` x3, `run_tests` x1 | — | — | — | 2026-09-24 13:32 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | BROKEN | — | — | — | 51 | `run` x30, `write_file` x13, `verify` x3 | — | — | — | 2026-09-24 13:30 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 30 | `run` x18, `write_file` x5, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 13:27 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x20, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 13:25 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | BROKEN | — | — | — | 50 | `run` x29, `write_file` x9, `run_tests` x4, `verify` x3 | — | — | — | 2026-09-24 13:32 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 37 | `run` x20, `write_file` x7, `verify` x4, `coverage` x2 | different | misses_the_point | poor | 2026-09-24 13:30 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | BROKEN | — | — | — | 33 | `run` x15, `write_file` x8, `coverage` x3, `verify` x3 | — | — | — | 2026-09-24 13:29 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 80% (4/5) | 4/5 | 4/5 | 33 | `run` x15, `write_file` x8, `verify` x4, `coverage` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 13:27 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 44 | `run` x20, `write_file` x11, `verify` x6, `coverage` x1, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 13:30 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 28 | `run` x16, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | same | partial | acceptable | 2026-09-24 13:28 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 47 | `run` x23, `write_file` x10, `verify` x5, `run_tests` x2, `coverage` x1 | — | — | — | 2026-09-24 13:30 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 37 | `run` x24, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | same | complete | acceptable | 2026-09-24 13:24 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | NO | — | — | — | 39 | `run` x27, `run_tests` x5, `write_file` x4 | — | — | — | 2026-09-24 13:28 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 27 | `run` x16, `write_file` x4, `verify` x3, `run_tests` x2 | — | — | — | 2026-09-24 13:27 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | BROKEN | — | — | — | 36 | `run` x20, `write_file` x8, `coverage` x2, `verify` x1 | — | — | — | 2026-09-24 13:29 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 44 | `run` x23, `write_file` x8, `coverage` x3, `mutation` x3, `verify` x3 | narrower | partial | acceptable | 2026-09-24 13:34 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 31 | `run` x15, `verify` x5, `write_file` x4, `coverage` x2, `mutation` x2 | broader | partial | poor | 2026-09-24 13:29 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 39 | `run` x13, `write_file` x10, `run_tests` x4, `verify` x4, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 13:29 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 25 | `run` x14, `verify` x3, `write_file` x3, `coverage` x1, `mutation` x1 | same | complete | poor | 2026-09-24 13:24 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 38 | `run` x20, `run_tests` x4, `write_file` x4, `verify` x2 | — | — | — | 2026-09-24 13:29 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 26 | `run` x13, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 13:28 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 7/9 | 7/9 | 44 | `run` x24, `write_file` x6, `coverage` x2, `mutation` x2, `verify` x2 | different | partial | poor | 2026-09-24 13:31 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 56% (10/18) | 1/10 | 1/10 | 44 | `run` x18, `write_file` x12, `verify` x6, `coverage` x3, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 13:32 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 3/4 | 4/4 | 38 | `run` x19, `write_file` x7, `coverage` x3, `verify` x3, `mutation` x2 | same | complete | acceptable | 2026-09-24 13:30 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 39 | `run` x21, `write_file` x7, `coverage` x3, `verify` x3, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 13:34 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 28 | `run` x17, `verify` x3, `coverage` x2, `write_file` x2, `mutation` x1 | narrower | complete | acceptable | 2026-09-24 13:35 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 27 | `run` x18, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1  (+1 edit reverted) | broader | partial | acceptable | 2026-09-24 13:32 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 18 | `run` x8, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | same | partial | acceptable | 2026-09-24 13:35 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 23 | `run` x7, `verify` x4, `write_file` x3, `coverage` x2, `mutation` x2, `run_tests` x2 | narrower | partial | poor | 2026-09-24 13:37 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 39 | `run` x12, `run_tests` x9, `write_file` x9, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 13:41 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 36 | `run` x13, `write_file` x8, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 13:38 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 28 | `run` x11, `verify` x4, `write_file` x4, `coverage` x3, `mutation` x3, `run_tests` x1 | broader | complete | good | 2026-09-24 13:34 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/1 | 0/1 | 28 | `run` x17, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | broader | partial | poor | 2026-09-24 13:34 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 22 | `run` x10, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1, `run_tests` x1 | same | partial | acceptable | 2026-09-24 13:36 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 28 | `run` x9, `coverage` x4, `verify` x4, `write_file` x4, `mutation` x2, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 13:40 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 19 | `run` x9, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | broader | complete | poor | 2026-09-24 13:36 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 24 | `run` x14, `write_file` x5, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-24 13:36 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 18 | `run` x8, `write_file` x3, `mutation` x2, `verify` x2, `coverage` x1 | narrower | partial | acceptable | 2026-09-24 13:42 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 42 | `run` x19, `write_file` x7, `run_tests` x5, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 13:42 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 22 | `run` x8, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3 | same | partial | poor | 2026-09-24 13:38 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 37 | `run` x20, `write_file` x10, `verify` x2, `coverage` x1 | — | — | — | 2026-09-24 13:42 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 38 | `run` x21, `write_file` x8, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 13:40 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 19 | `run` x9, `verify` x3, `write_file` x3, `coverage` x1, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 13:35 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 27 | `run` x11, `write_file` x7, `verify` x2 | — | — | — | 2026-09-24 13:43 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 29 | `run` x10, `verify` x5, `write_file` x5, `coverage` x4, `mutation` x2 | — | — | — | 2026-09-24 13:39 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | NO | — | — | — | 22 | `run` x7, `write_file` x4, `verify` x3, `run_tests` x2, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 13:39 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 40% (4/10) | 1/10 | 6/10 | 32 | `run` x14, `write_file` x6, `verify` x4, `coverage` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 13:39 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | NO | — | — | — | 51 | `run` x25, `write_file` x9, `verify` x6, `run_tests` x4, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 13:44 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 25 | `run` x9, `run_tests` x4, `write_file` x4, `coverage` x2, `mutation` x1, `verify` x1  (+1 edit reverted) | — | — | — | 2026-09-24 13:37 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 29 | `run` x16, `write_file` x5, `coverage` x2, `verify` x2 | — | — | — | 2026-09-24 13:39 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 37 | `run` x20, `write_file` x10 | — | — | — | 2026-09-24 13:41 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 52 | `run` x22, `write_file` x9, `run_tests` x8, `verify` x5, `mutation` x2 | — | — | — | 2026-09-24 13:44 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 51 | `run` x18, `write_file` x12, `verify` x7, `mutation` x4 | — | — | — | 2026-09-24 13:45 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | NO | — | — | — | 33 | `run` x13, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 13:42 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 29 | `run` x18, `write_file` x5, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 13:40 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 4/5 | 5/5 | 34 | `run` x18, `write_file` x6, `verify` x5, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 13:45 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 22 | `run` x13, `write_file` x3, `coverage` x1, `mutation` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 13:42 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 22 | `run` x8, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 13:48 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 26 | `run` x15, `write_file` x4, `run_tests` x2, `coverage` x1, `mutation` x1, `verify` x1 | broader | complete | acceptable | 2026-09-24 13:41 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 49 | `run` x20, `write_file` x11, `run_tests` x6, `coverage` x2, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 13:46 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 21 | `run` x11, `coverage` x2, `verify` x2, `mutation` x1, `run_tests` x1, `write_file` x1 | same | complete | acceptable | 2026-09-24 13:44 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 100% (2/2) | 0/2 | 1/2 | 28 | `run` x13, `coverage` x3, `verify` x3, `write_file` x3, `mutation` x2 | narrower | complete | acceptable | 2026-09-24 13:44 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 32 | `run` x22, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 13:43 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 100% (11/11) | no mutants | no mutants | 23 | `run` x12, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 13:44 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14598** (partial)
  - A Card value containing `''` followed by a space and more text is parsed as the complete value rather than being truncated or misinterpreted at the string/comment boundary.
- **astropy__astropy-7606** (partial)
  - The required False result for UnrecognizedUnit == None and True result for UnrecognizedUnit != None.
  - UnrecognizedUnit inequality with a regular unit and the corresponding membership expression.
  - The negative type-compatibility side of the changed type(self) check.
- **django__django-13012** (partial)
  - An ExpressionWrapper around an expression with non-empty group-by columns propagates those columns unchanged.
- **django__django-13449** (misses_the_point)
  - A SQLite Window expression returning a DecimalField must execute without the near "OVER" syntax error by applying numeric casting outside the OVER clause and must return correct lag values.
  - A SQLite Window expression with a non-Decimal output must continue through the ordinary Window SQL path without Decimal-specific casting.
- **django__django-13590** (partial)
  - Non-namedtuple lists and tuples continue through the fallback `type_(values)` reconstruction path after recursive resolution.
- **django__django-13794** (partial)
  - The actual template add-filter rendering path.
  - The add-filter case where both operands are lazy strings.
  - Generic addition of integer-valued lazy proxies.
- **django__django-14534** (partial)
  - A subwidget with no configured ID has id_for_label equal to None.
  - A custom auto_id format is propagated to each option's id_for_label with the appropriate option index suffix.
- **django__django-14792** (partial)
  - An unnamed datetime fixed-offset timezone returns its offset name, such as "UTC+10:00".
  - A datetime fixed-offset timezone with an explicit name preserves that name, such as "Etc/GMT-10".
  - A named pytz timezone falls back to its timezone name, such as "Europe/Madrid".
- **django__django-14915** (partial)
  - The hash is not checked against hash(value) itself.
  - The dictionary lookup is not asserted to succeed; in fact, the expected successful membership result is explicitly dismissed in a comment.
- **django__django-16139** (partial)
  - The href resolves correctly from an alternate-to_field UserAdmin change URL.
  - The replacement href is verified to remain valid from the conventional pk-based change URL.
- **django__django-16454** (partial)
  - Errors from those subparsers are rendered as human-facing CLI usage/error output instead of a traceback.
  - An explicitly supplied non-CommandParser parser class is left unwrapped and retains its native error behavior.
- **django__django-16560** (partial)
  - Constraint deconstruction includes a configured violation_error_code.
  - Constraint equality accounts for violation_error_code.
  - Constraint repr output includes a configured violation_error_code.
- **django__django-16667** (partial)
  - The resulting value is rejected by DateField/form validation as 'Enter a valid date.' rather than escaping as a server error.
- **matplotlib__matplotlib-20859** (partial)
  - Unsupported Legend parents still raise TypeError, with the error message accurately referring to FigureBase.
- **matplotlib__matplotlib-24870** (partial)
  - Recognition of boolean values supplied as Python lists or masked arrays.
  - The tricontour() boolean default-level path.
  - The tricontourf() boolean default-level path.
- **matplotlib__matplotlib-24970** (partial)
  - Correct float processing and special-value handling after the cast is moved outside the float-only branch.
  - Consistent colormap results for non-empty `uint8` and scalar `int`, `float16`, and `float` inputs.
- **psf__requests-2931** (partial)
  - prepare_url converts scalar string or binary URL parameters with to_native_string before query-string construction.
- **pydata__xarray-2905** (partial)
  - Pandas Series, Index, and DataFrame inputs continue to be converted to their underlying values.
- **pydata__xarray-4075** (partial)
  - sum_of_weights() converts boolean weights to numeric values and returns their numeric sum.
- **pydata__xarray-6744** (partial)
  - The center=False branch.
  - center=True behavior for the other tested widths, especially the even width 2 case and the boundary sizes 1 and 7.
- **pylint-dev__pylint-7277** (partial)
  - Preserve the first entry when it is an arbitrary custom path.
- **scikit-learn__scikit-learn-10297** (partial)
  - With store_cv_values=True, fitting one-dimensional classification targets stores cv_values_ with shape (n_samples, 1, n_alphas).
  - With store_cv_values=True, fitting multi-target classification labels stores cv_values_ with shape (n_samples, n_targets, n_alphas).
- **sphinx-doc__sphinx-7462** (partial)
  - The exact parenthesized doctree produced by the domain unparser, which is needed to establish that the annotation remains valid rather than merely non-crashing.
- **sympy__sympy-14976** (partial)
  - End-to-end arbitrary-precision evaluation through nsolve or an equivalent lambdified numerical computation.
- **sympy__sympy-20590** (partial)
  - Assignment of an undeclared attribute is rejected with `AttributeError`.
- **sympy__sympy-21596** (partial)
  - Excluding denominator-singular parameter values and handling an empty result.
  - Applying the same root filtering to the Naturals0 source domain.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-12308** — nothing collected on either side -- the file never ran
- **django__django-13023** — nothing collected on either side -- the file never ran
- **django__django-13513** — nothing collected on either side -- the file never ran
- **django__django-14765** — nothing collected on either side -- the file never ran
