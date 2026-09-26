# Run status, per pull request

Last run in this table: 2026-09-26 10:48 UTC.

- **70** instances across **12** repositories
- **45/70** fail-to-pass, of those that reached a verdict
- **45** measured for changed-line coverage: **mean 82%** per test, median 100%
- **63%** of the changed lines those tests were measured against (162/257, pooled)
- **32%** of every source line all 70 patches change (162/508) -- a fixed denominator, so this is the figure that compares across arms
- \$4.42 and 61.2M tokens in total
- **28** of these were sent a second-chance message after stopping with nothing to score, and **4** of them ended fail-to-pass; the other 42 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `loop_open` | 8 | 3 | 5 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 20 | 1 | 19 | 0 | **added by the flag** |

Of the **20** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 36 | `run_tests` x9, `write_file` x9, `run` x8, `verify` x3, `mutation` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 06:46 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 1/3 | 3/3 | 33 | `run` x17, `write_file` x5, `run_tests` x4, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:36 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 21 | `run` x10, `run_tests` x3, `write_file` x3, `mutation` x1, `verify` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:30 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 67% (4/6) | 0/4 | 4/4 | 34 | `run` x14, `mutation` x4, `run_tests` x4, `verify` x4, `write_file` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:33 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 55 | `run` x32, `write_file` x9, `verify` x6, `run_tests` x3, `mutation` x2 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 06:37 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 56 | `run` x17, `write_file` x16, `run_tests` x10, `verify` x4, `mutation` x2 | — | — | — | 2026-09-26 06:44 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 73 | `run` x22, `run_tests` x18, `write_file` x18, `mutation` x4, `verify` x4 | — | — | — | 2026-09-26 06:50 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 60% (3/5) | 1/3 | 2/3 | 33 | `run` x14, `verify` x5, `write_file` x5, `mutation` x3, `run_tests` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:39 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 57 | `run` x18, `write_file` x16, `run_tests` x11, `verify` x4, `mutation` x1 | — | — | — | 2026-09-26 06:51 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | NO | — | — | — | 66 | `run` x21, `write_file` x17, `run_tests` x14, `mutation` x4, `verify` x3 | — | — | — | 2026-09-26 06:54 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 17 | `run` x5, `run_tests` x3, `write_file` x3, `mutation` x2, `verify` x2 | narrower (3) | nearly complete (4) | acceptable (3) | 2026-09-26 06:43 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 68 | `run` x28, `write_file` x15, `run_tests` x10, `verify` x5, `mutation` x2 | tangential (2) | none (1) | reject (1) | 2026-09-26 07:00 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 45 | `run` x15, `write_file` x11, `run_tests` x8, `verify` x3, `mutation` x1 | — | — | — | 2026-09-26 06:56 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 18 | `run` x8, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 06:51 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 31 | `run` x17, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:53 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 25 | `run` x13, `write_file` x4, `mutation` x2, `run_tests` x2, `verify` x2 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 06:55 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 62 | `run` x33, `write_file` x11, `run_tests` x7 | — | — | — | 2026-09-26 07:04 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 23 | `run` x12, `run_tests` x3, `write_file` x3, `verify` x2, `mutation` x1 | close (4) | complete (5) | good (4) | 2026-09-26 06:59 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 31 | `run` x15, `run_tests` x4, `write_file` x4, `mutation` x3, `verify` x3 | narrower (3) | nearly complete (4) | good (4) | 2026-09-26 07:04 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 29% (2/7) | 1/6 | 2/6 | 55 | `run` x19, `run_tests` x11, `write_file` x11, `verify` x7, `mutation` x2 | tangential (2) | minor only (2) | poor (2) | 2026-09-26 07:12 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 22 | `run` x7, `run_tests` x4, `write_file` x3, `mutation` x2, `verify` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:03 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 31 | `run` x18, `run_tests` x3, `write_file` x3, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 07:08 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 34 | `run` x13, `write_file` x6, `run_tests` x5, `mutation` x4, `verify` x4 | equivalent (5) | main only (3) | poor (2) | 2026-09-26 07:14 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 49 | `write_file` x13, `run` x12, `run_tests` x11, `verify` x3, `mutation` x1 | — | — | — | 2026-09-26 07:16 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x14, `run_tests` x7, `verify` x2, `mutation` x1, `write_file` x1 | equivalent (5) | complete (5) | poor (2) | 2026-09-26 07:12 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 68 | `run` x22, `write_file` x14, `run_tests` x13, `verify` x7, `mutation` x4 | — | — | — | 2026-09-26 07:24 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 24 | `run` x13, `run_tests` x3, `mutation` x2, `verify` x2, `write_file` x2 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 07:15 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 57 | `run` x22, `write_file` x11, `run_tests` x10, `mutation` x5, `verify` x5 | — | — | — | 2026-09-26 07:31 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 50% (12/24) | 4/10 | 1/10 | 27 | `run` x10, `run_tests` x4, `verify` x4, `write_file` x4, `mutation` x2 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 07:22 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 17 | `run` x10, `run_tests` x2, `mutation` x1, `verify` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:19 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 31 | `run` x14, `run_tests` x4, `write_file` x4, `mutation` x3, `verify` x3 | tangential (2) | none (1) | acceptable (3) | 2026-09-26 07:24 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 28 | `run` x11, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:33 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 29 | `run` x18, `run_tests` x4, `write_file` x2, `mutation` x1, `verify` x1  (+1 edit reverted) | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:30 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 29 | `run` x15, `write_file` x4, `run_tests` x3, `verify` x3, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:37 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 2/10 | 2/10 | 20 | `run` x8, `verify` x3, `run_tests` x2, `write_file` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:36 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 50 | `run` x13, `write_file` x13, `run_tests` x11, `verify` x4, `mutation` x3 | — | — | — | 2026-09-26 09:24 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 64 | `run` x23, `write_file` x23, `run_tests` x6, `verify` x5, `mutation` x1 | — | — | — | 2026-09-26 09:24 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 20 | `run` x8, `write_file` x3, `mutation` x2, `run_tests` x2, `verify` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:38 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/1 | 0/1 | 41 | `run` x25, `run_tests` x4, `write_file` x4, `verify` x3, `mutation` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 09:13 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 30 | `run` x13, `run_tests` x4, `write_file` x4, `verify` x3, `mutation` x2 | equivalent (5) | main only (3) | good (4) | 2026-09-26 09:17 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 3/10 | 3/10 | 21 | `run` x6, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x2 | equivalent (5) | nearly complete (4) | acceptable (3) | 2026-09-26 09:20 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 17 | `run` x8, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:09 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 55 | `run` x23, `run_tests` x10, `write_file` x8, `verify` x4, `mutation` x1 | — | — | — | 2026-09-26 09:28 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 25 | `run` x6, `run_tests` x5, `verify` x4, `write_file` x4, `mutation` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 09:38 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 49 | `run` x20, `write_file` x9, `run_tests` x6, `verify` x4, `mutation` x3 | — | — | — | 2026-09-26 09:40 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | NO | — | — | — | 48 | `run_tests` x12, `write_file` x12, `run` x10, `verify` x4, `mutation` x2 | — | — | — | 2026-09-26 09:38 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 26 | `run` x14, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 09:28 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 62 | `write_file` x17, `run_tests` x16, `run` x13, `mutation` x5, `verify` x5  (+1 edit reverted) | — | — | — | 2026-09-26 09:40 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 24 | `run` x12, `verify` x3, `write_file` x3, `run_tests` x2, `mutation` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:34 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 51 | `run` x16, `write_file` x15, `run_tests` x6, `verify` x5, `mutation` x2 | — | — | — | 2026-09-26 09:49 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 31 | `run` x13, `verify` x5, `write_file` x5, `mutation` x3, `run_tests` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:47 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 15 | `run` x8, `run_tests` x2, `mutation` x1, `verify` x1, `write_file` x1 | close (4) | main only (3) | acceptable (3) | 2026-09-26 09:42 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 0/10 | 6/10 | 29 | `run` x14, `run_tests` x4, `write_file` x4, `mutation` x2, `verify` x2 | tangential (2) | none (1) | reject (1) | 2026-09-26 09:46 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 55% (26/47) | 1/10 | 4/10 | 55 | `run` x24, `write_file` x11, `run_tests` x10, `verify` x4, `mutation` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 10:02 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 43 | `run` x20, `run_tests` x6, `write_file` x5, `verify` x2, `mutation` x1  (+1 edit reverted) | — | — | — | 2026-09-26 09:52 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 61 | `run` x18, `write_file` x13, `run_tests` x11, `verify` x10, `mutation` x1 | — | — | — | 2026-09-26 10:04 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 55 | `run` x14, `write_file` x14, `run_tests` x10, `mutation` x5, `verify` x4 | — | — | — | 2026-09-26 10:05 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 63 | `run` x20, `write_file` x17, `run_tests` x13, `verify` x6, `mutation` x1 | — | — | — | 2026-09-26 10:11 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 47 | `write_file` x13, `run_tests` x11, `run` x10, `mutation` x4, `verify` x3 | — | — | — | 2026-09-26 10:08 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 35% (13/37) | 1/10 | 5/10 | 59 | `run` x24, `run_tests` x10, `write_file` x9, `verify` x6, `mutation` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 10:19 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 51 | `run` x18, `write_file` x9, `verify` x8, `run_tests` x7, `mutation` x1 | — | — | — | 2026-09-26 10:11 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 4/5 | 5/5 | 42 | `run` x19, `write_file` x7, `verify` x6, `run_tests` x4, `mutation` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 10:18 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | NO | — | — | — | 56 | `run` x29, `run_tests` x9, `write_file` x8, `mutation` x1, `verify` x1  (+1 edit reverted) | — | — | — | 2026-09-26 10:20 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 27 | `run` x9, `mutation` x4, `run_tests` x4, `verify` x4, `write_file` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:42 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 44 | `run` x20, `write_file` x12, `run_tests` x6, `verify` x2, `mutation` x1 | close (4) | nearly complete (4) | good (4) | 2026-09-26 10:23 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 56 | `run` x16, `write_file` x16, `run_tests` x11, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 10:27 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 34 | `run` x15, `write_file` x5, `run_tests` x4, `verify` x4, `mutation` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:48 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 24 | `run` x9, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | tangential (2) | none (1) | acceptable (3) | 2026-09-26 10:42 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 25 | `run` x17, `run_tests` x2, `write_file` x2, `mutation` x1, `verify` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 10:37 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | NO | — | — | — | 72 | `run` x26, `write_file` x20, `run_tests` x12, `verify` x4, `mutation` x2 | — | — | — | 2026-09-26 10:46 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (main only (3))
  - The line-surface-brightness unit `10-7J/s/kpc2` has the expected powers; the generated test only asserts `assert parsed is not None, f"Failed to parse {unit_str}"`.
