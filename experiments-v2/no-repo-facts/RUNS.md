# Run status, per pull request

Last run in this table: 2026-09-26 10:52 UTC.

- **70** instances across **12** repositories
- **46/70** fail-to-pass, of those that reached a verdict
- **45** measured for changed-line coverage: **mean 91%** per test, median 100%
- **75%** of the changed lines those tests were measured against (182/244, pooled)
- **36%** of every source line all 70 patches change (182/508) -- a fixed denominator, so this is the figure that compares across arms
- \$6.43 and 89.6M tokens in total
- **40** of these were sent a second-chance message after stopping with nothing to score, and **17** of them ended fail-to-pass; the other 30 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 2 | 1 | 1 | 0 | **added by the flag** |
| `collects_nothing+loop_open` | 1 | 1 | 0 | 0 | **added by the flag** |
| `loop_open` | 20 | 10 | 10 | 0 | from `require-tools` |
| `no_test` | 3 | 3 | 0 | 0 | from `require-tools` |
| `no_test+loop_open` | 2 | 1 | 1 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 12 | 1 | 11 | 0 | **added by the flag** |

Of the **15** refused for a reason the flag itself adds, **3** ended fail-to-pass.

Every row was produced with the same configuration: **`no-repo-facts`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 34 | `run` x16, `run_tests` x5, `write_file` x5, `coverage` x2, `verify` x2, `mutation` x1 | tangential (2) | none (1) | poor (2) | 2026-09-26 06:39 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 3/3 | 3/3 | 32 | `run` x17, `run_tests` x5, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:35 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 30 | `run` x14, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3, `run_tests` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:34 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 3/4 | 4/4 | 35 | `run` x19, `verify` x4, `coverage` x3, `write_file` x3, `run_tests` x2, `mutation` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:32 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | YES | 100% (1/1) | — | — | 41 | `run` x29, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 06:32 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 76 | `run` x36, `write_file` x22, `run_tests` x6, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 06:46 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 91 | `run` x32, `write_file` x20, `run_tests` x15, `coverage` x8, `verify` x6, `mutation` x3 | — | — | — | 2026-09-26 06:56 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 71 | `run` x53, `write_file` x8 | — | — | — | 2026-09-26 06:51 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 76 | `run` x30, `run_tests` x16, `write_file` x16, `verify` x4, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 06:56 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 85 | `run` x58, `write_file` x17 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:57 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 31 | `run` x17, `run_tests` x3, `verify` x3, `coverage` x2, `mutation` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:47 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 48 | `run` x30, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 06:54 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 78 | `run` x27, `run_tests` x16, `write_file` x15, `verify` x7, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-26 07:08 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 55 | `run` x26, `run_tests` x7, `write_file` x7, `verify` x5, `mutation` x4, `coverage` x3 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 07:01 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 31 | `run` x17, `run_tests` x4, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:54 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | NO | — | — | — | 72 | `run` x56, `write_file` x7, `run_tests` x1 | — | — | — | 2026-09-26 07:06 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | YES | 100% (4/4) | 2/2 | 2/2 | 40 | `run` x15, `run_tests` x5, `verify` x5, `write_file` x5, `coverage` x4, `mutation` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:06 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 30 | `run` x15, `run_tests` x4, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | close (4) | complete (5) | acceptable (3) | 2026-09-26 07:02 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 41 | `run` x17, `run_tests` x5, `write_file` x5, `coverage` x4, `verify` x4, `mutation` x3 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:08 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 43% (3/7) | 0/6 | 2/6 | 80 | `run` x41, `write_file` x12, `run_tests` x9, `verify` x8, `coverage` x3, `mutation` x1 | tangential (2) | none (1) | reject (1) | 2026-09-26 07:22 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 38 | `run` x26, `run_tests` x4, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | equivalent (5) | complete (5) | exemplary (5) | 2026-09-26 07:06 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 46 | `run` x26, `run_tests` x5, `write_file` x5, `verify` x4, `mutation` x2, `coverage` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:13 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 33 | `run` x15, `run_tests` x4, `mutation` x3, `verify` x3, `write_file` x3, `coverage` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 07:14 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 66 | `run` x50, `write_file` x5, `run_tests` x1 | — | — | — | 2026-09-26 07:18 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 35 | `run` x21, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:14 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | YES | — | — | — | 80 | `run` x70  (+1 edit reverted) | not measured: rescored offline | — | — | 2026-09-26 07:26 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | NO | — | — | — | 65 | `run` x25, `write_file` x14, `run_tests` x6, `coverage` x4, `mutation` x4, `verify` x4 | — | — | — | 2026-09-26 07:27 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 48 | `run` x21, `write_file` x9, `run_tests` x8, `coverage` x2, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 07:26 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 57 | `run` x27, `verify` x9, `write_file` x9, `coverage` x4, `mutation` x2, `run_tests` x2 | — | — | — | 2026-09-26 07:29 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 24 | `run` x13, `run_tests` x4, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:21 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 48 | `run` x19, `run_tests` x6, `write_file` x6, `verify` x5, `coverage` x4, `mutation` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:29 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 24 | `run` x12, `coverage` x2, `run_tests` x2, `verify` x2, `write_file` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:31 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 49 | `run` x28, `run_tests` x4, `verify` x4, `coverage` x3, `write_file` x3, `mutation` x2 | narrower (3) | none (1) | reject (1) | 2026-09-26 07:38 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 46 | `run` x28, `verify` x4, `write_file` x4, `run_tests` x3, `coverage` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:17 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 30 | `run` x13, `coverage` x3, `run_tests` x3, `verify` x3, `write_file` x3, `mutation` x2 | tangential (2) | main only (3) | poor (2) | 2026-09-26 09:20 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 63 | `run` x26, `write_file` x11, `run_tests` x9, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 09:26 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 73 | `run` x34, `write_file` x13, `run_tests` x12, `verify` x4, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 09:26 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 58 | `run` x46, `write_file` x4  (+1 edit reverted) | equivalent (5) | complete (5) | exemplary (5) | 2026-09-26 09:18 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 100% (3/3) | 1/1 | 0/1 | 38 | `run` x23, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | close (4) | main only (3) | poor (2) | 2026-09-26 09:12 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 46 | `run` x22, `write_file` x5, `run_tests` x4, `verify` x4, `coverage` x3, `mutation` x3 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 09:18 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 25 | `run` x10, `run_tests` x3, `verify` x3, `coverage` x2, `write_file` x2, `mutation` x1 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:19 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 28 | `run` x18, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:15 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | YES | 83% (5/6) | 2/6 | 4/6 | 76 | `run` x21, `write_file` x17, `verify` x12, `run_tests` x11, `coverage` x4, `mutation` x1 | tangential (2) | minor only (2) | poor (2) | 2026-09-26 09:40 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 29 | `run` x14, `run_tests` x4, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:37 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 62 | `run` x46, `write_file` x10 | — | — | — | 2026-09-26 09:47 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | NO | — | — | — | 63 | `run` x20, `write_file` x18, `run_tests` x9, `verify` x6, `mutation` x2, `coverage` x1 | — | — | — | 2026-09-26 09:42 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 31 | `run` x17, `write_file` x4, `run_tests` x3, `coverage` x2, `verify` x2, `mutation` x1 | equivalent (5) | main only (3) | poor (2) | 2026-09-26 09:30 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 79 | `run` x33, `write_file` x20, `run_tests` x13, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 09:40 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 32 | `run` x18, `verify` x4, `write_file` x4, `run_tests` x2, `coverage` x1, `mutation` x1 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:36 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 51 | `run` x13, `write_file` x12, `run_tests` x10, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 09:54 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 70 | `run` x49, `write_file` x7, `run_tests` x5 | — | — | — | 2026-09-26 09:51 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 23 | `run` x13, `mutation` x2, `run_tests` x2, `verify` x2, `coverage` x1, `write_file` x1 | close (4) | complete (5) | poor (2) | 2026-09-26 09:49 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 20% (2/10) | 1/10 | 6/10 | 47 | `run` x21, `verify` x6, `coverage` x5, `write_file` x5, `mutation` x3, `run_tests` x3 | tangential (2) | none (1) | poor (2) | 2026-09-26 09:52 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 60% (28/47) | 1/10 | 4/10 | 46 | `run` x22, `verify` x5, `write_file` x5, `coverage` x4, `mutation` x2, `run_tests` x1 | tangential (2) | none (1) | poor (2) | 2026-09-26 10:02 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 88% (14/16) | 8/10 | 8/10 | 39 | `run` x20, `run_tests` x5, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x1 | equivalent (5) | nearly complete (4) | good (4) | 2026-09-26 09:53 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 63 | `run` x32, `write_file` x10, `run_tests` x6, `verify` x4, `coverage` x3, `mutation` x1 | — | — | — | 2026-09-26 10:05 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 67 | `run` x23, `write_file` x16, `run_tests` x12, `verify` x9 | — | — | — | 2026-09-26 10:05 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | YES | 100% (2/2) | 6/8 | 6/8 | 56 | `run` x35, `write_file` x7, `run_tests` x5, `verify` x3, `coverage` x2, `mutation` x2  (+1 edit reverted) | narrower (3) | main only (3) | poor (2) | 2026-09-26 10:10 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 62 | `run` x20, `write_file` x13, `run_tests` x11, `coverage` x5, `mutation` x3, `verify` x3 | — | — | — | 2026-09-26 10:16 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 43% (16/37) | 1/10 | 5/10 | 66 | `run` x26, `write_file` x11, `verify` x9, `run_tests` x8, `coverage` x5, `mutation` x1  (+1 edit reverted) | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:24 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 57 | `run` x19, `run_tests` x10, `write_file` x8, `coverage` x5, `verify` x5, `mutation` x1 | — | — | — | 2026-09-26 10:15 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 5/5 | 5/5 | 31 | `run` x17, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | close (4) | main only (3) | reject (1) | 2026-09-26 10:16 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | NO | — | — | — | 67 | `run` x26, `run_tests` x14, `write_file` x7, `coverage` x6, `verify` x4, `mutation` x2  (+1 edit reverted) | — | — | — | 2026-09-26 10:29 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 39 | `run` x21, `verify` x4, `write_file` x4, `mutation` x3, `run_tests` x3, `coverage` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 18 | `run` x9, `run_tests` x3, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:19 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | YES | 100% (2/2) | 1/2 | 1/2 | 64 | `run` x34, `write_file` x11, `run_tests` x8, `mutation` x3, `verify` x3, `coverage` x2 | tangential (2) | main only (3) | poor (2) | 2026-09-26 10:35 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 26 | `run` x17, `run_tests` x3, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 44 | `run` x19, `run_tests` x6, `verify` x4, `write_file` x4, `coverage` x3, `mutation` x2 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 10:48 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 36 | `run` x19, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | NO | — | — | — | 84 | `run` x49, `write_file` x15, `verify` x6, `run_tests` x3, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 10:52 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (none (1))
  - Repeated unparenthesized division such as "km/s/Mpc" accumulates all later units in the denominator.
  - "10+3J/m/s/kpc2" parses as 10^3 J divided by m and kpc^2, with the correct unit equivalence.
  - "10-7J/s/kpc2" parses as 10^-7 J divided by s and kpc^2, with the correct unit equivalence.
