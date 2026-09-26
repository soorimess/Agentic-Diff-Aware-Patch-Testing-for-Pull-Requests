# Run status, per pull request

Last run in this table: 2026-09-26 10:49 UTC.

- **70** instances across **12** repositories
- **54/70** fail-to-pass, of those that reached a verdict
- **54** measured for changed-line coverage: **mean 87%** per test, median 100%
- **71%** of the changed lines those tests were measured against (216/304, pooled)
- **43%** of every source line all 70 patches change (216/508) -- a fixed denominator, so this is the figure that compares across arms
- \$3.14 and 43.3M tokens in total
- **20** of these were sent a second-chance message after stopping with nothing to score, and **4** of them ended fail-to-pass; the other 50 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `loop_open` | 5 | 4 | 1 | 0 | from `require-tools` |
| `no_test` | 1 | 0 | 1 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 14 | 0 | 14 | 0 | **added by the flag** |

Of the **14** refused for a reason the flag itself adds, **0** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool+mutation-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 14 | `run_tests` x4, `run` x3, `write_file` x3, `verify` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 06:29 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 4/7 | 7/7 | 29 | `run` x16, `write_file` x5, `run_tests` x3, `verify` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:31 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 17 | `run` x10, `run_tests` x2, `verify` x2, `write_file` x1 | close (4) | nearly complete (4) | good (4) | 2026-09-26 06:28 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 0/9 | 9/9 | 16 | `run` x11, `run_tests` x1, `verify` x1, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:24 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 46 | `run` x29, `write_file` x7, `verify` x6, `run_tests` x1 | narrower (3) | complete (5) | good (4) | 2026-09-26 06:36 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 68 | `run` x30, `write_file` x17, `run_tests` x11, `verify` x4 | — | — | — | 2026-09-26 06:42 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 72 | `run` x35, `write_file` x22, `run_tests` x5, `verify` x3 | — | — | — | 2026-09-26 06:44 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 60% (3/5) | 0/6 | 4/6 | 30 | `run` x16, `run_tests` x5, `write_file` x5, `verify` x2 | tangential (2) | none (1) | acceptable (3) | 2026-09-26 06:37 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 61 | `run` x21, `write_file` x18, `run_tests` x9, `verify` x4 | — | — | — | 2026-09-26 06:50 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 59 | `run` x35, `write_file` x9, `run_tests` x6, `verify` x5 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:49 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 32 | `run` x17, `run_tests` x7, `write_file` x4, `verify` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:46 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/10 | 8/10 | 35 | `run` x15, `run_tests` x7, `write_file` x7, `verify` x3 | tangential (2) | none (1) | reject (1) | 2026-09-26 06:52 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 55 | `write_file` x19, `run` x17, `run_tests` x9, `verify` x3 | — | — | — | 2026-09-26 06:59 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 10/10 | 9/10 | 18 | `run` x8, `verify` x3, `write_file` x3, `run_tests` x2 | narrower (3) | complete (5) | poor (2) | 2026-09-26 06:51 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 23 | `run` x18, `run_tests` x1, `verify` x1, `write_file` x1 | close (4) | main only (3) | good (4) | 2026-09-26 06:51 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x15, `run_tests` x4, `write_file` x4, `verify` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:55 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 57 | `run` x23, `write_file` x16, `verify` x8, `run_tests` x4 | — | — | — | 2026-09-26 07:03 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 23 | `run` x10, `run_tests` x4, `write_file` x4, `verify` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:00 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 34 | `run` x22, `run_tests` x5, `write_file` x4, `verify` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:02 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 43% (3/7) | 2/10 | 4/10 | 32 | `run` x17, `write_file` x5, `verify` x4, `run_tests` x3 | tangential (2) | minor only (2) | acceptable (3) | 2026-09-26 07:06 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 26 | `run` x13, `run_tests` x4, `write_file` x4, `verify` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:05 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 1/2 | 2/2 | 29 | `run` x18, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 07:08 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 1/1 | 1/1 | 35 | `run` x21, `write_file` x5, `run_tests` x4, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:12 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 55 | `run` x21, `run_tests` x13, `write_file` x13 | — | — | — | 2026-09-26 07:16 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | NO | — | — | — | 50 | `run` x20, `write_file` x13, `run_tests` x7, `verify` x2 | — | — | — | 2026-09-26 07:17 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | YES | 100% (6/6) | 2/2 | 2/2 | 39 | `run` x15, `run_tests` x8, `write_file` x7, `verify` x5 | close (4) | complete (5) | acceptable (3) | 2026-09-26 07:16 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 2/2 | 2/2 | 29 | `run` x19, `run_tests` x3, `write_file` x2, `verify` x1 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 07:15 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 9/10 | 9/10 | 25 | `run` x11, `run_tests` x4, `write_file` x4, `verify` x3 | tangential (2) | minor only (2) | acceptable (3) | 2026-09-26 07:20 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 44% (8/18) | 0/10 | 0/10 | 25 | `run` x10, `run_tests` x5, `write_file` x5, `verify` x2 | narrower (3) | minor only (2) | good (4) | 2026-09-26 07:21 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 21 | `run` x13, `run_tests` x3, `write_file` x2, `verify` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:20 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 21 | `run` x12, `write_file` x3, `run_tests` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:22 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 7/10 | 10/10 | 32 | `run` x17, `write_file` x6, `run_tests` x3, `verify` x3 | narrower (3) | complete (5) | good (4) | 2026-09-26 07:32 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 44 | `run` x24, `write_file` x8, `run_tests` x5, `verify` x3 | close (4) | main only (3) | acceptable (3) | 2026-09-26 07:33 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 25 | `run` x16, `verify` x3, `run_tests` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:35 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 1/10 | 20 | `run` x9, `run_tests` x3, `write_file` x3, `verify` x2 | tangential (2) | main only (3) | poor (2) | 2026-09-26 07:35 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | YES | 100% (7/7) | 9/10 | 7/10 | 21 | `run` x10, `run_tests` x4, `write_file` x3, `verify` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:15 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 68 | `run` x25, `write_file` x15, `run_tests` x13, `verify` x8 | — | — | — | 2026-09-26 09:23 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 20 | `run` x11, `write_file` x3, `run_tests` x2, `verify` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:38 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/2 | 0/2 | 23 | `run` x13, `run_tests` x3, `verify` x2, `write_file` x2 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 07:37 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 36 | `run` x17, `run_tests` x7, `write_file` x7, `verify` x1 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 09:17 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 14 | `run` x4, `run_tests` x4, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:15 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 27 | `run` x18, `run_tests` x3, `verify` x2, `write_file` x2  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:11 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 55 | `write_file` x15, `run_tests` x13, `run` x10, `verify` x7 | — | — | — | 2026-09-26 09:29 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 16 | `run` x7, `run_tests` x3, `write_file` x3, `verify` x1 | narrower (3) | nearly complete (4) | good (4) | 2026-09-26 09:30 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 35 | `run` x19, `run_tests` x6, `write_file` x4, `verify` x3 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:30 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 7/7 | 7/7 | 24 | `run` x13, `run_tests` x4, `write_file` x3, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:30 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 64 | `run` x24, `write_file` x22, `verify` x6, `run_tests` x5 | — | — | — | 2026-09-26 09:38 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 44 | `run` x17, `write_file` x13, `run_tests` x8 | — | — | — | 2026-09-26 09:32 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 5/10 | 5/10 | 23 | `run` x11, `write_file` x4, `run_tests` x3, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:34 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | YES | 100% (2/2) | 0/2 | 0/2 | 26 | `run` x8, `run_tests` x6, `write_file` x6, `verify` x4 | tangential (2) | main only (3) | poor (2) | 2026-09-26 09:41 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 4/10 | 4/10 | 21 | `run` x12, `run_tests` x2, `verify` x2, `write_file` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:40 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 7/9 | 9/9 | 23 | `run` x11, `write_file` x4, `run_tests` x3, `verify` x3 | close (4) | complete (5) | acceptable (3) | 2026-09-26 09:47 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 3/10 | 6/10 | 32 | `run` x17, `run_tests` x5, `write_file` x4, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:44 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (27/47) | 1/10 | 4/10 | 30 | `run` x15, `run_tests` x5, `write_file` x4, `verify` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:52 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 15 | `run` x6, `run_tests` x4, `write_file` x2, `verify` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:46 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 54 | `run` x17, `run_tests` x13, `write_file` x13, `verify` x5 | — | — | — | 2026-09-26 10:01 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 49 | `run` x17, `write_file` x12, `run_tests` x10, `verify` x4 | — | — | — | 2026-09-26 10:01 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 55 | `run` x17, `run_tests` x12, `write_file` x12, `verify` x7 | — | — | — | 2026-09-26 10:07 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | YES | 100% (3/3) | 3/8 | 6/8 | 34 | `run` x9, `run_tests` x9, `write_file` x8, `verify` x4 | tangential (2) | none (1) | poor (2) | 2026-09-26 10:03 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 38% (14/37) | 2/10 | 6/10 | 21 | `run` x13, `run_tests` x2, `verify` x2, `write_file` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:00 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 49 | `run` x19, `run_tests` x11, `write_file` x9, `verify` x3 | — | — | — | 2026-09-26 10:09 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 6/10 | 10/10 | 35 | `run` x16, `write_file` x7, `run_tests` x6, `verify` x3 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 10:17 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 21 | `run` x13, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:15 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 21 | `run` x10, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:49 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 24 | `run` x10, `write_file` x5, `run_tests` x4, `verify` x3 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 10:21 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 54 | `run` x23, `run_tests` x10, `write_file` x10, `verify` x4 | — | — | — | 2026-09-26 10:26 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 18 | `run` x11, `run_tests` x2, `verify` x2, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:47 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 21 | `run` x8, `verify` x4, `write_file` x4, `run_tests` x2 | tangential (2) | none (1) | reject (1) | 2026-09-26 10:41 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 27 | `run` x14, `run_tests` x4, `write_file` x4, `verify` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:40 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 31 | `run` x13, `run_tests` x6, `write_file` x6, `verify` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:42 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (none (1))
  - Repeated division in a CDS unit is associated left-to-right, as in km/s/Mpc.
  - 10+3J/m/s/kpc2 is parsed as 1000 J/(m s kpc2), with all three units in the denominator.
  - 10-7J/s/kpc2 is parsed as 1e-7 J/(s kpc2), with kpc2 remaining in the denominator.