- **astropy__astropy-14539** (main only (3))
  - Differing Q-format variable-length-array data is reported with the correct differing rows, values, totals, ratios, and report text.
- **astropy__astropy-14598** (nearly complete (4))
  - A long card value containing `''` followed by a space and then text round-trips unchanged.
- **astropy__astropy-7606** (main only (3))
  - Ordinary UnitBase equality with an invalid operand such as None returns NotImplemented instead of raising.
  - UnrecognizedUnit equality with a valid operand is restricted to a compatible type and matching name.
- **django__django-10914** (nearly complete (4))
  - A file saved through the TemporaryUploadedFile and rename path also receives mode 0o644.
- **django__django-12308** (main only (3))
  - A None JSONField value displays the configured empty-value marker.
  - A JSON-serializable list value is rendered as a JSON array.
  - A JSON-serializable string value is rendered as a quoted JSON string.
- **django__django-13023** (nearly complete (4))
  - Values whose Decimal conversion raises ValueError, such as the empty tuple (), produce ValidationError.
- **django__django-13449** (none (1))
  - On SQLite, a Window expression with a DecimalField output, including Lag, is cast outside OVER so it executes and returns correct values instead of a syntax error.
  - On SQLite, Window expressions with non-DecimalField outputs retain the ordinary window SQL path without the DecimalField cast.
