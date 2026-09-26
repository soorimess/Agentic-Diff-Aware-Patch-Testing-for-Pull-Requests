# Run status, per pull request

Last run in this table: 2026-09-26 10:50 UTC.

- **70** instances across **12** repositories
- **45/70** fail-to-pass, of those that reached a verdict
- **45** measured for changed-line coverage: **mean 86%** per test, median 100%
- **69%** of the changed lines those tests were measured against (179/259, pooled)
- **35%** of every source line all 70 patches change (179/508) -- a fixed denominator, so this is the figure that compares across arms
- \$4.50 and 62.3M tokens in total
- **22** of these were sent a second-chance message after stopping with nothing to score, and **2** of them ended fail-to-pass; the other 48 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `passes_at_base` | 21 | 2 | 19 | 0 | **added by the flag** |
| `reads_source` | 1 | 0 | 1 | 0 | from `require-tools` |

Of the **21** refused for a reason the flag itself adds, **2** ended fail-to-pass.

Every row was produced with the same configuration: **`no-require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

The three judge columns are levels from 1 (worst) to 5 (best), printed as `label (level)`:

| scale | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| concept -- same behaviour as the maintainer's test? | different | tangential | narrower | close | equivalent |
| issue -- every behaviour the pull request settles? | none | minor only | main only | nearly complete | complete |
| readable -- would it pass review? | reject | poor | acceptable | good | exemplary |

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 58 | `run` x17, `run_tests` x12, `write_file` x12, `coverage` x4, `verify` x4, `mutation` x1 | — | — | — | 2026-09-26 06:51 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 3/3 | 3/3 | 29 | `run` x14, `write_file` x4, `run_tests` x3, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | complete (5) | good (4) | 2026-09-26 06:33 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 23 | `run` x10, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:31 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 67% (4/6) | 0/4 | 4/4 | 34 | `run` x17, `verify` x4, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:34 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 47 | `run` x25, `write_file` x6, `run_tests` x5, `verify` x4, `coverage` x2, `mutation` x2 | close (4) | main only (3) | poor (2) | 2026-09-26 06:39 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 63 | `run` x28, `write_file` x15, `run_tests` x8, `coverage` x4, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-26 06:43 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 73 | `run` x26, `write_file` x18, `run_tests` x8, `verify` x6, `coverage` x5, `mutation` x4 | — | — | — | 2026-09-26 06:50 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 63 | `run` x19, `write_file` x13, `run_tests` x11, `coverage` x5, `verify` x4, `mutation` x3 | — | — | — | 2026-09-26 06:55 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 72 | `run` x23, `write_file` x20, `run_tests` x13, `coverage` x6, `verify` x4 | — | — | — | 2026-09-26 06:53 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x11, `run_tests` x4, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 06:43 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 24 | `run` x10, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:46 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 55 | `run` x23, `write_file` x11, `run_tests` x8, `coverage` x3, `verify` x3  (+1 edit reverted) | — | — | — | 2026-09-26 06:56 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 60 | `run` x22, `write_file` x13, `run_tests` x11, `mutation` x3, `verify` x3, `coverage` x1 | — | — | — | 2026-09-26 07:05 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 24 | `run` x8, `run_tests` x4, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | close (4) | complete (5) | acceptable (3) | 2026-09-26 06:53 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 75% (3/4) | no mutants | no mutants | 31 | `run` x10, `write_file` x6, `run_tests` x4, `coverage` x3, `verify` x3, `mutation` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:54 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 32 | `run` x16, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 06:56 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 59 | `run` x26, `write_file` x13, `run_tests` x7, `verify` x3, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 07:07 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 22 | `run` x8, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:00 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 50% (1/2) | no mutants | no mutants | 34 | `run` x18, `verify` x4, `coverage` x3, `write_file` x3, `run_tests` x2, `mutation` x1 | narrower (3) | main only (3) | reject (1) | 2026-09-26 07:06 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 29% (2/7) | 1/6 | 2/6 | 48 | `run` x19, `run_tests` x9, `write_file` x9, `verify` x4, `coverage` x3, `mutation` x1 | tangential (2) | minor only (2) | exemplary (5) | 2026-09-26 07:11 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 34 | `run` x17, `write_file` x5, `run_tests` x3, `verify` x3, `mutation` x2, `coverage` x1  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:08 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 37 | `run` x20, `run_tests` x4, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:10 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 33 | `run` x12, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:14 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 48 | `run` x22, `run_tests` x8, `write_file` x8, `verify` x3, `coverage` x1, `mutation` x1  (+1 edit reverted) | — | — | — | 2026-09-26 07:16 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x15, `run_tests` x3, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:13 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 50 | `run` x20, `write_file` x11, `run_tests` x10 | — | — | — | 2026-09-26 07:20 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 28 | `run` x16, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:16 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 7/9 | 7/9 | 78 | `run` x27, `write_file` x15, `run_tests` x14, `verify` x10, `coverage` x3, `mutation` x2 | tangential (2) | none (1) | poor (2) | 2026-09-26 07:35 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 61% (11/18) | 1/10 | 1/10 | 36 | `run` x15, `write_file` x6, `run_tests` x4, `verify` x4, `coverage` x3, `mutation` x2 | narrower (3) | minor only (2) | good (4) | 2026-09-26 07:25 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 19 | `run` x10, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:20 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x10, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:24 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 24 | `run` x10, `run_tests` x3, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 07:31 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 21 | `run` x13, `run_tests` x2, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 07:30 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 28 | `run` x11, `run_tests` x4, `verify` x4, `write_file` x3, `coverage` x2, `mutation` x1 | narrower (3) | nearly complete (4) | good (4) | 2026-09-26 07:38 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | NO | — | — | — | 39 | `run` x11, `run_tests` x8, `write_file` x8, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 09:20 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 52 | `run` x15, `run_tests` x11, `write_file` x11, `coverage` x3, `mutation` x2, `verify` x1 | — | — | — | 2026-09-26 09:25 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 55 | `run` x23, `write_file` x13, `run_tests` x12 | — | — | — | 2026-09-26 09:21 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 25 | `run` x7, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:10 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/1 | 0/1 | 40 | `run` x18, `coverage` x5, `verify` x5, `write_file` x5, `run_tests` x2, `mutation` x1 | equivalent (5) | nearly complete (4) | poor (2) | 2026-09-26 09:17 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | NO | — | — | — | 38 | `run` x10, `run_tests` x9, `write_file` x9, `coverage` x3, `verify` x3, `mutation` x1 | — | — | — | 2026-09-26 09:20 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 21 | `run` x7, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 09:20 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 21 | `run` x11, `run_tests` x2, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1  (+1 edit reverted) | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:15 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 33 | `run` x14, `run_tests` x5, `write_file` x5, `verify` x4, `coverage` x1, `mutation` x1  (+1 edit reverted) | — | — | — | 2026-09-26 09:18 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 20 | `coverage` x3, `mutation` x3, `run` x3, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 09:35 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 50 | `run` x19, `write_file` x10, `run_tests` x8, `mutation` x4, `verify` x2, `coverage` x1  (+1 edit reverted) | — | — | — | 2026-09-26 09:41 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 28 | `run` x12, `run_tests` x4, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:31 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 37 | `run` x14, `run_tests` x6, `write_file` x6, `coverage` x3, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 09:32 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 57 | `run` x17, `write_file` x15, `run_tests` x9, `verify` x4, `coverage` x3, `mutation` x2 | — | — | — | 2026-09-26 09:36 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 28 | `run` x10, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x1 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 09:37 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 53 | `run` x16, `run_tests` x12, `write_file` x12, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 09:52 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 32 | `run` x17, `write_file` x4, `run_tests` x3, `verify` x2, `coverage` x1, `mutation` x1 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 09:43 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 22 | `run` x11, `run_tests` x3, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:47 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 20% (2/10) | 0/10 | 6/10 | 47 | `run` x25, `write_file` x6, `run_tests` x4, `verify` x4, `coverage` x3, `mutation` x2 | tangential (2) | none (1) | reject (1) | 2026-09-26 09:51 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (27/47) | 1/10 | 4/10 | 49 | `run` x22, `write_file` x8, `verify` x5, `coverage` x4, `run_tests` x3, `mutation` x2 | tangential (2) | minor only (2) | poor (2) | 2026-09-26 10:03 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 88% (14/16) | 8/10 | 8/10 | 22 | `run` x8, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:49 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 59 | `run` x21, `write_file` x10, `run_tests` x9, `verify` x7, `coverage` x4, `mutation` x1 | — | — | — | 2026-09-26 10:03 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 86 | `run` x38, `run_tests` x19, `write_file` x17, `coverage` x3, `mutation` x1, `verify` x1 | — | — | — | 2026-09-26 10:11 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 59 | `run` x22, `write_file` x15, `run_tests` x9, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 10:08 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 53 | `run_tests` x13, `write_file` x13, `run` x12, `coverage` x3, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 10:11 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 35% (13/37) | 1/10 | 5/10 | 33 | `run` x11, `write_file` x6, `verify` x5, `coverage` x4, `run_tests` x4, `mutation` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:08 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 30 | `run` x16, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | — | — | — | 2026-09-26 10:03 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | NO | — | — | — | 86 | `run` x29, `write_file` x27, `run_tests` x24  (+1 edit reverted) | — | — | — | 2026-09-26 10:24 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 19 | `run` x9, `coverage` x2, `run_tests` x2, `verify` x2, `mutation` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:16 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 25 | `run` x9, `run_tests` x5, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | close (4) | nearly complete (4) | good (4) | 2026-09-26 10:43 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 28 | `run` x10, `verify` x4, `write_file` x4, `coverage` x3, `run_tests` x3, `mutation` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:26 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | YES | 100% (2/2) | 1/2 | 1/2 | 24 | `run` x8, `run_tests` x4, `write_file` x4, `coverage` x2, `verify` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:26 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 25 | `run` x12, `run_tests` x3, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:48 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 36 | `run` x20, `coverage` x3, `run_tests` x3, `write_file` x3, `mutation` x2, `verify` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 10:47 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 25 | `run` x12, `write_file` x3, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 10:43 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 41 | `run` x16, `write_file` x8, `run_tests` x5, `verify` x5, `coverage` x2, `mutation` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:50 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14598** (nearly complete (4))
  - A long value with `''` followed by a space and more text round-trips unchanged.
- **astropy__astropy-7606** (main only (3))
  - Ordinary UnitBase equality with invalid operands such as None declines with NotImplemented instead of raising.
  - UnrecognizedUnit equality requires an operand compatible with type(self) as well as the same name.
- **django__django-10914** (main only (3))
  - A default ordinary or in-memory upload using the MemoryUploadedFile/content path is stored with mode 0o644.
- **django__django-13012** (main only (3))
  - A wrapped non-constant expression preserves the wrapped expression's group-by columns.
- **django__django-13023** (main only (3))
  - ValueError-causing invalid inputs, such as an empty tuple, are converted into ValidationError.
- **django__django-13794** (main only (3))
  - The add filter concatenates a lazy string on the left with another lazy string.
  - Lazy proxy addition works for two lazy integer operands.
- **django__django-14534** (nearly complete (4))
  - When no id is available, id_for_label returns None instead of generating an ID.
- **django__django-14608** (main only (3))
  - A ValidationError raised by the formset's clean() method is wrapped in an ErrorList with the nonform CSS class.
- **django__django-14725** (minor only (2))
  - An edit-only model formset updates existing objects without saving changed extra forms.
  - An edit-only inline formset updates existing child objects without saving changed extra forms.
  - An edit-only model formset does not create an object from a submitted ID outside its queryset.
- **django__django-14792** (main only (3))
  - The datetime.timezone cases.
  - The fixed-offset zoneinfo case.
  - The named zoneinfo case.
- **django__django-14915** (main only (3))
  - A wrapper hashes like its underlying raw value so it can interoperate with dictionaries keyed by that raw value.
  - Wrappers with different underlying values produce different hashes for the distinct primary keys used by the fix.
- **django__django-16454** (none (1))
  - Default CommandParser subparsers must produce formatted errors for invalid arguments rather than a traceback.
  - Explicit vanilla argparse subparsers must retain their normal formatted invalid-argument errors.
- **django__django-16560** (minor only (2))
  - PostgreSQL ExclusionConstraint accepts and stores a custom violation_error_code.
  - Constraint equality distinguishes different violation_error_code values and accepts equal values.
  - CheckConstraint and ExclusionConstraint repr output includes a configured violation_error_code.
- **django__django-16667** (main only (3))
  - Submitting an oversized date through a form produces a normal invalid-form result with "Enter a valid date." instead of crashing.
- **matplotlib__matplotlib-20859** (none (1))
  - A SubFigure is accepted as a legend parent and the resulting legend is attached to that SubFigure.
  - A regular Figure remains accepted as a legend parent.
  - An Axes remains accepted as a legend parent.
- **matplotlib__matplotlib-24870** (nearly complete (4))
  - Triangular contour with boolean data and no explicit levels defaults to [0.5].
  - Filled triangular contour with boolean data and no explicit levels defaults to [0, 0.5, 1].
- **psf__requests-2931** (nearly complete (4))
  - String or bytes supplied as URL params are converted to native text before query-string encoding.
- **pydata__xarray-4075** (main only (3))
  - weighted variance with boolean weights uses the numeric sum of weights for normalization.
  - weighted standard deviation with boolean weights uses the numeric sum of weights for normalization.
- **pydata__xarray-6744** (main only (3))
  - center=True iteration for sizes other than 3, including even-size and other edge-position cases.
  - center=False manual iteration and its trailing/right-aligned windows.
- **scikit-learn__scikit-learn-10297** (minor only (2))
  - The true flag's documented output shape for one-dimensional labels is not asserted; the test only asserts that cv_values_ is not None.
  - The true flag's multi-target behaviour and its documented output shape are not tested.
  - Acceptance and forwarding of store_cv_values=True are only exercised by avoiding an exception, with no assertion directly pinning that API behaviour.
- **scikit-learn__scikit-learn-14087** (minor only (2))
  - refit=False uses the resolved multi_class value when aggregating coefficient paths, so the auto multi-class path does not take the wrong indexing branch
- **scikit-learn__scikit-learn-9288** (main only (3))
  - Exact equality of the cluster assignments in labels_ between single-threaded and parallel runs.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python domain parser renders `Tuple[()]` as the expected doctree with `(` and `)` nodes.
  - The AST string unparser renders an empty tuple as `"()"`.
- **sphinx-doc__sphinx-7590** (minor only (2))
  - The C-domain parser uses the corrected integer and floating-point literal suffix parsing.
  - Integer literals followed by user-defined suffixes produce the correct user-defined-literal AST and mangling.
  - Decimal floating-point literals followed by user-defined suffixes produce the correct AST and mangling.
- **sympy__sympy-12489** (main only (3))
  - The empty, Cycle, multiple-argument, integer, and resizing or reuse constructor branches retain the requested subclass.
  - Addition results retain the dynamic subclass type.
  - rmul_with_af results retain the dynamic subclass type.
- **sympy__sympy-16450** (nearly complete (4))
  - The complete inferred assumptions0 set is preserved, not merely selected individual properties.
- **sympy__sympy-17318** (main only (3))
  - The denestable expression from the report continues to simplify to I.
- **sympy__sympy-19637** (none (1))
  - A parenthesized input without spaces is parsed successfully as 2*x/(x-1) instead of raising UnboundLocalError.
- **sympy__sympy-21596** (main only (3))
  - Roots of the reality condition are filtered by the parameter domain, including noninteger roots over Integers and extra roots over Naturals0.
  - When the imaginary-part equation cannot be solved linearly, the result is represented with a ConditionSet rather than an incorrect finite subtraction.
  - Zeros of denominators are removed from candidate parameters, including denominator cases that leave a finite result or EmptySet.
