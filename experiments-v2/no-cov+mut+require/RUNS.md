# Run status, per pull request

Last run in this table: 2026-09-26 10:49 UTC.

- **70** instances across **12** repositories
- **44/70** fail-to-pass, of those that reached a verdict
- **44** measured for changed-line coverage: **mean 83%** per test, median 100%
- **65%** of the changed lines those tests were measured against (150/232, pooled)
- **30%** of every source line all 70 patches change (150/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.18 and 43.9M tokens in total
- **18** of these were sent a second-chance message after stopping with nothing to score, and **0** of them ended fail-to-pass; the other 52 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `passes_at_base` | 18 | 0 | 18 | 0 | **added by the flag** |

Of the **18** refused for a reason the flag itself adds, **0** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool+mutation-tool+require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 26 | `run` x9, `write_file` x6, `run_tests` x5, `verify` x2 | — | — | — | 2026-09-26 06:40 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 4/7 | 7/7 | 26 | `run` x13, `write_file` x5, `run_tests` x3, `verify` x3 | tangential (2) | none (1) | poor (2) | 2026-09-26 06:34 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 13 | `run` x7, `run_tests` x2, `verify` x1, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:23 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 67% (4/6) | 0/9 | 9/9 | 24 | `run` x14, `run_tests` x3, `verify` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:28 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 38 | `run` x25, `write_file` x6, `verify` x3, `run_tests` x1 | narrower (3) | complete (5) | poor (2) | 2026-09-26 06:32 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 64 | `run` x25, `write_file` x21, `run_tests` x7, `verify` x4 | — | — | — | 2026-09-26 06:42 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 56 | `run` x22, `write_file` x14, `run_tests` x11, `verify` x2 | — | — | — | 2026-09-26 06:43 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 60% (3/5) | 0/6 | 4/6 | 36 | `run` x18, `run_tests` x6, `write_file` x6, `verify` x3  (+1 edit reverted) | narrower (3) | none (1) | poor (2) | 2026-09-26 06:42 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 57 | `run` x28, `write_file` x15, `run_tests` x5, `verify` x3 | — | — | — | 2026-09-26 06:49 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 28 | `run` x15, `write_file` x5, `run_tests` x4, `verify` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:44 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 18 | `run` x8, `verify` x3, `write_file` x3, `run_tests` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:44 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 52 | `run` x25, `write_file` x10, `run_tests` x9, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-26 06:54 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 50 | `run` x20, `write_file` x11, `run_tests` x10, `verify` x3 | — | — | — | 2026-09-26 06:58 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 80% (4/5) | 9/10 | 9/10 | 22 | `run` x7, `run_tests` x5, `write_file` x5, `verify` x3 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 06:53 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 75% (3/4) | no mutants | no mutants | 29 | `run` x19, `run_tests` x3, `write_file` x3, `verify` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:53 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 20 | `run` x14, `verify` x2, `run_tests` x1, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:55 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 57 | `run` x39, `write_file` x9, `run_tests` x4, `verify` x1 | — | — | — | 2026-09-26 07:03 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 30 | `run` x17, `verify` x4, `write_file` x4, `run_tests` x3 | close (4) | complete (5) | acceptable (3) | 2026-09-26 07:02 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 25 | `run` x13, `write_file` x4, `run_tests` x3, `verify` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 07:02 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 29% (2/7) | 0/10 | 4/10 | 54 | `run` x32, `write_file` x10, `run_tests` x6, `verify` x2 | tangential (2) | minor only (2) | reject (1) | 2026-09-26 07:11 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 2/3 | 1/3 | 14 | `run` x7, `verify` x2, `write_file` x2, `run_tests` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:02 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 69 | `write_file` x21, `run` x20, `run_tests` x19, `verify` x3 | — | — | — | 2026-09-26 07:17 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 0/1 | 1/1 | 29 | `run` x21, `run_tests` x2, `verify` x2, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 07:10 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 54 | `run_tests` x14, `write_file` x14, `run` x13, `verify` x5 | — | — | — | 2026-09-26 07:17 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 32 | `run` x23, `run_tests` x3, `write_file` x2, `verify` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:13 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 32 | `run` x18, `write_file` x5, `run_tests` x4, `verify` x2 | — | — | — | 2026-09-26 07:14 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 2/2 | 2/2 | 20 | `run` x13, `run_tests` x2, `verify` x1, `write_file` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:14 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 49 | `run` x26, `write_file` x8, `run_tests` x5, `verify` x5 | — | — | — | 2026-09-26 07:26 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 24 | `run` x12, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | 2026-09-26 07:19 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 15 | `run` x7, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:20 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 25 | `run` x13, `write_file` x4, `run_tests` x3, `verify` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:23 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 75% (3/4) | 6/10 | 10/10 | 21 | `run` x9, `run_tests` x6, `write_file` x2, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:29 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 28 | `run` x16, `run_tests` x4, `write_file` x4, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:31 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 18 | `run` x8, `verify` x3, `run_tests` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:34 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 1/10 | 1/10 | 26 | `run` x9, `run_tests` x5, `write_file` x5, `verify` x4 | tangential (2) | main only (3) | acceptable (3) | 2026-09-26 07:38 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 53 | `run` x17, `write_file` x13, `run_tests` x10, `verify` x5 | — | — | — | 2026-09-26 09:17 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 61 | `run` x22, `write_file` x13, `run_tests` x12, `verify` x6 | — | — | — | 2026-09-26 09:19 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 23 | `run` x14, `run_tests` x3, `write_file` x2, `verify` x1 | equivalent (5) | complete (5) | exemplary (5) | 2026-09-26 07:38 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/2 | 0/2 | 23 | `run` x14, `run_tests` x4, `verify` x1, `write_file` x1 | narrower (3) | nearly complete (4) | poor (2) | 2026-09-26 07:38 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 28 | `run` x16, `write_file` x4, `run_tests` x3, `verify` x2 | equivalent (5) | nearly complete (4) | acceptable (3) | 2026-09-26 09:12 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 18 | `run` x10, `write_file` x3, `run_tests` x2, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:15 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 16 | `run` x10, `write_file` x2, `run_tests` x1  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:06 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 39 | `run` x14, `run_tests` x10, `write_file` x9, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-26 09:23 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 18 | `run` x6, `run_tests` x4, `write_file` x3, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:29 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 37 | `run` x15, `write_file` x8, `run_tests` x5, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-26 09:36 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 7/7 | 7/7 | 19 | `run` x7, `run_tests` x4, `write_file` x3, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:28 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 31 | `run` x22, `write_file` x3, `run_tests` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:28 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 58 | `run` x22, `write_file` x16, `run_tests` x8, `verify` x4 | — | — | — | 2026-09-26 09:34 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 44 | `run` x31, `run_tests` x4, `write_file` x4, `verify` x2  (+1 edit reverted) | — | — | — | 2026-09-26 09:36 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 44 | `run` x13, `write_file` x11, `run_tests` x10, `verify` x3 | — | — | — | 2026-09-26 09:49 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 4/10 | 4/10 | 32 | `run` x19, `write_file` x4, `run_tests` x3, `verify` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:44 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 16 | `run` x9, `run_tests` x2, `write_file` x2, `verify` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:41 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 20% (2/10) | 1/10 | 6/10 | 27 | `run` x14, `run_tests` x4, `write_file` x4, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:44 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (27/47) | 1/10 | 4/10 | 46 | `run` x34, `run_tests` x5, `write_file` x4, `verify` x1 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:52 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 27 | `run` x16, `run_tests` x4, `write_file` x3, `verify` x1  (+1 edit reverted) | — | — | — | 2026-09-26 09:47 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 60 | `run` x22, `run_tests` x10, `write_file` x10, `verify` x9 | — | — | — | 2026-09-26 10:02 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 57 | `run` x37, `write_file` x14 | — | — | — | 2026-09-26 10:00 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 60 | `run` x24, `write_file` x16, `run_tests` x10, `verify` x3 | — | — | — | 2026-09-26 10:07 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 44 | `run` x19, `run_tests` x8, `write_file` x8, `verify` x2 | — | — | — | 2026-09-26 10:03 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 38% (14/37) | 2/10 | 6/10 | 35 | `run` x11, `write_file` x8, `verify` x7, `run_tests` x6 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:06 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 22 | `run` x7, `write_file` x6, `run_tests` x4, `verify` x2 | — | — | — | 2026-09-26 10:02 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 10/10 | 10/10 | 48 | `run_tests` x14, `run` x13, `write_file` x13, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 10:24 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 25 | `run` x12, `run_tests` x4, `write_file` x4, `verify` x3 | narrower (3) | complete (5) | good (4) | 2026-09-26 10:16 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 33 | `run` x22, `write_file` x5, `run_tests` x2, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:49 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 23 | `run` x16, `run_tests` x2, `verify` x2, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:20 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 47 | `run` x18, `write_file` x10, `run_tests` x9, `verify` x2 | — | — | — | 2026-09-26 10:24 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 17 | `run` x8, `run_tests` x3, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:48 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 21 | `run` x12, `run_tests` x2, `verify` x2, `write_file` x2 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 10:38 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 26 | `run` x13, `run_tests` x5, `write_file` x3, `verify` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 10:39 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 22 | `run` x6, `verify` x5, `write_file` x5, `run_tests` x4 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:43 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (none (1))
  - Identical Q-format VLA data is not reported as different.
  - Unequal Q-format VLA data is compared element-wise and reported with the correct differing values and aggregate statistics.
- **astropy__astropy-14598** (nearly complete (4))
  - A long value containing `''` before a space and then ordinary characters round-trips unchanged.
- **astropy__astropy-7606** (main only (3))
  - UnitBase equality returning NotImplemented for invalid operands.
  - Matching-name UnrecognizedUnit equality.
  - Inequality between an UnrecognizedUnit and an ordinary unit such as u.m.
- **django__django-12308** (none (1))
  - Truthful dictionary values are displayed as valid JSON.
  - Truthful list values are displayed as valid JSON.
  - Truthful string values are displayed as valid JSON.
- **django__django-13012** (main only (3))
  - An ExpressionWrapper around a non-constant expression delegates get_group_by_cols() and preserves the wrapped expression as a group-by column.
- **django__django-13023** (main only (3))
  - ValueError-producing invalid values, such as the empty tuple case.
  - The broader set of invalid values exercised by the fix, beyond the single dictionary representative.
- **django__django-13794** (main only (3))
  - The add filter concatenates a lazy string on the left with an ordinary string on the right.
  - The add filter concatenates a lazy string on the left with another lazy string on the right.
  - Lazy integer values support addition and produce 9.
- **django__django-14534** (nearly complete (4))
  - When no ID is present in the subwidget attrs, BoundWidget.id_for_label returns None.
- **django__django-14608** (main only (3))
  - The initially created non-form ErrorList uses the nonform CSS class for built-in too-many-forms and too-few-forms validation errors.
- **django__django-14725** (minor only (2))
  - the returned model formset actually suppresses creation while updating existing objects
  - the returned inline formset actually suppresses creation while updating existing objects
  - an edit-only model formset does not create an object submitted outside its queryset
- **django__django-14915** (nearly complete (4))
  - Wrappers with different primary-key values have different hashes in the tested cases.
- **django__django-16139** (main only (3))
  - Resolution of the link from a UserAdmin change URL reached through a non-PK to_field.
  - Resolution of the new relative link from a normal primary-key-addressed UserAdmin change URL.
- **django__django-16667** (main only (3))
  - A form using the widget treats that fallback as an invalid date and reports "Enter a valid date." instead of crashing.
- **matplotlib__matplotlib-20676** (main only (3))
  - Interactive vertical construction preserves the y-axis bounds through the symmetric branch.
  - Construction preserves the orthogonal axis bounds for the vertical direction.
  - Initial edge handles use the corresponding axis bounds as their positions.
- **matplotlib__matplotlib-20859** (main only (3))
  - The created Legend is associated with the SubFigure as its figure.
  - An unsupported Legend parent raises TypeError with the updated FigureBase wording.
- **matplotlib__matplotlib-24870** (main only (3))
  - The Python-list and masked-array variants of the regular contour and contourf defaults.
  - The tricontour() default of [0.5] for boolean z.
  - The tricontourf() default of [0, 0.5, 1] for boolean z.
- **matplotlib__matplotlib-24970** (main only (3))
  - Correct returned colormap values for unsigned-integer inputs.
  - Correct floating-point conversion and returned colormap values.
- **psf__requests-2931** (nearly complete (4))
  - String or bytes supplied as `params` to `prepare_url` are converted to a native string before query encoding.
- **pydata__xarray-2905** (nearly complete (4))
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their values arrays.
- **pydata__xarray-4075** (main only (3))
  - sum_of_weights() converts boolean weights to integers and returns their numeric count
- **pydata__xarray-6744** (main only (3))
  - center=True alignment for the other parameterized window sizes, including even size 2 and sizes 1 and 7.
  - center=False manual iteration retains the expected trailing-window alignment.
- **pytest-dev__pytest-6197** (main only (3))
  - Pytest must not add src to sys.path as a side effect of collection.
- **scikit-learn__scikit-learn-14087** (none (1))
  - The resolved OVR coefficient-path branch, including binary multi_class='auto', works with refit=False.
  - The resolved multinomial coefficient-path branch works with refit=False.
  - Non-elasticnet penalties avoid indexing l1_ratios_ and record None in l1_ratio_.
- **sphinx-doc__sphinx-7462** (main only (3))
  - The exact `Tuple[()]` punctuation-node structure produced by the Python domain.
  - `sphinx.pycode.ast.unparse` returning `()` for an empty tuple AST.
- **sphinx-doc__sphinx-7590** (none (1))
  - Integer literals with user-defined suffixes are parsed as user-defined literals with the correct mangled identity.
  - Decimal floating-point literals with user-defined suffixes, including 6.62607015e-34q_J, are parsed with the correct mangled identity.
  - Hexadecimal floating-point literals with user-defined suffixes are parsed with the correct mangled identity.
- **sympy__sympy-12489** (main only (3))
  - A subclass constructed with no arguments gets an identity instance of that subclass.
  - A subclass constructed from multiple positional cycle arguments gets an instance of that subclass.
  - A subclass constructed from an integer gets an instance of that subclass.
- **sympy__sympy-14976** (main only (3))
  - The exact wrapping of both the numerator and denominator as mpmath.mpf values.
  - The arbitrary-precision nsolve result for an expression involving a Rational.
- **sympy__sympy-16450** (main only (3))
  - Preservation of other explicit assumptions on a newly created replacement; the multiple-assumptions test sets positive=True, so posify does not replace the symbol.
- **sympy__sympy-19637** (none (1))
  - `kernS` parses an expression without spaces and returns `2*x/(x-1)` instead of raising `UnboundLocalError`.
  - `kernS` continues to parse an expression containing spaces correctly through the existing spaces branch.
- **sympy__sympy-20590** (main only (3))
  - Slotted SymPy instances reject assignment of arbitrary new attributes.
- **sympy__sympy-21596** (main only (3))
  - The reported intersection retains exactly the real image values `-1` and `1`.
  - The integer image with imaginary part `(n - 1)*(n + 1/2)` intersects Reals at `1`.
  - The corresponding Naturals0 image with an additional `(n + 1)` factor intersects Reals at `1`.