- **astropy__astropy-14539** (main only (3))
  - Different values in Q-format VLA columns must be detected and reported with the correct per-row and aggregate results.
- **astropy__astropy-14598** (nearly complete (4))
  - Preserve double single quotes followed by a space and then additional text.
- **astropy__astropy-7606** (nearly complete (4))
  - UnrecognizedUnit equality involving subclasses follows the new concrete-type check rather than the old broad UnrecognizedUnit check.
- **django__django-13012** (main only (3))
  - A wrapper around a non-constant expression with group-by columns returns the wrapped expression's group-by columns.
- **django__django-13023** (main only (3))
  - Other non-convertible TypeError inputs such as lists, sets, objects, and complex numbers.
  - Malformed sequence values that cause ValueError, such as an empty tuple.
- **django__django-13590** (nearly complete (4))
  - List lookup values continue to be reconstructed while preserving their type and values.
- **django__django-13794** (main only (3))
  - Two lazy string proxies can be concatenated.
  - Lazy proxies with non-string result classes can be added, as demonstrated by integer-valued proxies.
- **django__django-14559** (main only (3))
  - The return value is accumulated across multiple update batches.
  - Duplicate objects are counted once in one batch and once per batch across separate batches.
- **django__django-14608** (main only (3))
  - Non-form errors added by maximum-form-count validation render with the nonform CSS class.
  - Non-form errors added by minimum-form-count validation render with the nonform CSS class.
