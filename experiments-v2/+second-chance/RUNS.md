# Run status, per pull request

Last run in this table: 2026-09-26 10:51 UTC.

- **70** instances across **12** repositories
- **47/70** fail-to-pass, of those that reached a verdict
- **47** measured for changed-line coverage: **mean 90%** per test, median 100%
- **75%** of the changed lines those tests were measured against (195/259, pooled)
- **38%** of every source line all 70 patches change (195/508) -- a fixed denominator, so this is the figure that compares across arms
- \$5.30 and 73.6M tokens in total
- **37** of these were sent a second-chance message after stopping with nothing to score, and **14** of them ended fail-to-pass; the other 33 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `loop_open` | 18 | 13 | 5 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 18 | 1 | 17 | 0 | **added by the flag** |
| `passes_at_base+loop_open+reads_source` | 1 | 0 | 1 | 0 | **added by the flag** |

Of the **19** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 55 | `run` x15, `run_tests` x10, `write_file` x10, `coverage` x6, `verify` x3, `mutation` x2 | — | — | — | 2026-09-26 06:48 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 3/3 | 3/3 | 32 | `run` x16, `run_tests` x4, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:33 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 23 | `run` x7, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:34 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 100% (6/6) | 3/4 | 4/4 | 26 | `run` x11, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:30 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | NO | — | — | — | 71 | `run` x31, `write_file` x19, `verify` x7, `coverage` x3, `mutation` x3, `run_tests` x1 | — | — | — | 2026-09-26 06:48 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 69 | `run` x30, `write_file` x18, `run_tests` x11, `verify` x3 | — | — | — | 2026-09-26 06:44 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 66 | `run` x33, `write_file` x18, `run_tests` x8 | — | — | — | 2026-09-26 06:46 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 100% (5/5) | 2/3 | 2/3 | 33 | `run` x17, `run_tests` x4, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x1 | close (4) | nearly complete (4) | poor (2) | 2026-09-26 06:40 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 56 | `run` x22, `write_file` x16, `run_tests` x6, `verify` x5 | — | — | — | 2026-09-26 06:48 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 38 | `run` x21, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:46 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 20 | `run` x8, `write_file` x3, `coverage` x2, `run_tests` x2, `verify` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:43 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 73 | `run` x30, `run_tests` x13, `write_file` x11, `verify` x6, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 06:59 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 50 | `run` x22, `run_tests` x10, `write_file` x10 | — | — | — | 2026-09-26 06:58 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 20 | `run` x8, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | narrower (3) | complete (5) | poor (2) | 2026-09-26 06:51 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 32 | `run` x22, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:54 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 39 | `run` x18, `write_file` x6, `run_tests` x4, `verify` x4, `coverage` x2, `mutation` x1 | close (4) | main only (3) | acceptable (3) | 2026-09-26 06:59 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | YES | 25% (1/4) | 0/2 | 2/2 | 42 | `run` x14, `verify` x8, `write_file` x8, `coverage` x3, `run_tests` x3, `mutation` x1  (+1 edit reverted) | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 07:04 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 31 | `run` x13, `run_tests` x7, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 07:01 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 43 | `run` x25, `run_tests` x7, `write_file` x6, `coverage` x1, `mutation` x1, `verify` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:05 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 74 | `write_file` x25, `run` x20, `verify` x14, `run_tests` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 07:18 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 36 | `run` x14, `run_tests` x6, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x2  (+1 edit reverted) | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:08 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 0/1 | 1/1 | 29 | `run` x14, `run_tests` x4, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:08 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 24 | `run` x12, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | main only (3) | acceptable (3) | 2026-09-26 07:11 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 64 | `run` x28, `write_file` x15, `run_tests` x5, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-26 07:22 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 34 | `run` x17, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | equivalent (5) | nearly complete (4) | acceptable (3) | 2026-09-26 07:14 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 88 | `run` x30, `write_file` x20, `run_tests` x18, `verify` x6, `coverage` x4, `mutation` x2 | — | — | — | 2026-09-26 07:28 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 1/1 | 1/1 | 27 | `run` x16, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x1 | close (4) | complete (5) | acceptable (3) | 2026-09-26 07:15 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 67 | `write_file` x17, `run` x15, `run_tests` x14, `coverage` x5, `mutation` x5, `verify` x4 | — | — | — | 2026-09-26 07:33 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 67% (12/18) | 1/10 | 1/10 | 36 | `run` x7, `write_file` x7, `coverage` x5, `verify` x5, `run_tests` x4, `mutation` x3 | narrower (3) | minor only (2) | good (4) | 2026-09-26 07:28 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 31 | `run` x15, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3, `run_tests` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:23 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | no mutants | no mutants | 28 | `run` x12, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 07:28 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 22 | `run` x13, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1 | narrower (3) | complete (5) | good (4) | 2026-09-26 07:30 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 45 | `run` x24, `run_tests` x5, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x2 | narrower (3) | none (1) | poor (2) | 2026-09-26 07:36 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 76% (13/17) | no mutants | no mutants | 33 | `run` x17, `verify` x4, `run_tests` x3, `coverage` x2, `write_file` x2, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:15 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 2/10 | 32 | `run` x11, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | tangential (2) | main only (3) | acceptable (3) | 2026-09-26 07:39 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 50 | `run` x13, `write_file` x12, `run_tests` x7, `verify` x7, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 09:23 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 52 | `run` x17, `run_tests` x10, `write_file` x10, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 09:23 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 23 | `run` x7, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:38 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 100% (3/3) | 0/1 | 0/1 | 33 | `run` x14, `verify` x4, `write_file` x4, `coverage` x3, `run_tests` x3, `mutation` x2 | narrower (3) | nearly complete (4) | poor (2) | 2026-09-26 09:13 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 52 | `run` x18, `write_file` x10, `run_tests` x7, `verify` x5, `coverage` x4, `mutation` x1 | equivalent (5) | main only (3) | good (4) | 2026-09-26 09:23 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 22 | `run` x10, `run_tests` x3, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:19 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 19 | `run` x7, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:11 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 65 | `run` x19, `write_file` x14, `verify` x11, `run_tests` x10, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-26 09:28 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 9/10 | 14 | `run` x5, `run_tests` x2, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | narrower (3) | nearly complete (4) | good (4) | 2026-09-26 09:30 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 65 | `run` x26, `write_file` x12, `run_tests` x10, `verify` x4, `mutation` x3, `coverage` x2  (+1 edit reverted) | — | — | — | 2026-09-26 09:50 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 26 | `run` x8, `run_tests` x4, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | equivalent (5) | complete (5) | acceptable (3) | 2026-09-26 09:30 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 24 | `run` x13, `run_tests` x2, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1 | equivalent (5) | main only (3) | poor (2) | 2026-09-26 09:28 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 67 | `run` x18, `write_file` x16, `run_tests` x13, `verify` x5, `coverage` x4, `mutation` x4 | — | — | — | 2026-09-26 09:39 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 37 | `run` x16, `run_tests` x5, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x2 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 09:43 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 49 | `run` x14, `write_file` x14, `run_tests` x12 | — | — | — | 2026-09-26 09:51 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 2/5 | 2/5 | 68 | `run` x20, `verify` x12, `write_file` x12, `coverage` x8, `run_tests` x6, `mutation` x1 | narrower (3) | none (1) | poor (2) | 2026-09-26 09:58 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 29 | `run` x14, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | close (4) | none (1) | acceptable (3) | 2026-09-26 09:50 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 2/10 | 6/10 | 50 | `run` x23, `verify` x7, `write_file` x7, `coverage` x3, `run_tests` x3, `mutation` x1 | tangential (2) | none (1) | poor (2) | 2026-09-26 09:49 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 62% (29/47) | 1/10 | 4/10 | 41 | `run` x19, `run_tests` x6, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x2 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:58 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 88% (14/16) | 8/10 | 8/10 | 36 | `run` x15, `run_tests` x4, `write_file` x4, `coverage` x3, `mutation` x3, `verify` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:54 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 69 | `run` x27, `write_file` x13, `run_tests` x11, `verify` x5, `coverage` x3, `mutation` x3 | — | — | — | 2026-09-26 10:11 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 74 | `run` x39, `run_tests` x10, `write_file` x8, `coverage` x4, `verify` x4, `mutation` x1  (+2 edits reverted) | — | — | — | 2026-09-26 10:06 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 75 | `run` x23, `write_file` x20, `run_tests` x14, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-26 10:15 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | YES | 100% (3/3) | 1/4 | 3/4 | 34 | `run` x13, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:03 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 38% (14/37) | 1/10 | 5/10 | 57 | `run` x18, `write_file` x11, `coverage` x8, `verify` x8, `run_tests` x4, `mutation` x2 | narrower (3) | main only (3) | exemplary (5) | 2026-09-26 10:25 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 54 | `run` x23, `run_tests` x9, `coverage` x4, `write_file` x4, `mutation` x2, `verify` x2 | — | — | — | 2026-09-26 10:12 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 5/5 | 5/5 | 66 | `run` x21, `write_file` x15, `verify` x11, `run_tests` x5, `coverage` x4, `mutation` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 10:30 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 3/3 | 3/3 | 28 | `run` x8, `write_file` x5, `verify` x4, `coverage` x3, `mutation` x3, `run_tests` x3 | narrower (3) | complete (5) | good (4) | 2026-09-26 10:23 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 1/3 | 3/3 | 30 | `run` x16, `run_tests` x3, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2  (+1 edit reverted) | narrower (3) | main only (3) | good (4) | 2026-09-26 10:38 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 31 | `run` x17, `write_file` x4, `coverage` x2, `mutation` x2, `run_tests` x2, `verify` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:24 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 57 | `run` x20, `write_file` x11, `run_tests` x10, `coverage` x3, `verify` x3, `mutation` x2 | — | — | — | 2026-09-26 10:33 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 2/3 | 2/3 | 21 | `run` x12, `run_tests` x2, `verify` x2, `coverage` x1, `mutation` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 49 | `run` x22, `run_tests` x5, `verify` x5, `write_file` x5, `coverage` x3, `mutation` x3 | narrower (3) | none (1) | poor (2) | 2026-09-26 10:51 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | no mutants | no mutants | 31 | `run` x13, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | close (4) | main only (3) | good (4) | 2026-09-26 10:47 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | NO | — | — | — | 57 | `run` x18, `write_file` x16, `run_tests` x8, `verify` x6, `coverage` x2 | — | — | — | 2026-09-26 10:48 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (main only (3))
  - Unequal Q-format VLA elements are reported with the correct differing values and difference statistics.
