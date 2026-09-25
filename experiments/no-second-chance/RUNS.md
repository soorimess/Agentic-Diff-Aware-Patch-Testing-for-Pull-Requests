# Run status, per pull request

Last run in this table: 2026-09-24 09:29 UTC.

- **70** instances across **12** repositories
- **44/63** fail-to-pass, of those that reached a verdict
- **44** measured for changed-line coverage: **mean 88%** per test, median 100%
- **74%** of the changed lines those tests were measured against (195/263, pooled)
- **38%** of every source line all 70 patches change (195/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.52 and 48.3M tokens in total
- **41** of these were sent a second-chance message after stopping with nothing to score, and **15** of them ended fail-to-pass; the other 29 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `loop_open` | 41 | 15 | 19 | 7 | from `require-tools` |
Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 24 | `run` x8, `write_file` x6, `coverage` x2, `mutation` x2, `verify` x2 | same | partial | poor | 2026-09-24 09:12 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 1/3 | 3/3 | 21 | `run` x9, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2, `run_tests` x1 | narrower | partial | poor | 2026-09-24 09:17 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 20 | `run` x7, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 09:15 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 3/4 | 4/4 | 36 | `run` x22, `verify` x3, `coverage` x2, `write_file` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 09:15 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 47 | `run` x30, `write_file` x8, `verify` x3, `run_tests` x1  (+1 edit reverted) | — | — | — | 2026-09-24 09:14 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 40 | `run` x20, `write_file` x9, `verify` x4, `mutation` x1 | — | — | — | 2026-09-24 09:11 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 47 | `run` x18, `write_file` x11, `verify` x6, `run_tests` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 09:24 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 100% (5/5) | 2/3 | 2/3 | 37 | `run` x22, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 09:21 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 44 | `run` x20, `write_file` x11, `verify` x4, `run_tests` x2 | — | — | — | 2026-09-24 09:16 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 36 | `run` x16, `write_file` x7, `verify` x4, `coverage` x3, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 09:15 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 45 | `run` x21, `write_file` x10, `verify` x5, `coverage` x3, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 09:12 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 40 | `run` x29, `write_file` x6 | — | — | — | 2026-09-24 09:06 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | BROKEN | — | — | — | 41 | `run` x22, `write_file` x11, `verify` x4 | — | — | — | 2026-09-24 09:14 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | NO | — | — | — | 39 | `run` x12, `write_file` x9, `verify` x6, `coverage` x4, `run_tests` x2, `mutation` x1 | — | — | — | 2026-09-24 09:16 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 27 | `run` x14, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x1, `run_tests` x1 | narrower | partial | poor | 2026-09-24 09:11 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 29 | `run` x17, `coverage` x2, `run_tests` x2, `verify` x2, `write_file` x2, `mutation` x1 | broader | partial | acceptable | 2026-09-24 09:04 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | YES | 25% (1/4) | 0/2 | 2/2 | 37 | `run` x15, `write_file` x6, `coverage` x4, `verify` x4, `run_tests` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 09:09 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | BROKEN | — | — | — | 48 | `run` x29, `write_file` x11, `verify` x2, `run_tests` x1 | — | — | — | 2026-09-24 09:13 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | BROKEN | — | — | — | 44 | `run` x26, `write_file` x7, `verify` x3, `run_tests` x2 | — | — | — | 2026-09-24 09:15 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 43% (3/7) | 1/6 | 2/6 | 45 | `run` x23, `write_file` x7, `verify` x5, `coverage` x3, `mutation` x1 | different | partial | poor | 2026-09-24 09:22 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | BROKEN | — | — | — | 47 | `run` x29, `write_file` x7, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 09:22 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 30 | `run` x15, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 09:07 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 33 | `run` x18, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | narrower | partial | acceptable | 2026-09-24 09:10 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 47 | `run` x26, `write_file` x11, `verify` x5 | — | — | — | 2026-09-24 09:16 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 26 | `run` x19, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1 | narrower | partial | acceptable | 2026-09-24 09:16 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 48 | `run` x25, `write_file` x11, `coverage` x2, `verify` x2, `mutation` x1 | — | — | — | 2026-09-24 09:19 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 35 | `run` x22, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2, `run_tests` x1 | narrower | partial | acceptable | 2026-09-24 09:12 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | BROKEN | — | — | — | 42 | `run` x24, `write_file` x10, `verify` x4 | — | — | — | 2026-09-24 09:23 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 67% (12/18) | 1/10 | 1/10 | 27 | `run` x7, `write_file` x6, `coverage` x4, `run_tests` x3, `verify` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 09:20 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | BROKEN | — | — | — | 36 | `run` x28, `write_file` x3 | — | — | — | 2026-09-24 09:07 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 25 | `run` x16, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 09:03 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 20 | `run` x9, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | narrower | partial | poor | 2026-09-24 09:11 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 39 | `run` x23, `write_file` x6, `verify` x2, `coverage` x1, `mutation` x1 | same | partial | poor | 2026-09-24 09:13 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 28 | `run` x9, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x1 | narrower | partial | poor | 2026-09-24 09:19 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 27 | `run` x12, `write_file` x5, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 09:08 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 42 | `run` x17, `write_file` x7, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-24 09:19 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 42 | `run` x14, `write_file` x8, `coverage` x7, `verify` x7, `mutation` x2 | — | — | — | 2026-09-24 09:19 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 24 | `run` x9, `verify` x5, `write_file` x4, `coverage` x2, `mutation` x2 | broader | complete | acceptable | 2026-09-24 09:17 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 100% (3/3) | 1/1 | 0/1 | 31 | `run` x14, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x2, `run_tests` x2 | broader | partial | poor | 2026-09-24 09:19 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 45 | `run` x21, `write_file` x10, `verify` x3, `coverage` x2, `mutation` x2, `run_tests` x2 | same | partial | poor | 2026-09-24 09:25 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 27 | `run` x13, `coverage` x3, `verify` x3, `write_file` x3, `mutation` x2 | broader | complete | acceptable | 2026-09-24 09:22 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 19 | `run` x10, `verify` x3, `write_file` x2, `coverage` x1, `mutation` x1 | broader | complete | acceptable | 2026-09-24 09:15 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 42 | `run` x15, `write_file` x9, `run_tests` x7, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 09:17 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 28 | `run` x14, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | narrower | partial | poor | 2026-09-24 09:22 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 40 | `run` x17, `write_file` x7, `coverage` x3, `run_tests` x3, `verify` x3 | — | — | — | 2026-09-24 09:19 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 21 | `run` x11, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | broader | complete | poor | 2026-09-24 09:08 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 31 | `run` x17, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 09:17 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 32 | `run` x17, `write_file` x8, `verify` x1 | — | — | — | 2026-09-24 09:22 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 2/6 | 3/6 | 50 | `run` x27, `write_file` x5, `verify` x4, `coverage` x3, `mutation` x3, `run_tests` x3  (+1 edit reverted) | narrower | partial | poor | 2026-09-24 09:23 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 31 | `run` x14, `write_file` x8, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 09:24 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 46 | `run` x24, `write_file` x7, `verify` x5, `coverage` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 09:19 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 24 | `run` x13, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2, `run_tests` x1 | same | partial | acceptable | 2026-09-24 09:14 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 2/10 | 6/10 | 43 | `run` x26, `write_file` x5, `coverage` x3, `verify` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 09:20 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 64% (30/47) | 1/10 | 4/10 | 47 | `run` x21, `write_file` x8, `run_tests` x4, `verify` x4, `coverage` x3, `mutation` x2 | narrower | partial | poor | 2026-09-24 09:27 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 28 | `run` x17, `verify` x3, `coverage` x2, `write_file` x2, `mutation` x1 | broader | complete | good | 2026-09-24 09:18 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 41 | `run` x17, `write_file` x10, `verify` x6 | — | — | — | 2026-09-24 09:22 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 32 | `run` x15, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 09:20 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 41 | `run` x26, `write_file` x7, `verify` x2 | — | — | — | 2026-09-24 09:21 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | YES | 100% (3/3) | 1/4 | 3/4 | 28 | `run` x9, `write_file` x5, `coverage` x3, `mutation` x3, `verify` x3 | different | partial | poor | 2026-09-24 09:22 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 43% (16/37) | 2/10 | 5/10 | 35 | `run` x16, `write_file` x6, `verify` x4, `coverage` x3, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 09:26 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 36 | `run` x15, `write_file` x7, `verify` x5, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 09:24 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 4/5 | 5/5 | 32 | `run` x20, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | narrower | partial | poor | 2026-09-24 09:22 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 15 | `run` x9, `coverage` x1, `mutation` x1, `run_tests` x1, `verify` x1, `write_file` x1 | broader | complete | poor | 2026-09-24 09:18 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 24 | `run` x12, `mutation` x3, `coverage` x2, `verify` x2, `write_file` x2 | narrower | partial | poor | 2026-09-24 09:29 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 29 | `run` x16, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2  (+1 edit reverted) | broader | complete | acceptable | 2026-09-24 09:23 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 42 | `run` x21, `write_file` x7, `coverage` x2, `verify` x2, `mutation` x1, `run_tests` x1 | — | — | — | 2026-09-24 09:26 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 20 | `run` x8, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2, `run_tests` x1  (+1 edit reverted) | same | complete | acceptable | 2026-09-24 09:25 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 40 | `run` x24, `verify` x4, `coverage` x3, `write_file` x3, `mutation` x2  (+1 edit reverted) | narrower | partial | poor | 2026-09-24 09:27 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 40 | `run` x23, `write_file` x8, `coverage` x1, `mutation` x1, `run_tests` x1, `verify` x1 | narrower | partial | poor | 2026-09-24 09:26 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 40 | `run` x21, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 09:28 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (partial)
  - It does not positively assert the expected unit equivalence for 10+3J/m/s/kpc2.
  - It does not positively assert the expected unit equivalence for 10-7J/s/kpc2.
  - It does not verify the general left-associative chained-division behaviour except through fragile string non-equality checks.
- **astropy__astropy-14539** (partial)
  - Differing Q-format variable-length array table data must be compared row-wise and reported with the correct differing rows, values, counts, and summary.
- **astropy__astropy-14598** (partial)
  - Long FITS string values containing two consecutive single-quote characters followed by a space and more value text are parsed as one string rather than stopping at the quote-space sequence.
- **astropy__astropy-7606** (partial)
  - Reflected or container comparisons involving None, such as `unit not in (None, u.m)`, do not raise.
  - UnrecognizedUnit equality to its string name.
  - UnrecognizedUnit inequality with a recognized unit.
- **django__django-12308** (partial)
  - Truthy JSONField array/list values are displayed using JSON serialization.
  - Truthy JSONField string values are displayed using JSON serialization.
  - If JSONField preparation raises TypeError for invalid JSON, display_for_field() falls back to display_for_value() instead of propagating the error.
- **django__django-13012** (partial)
  - ExpressionWrapper delegates to a wrapped expression with non-empty group-by columns so the inner expression's columns are returned.
- **django__django-13023** (partial)
  - Values rejected by decimal.Decimal() with ValueError, such as empty tuple or empty list, raise ValidationError instead of leaking ValueError.
  - The resulting ValidationError uses DecimalField's standard invalid decimal error message.
- **django__django-13794** (partial)
  - The template `add` filter should concatenate an eager string with a lazy string argument instead of returning an empty string.
  - The template `add` filter should concatenate two lazy strings instead of returning an empty string.
  - Lazy-proxy addition should work for non-string result types such as integers.
- **django__django-14534** (partial)
  - BoundWidget.id_for_label returns None when the subwidget attrs contain no id instead of inventing one.
- **django__django-14559** (partial)
  - bulk_update() returns the total number of rows matched by the underlying update() calls for non-empty input.
  - bulk_update() accumulates matched-row counts per batch, so duplicates in one batch count once while duplicates in separate batches can be counted per batch.
- **django__django-14725** (partial)
  - edit_only=True makes model formset save() skip creation of new objects from posted extra forms
  - edit_only=True still allows saving changes to existing model formset objects
  - inlineformset_factory accepts and forwards edit_only to the generated inline formset
- **django__django-14792** (partial)
  - The negative-offset pytz Etc/GMT+5 case is asserted with the wrong expected value, '-0500' instead of the pytz tzname form such as '-05'.
  - zoneinfo named-timezone fallback to str(timezone) is not covered.
  - datetime.timezone fixed-offset behaviour is not covered.
- **django__django-14915** (partial)
  - Its hash is the hash of the wrapped value, making it compatible with equality and with lookups against existing raw choice values.
  - Two ModelChoiceIteratorValue objects with the same wrapped value hash the same regardless of their instance.
  - ModelChoiceIteratorValue objects with different wrapped values have the corresponding different hashes.
- **django__django-15569** (partial)
  - Unregistering with an explicit lookup_name also reaches the same cache-clearing behaviour.
  - Using _clear_cached_lookups() invalidates cached lookups for the registry class and its subclasses, matching register_lookup().
- **django__django-16139** (partial)
  - That href resolves correctly to the admin password-change view when the user change page is accessed via a non-pk to_field value.
- **django__django-16560** (partial)
  - No test calls validate() or asserts ValidationError.code.
  - No BaseConstraint deconstruct coverage.
  - No precise CheckConstraint repr/equality coverage.
- **django__django-16667** (partial)
  - A form using SelectDateWidget treats the overflow-derived value as an invalid date rather than propagating an exception.
  - The "0-0-0" sentinel is rejected by date field cleaning with the normal "Enter a valid date." validation error.
- **matplotlib__matplotlib-20676** (partial)
  - The edge handles are initialized at the current active-axis bounds.
  - The inactive axis bounds are also preserved.
  - After an interactive press/move update, bounds remain unchanged and edge handles move to the selected endpoints.
- **matplotlib__matplotlib-20859** (partial)
  - The legend created for a SubFigure is associated with that SubFigure via set_figure(parent).
  - Invalid legend parents still raise TypeError, now referring to Axes or FigureBase.
- **matplotlib__matplotlib-24870** (partial)
  - Regular contour and contourf preserve and detect boolean dtype for nested-list and masked-array inputs.
  - Regular contour and contourf preserve and detect boolean dtype on the x, y, z argument path as well as the z-only path.
  - tricontour on boolean z data with no explicit levels defaults to [0.5].
- **matplotlib__matplotlib-24970** (partial)
  - The dtype conversion still preserves the expected colormap result for scalar integer and float inputs.
  - Float inputs still have their astype(int) conversion performed under np.errstate(invalid='ignore') so invalid float values remain warning-suppressed.
- **psf__requests-2931** (partial)
  - that the prepared body remains bytes
  - that raw str/bytes params are converted correctly and appear correctly in the prepared URL
- **pydata__xarray-2905** (partial)
  - Pandas Series, Index, and DataFrame objects are still unwrapped to their .values arrays.
- **pydata__xarray-6744** (partial)
  - The `center=False` branch.
  - Window sizes 1, 2, and 7, including even-sized and boundary cases.
  - Direct verification of the yielded window contents rather than only their means.
- **scikit-learn__scikit-learn-10297** (partial)
  - With store_cv_values=True and cv=None, fitting stores cross-validation values in cv_values_.
  - For a one-dimensional classifier target, cv_values_ has shape (n_samples, 1, n_alphas).
  - For a multi-target classifier target, cv_values_ has shape (n_samples, n_targets, n_alphas).
- **scikit-learn__scikit-learn-14087** (partial)
  - The no-refit multinomial coefficient averaging path still works when the resolved multi_class is multinomial.
  - For elasticnet penalties, l1_ratio_ is still computed from the selected best l1_ratios.
- **scikit-learn__scikit-learn-9288** (partial)
  - The generated test does not verify exact equality of the resulting labels or centers, only equality of inertia.
- **sphinx-doc__sphinx-7462** (partial)
  - `sphinx.domains.python` renders that empty tuple annotation with explicit `(` and `)` punctuation nodes.
  - `sphinx.pycode.ast.unparse` returns the string `()` for an empty `ast.Tuple`.
- **sphinx-doc__sphinx-7590** (partial)
  - C++ hexadecimal floating literals can be parsed with user-defined literal suffixes.
  - Character literal UDLs with the full set of prefixes and escape forms.
  - Parsed C++ UDLs are represented as the corresponding literal-operator expression rather than merely consumed as plain literals.
- **sphinx-doc__sphinx-9658** (partial)
  - Mocked classes keep their leaf class name in the actual rendered base-class/stringification path.
  - `restify()` renders a mocked class as a full Python class cross-reference such as `:py:class:`unknown.secret.Class``.
  - `stringify()` renders a mocked class as the full dotted name such as `unknown.secret.Class`.
- **sympy__sympy-12489** (partial)
  - Other Permutation.__new__ branches changed to use cls, including empty/size, integer, multiple-cycle arguments, and existing-instance resizing.
  - _af_new is class-aware as a distinct internal constructor path.
  - Mixed base/subclass multiplication preserves the dispatch-dependent result type.
- **sympy__sympy-14976** (partial)
  - It does not require numerator and denominator to be separately wrapped as mpmath.mpf values.
  - It does not effectively test nsolve precision, because AssertionError and other failures in that check are caught and ignored.
- **sympy__sympy-16450** (partial)
  - For symbols that posify actually replaces, carry arbitrary other assumptions from assumptions0, such as integer, rational, prime, even, or odd.
- **sympy__sympy-19637** (partial)
  - It never verifies that the reported input returns 2*x/(x-1) or that any returned expression has the expected value.
- **sympy__sympy-20590** (partial)
  - Assigning an arbitrary new attribute to the affected object raises AttributeError.
- **sympy__sympy-21596** (partial)
  - The reported intersection is the exact finite set FiniteSet(-1, 1), not a larger sampled-correct set.
  - Linear zeros of factored imaginary parts are kept as candidates and intersected with the original base set, discarding roots outside Integers or Naturals0.
  - When the imaginary-part numerator cannot be solved linearly, the result is represented with a ConditionSet.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-13513** — nothing collected on either side -- the file never ran
- **django__django-14580** — nothing collected on either side -- the file never ran
- **django__django-14608** — nothing collected on either side -- the file never ran
- **django__django-14765** — nothing collected on either side -- the file never ran
- **django__django-16454** — nothing collected on either side -- the file never ran
- **django__django-16642** — nothing collected on either side -- the file never ran
