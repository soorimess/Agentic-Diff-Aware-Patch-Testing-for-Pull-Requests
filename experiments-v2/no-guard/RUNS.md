# Run status, per pull request

Last run in this table: 2026-09-26 10:52 UTC.

- **70** instances across **12** repositories
- **48/68** fail-to-pass, of those that reached a verdict
- **48** measured for changed-line coverage: **mean 88%** per test, median 100%
- **75%** of the changed lines those tests were measured against (201/269, pooled)
- **40%** of every source line all 70 patches change (201/508) -- a fixed denominator, so this is the figure that compares across arms
- \$5.48 and 76.0M tokens in total
- **35** of these were sent a second-chance message after stopping with nothing to score, and **14** of them ended fail-to-pass; the other 35 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 1 | 1 | 0 | 0 | **added by the flag** |
| `loop_open` | 14 | 10 | 3 | 1 | from `require-tools` |
| `no_test` | 1 | 0 | 1 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 19 | 3 | 16 | 0 | **added by the flag** |

Of the **20** refused for a reason the flag itself adds, **4** ended fail-to-pass.

Every row was produced with the same configuration: **`no-guard`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 31 | `run_tests` x8, `write_file` x8, `run` x6, `verify` x3, `coverage` x2, `mutation` x1 | narrower (3) | none (1) | poor (2) | 2026-09-26 06:43 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 1/3 | 3/3 | 43 | `run` x19, `write_file` x6, `run_tests` x5, `verify` x4, `coverage` x2, `mutation` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:37 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 23 | `run` x12, `coverage` x2, `run_tests` x2, `verify` x2, `mutation` x1, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:28 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 3/4 | 4/4 | 39 | `run` x16, `verify` x5, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3 | close (4) | main only (3) | acceptable (3) | 2026-09-26 06:38 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 59 | `run` x38, `write_file` x8, `verify` x4, `run_tests` x2, `coverage` x1, `mutation` x1 | narrower (3) | complete (5) | good (4) | 2026-09-26 06:38 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 68 | `run` x26, `write_file` x15, `run_tests` x13, `verify` x4, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 06:45 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 95 | `run` x45, `write_file` x18, `run_tests` x15, `verify` x10, `coverage` x1 | — | — | — | 2026-09-26 06:55 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 100% (5/5) | 2/3 | 2/3 | 32 | `run` x13, `write_file` x5, `verify` x4, `mutation` x3, `run_tests` x3, `coverage` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:39 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 61 | `run` x20, `write_file` x14, `verify` x9, `run_tests` x8, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-26 06:52 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 41 | `run` x21, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:45 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 26 | `run` x10, `coverage` x3, `run_tests` x3, `verify` x3, `write_file` x3, `mutation` x2 | narrower (3) | nearly complete (4) | acceptable (3) | 2026-09-26 06:46 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 50 | `run` x19, `run_tests` x9, `write_file` x9, `verify` x4, `coverage` x2, `mutation` x2 | tangential (2) | none (1) | reject (1) | 2026-09-26 06:56 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 64 | `run` x23, `run_tests` x12, `write_file` x12, `verify` x8, `mutation` x2, `coverage` x1 | — | — | — | 2026-09-26 07:04 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 25 | `run` x6, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | narrower (3) | complete (5) | poor (2) | 2026-09-26 06:55 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 33 | `run` x20, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | close (4) | nearly complete (4) | good (4) | 2026-09-26 06:53 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 21 | `run` x11, `coverage` x2, `run_tests` x2, `verify` x2, `mutation` x1, `write_file` x1 | equivalent (5) | nearly complete (4) | acceptable (3) | 2026-09-26 06:53 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 64 | `run` x31, `write_file` x13, `run_tests` x8, `verify` x5, `coverage` x1 | — | — | — | 2026-09-26 07:05 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 28 | `run` x9, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | close (4) | complete (5) | good (4) | 2026-09-26 07:03 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 50% (1/2) | no mutants | no mutants | 58 | `run` x24, `write_file` x11, `verify` x8, `run_tests` x5, `coverage` x4, `mutation` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:13 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 43% (3/7) | 1/6 | 2/6 | 45 | `run` x20, `write_file` x6, `verify` x5, `coverage` x4, `run_tests` x3, `mutation` x2 | tangential (2) | minor only (2) | reject (1) | 2026-09-26 07:14 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | NO | — | — | — | 47 | `run` x13, `write_file` x9, `run_tests` x7, `verify` x5, `coverage` x3, `mutation` x3 | — | — | — | 2026-09-26 07:13 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 53 | `run` x15, `run_tests` x11, `write_file` x11, `coverage` x4, `mutation` x3, `verify` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:16 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x12, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2, `run_tests` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:11 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 68 | `run` x26, `write_file` x11, `run_tests` x10, `verify` x6, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-26 07:22 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | BROKEN | — | — | — | 36 | `run` x22, `run_tests` x7, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | — | — | — | 2026-09-26 07:12 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | YES | 100% (6/6) | 1/1 | 1/1 | 61 | `run` x21, `write_file` x14, `verify` x13, `coverage` x3, `run_tests` x3, `mutation` x2 | equivalent (5) | complete (5) | poor (2) | 2026-09-26 07:25 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 26 | `run` x13, `run_tests` x3, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 07:16 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 64 | `write_file` x21, `run` x20, `verify` x8, `run_tests` x7, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 07:29 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 56% (10/18) | 1/10 | 1/10 | 41 | `run` x11, `run_tests` x7, `write_file` x7, `verify` x5, `coverage` x3, `mutation` x3 | narrower (3) | minor only (2) | poor (2) | 2026-09-26 07:28 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 23 | `run` x15, `run_tests` x2, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:20 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 27 | `run` x10, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:24 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 19 | `run` x5, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:32 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 36 | `run` x16, `write_file` x4, `coverage` x3, `run_tests` x3, `verify` x3, `mutation` x2 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 07:35 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 94% (16/17) | no mutants | no mutants | 33 | `run` x18, `coverage` x3, `run_tests` x3, `verify` x3, `write_file` x3, `mutation` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 07:39 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 25 | `run` x6, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | tangential (2) | main only (3) | poor (2) | 2026-09-26 09:20 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 66 | `run` x21, `write_file` x14, `run_tests` x10, `verify` x8, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 09:27 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 65 | `run` x28, `write_file` x13, `run_tests` x8, `verify` x8, `coverage` x1 | — | — | — | 2026-09-26 09:23 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 25 | `run` x7, `run_tests` x5, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:13 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/1 | 0/1 | 38 | `run` x13, `run_tests` x5, `verify` x5, `write_file` x5, `coverage` x4, `mutation` x3 | close (4) | nearly complete (4) | poor (2) | 2026-09-26 09:18 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 39 | `run` x14, `verify` x5, `write_file` x5, `run_tests` x4, `coverage` x3, `mutation` x2 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 09:21 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 17 | `run` x3, `verify` x3, `write_file` x3, `coverage` x2, `run_tests` x2, `mutation` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:16 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 19 | `run` x11, `run_tests` x2, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:08 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 67 | `write_file` x19, `run_tests` x15, `run` x14, `verify` x8, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 09:30 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 19 | `run` x9, `run_tests` x3, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | narrower (3) | nearly complete (4) | acceptable (3) | 2026-09-26 09:31 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 1/1 | 1/1 | 63 | `run` x33, `write_file` x10, `run_tests` x7, `verify` x5, `coverage` x2, `mutation` x1 | narrower (3) | complete (5) | poor (2) | 2026-09-26 09:41 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 29 | `run` x11, `write_file` x5, `run_tests` x4, `verify` x3, `coverage` x1, `mutation` x1 | close (4) | nearly complete (4) | poor (2) | 2026-09-26 09:31 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 61 | `run` x19, `write_file` x10, `run_tests` x9, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 09:40 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 71 | `run` x22, `write_file` x15, `run_tests` x14, `verify` x6, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 09:41 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | BROKEN | — | — | — | 68 | `run` x35, `run_tests` x11, `write_file` x11, `verify` x1 | — | — | — | 2026-09-26 09:41 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 49 | `run` x13, `write_file` x11, `verify` x5, `coverage` x3, `mutation` x3, `run_tests` x3 | — | — | — | 2026-09-26 09:53 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 32 | `run` x12, `write_file` x6, `verify` x5, `coverage` x2, `run_tests` x2, `mutation` x1 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:45 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 27 | `run` x6, `run_tests` x4, `verify` x4, `write_file` x4, `coverage` x3, `mutation` x3 | close (4) | complete (5) | acceptable (3) | 2026-09-26 09:55 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 2/10 | 6/10 | 43 | `run` x10, `run_tests` x8, `write_file` x8, `verify` x7, `coverage` x4, `mutation` x2 | tangential (2) | none (1) | poor (2) | 2026-09-26 09:51 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 60% (28/47) | 1/10 | 4/10 | 51 | `run` x27, `run_tests` x6, `write_file` x6, `coverage` x3, `verify` x3, `mutation` x2 | narrower (3) | none (1) | reject (1) | 2026-09-26 10:02 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 88% (14/16) | 8/10 | 8/10 | 49 | `run` x21, `run_tests` x7, `write_file` x6, `coverage` x4, `mutation` x3, `verify` x3 | close (4) | complete (5) | acceptable (3) | 2026-09-26 09:56 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 84 | `run` x33, `write_file` x17, `verify` x14, `run_tests` x13 | — | — | — | 2026-09-26 10:10 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 57 | `write_file` x15, `run` x14, `run_tests` x13, `verify` x6, `mutation` x2, `coverage` x1 | — | — | — | 2026-09-26 10:04 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 65 | `run` x28, `write_file` x13, `run_tests` x12, `coverage` x3, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 10:13 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 55 | `run` x15, `run_tests` x12, `write_file` x11, `coverage` x4, `verify` x4, `mutation` x1 | — | — | — | 2026-09-26 10:11 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 54% (20/37) | 4/10 | 5/10 | 36 | `run` x18, `write_file` x5, `verify` x4, `run_tests` x3, `coverage` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:07 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 42 | `run` x12, `run_tests` x8, `write_file` x6, `coverage` x3, `verify` x3, `mutation` x1 | — | — | — | 2026-09-26 10:09 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 5/5 | 5/5 | 76 | `run` x58, `run_tests` x7, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | close (4) | complete (5) | acceptable (3) | 2026-09-26 10:23 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 23 | `run` x6, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2 | equivalent (5) | main only (3) | good (4) | 2026-09-26 10:18 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 33 | `run` x14, `verify` x4, `write_file` x4, `coverage` x3, `mutation` x3, `run_tests` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:45 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 30 | `run` x14, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:25 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | YES | 100% (2/2) | 1/2 | 1/2 | 59 | `run` x25, `write_file` x9, `run_tests` x7, `coverage` x5, `verify` x5, `mutation` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:44 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 29 | `run` x10, `run_tests` x4, `verify` x4, `write_file` x4, `coverage` x3, `mutation` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:49 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 34 | `run` x13, `run_tests` x5, `write_file` x5, `coverage` x3, `verify` x3, `mutation` x2 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 10:47 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 29 | `run` x18, `run_tests` x3, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:41 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | NO | — | — | — | 65 | `run` x25, `write_file` x14, `run_tests` x11, `coverage` x4, `verify` x3, `mutation` x1 | — | — | — | 2026-09-26 10:52 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (none (1))
  - 10+3J/m/s/kpc2 must parse to the expected unit value rather than merely avoiding the old string representation.
  - 10-7J/s/kpc2 must parse to the expected unit value rather than merely avoiding the old string representation.