- **astropy__astropy-14539** (main only (3))
  - Files with differing Q-format variable-length column values report the differing rows and correct difference details.
- **astropy__astropy-14598** (nearly complete (4))
  - A value with doubled single quotes followed by a space and further text round-trips with both quotes preserved.
- **astropy__astropy-7606** (nearly complete (4))
  - The concrete-type/name guard in UnrecognizedUnit.__eq__ is not asserted for a valid unit-like operand.
- **django__django-12308** (none (1))
  - Truthy JSONField values that can be prepared are displayed as exact valid JSON.
  - Truthy values that cannot be JSON-prepared fall back to the ordinary display representation instead of raising an error.
- **django__django-13012** (main only (3))
  - An ExpressionWrapper around an expression with non-empty group-by columns preserves and returns those wrapped expression columns.
- **django__django-13023** (main only (3))
  - Other unsupported values such as lists, sets, arbitrary objects, and complex values that cause TypeError.
  - Malformed tuple values that cause Decimal conversion to raise ValueError.
  - Non-numeric strings and byte strings that cause Decimal conversion to raise decimal.InvalidOperation.
- **django__django-13449** (none (1))
  - SQLite Window expressions with a DecimalField, including Lag, are cast in the correct place so the query executes and returns correct values.
  - SQLite Window expressions without a DecimalField continue through the ordinary Window SQL path without the Decimal-specific casting.