- **django__django-13590** (none (1))
  - A namedtuple supplied as a __range value is reconstructed with expanded elements and produces the correct filtered result.
  - A regular tuple supplied as a __range value continues to be reconstructed and filtered correctly.
  - A list supplied as a __range value continues to be reconstructed and filtered correctly.
- **django__django-13794** (main only (3))
  - The add filter concatenates two lazy strings.
  - Lazy proxy values with non-string results support addition, such as two lazy integers producing 9.
- **django__django-14534** (nearly complete (4))
  - When no widget ID or auto_id is available, id_for_label is None rather than a fabricated ID.
- **django__django-14608** (nearly complete (4))
  - A newly initialized FormSet non_form_errors ErrorList has the nonform CSS class.
- **django__django-14725** (minor only (2))
  - inlineformset_factory exposes and propagates an edit_only parameter defaulting to False
  - edit-only model formsets do not save submitted new objects
  - edit-only model formsets still save changes to existing objects
- **django__django-14792** (main only (3))
  - Fixed-offset datetime.timezone and zoneinfo objects also return their offset or supplied name through tzname(None).
  - Named or non-fixed datetime, pytz, and zoneinfo timezones retain their names.
  - A falsy tzname(None) result falls back to str(timezone).
- **django__django-14915** (main only (3))
  - Dictionary membership using a ModelChoiceIteratorValue matches a key equal to its underlying value; self.assertTrue(True) does not assert that the membership result is true.
- **django__django-16560** (minor only (2))
  - BaseConstraint directly accepts and stores a custom violation_error_code.
  - Constraint equality distinguishes different violation_error_code values.
  - CheckConstraint repr() includes a custom violation_error_code.