- **django__django-14725** (none (1))
  - A model formset with edit_only=True does not create objects from extra submitted forms.
  - A model formset with edit_only=True still saves changes to existing objects.
  - An inline formset with edit_only=True does not create new inline objects while still saving changes to existing children.
- **django__django-14792** (main only (3))
  - Named timezone objects retain their timezone name.
  - Timezone objects with no tzname(None) value fall back to str(timezone).
- **django__django-14915** (main only (3))
  - A wrapper's hash matches the hash of its raw wrapped value for lookup against a dictionary keyed by that raw value; the generated test uses the wrapper itself as the dictionary key.
  - For distinct wrapped primary keys, the resulting hashes are unequal; the generated test has no assertion comparing those hashes.
- **django__django-16667** (main only (3))
  - The resulting pseudo-date is rejected by form validation with an "Enter a valid date." error.
- **matplotlib__matplotlib-20676** (main only (3))
  - Horizontal edge handles are initially positioned at the x-axis bounds.
  - Vertical edge handles are initially positioned at the y-axis bounds.
  - After interaction, edge handles update to the selected extents without changing either axis's bounds.
- **matplotlib__matplotlib-20859** (none (1))
  - A SubFigure is accepted as a legend parent and the resulting legend is associated with that SubFigure.
  - A regular Figure remains accepted as a legend parent after the check is generalized to FigureBase.
  - An unsupported non-Axes, non-FigureBase parent is rejected with a TypeError whose message refers to FigureBase.