- **astropy__astropy-14539** (main only (3))
  - Unequal Q-format VLA data must be reported with the differing row values and correct aggregate difference information.
- **astropy__astropy-14598** (nearly complete (4))
  - A long FITS card value containing doubled single quotes followed by a space and text round-trips unchanged.
- **astropy__astropy-7606** (main only (3))
  - The generated test does not verify that UnitBase.__eq__ delegates an unparseable comparison by returning NotImplemented; its regular-unit test only observes the final False result, which the old implementation also produced.
  - The reverse-comparison and membership path, such as None == unit and unit not in (None, u.m), is not asserted.
  - The type(self)-specific subclass equality behaviour is not tested.
- **django__django-12308** (nearly complete (4))
  - Invalid JSONField values fall back to the exact display_for_value result; the generated test checks only that the result is a string.
- **django__django-13012** (main only (3))
  - A wrapped expression with non-empty group-by columns delegates those columns unchanged.
- **django__django-13023** (nearly complete (4))
  - A malformed value producing ValueError is converted to ValidationError.
- **django__django-13449** (none (1))
  - SQLite can execute a Window/Lag expression whose output is a DecimalField by placing the numeric cast outside the OVER clause and returning the correct lag values.
  - SQLite window expressions with non-Decimal output retain ordinary window SQL without the DecimalField-specific cast handling.