- **django__django-16667** (none (1))
  - SelectDateWidget.value_from_datadict catches OverflowError from an oversized date component and returns '0-0-0'.
  - A DateField form using SelectDateWidget treats that result as invalid with the 'Enter a valid date.' error instead of crashing.
- **matplotlib__matplotlib-20676** (main only (3))
  - Horizontal interactive edge handles initially use the existing x-axis bounds.
  - Vertical interactive edge handles initially use the existing y-axis bounds.
  - Moving a horizontal selector preserves both axis bounds.
- **matplotlib__matplotlib-20859** (main only (3))
  - The legend created for a SubFigure is associated with that SubFigure (`legend.figure is subfig`).
  - An unsupported parent still raises `TypeError` with the updated `FigureBase` error message.
- **matplotlib__matplotlib-24870** (main only (3))
  - Regular contour() with a boolean list defaults to [0.5].
  - Regular contour() with a masked boolean array defaults to [0.5].
  - Regular contourf() with a boolean list defaults to [0, 0.5, 1].
- **matplotlib__matplotlib-24970** (main only (3))
  - Scalar uint8 input maps to the same color as numeric zero after the integer cast.
  - Signed integer inputs continue to map zero correctly.
  - Float16 and float inputs continue to map zero correctly through normalization and casting.
- **psf__requests-2931** (nearly complete (4))
  - String or bytes `params` passed to `prepare_url` are converted with `to_native_string` before parameter encoding so URL query handling remains correct.
- **pydata__xarray-2905** (main only (3))
  - Pandas Series, Index, and DataFrame inputs continue to be converted to their values data.
- **pydata__xarray-4075** (nearly complete (4))
  - The NaN test leaves only one valid True weight, so its assertion also passes before the fix and does not cover numeric normalization after masking when multiple valid True weights remain.
- **pydata__xarray-6744** (main only (3))
  - Centered iteration for the other tested window sizes 1, 2, and 7.
  - The center=False trailing-window branch.
- **pytest-dev__pytest-6197** (main only (3))
  - Pytest must not add src to sys.path merely while collecting, leaving packages under src unimportable.
- **scikit-learn__scikit-learn-10297** (main only (3))
  - With one-dimensional targets, fitting with store_cv_values=True creates cv_values_ with shape (n_samples, 1, n_alphas).
  - With multiple targets, fitting with store_cv_values=True creates cv_values_ with shape (n_samples, n_targets, n_alphas).
- **scikit-learn__scikit-learn-14087** (none (1))
  - The generated test reaches the binary auto/ovr path but has no assertion that pins the corrected coefficient-path indexing or its expected result.
  - The generated test does not assert that l1_ratio_ is None for the l2 cases.
  - The generated test never exercises or asserts the elasticnet l1-ratio selection path.
- **scikit-learn__scikit-learn-9288** (main only (3))
  - Serial and parallel KMeans runs have the same per-sample cluster assignments.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python-domain unparser renders the empty tuple in `Tuple[()]` as explicit opening and closing punctuation without raising `IndexError`.
  - `sphinx.pycode.ast.unparse` returns `"()"` for an empty `ast.Tuple`.
- **sphinx-doc__sphinx-7590** (none (1))
  - Integer user-defined literals, including integer suffix combinations, parse and receive the expected UDL AST/mangled ID.
  - Decimal floating-point user-defined literals, including floating-point suffix combinations, parse and receive the expected UDL AST/mangled ID.
  - Hexadecimal floating-point user-defined literals parse and receive the expected UDL AST/mangled ID.
- **sympy__sympy-12489** (main only (3))
  - All ordinary `Permutation.__new__` input branches preserve the requested subclass, including copy and size-adjustment paths.
  - Permutation-producing operations such as addition, multiplication, inversion, powers, conjugation, and lexicographic advancement preserve the dynamic subclass and dispatch through it.
  - Left and right multiplication use the class of the operand performing the operation, so subclass-left results preserve the subclass while base-left results remain base `Permutation` objects.
- **sympy__sympy-14976** (main only (3))
  - The exact numerator-and-denominator output is preserved.
  - nsolve obtains the rational solution at arbitrary precision through the mpmath lambdify path.
- **sympy__sympy-16450** (main only (3))
  - Retention of other source assumptions and the complete inferred assumptions0 closure: the multiple-assumption test sets positive=True, so posify does not replace that symbol and its assertions only inspect the original symbol.
- **sympy__sympy-16766** (nearly complete (4))
  - The complete result is exactly the expected indexing expression rather than merely ending with it.
- **sympy__sympy-19637** (none (1))
  - No-space input sets hit to False and parses successfully to the correct expression instead of raising UnboundLocalError.
  - Space-containing input creates the replacement kernel before computing hit and preserves the correct space-normalization and parsing behaviour.
