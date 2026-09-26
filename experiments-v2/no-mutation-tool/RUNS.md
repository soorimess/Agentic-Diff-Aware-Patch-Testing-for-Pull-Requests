# Run status, per pull request

Last run in this table: 2026-09-26 10:52 UTC.

- **70** instances across **12** repositories
- **51/69** fail-to-pass, of those that reached a verdict
- **51** measured for changed-line coverage: **mean 92%** per test, median 100%
- **83%** of the changed lines those tests were measured against (206/247, pooled)
- **41%** of every source line all 70 patches change (206/508) -- a fixed denominator, so this is the figure that compares across arms
- \$4.37 and 60.4M tokens in total
- **29** of these were sent a second-chance message after stopping with nothing to score, and **10** of them ended fail-to-pass; the other 41 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 1 | 0 | 0 | 1 | **added by the flag** |
| `loop_open` | 11 | 10 | 1 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 17 | 0 | 17 | 0 | **added by the flag** |

Of the **18** refused for a reason the flag itself adds, **0** ended fail-to-pass.

Every row was produced with the same configuration: **`no-mutation-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 49 | `run` x12, `write_file` x12, `run_tests` x9, `verify` x6, `coverage` x4 | — | — | — | 2026-09-26 06:48 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 4/7 | 7/7 | 32 | `run` x20, `run_tests` x4, `write_file` x3, `coverage` x1, `verify` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 06:38 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 14 | `run` x8, `coverage` x1, `run_tests` x1, `verify` x1, `write_file` x1 | close (4) | nearly complete (4) | good (4) | 2026-09-26 06:26 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 5/9 | 9/9 | 25 | `run` x13, `run_tests` x3, `coverage` x2, `verify` x2, `write_file` x2 | equivalent (5) | nearly complete (4) | poor (2) | 2026-09-26 06:28 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 65 | `run` x37, `write_file` x16, `verify` x5, `run_tests` x1 | — | — | — | 2026-09-26 06:44 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 59 | `run` x19, `write_file` x17, `run_tests` x12, `verify` x4 | — | — | — | 2026-09-26 06:44 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | YES | 100% (1/1) | 2/2 | 2/2 | 19 | `run` x7, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 06:25 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 100% (5/5) | 3/6 | 4/6 | 25 | `run` x12, `verify` x3, `write_file` x3, `coverage` x2, `run_tests` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 06:39 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 59 | `run` x18, `write_file` x15, `run_tests` x11, `verify` x6, `coverage` x2 | — | — | — | 2026-09-26 06:51 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 38 | `run` x20, `run_tests` x7, `write_file` x7, `coverage` x1, `verify` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:46 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 22 | `run` x7, `write_file` x4, `coverage` x3, `run_tests` x3, `verify` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:45 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 63 | `run` x23, `write_file` x14, `run_tests` x10, `verify` x6, `coverage` x1  (+1 edit reverted) | — | — | — | 2026-09-26 06:57 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 51 | `run` x19, `write_file` x11, `run_tests` x9, `verify` x4, `coverage` x1 | — | — | — | 2026-09-26 07:02 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 10/10 | 9/10 | 27 | `run` x10, `run_tests` x4, `write_file` x4, `coverage` x3, `verify` x3 | narrower (3) | complete (5) | poor (2) | 2026-09-26 06:54 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 41 | `run` x18, `write_file` x8, `verify` x6, `coverage` x3, `run_tests` x3 | narrower (3) | none (1) | poor (2) | 2026-09-26 06:58 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 41 | `run` x16, `write_file` x8, `run_tests` x6, `verify` x5, `coverage` x2 | close (4) | nearly complete (4) | good (4) | 2026-09-26 07:01 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 56 | `run` x20, `write_file` x15, `run_tests` x9, `verify` x6 | — | — | — | 2026-09-26 07:06 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 35 | `run` x15, `run_tests` x6, `write_file` x6, `coverage` x2, `verify` x2 | close (4) | complete (5) | good (4) | 2026-09-26 07:03 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 28 | `run` x20, `run_tests` x2, `write_file` x2, `coverage` x1, `verify` x1 | narrower (3) | nearly complete (4) | acceptable (3) | 2026-09-26 07:02 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 29% (2/7) | 0/10 | 4/10 | 69 | `run` x26, `write_file` x13, `run_tests` x11, `verify` x8, `coverage` x5 | tangential (2) | minor only (2) | reject (1) | 2026-09-26 07:18 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 24 | `run` x10, `coverage` x3, `verify` x3, `write_file` x3, `run_tests` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:06 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 1/2 | 2/2 | 33 | `run` x20, `coverage` x3, `verify` x3, `write_file` x3, `run_tests` x2 | narrower (3) | main only (3) | exemplary (5) | 2026-09-26 07:10 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 0/1 | 1/1 | 27 | `run` x14, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:11 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 51 | `run` x14, `write_file` x14, `run_tests` x7, `verify` x5, `coverage` x3 | — | — | — | 2026-09-26 07:20 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 30 | `run` x21, `run_tests` x3, `write_file` x2, `coverage` x1, `verify` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:13 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 65 | `run` x20, `write_file` x17, `run_tests` x11, `coverage` x5, `verify` x5  (+1 edit reverted) | — | — | — | 2026-09-26 07:24 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | NO | — | — | — | 63 | `run` x18, `write_file` x16, `run_tests` x10, `coverage` x5, `verify` x5 | — | — | — | 2026-09-26 07:26 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 9/10 | 9/10 | 32 | `run` x15, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2 | tangential (2) | none (1) | poor (2) | 2026-09-26 07:22 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 78% (14/18) | 0/10 | 0/10 | 32 | `run` x13, `write_file` x5, `run_tests` x4, `verify` x4, `coverage` x3 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 07:23 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 23 | `run` x10, `coverage` x3, `verify` x3, `write_file` x3, `run_tests` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:21 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 24 | `run` x16, `run_tests` x2, `verify` x2, `coverage` x1, `write_file` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:22 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 7/10 | 10/10 | 21 | `run` x10, `run_tests` x3, `coverage` x2, `verify` x2, `write_file` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:31 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 35 | `run` x18, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 07:35 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 94% (16/17) | no mutants | no mutants | 29 | `run` x16, `coverage` x3, `verify` x3, `write_file` x3, `run_tests` x2 | close (4) | complete (5) | poor (2) | 2026-09-26 09:14 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 1/10 | 21 | `run` x8, `run_tests` x3, `verify` x3, `coverage` x2, `write_file` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:37 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 60 | `run` x24, `run_tests` x14, `write_file` x14  (+1 edit reverted) | — | — | — | 2026-09-26 09:22 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | YES | 100% (11/11) | 9/10 | 9/10 | 39 | `run` x23, `write_file` x5, `run_tests` x4, `verify` x3, `coverage` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:17 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 17 | `run` x7, `run_tests` x4, `verify` x2, `coverage` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:37 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 100% (3/3) | 1/2 | 0/2 | 33 | `run` x15, `coverage` x4, `verify` x4, `write_file` x4, `run_tests` x3 | close (4) | nearly complete (4) | poor (2) | 2026-09-26 09:09 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 36 | `write_file` x10, `run` x9, `verify` x8, `coverage` x3, `run_tests` x3 | equivalent (5) | main only (3) | good (4) | 2026-09-26 09:19 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 24 | `run` x11, `run_tests` x4, `write_file` x3, `verify` x2, `coverage` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:19 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 16 | `run` x10, `coverage` x1, `run_tests` x1, `verify` x1, `write_file` x1 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 09:12 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 52 | `run` x15, `write_file` x14, `run_tests` x11, `verify` x4  (+1 edit reverted) | — | — | — | 2026-09-26 09:28 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 17 | `run` x5, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:31 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 60 | `run` x36, `write_file` x8, `run_tests` x7, `verify` x3, `coverage` x1  (+2 edits reverted) | narrower (3) | none (1) | reject (1) | 2026-09-26 09:37 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 6/7 | 7/7 | 30 | `run` x15, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x1 | close (4) | nearly complete (4) | poor (2) | 2026-09-26 09:32 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 36 | `run` x16, `write_file` x5, `run_tests` x4, `verify` x4, `coverage` x2 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 09:31 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 54 | `write_file` x21, `run` x14, `run_tests` x5, `verify` x4, `coverage` x3 | — | — | — | 2026-09-26 09:36 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 5/10 | 5/10 | 59 | `run` x41, `verify` x5, `write_file` x5, `run_tests` x4, `coverage` x1  (+1 edit reverted) | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:42 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 53 | `write_file` x15, `run_tests` x12, `run` x8, `verify` x8, `coverage` x2 | — | — | — | 2026-09-26 09:52 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 4/10 | 4/10 | 46 | `run` x15, `verify` x8, `write_file` x8, `coverage` x6, `run_tests` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 09:51 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 21 | `run` x14, `run_tests` x2, `coverage` x1, `verify` x1, `write_file` x1 | close (4) | complete (5) | acceptable (3) | 2026-09-26 09:44 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 100% (10/10) | 6/10 | 6/10 | 33 | `run` x12, `verify` x5, `write_file` x5, `coverage` x4, `run_tests` x3 | narrower (3) | minor only (2) | poor (2) | 2026-09-26 09:47 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | NO | — | — | — | 71 | `run` x33, `write_file` x14, `run_tests` x10, `verify` x4, `coverage` x2 | — | — | — | 2026-09-26 09:58 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 29 | `run` x13, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 09:50 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 55 | `run` x16, `write_file` x13, `run_tests` x12, `verify` x7 | — | — | — | 2026-09-26 10:07 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 59 | `run` x19, `write_file` x15, `run_tests` x12, `verify` x6, `coverage` x1 | — | — | — | 2026-09-26 10:05 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 66 | `run` x21, `write_file` x16, `run_tests` x13, `verify` x7, `coverage` x3 | — | — | — | 2026-09-26 10:13 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | YES | 100% (3/3) | 4/8 | 6/8 | 23 | `run` x10, `run_tests` x6, `write_file` x3, `coverage` x1, `verify` x1 | tangential (2) | none (1) | poor (2) | 2026-09-26 09:57 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 43% (16/37) | 3/10 | 6/10 | 31 | `run` x8, `write_file` x7, `run_tests` x6, `verify` x5, `coverage` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:07 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 55 | `run` x17, `run_tests` x8, `write_file` x8, `verify` x7, `coverage` x5  (+1 edit reverted) | — | — | — | 2026-09-26 10:17 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 10/10 | 10/10 | 35 | `run` x15, `write_file` x7, `run_tests` x5, `verify` x4, `coverage` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:18 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 57 | `run` x22, `write_file` x14, `run_tests` x8, `verify` x8, `coverage` x2 | narrower (3) | complete (5) | good (4) | 2026-09-26 10:30 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 23 | `run` x8, `verify` x4, `coverage` x3, `run_tests` x3, `write_file` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:52 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 40 | `run` x22, `write_file` x7, `coverage` x3, `run_tests` x3, `verify` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:26 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | YES | 100% (2/2) | 3/5 | 3/5 | 31 | `run` x16, `write_file` x6, `coverage` x2, `run_tests` x2, `verify` x2 | narrower (3) | main only (3) | reject (1) | 2026-09-26 10:27 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 32 | `run` x18, `run_tests` x3, `verify` x3, `coverage` x2, `write_file` x2  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:50 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 31 | `run` x12, `run_tests` x5, `verify` x4, `write_file` x4, `coverage` x2 | tangential (2) | none (1) | acceptable (3) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 33 | `run` x17, `write_file` x5, `verify` x4, `run_tests` x3, `coverage` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 47 | `run` x18, `write_file` x9, `run_tests` x6, `verify` x5, `coverage` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:51 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (main only (3))
  - Unequal Q-format VLA elements are compared and reported with the correct differing values and aggregate statistics.
- **astropy__astropy-14598** (nearly complete (4))
  - A value with doubled single quotes followed by spaces round-trips unchanged.
- **astropy__astropy-7606** (nearly complete (4))
  - The subclass-sensitive consequence of replacing isinstance(other, UnrecognizedUnit) with isinstance(other, type(self)) is not tested.
- **django__django-12308** (main only (3))
  - Non-empty JSONField lists are displayed as exact JSON arrays.
  - Non-empty JSONField strings are displayed as exact JSON strings with JSON quoting.
  - Values that raise TypeError during JSON preparation produce the expected display_for_value fallback.
- **django__django-13012** (main only (3))
  - A nonconstant expression wrapped in ExpressionWrapper delegates group-by column calculation to the wrapped expression.
- **django__django-13023** (main only (3))
  - Other `TypeError`-producing invalid values are converted into `ValidationError`.
  - Invalid values causing `ValueError` are converted into `ValidationError`.
- **django__django-13794** (none (1))
  - The add filter concatenates an ordinary string on the left with a lazy string and produces "stringlazy".
  - The add filter concatenates a lazy string on the left with another lazy string and produces "stringlazy".
  - Two lazy numeric values can be added and produce 9.
- **django__django-14534** (nearly complete (4))
  - When attrs has no id, BoundWidget.id_for_label returns None rather than an invented id.
- **django__django-14608** (nearly complete (4))
  - The initially created _non_form_errors ErrorList has error_class='nonform' when full_clean() does not replace it.
- **django__django-14725** (minor only (2))
  - An edit-only model formset does not save submitted extra or new objects.
  - An edit-only model formset still saves changes to existing objects.
  - An edit-only inline formset does not save submitted extra or new child objects.
- **django__django-14792** (main only (3))
  - An unnamed datetime.timezone fixed offset returns its generated name, such as 'UTC+10:00'.
  - A named datetime.timezone preserves its supplied name, such as 'Etc/GMT-10'.
  - A named zoneinfo timezone falls back to its canonical zone name.
- **django__django-14915** (main only (3))
  - Wrappers with the same underlying value have the same hash regardless of their instance object.
  - A wrapper has the same hash as its underlying raw value, allowing lookups in dictionaries keyed by that raw value.
- **django__django-16454** (none (1))
  - CommandParser subparser errors are rendered as human-facing management-command errors rather than tracebacks.
  - Explicit argparse.ArgumentParser subparsers retain vanilla argparse error formatting.
- **django__django-16560** (minor only (2))
  - BaseConstraint-specific storage of violation_error_code.
  - PostgreSQL ExclusionConstraint accepting and storing violation_error_code.
  - ExclusionConstraint equality and repr() including violation_error_code.
- **django__django-16667** (main only (3))
  - The fallback pseudo-date is rejected as invalid with the normal "Enter a valid date." validation error.
- **matplotlib__matplotlib-20676** (main only (3))
  - Interactive horizontal construction preserves the original y-axis bounds.
  - Interactive vertical construction preserves the original x-axis bounds.
  - Horizontal edge handles initially equal the current x-axis bounds.
- **matplotlib__matplotlib-20859** (main only (3))
  - A legend created for a SubFigure is attached to that SubFigure.
  - Unsupported parents remain rejected with the updated FigureBase error wording.
- **matplotlib__matplotlib-24970** (main only (3))
  - The uint8 lookup preserves the expected mapped colormap values.
  - The float and float16 scaling, clipping, NaN handling, and casting paths preserve their expected mapped values.
- **mwaskom__seaborn-3069** (main only (3))
  - Nominal x-axis gridlines are hidden.
  - Nominal y-axis gridlines are hidden.
  - Explicit y-axis limits override the nominal automatic limits.
- **psf__requests-2931** (nearly complete (4))
  - String or bytes URL parameters are converted to a native string before URL parameter encoding and produce the intended query URL.
- **pydata__xarray-2905** (main only (3))
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their values data.
- **pydata__xarray-4629** (nearly complete (4))
  - Variable-level attrs merged with combine_attrs='override' are copied rather than shared with the first source variable.
- **pydata__xarray-6744** (main only (3))
  - center=True iteration for window sizes 1, 2, and 7, particularly the even-sized window offset and exact boundary windows.
  - center=False iteration for window sizes 1, 2, and 7 and their exact boundary windows.
- **pylint-dev__pylint-4970** (none (1))
  - A zero minimum similarity threshold disables duplicate-code checking, so the run returns without computing or displaying similarities.
- **pylint-dev__pylint-7277** (nearly complete (4))
  - A first sys.path entry equal to os.getcwd() is removed.
- **pytest-dev__pytest-6197** (main only (3))
  - Pytest must not add src to sys.path, so packages located under src are not importable merely because they exist.
- **scikit-learn__scikit-learn-10297** (main only (3))
  - With store_cv_values=True and one-dimensional y, fitting creates cv_values_ with shape (n_samples, 1, n_alphas).
  - With store_cv_values=True and multi-target y, fitting creates cv_values_ with shape (n_samples, n_targets, n_alphas).
- **scikit-learn__scikit-learn-14087** (nearly complete (4))
  - Elasticnet penalties continue selecting and storing l1_ratio_ values.
- **sphinx-doc__sphinx-7462** (minor only (2))
  - The Python domain unparser's expected doctree output for Tuple[()], because its assertions only check the result type and weak length conditions.
- **sphinx-doc__sphinx-7757** (minor only (2))
  - The positional-only parameter b in (a, b=0, /, c=1) receives the exact default '0'.
  - The positional-or-keyword parameter c in (a, b=0, /, c=1) receives the exact default '1'.
  - The positional-only parameter b in (a, b=0, /) receives the exact default '0'.
- **sphinx-doc__sphinx-9658** (none (1))
  - restify renders a mocked class as :py:class:`unknown.secret.Class` with its complete qualified name.
  - stringify returns unknown.secret.Class for a mocked class.
- **sympy__sympy-12489** (main only (3))
  - Construction from a base Permutation or with a size adjustment creates the requested subclass.
  - Integer shorthand construction uses the requested subclass.
  - Multi-argument cycle and Cycle-object construction use the requested subclass.
- **sympy__sympy-14976** (main only (3))
  - A lambdified expression using a rational constant produces the correct arbitrary-precision result in nsolve.
- **sympy__sympy-16450** (main only (3))
  - Preservation of other pre-existing assumptions such as integer, rational, prime, even, or odd assumptions.
- **sympy__sympy-17318** (main only (3))
  - The guarded _sqrt_match(4 + I) case must return [] without raising IndexError.
  - The denestable reported radical expression must simplify to I.
- **sympy__sympy-19637** (none (1))
  - A no-space expression sets hit to False and is parsed into the correct expression instead of raising UnboundLocalError.
  - A space-containing expression continues through the kern replacement branch and is parsed correctly.
- **sympy__sympy-21596** (main only (3))
  - The reported intersection is asserted to be exactly FiniteSet(-1, 1).
  - Imaginary-part filtering handles alternate factorized expressions over Integers and Naturals0.
  - An unsolved imaginary equation is represented by a ConditionSet.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