- **astropy__astropy-14598** (nearly complete (4))
  - A long FITS Card value containing doubled single quotes followed by a space and text round-trips unchanged.
- **astropy__astropy-7606** (nearly complete (4))
  - The type(self) change is not exercised with an UnrecognizedUnit subclass or another differing UnrecognizedUnit type.
- **django__django-12308** (nearly complete (4))
  - Truthy JSON scalar strings are displayed as JSON strings.
- **django__django-13012** (main only (3))
  - A wrapper around a non-constant expression preserves the wrapped expression's group-by columns.
- **django__django-13023** (main only (3))
  - Other unsupported TypeError inputs beyond the two dictionary examples.
  - Values whose Decimal conversion raises ValueError.
  - Values whose Decimal conversion raises decimal.InvalidOperation.
- **django__django-13794** (nearly complete (4))
  - Addition works when both operands are lazy values, including non-string lazy values.
- **django__django-14534** (main only (3))
  - The exact custom-ID result for the second CheckboxSelectMultiple option.
  - The no-ID (`auto_id=False`) branch returning None.
- **django__django-14559** (minor only (2))
  - A non-empty bulk_update() returns the sum of rows matched across all update batches.
  - Duplicate objects in a single batch count only once.
  - Duplicate objects split across batches contribute once per batch.