- **django__django-13794** (main only (3))
  - The add filter concatenates two lazy strings.
  - Lazy proxies whose values are integers support addition.
- **django__django-14534** (nearly complete (4))
  - When no ID is configured, such as with auto_id=False, id_for_label returns None.
- **django__django-14608** (main only (3))
  - Management-form validation errors retain `nonform` on the initially created list; the management-form test's `clean()` method raises afterward and overwrites that list.
  - Too-many-form validation errors render with `nonform`.
  - Too-few-form validation errors render with `nonform`.
- **django__django-14725** (minor only (2))
  - inlineformset_factory accepts and propagates edit_only=True.
  - An edit-only model formset still saves changes to existing objects.
  - An edit-only model formset does not save submitted new or extra forms.
- **django__django-14792** (main only (3))
  - An unnamed fixed-offset `datetime.timezone` returns its generated offset name, such as `UTC+10:00`.
  - A named fixed-offset `datetime.timezone` preserves its explicit name, such as `Etc/GMT-10`.
  - A named pytz timezone falls back to its timezone name, such as `Europe/Madrid`.
- **django__django-14915** (main only (3))
  - Objects with the same underlying value have the same hash when their associated instances differ.
  - Objects with different underlying values have different hashes in the tested cases.
- **django__django-16454** (minor only (2))
  - A nested invalid argument in a command-line management command is rendered as a two-line human-facing error rather than a traceback.
  - An explicit non-CommandParser class such as argparse.ArgumentParser remains supported and retains its normal argparse error formatting.