- **django__django-13794** (nearly complete (4))
  - Lazy non-string values retain addition support, exemplified by two lazy integers adding to 9.
- **django__django-14534** (nearly complete (4))
  - When no ID is assigned, id_for_label returns None instead of fabricating an ID.
- **django__django-14608** (main only (3))
  - Validation errors raised by FormSet.clean() are stored in a non_form_errors ErrorList with the 'nonform' CSS class.
- **django__django-14725** (minor only (2))
  - A model formset with edit_only=True ignores submitted new forms.
  - A model formset with edit_only=True still saves changes to existing objects.
  - An inline formset with edit_only=True ignores submitted new inline objects.
- **django__django-14792** (main only (3))
  - An unnamed datetime.timezone fixed offset returns "UTC+10:00".
  - A named datetime.timezone fixed offset preserves the name "Etc/GMT-10".
  - A named pytz timezone returns "Europe/Madrid".
- **django__django-14915** (main only (3))
  - The hash is derived from the wrapped value, including equal hashes for wrappers with the same value but different instances and compatibility with an underlying dictionary key.
- **django__django-16560** (minor only (2))
  - ExclusionConstraint accepts and stores a custom violation_error_code.
  - Constraints without a custom code retain a None violation_error_code; the generated assertion is conditional on hasattr() and is therefore not a complete check.
  - Constraint equality distinguishes otherwise identical constraints with different violation_error_code values.