- **django__django-14608** (main only (3))
  - The initialized ErrorList path used by accumulated form-count validation errors carries the nonform class.
- **django__django-14792** (main only (3))
  - A fixed-offset zoneinfo timezone such as Etc/GMT-10 returns its offset "+10" for use by database timezone conversion.
  - A named pytz timezone such as Europe/Madrid retains its timezone name.
  - A named zoneinfo timezone such as Europe/Madrid retains its timezone name.
- **django__django-14915** (main only (3))
  - A ModelChoiceIteratorValue hashes compatibly with its raw wrapped value for lookups in mappings keyed by that value, such as {1: ...}.
- **django__django-15569** (nearly complete (4))
  - Unregistering a lookup using an explicitly supplied lookup_name clears the cached lookup mapping.
- **django__django-16560** (minor only (2))
  - ExclusionConstraint accepts and stores a supplied violation_error_code.
  - CheckConstraint.validate() raises a ValidationError with the custom code.
  - Supported UniqueConstraint validation paths raise a ValidationError with the custom code.
- **django__django-16667** (main only (3))
  - A DateField form using SelectDateWidget handles that fallback as a normal invalid-date submission, returning False with an "Enter a valid date." error instead of crashing.
- **matplotlib__matplotlib-20859** (none (1))
  - A SubFigure, as a FigureBase parent, can create a legend that is associated with that SubFigure.
  - A regular Figure continues to be accepted as a legend parent.
  - An Axes continues to be accepted as a legend parent.