- **matplotlib__matplotlib-24870** (main only (3))
  - Regular contour with a Python boolean list.
  - Regular contourf with a Python boolean list.
  - Regular contour with a masked boolean array.
- **matplotlib__matplotlib-24970** (main only (3))
  - Unsigned integer inputs are converted to signed indices before sentinel indexing so the uint8 lookup produces the expected colormap result.
  - The existing lookup behaviour for int, float16, and float inputs remains correct after the cast is moved outside the float-only branch.
- **psf__requests-2931** (main only (3))
  - `prepare_url` converts string or bytes query parameters to native text before appending them to the URL.
- **pydata__xarray-2905** (main only (3))
  - Pandas Series, Index, and DataFrame inputs continue to be converted to their values data.
- **pydata__xarray-4687** (minor only (2))
  - keep_attrs=True preserves the attributes of x on the where result.
- **pydata__xarray-6744** (main only (3))
  - center=True with even window size 2
  - center=True with window sizes 1 and 7
  - center=False with window sizes 1, 2, and 7
- **pytest-dev__pytest-6197** (main only (3))
  - A `src` directory is not added to `sys.path`, so a package under it remains unimportable.
- **scikit-learn__scikit-learn-10297** (main only (3))
  - The expected cv_values_ shape for one-dimensional y.
  - The multi-target y branch and its expected cv_values_ shape.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python-domain annotation unparser renders an empty tuple as explicit "(" and ")" punctuation inside Tuple[()].
  - The Python AST string unparser returns "()" for an empty tuple AST.
- **sphinx-doc__sphinx-7590** (none (1))
  - Integer literals with user-defined suffixes are parsed and receive the correct user-defined-literal AST and mangled ID.
  - Decimal floating-point literals with user-defined suffixes, including the reported `6.62607015e-34q_J` case, are parsed and mangled correctly.
  - Hexadecimal floating-point literals with user-defined suffixes are parsed and mangled correctly.
- **sphinx-doc__sphinx-7757** (nearly complete (4))
  - Later positional-or-keyword parameters after `/` are offset correctly when there is more than one such parameter, for example `(a, b=0, /, c=1, d=2)`.
- **sphinx-doc__sphinx-9591** (main only (3))
  - The symmetric typed Python attribute declaration case.
- **sympy__sympy-12489** (main only (3))
  - Multiple positional cycle arguments construct an instance of the requested subclass.
  - Construction from an existing permutation with size adjustment uses the requested subclass.
  - __add__ returns an instance of the subclass receiver.
- **sympy__sympy-14976** (main only (3))
  - nsolve preserves the requested full precision when solving an equation containing a Rational.
- **sympy__sympy-16450** (nearly complete (4))
  - Preservation of additional assumptions forwarded through assumptions0, such as even=True or odd=True.
- **sympy__sympy-17318** (main only (3))
  - The reported expression remains denestable and produces I.
  - An expression that genuinely cannot be denested is returned unchanged.
- **sympy__sympy-19637** (none (1))
  - The no-space input must produce the exact parsed expression `2*x/(x-1)`.
  - The spaced input must produce its correct parsed expression rather than merely a non-`None` result.