- **django__django-16667** (main only (3))
  - A form using SelectDateWidget treats that input as invalid and reports "Enter a valid date." instead of crashing.
- **matplotlib__matplotlib-20676** (main only (3))
  - Horizontal interactive construction initializes edge handles at the current x bounds.
  - Vertical interactive construction initializes edge handles at the current y bounds.
  - After horizontal selection movement, both axis bounds remain unchanged and the edge handles move to the selected extents.
- **matplotlib__matplotlib-20859** (none (1))
  - A SubFigure, as a FigureBase, is accepted as a legend parent and the resulting legend is associated with that SubFigure.
  - A regular Figure remains accepted as a legend parent.
  - An Axes remains accepted as a legend parent.
- **matplotlib__matplotlib-24870** (nearly complete (4))
  - Boolean list and masked-array inputs to 2-D contouring retain boolean auto-level detection.
- **matplotlib__matplotlib-24970** (main only (3))
  - Colormap indexing produces equivalent output for uint8, int, float16, and float zero inputs.
- **psf__requests-2931** (nearly complete (4))
  - String or byte query parameters passed to `prepare_url` are normalized with `to_native_string` before query construction.
- **pydata__xarray-2905** (main only (3))
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their `.values`.
- **pydata__xarray-6744** (nearly complete (4))
  - center=True iteration for an even window size, especially size 2, which exercises the distinct offset case
- **pylint-dev__pylint-7277** (nearly complete (4))
  - A leading current-working-directory path is removed.
- **scikit-learn__scikit-learn-14087** (none (1))
  - The auto-to-OVR coefficient-path behavior is only exercised by clf.fit(X, y); the generic non-None assertions do not pin its expected result.
  - The non-elasticnet l1_ratio_ behavior is not pinned because assert ratio is None or ratio == 0.0 permits an incorrect 0.0 value.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python-domain unparser renders an empty tuple annotation as `(` and `)` punctuation nodes instead of popping an empty result.
  - The pycode AST unparser renders an empty tuple as the string `()`.
- **sphinx-doc__sphinx-7590** (none (1))
  - The C++ parser accepts decimal floating-point UDLs, including `6.62607015e-34q_J`, as user-defined-literal ASTs.
  - The C++ parser accepts hexadecimal floating-point UDLs with their exponent, sign, and suffix forms.
  - The C++ parser accepts integer UDLs without consuming the UDL identifier as an ordinary integer suffix.
- **sympy__sympy-12489** (main only (3))
  - Construction from Cycle input and multiple cycle arguments returns an instance of the requested subclass.
  - Construction from an existing subclass instance, including resizing, preserves the requested subclass.
  - Multiplication with a base Permutation as the left operand preserves the base result type when the subclass is on the right.
- **sympy__sympy-15349** (main only (3))
  - The optional-v path that applies the corrected rotation matrix to a supplied vector.
- **sympy__sympy-16450** (main only (3))
  - Other original assumptions and their derived assumptions are not tested on a symbol that actually enters posify's replacement branch.
- **sympy__sympy-17318** (main only (3))
  - _sqrt_match returning the specific no-match value [] for an additive expression with a negative rational square.
  - Returning the related expression containing sqrt(4 + I) unchanged.
  - Preservation of the separate successful denesting path.
- **sympy__sympy-19637** (none (1))
  - A no-space input to kernS avoids the unbound kern reference and returns the correctly parsed expression.
- **sympy__sympy-20590** (main only (3))
  - Affected immutable instances reject assignment of undeclared attributes.

## Without a verdict

- **django__django-15569** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: dj...
- **scikit-learn__scikit-learn-10297** — the agent changed 1 file(s) that already existed, so the before-the-fix run is not a fact about this pull request: sk...