- **matplotlib__matplotlib-24870** (main only (3))
  - Triangular tricontour with boolean data defaults to the single level [0.5].
  - Triangular tricontourf with boolean data defaults to the levels [0, 0.5, 1].
- **matplotlib__matplotlib-24970** (main only (3))
  - Colormap output remains correct for uint8, int, float16, and float inputs after the common integer cast.
- **psf__requests-2931** (nearly complete (4))
  - String or bytes URL parameters are normalized with `to_native_string` before URL query construction.
- **pydata__xarray-2905** (main only (3))
  - Pandas Series, Index, and DataFrame inputs continue to be unwrapped to their values data.
- **pydata__xarray-4075** (main only (3))
  - The public `sum_of_weights()` method returns an integer count for boolean weights instead of a boolean dot-product result.
- **pydata__xarray-6744** (nearly complete (4))
  - The additional size-1, size-2, and size-7 parameter cases exercised by the developer test.
- **pytest-dev__pytest-6197** (main only (3))
  - Pytest does not add src to sys.path or make a package under src importable during collection.
- **scikit-learn__scikit-learn-10297** (minor only (2))
  - Acceptance of the store_cv_values keyword as the fixed constructor behaviour.
  - The documented cv_values_ shape for one-dimensional labels.
  - The documented cv_values_ shape for multi-target labels.
- **scikit-learn__scikit-learn-14087** (none (1))
  - With refit=False and effective OVR classification from multi_class='auto', coefficient selection uses the OVR coefficient-path shape without raising IndexError.
  - With refit=False and a non-elasticnet penalty, l1_ratio_ is handled as None without indexing unavailable l1-ratio values.
- **scikit-learn__scikit-learn-9288** (none (1))
  - Exact n_jobs-independent KMeans results: the np.allclose assertions allow the reported small discrepancy and do not pin exact clustering equality.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python domain renders `Tuple[()]` with explicit `(` and `)` punctuation nodes instead of popping from an empty list.
  - The Python AST unparser renders an empty tuple as the string `()`.
- **sphinx-doc__sphinx-7590** (main only (3))
  - C++ hexadecimal floating-point literals with user-defined suffixes are accepted.
  - UDL ASTs receive the expected mangled IDs, including correct handling of standard literal suffixes.
  - UDL identifiers are rendered and referenced as `operator""<identifier>`.
- **sphinx-doc__sphinx-9658** (main only (3))
  - `_MockObject` initializes `__qualname__` consistently from its `__name__`.
  - `restify` renders mocked classes with their complete qualified name.
  - `stringify` renders mocked classes with their complete qualified name.
- **sympy__sympy-12489** (main only (3))
  - List/tuple, integer, Cycle, and multi-argument constructor paths return the subclass type.
  - Passing an existing subclass to the constructor, including size adjustment, retains the subclass type.
  - `__add__` on a subclass returns a subclass instance.
- **sympy__sympy-14976** (main only (3))
  - The nsolve path preserves arbitrary precision for a rational target.
- **sympy__sympy-16450** (main only (3))
  - The full assumptions0 set is preserved, including infinite=False and the remaining derived or copied assumptions such as real, nonzero, zero, complex, hermitian, and other possible assumptions such as rational, prime, even, or odd.
- **sympy__sympy-19637** (none (1))
  - A parenthesized expression with no spaces is parsed successfully and yields 2*x/(x-1) instead of raising UnboundLocalError.
  - A parenthesized expression containing spaces continues to parse successfully through the space-handling branch.
- **sympy__sympy-20590** (main only (3))
  - Slotted SymPy instances reject arbitrary attribute assignment.