- **django__django-16560** (minor only (2))
  - ExclusionConstraint accepts and forwards a supplied violation_error_code.
  - BaseConstraint deconstruction includes a non-None violation_error_code.
  - Constraint equality distinguishes constraints with different violation_error_code values.
- **django__django-16667** (main only (3))
  - A form using SelectDateWidget handles overflowing submitted input as a normal validation failure and reports "Enter a valid date.".
- **matplotlib__matplotlib-20859** (main only (3))
  - A legend created for a SubFigure is associated with that SubFigure as its figure.
  - An unsupported parent still raises TypeError with the updated FigureBase wording.
- **matplotlib__matplotlib-24870** (main only (3))
  - Regular contour on Python-list and masked boolean inputs.
  - Filled contourf on Python-list and masked boolean inputs.
  - Both triangulated tricontour and tricontourf paths.
- **matplotlib__matplotlib-24970** (main only (3))
  - Unsigned integer inputs produce the correct colormap result after being converted to a signed integer index type.
  - Floating-point inputs retain correct scaling, clipping, and integer conversion for ordinary and out-of-range values.
- **matplotlib__matplotlib-25960** (main only (3))
  - The horizontal wspace branch produces the requested horizontal gaps and widths for every column.
  - The vertical hspace branch produces the requested vertical gaps and heights for every row.
  - Omitted wspace and hspace produce actual zero, tightly packed spacing rather than merely matching another potentially incorrect layout.
- **psf__requests-2931** (nearly complete (4))
  - String or bytes URL parameters are converted to a native string before URL parameter encoding.
- **pydata__xarray-2905** (nearly complete (4))
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their .values arrays.
- **pydata__xarray-6744** (nearly complete (4))
  - The size-specific behavior for window sizes 1, 2, and 7, including centered even-size boundary placement
- **pylint-dev__pylint-4970** (none (1))
  - Setting `min-similarity-lines` to zero disables duplicate-code checking, yielding a successful run with no duplicate-code output.
- **scikit-learn__scikit-learn-10297** (main only (3))
  - The documented cv_values_ shape for one-dimensional labels.
  - The documented cv_values_ shape for two-dimensional labels.
- **scikit-learn__scikit-learn-13124** (main only (3))
  - The changed fold outputs have different per-class sample membership rather than only a different fold order.
- **scikit-learn__scikit-learn-14087** (none (1))
  - Use the resolved multi_class value to select the correct OVR coefficient-path indexing for refit=False.
  - Use the resolved multi_class value to select the correct multinomial coefficient-path indexing for refit=False.
  - Avoid indexing l1_ratios_ for non-elasticnet penalties and set l1_ratio_ to None.
- **sphinx-doc__sphinx-7462** (main only (3))
  - The AST unparser returns the string `()` for an empty tuple.
- **sphinx-doc__sphinx-7590** (main only (3))
  - Hexadecimal floating-point user-defined literal suffixes.
  - Character literal user-defined suffixes.
  - The expected AST mangling containing the literal and suffix identifier.
- **sphinx-doc__sphinx-9658** (none (1))
  - `restify` renders a mocked class as `:py:class:\`unknown.secret.Class\``.
  - `stringify` returns `unknown.secret.Class` for a mocked class.
- **sympy__sympy-12489** (main only (3))
  - Construction through an explicit Cycle object, with no arguments, or with multiple cycle arguments.
  - Passing a base Permutation to a subclass constructor, including size adjustment, produces the subclass.
  - __add__, rmul_with_af, mul_inv, __rmul__, __mul__, __pow__, __xor__, __invert__, and next_lex preserve subclass results.
- **sympy__sympy-14976** (none (1))
  - MpmathPrinter must emit both the numerator and denominator of a Rational as `mpmath.mpf` values.
  - The mpmath lambdify/nsolve path must preserve arbitrary precision for rational constants.
- **sympy__sympy-16450** (main only (3))
  - Other explicit assumptions such as integer, rational, prime, even, and odd are carried into the positive replacement.
- **sympy__sympy-19637** (none (1))
  - kernS("(2*x)/(x-1)") returns the correctly parsed expression 2*x/(x-1) instead of failing with UnboundLocalError.
- **sympy__sympy-20590** (main only (3))
  - Instances of those classes reject assignment of arbitrary attributes with AttributeError.
- **sympy__sympy-21596** (main only (3))
  - The first intersection is asserted to be exactly {-1, 1}, with no other members.
  - Factorized imaginary-part filtering over Integers yielding only 1.
  - The corresponding Naturals0 case yielding only 1.
