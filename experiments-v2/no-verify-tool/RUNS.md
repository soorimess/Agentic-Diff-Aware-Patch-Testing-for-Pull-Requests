# Run status, per pull request

Last run in this table: 2026-09-26 10:46 UTC.

- **70** instances across **12** repositories
- **38/69** fail-to-pass, of those that reached a verdict
- **38** measured for changed-line coverage: **mean 83%** per test, median 100%
- **71%** of the changed lines those tests were measured against (147/208, pooled)
- **29%** of every source line all 70 patches change (147/508) -- a fixed denominator, so this is the figure that compares across arms
- \$2.47 and 33.8M tokens in total
- **22** of these were sent a second-chance message after stopping with nothing to score, and **1** of them ended fail-to-pass; the other 48 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 1 | 0 | 0 | 1 | **added by the flag** |
| `no_test` | 1 | 0 | 1 | 0 | from `require-tools` |
| `passes_at_base` | 20 | 1 | 19 | 0 | **added by the flag** |

Of the **21** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`no-verify-tool+coverage-tool+mutation-tool+require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

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
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 41 | `run` x11, `run_tests` x10, `write_file` x10 | — | — | — | 2026-09-26 06:45 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | NO | — | — | — | 38 | `run` x12, `write_file` x11, `run_tests` x9 | — | — | — | 2026-09-26 06:43 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 14 | `run` x8, `run_tests` x3, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:24 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 67% (4/6) | 0/9 | 9/9 | 20 | `run` x14, `run_tests` x2, `write_file` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 06:27 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 66 | `run` x44, `write_file` x14, `run_tests` x3 | — | — | — | 2026-09-26 06:43 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 52 | `run` x20, `write_file` x16, `run_tests` x9 | — | — | — | 2026-09-26 06:41 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 23 | `run` x13, `run_tests` x4, `write_file` x4 | — | — | — | 2026-09-26 06:29 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 60% (3/5) | 1/6 | 4/6 | 21 | `run` x16, `run_tests` x2, `write_file` x1 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 06:38 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 58 | `run` x19, `write_file` x18, `run_tests` x14 | — | — | — | 2026-09-26 06:49 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 34 | `run` x22, `run_tests` x5, `write_file` x5 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:45 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 16 | `run` x11, `run_tests` x2, `write_file` x1 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:43 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 26 | `run` x13, `run_tests` x4, `write_file` x3 | — | — | — | 2026-09-26 06:48 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 53 | `write_file` x17, `run` x16, `run_tests` x13 | — | — | — | 2026-09-26 06:57 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | NO | — | — | — | 38 | `write_file` x12, `run` x10, `run_tests` x10 | — | — | — | 2026-09-26 06:56 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 30 | `run` x22, `write_file` x4, `run_tests` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 06:52 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 24 | `run` x17, `run_tests` x3, `write_file` x2 | close (4) | main only (3) | acceptable (3) | 2026-09-26 06:54 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | YES | 100% (4/4) | 5/6 | 6/6 | 26 | `run` x18, `run_tests` x3, `write_file` x3 | narrower (3) | main only (3) | good (4) | 2026-09-26 06:58 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 16 | `run` x8, `run_tests` x3, `write_file` x3 | close (4) | complete (5) | acceptable (3) | 2026-09-26 06:58 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 23 | `run` x15, `run_tests` x3, `write_file` x3 | narrower (3) | nearly complete (4) | good (4) | 2026-09-26 07:00 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | YES | 57% (4/7) | 3/10 | 4/10 | 31 | `run` x18, `run_tests` x5, `write_file` x5 | tangential (2) | minor only (2) | good (4) | 2026-09-26 07:06 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | NO | — | — | — | 27 | `write_file` x9, `run_tests` x7, `run` x6 | — | — | — | 2026-09-26 07:05 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | YES | 100% (1/1) | 1/2 | 2/2 | 20 | `run` x16, `run_tests` x1, `write_file` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:06 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | NO | — | — | — | 17 | `run` x9, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-26 07:07 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 45 | `run` x14, `write_file` x13, `run_tests` x10 | — | — | — | 2026-09-26 07:16 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 26 | `run` x16, `run_tests` x4, `write_file` x4 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:11 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 22 | `run` x12, `run_tests` x4, `write_file` x4 | — | — | — | 2026-09-26 07:11 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 2/2 | 2/2 | 28 | `run` x18, `run_tests` x4, `write_file` x4 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 07:15 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 57 | `run` x25, `write_file` x15, `run_tests` x10 | — | — | — | 2026-09-26 07:28 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 44% (8/18) | 0/10 | 0/10 | 25 | `run` x8, `run_tests` x7, `write_file` x7 | narrower (3) | minor only (2) | acceptable (3) | 2026-09-26 07:21 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 13 | `run` x7, `run_tests` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:18 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 17 | `run` x12, `run_tests` x2, `write_file` x1 | close (4) | complete (5) | acceptable (3) | 2026-09-26 07:20 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 7/10 | 10/10 | 30 | `run` x22, `run_tests` x3, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:30 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 27 | `run` x16, `run_tests` x5, `write_file` x3 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 07:30 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 22 | `run` x9, `run_tests` x4, `write_file` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 07:36 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 1/10 | 1/10 | 31 | `run` x14, `run_tests` x7, `write_file` x7 | tangential (2) | main only (3) | acceptable (3) | 2026-09-26 09:16 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 20 | `run` x13, `run_tests` x3, `write_file` x2 | — | — | — | 2026-09-26 07:38 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 32 | `run` x22, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-26 09:11 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 14 | `run` x4, `run_tests` x4, `write_file` x4 | equivalent (5) | complete (5) | good (4) | 2026-09-26 07:36 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/2 | 0/2 | 21 | `run` x9, `run_tests` x5, `write_file` x5 | close (4) | nearly complete (4) | acceptable (3) | 2026-09-26 07:38 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 28 | `run` x12, `write_file` x7, `run_tests` x5 | equivalent (5) | nearly complete (4) | acceptable (3) | 2026-09-26 09:14 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 10 | `run` x4, `run_tests` x2, `write_file` x2 | narrower (3) | main only (3) | good (4) | 2026-09-26 09:12 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | NO | — | — | — | 12 | `run` x7, `run_tests` x2, `write_file` x1 | — | — | — | 2026-09-26 09:08 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 40 | `run` x14, `run_tests` x10, `write_file` x10 | — | — | — | 2026-09-26 09:22 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 11 | `run` x6, `run_tests` x2, `write_file` x1 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:27 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 25 | `run` x19, `run_tests` x2, `write_file` x2 | — | — | — | 2026-09-26 09:31 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 67% (2/3) | 1/7 | 7/7 | 25 | `run` x14, `run_tests` x4, `write_file` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:28 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 58 | `run` x18, `write_file` x18, `run_tests` x16 | — | — | — | 2026-09-26 09:37 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 46 | `run_tests` x15, `write_file` x15, `run` x9 | — | — | — | 2026-09-26 09:33 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 17 | `run` x11, `run_tests` x2, `write_file` x2 | — | — | — | 2026-09-26 09:31 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 39 | `run_tests` x11, `write_file` x11, `run` x9 | — | — | — | 2026-09-26 09:46 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 28 | `run` x14, `run_tests` x5, `write_file` x5 | — | — | — | 2026-09-26 09:40 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 20 | `run` x8, `write_file` x5, `run_tests` x4 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 09:43 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 3/10 | 6/10 | 21 | `run` x12, `run_tests` x4, `write_file` x3 | tangential (2) | none (1) | poor (2) | 2026-09-26 09:42 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (27/47) | 1/10 | 4/10 | 26 | `run` x16, `run_tests` x5, `write_file` x3 | narrower (3) | main only (3) | poor (2) | 2026-09-26 09:50 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 88% (14/16) | 8/10 | 8/10 | 18 | `run` x9, `run_tests` x4, `write_file` x3 | equivalent (5) | complete (5) | good (4) | 2026-09-26 09:47 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 63 | `write_file` x20, `run_tests` x18, `run` x17 | — | — | — | 2026-09-26 10:05 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 63 | `run` x20, `write_file` x18, `run_tests` x17 | — | — | — | 2026-09-26 10:04 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 53 | `run` x21, `run_tests` x13, `write_file` x13 | — | — | — | 2026-09-26 10:03 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 38 | `run` x13, `run_tests` x9, `write_file` x9 | — | — | — | 2026-09-26 10:03 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | NO | — | — | — | 21 | `run` x12, `run_tests` x3, `write_file` x2 | — | — | — | 2026-09-26 09:57 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 15 | `run` x7, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-26 09:58 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | NO | — | — | — | 41 | `run` x12, `run_tests` x12, `write_file` x12 | — | — | — | 2026-09-26 10:13 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 17 | `run` x9, `run_tests` x3, `write_file` x3 | narrower (3) | complete (5) | acceptable (3) | 2026-09-26 10:11 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 16 | `run` x12, `run_tests` x1, `write_file` x1 | close (4) | complete (5) | good (4) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 19 | `run` x13, `run_tests` x2, `write_file` x2 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:16 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 42 | `run` x22, `write_file` x8, `run_tests` x6 | — | — | — | 2026-09-26 10:22 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 13 | `run` x9, `run_tests` x1, `write_file` x1 | equivalent (5) | complete (5) | good (4) | 2026-09-26 10:46 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 22 | `run` x11, `run_tests` x5, `write_file` x3 | narrower (3) | none (1) | acceptable (3) | 2026-09-26 10:35 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 24 | `run` x13, `run_tests` x4, `write_file` x4 | close (4) | main only (3) | acceptable (3) | 2026-09-26 10:34 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 27 | `run` x20, `run_tests` x2, `write_file` x2 | narrower (3) | main only (3) | acceptable (3) | 2026-09-26 10:42 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14598** (nearly complete (4))
  - Preserve doubled single quotes when followed by a space and additional text.
- **astropy__astropy-7606** (main only (3))
  - UnitBase equality with an unparseable operand returning NotImplemented.
  - Successful same-name UnrecognizedUnit equality and rejection of other unit types based on the concrete type check.
- **django__django-12308** (nearly complete (4))
  - Invalid JSON input is caught and displayed through the ordinary fallback rather than raising.
- **django__django-13012** (main only (3))
  - A wrapped non-constant expression delegates get_group_by_cols() and preserves the wrapped expression's non-empty group-by columns.
- **django__django-13023** (main only (3))
  - Other unsupported values that cause TypeError, such as tuples, lists, sets, arbitrary objects, and complex numbers, are converted to the same ValidationError.
  - Other invalid conversion inputs, including nonnumeric strings and bytes, produce the field's ValidationError rather than a raw conversion exception.
- **django__django-13794** (main only (3))
  - The add filter concatenates two lazy strings.
  - Lazy proxy values representing integers can be added to produce 9.
- **django__django-14534** (main only (3))
  - A custom auto_id format is preserved in each CheckboxSelectMultiple subwidget's id_for_label.
  - When no id is supplied, the subwidget's id_for_label is None.
- **django__django-14559** (main only (3))
  - Counts from multiple update batches are accumulated.
  - Duplicate objects within one batch count the matched database row once.
  - Duplicate objects in separate batches contribute once per batch.
- **django__django-14608** (nearly complete (4))
  - Built-in formset form-count errors accumulated in the initially created non-form ErrorList render with the nonform CSS class.
- **django__django-14725** (minor only (2))
  - An edit-only model formset does not create objects from extra submitted forms
  - An edit-only model formset still saves changes to existing objects
  - An edit-only model formset does not create a submitted object outside its queryset
- **django__django-14792** (main only (3))
  - The unnamed `datetime.timezone` case returning `UTC+10:00`.
  - The custom-named `datetime.timezone` case preserving `Etc/GMT-10`.
  - Named pytz and zoneinfo timezones preserving names such as `Europe/Madrid`.
- **django__django-16560** (minor only (2))
  - ExclusionConstraint accepts and stores violation_error_code.
  - Constraint deconstruction includes a non-default violation_error_code.
  - Constraint equality distinguishes otherwise identical constraints with different violation_error_code values.
- **matplotlib__matplotlib-20676** (main only (3))
  - Horizontal interactive edge handles initially use the existing x bounds.
  - Vertical interactive edge handles initially use the existing y bounds.
  - After a horizontal interactive press/onmove, the x-axis bounds remain unchanged.
- **matplotlib__matplotlib-20859** (nearly complete (4))
  - An unsupported legend parent raises TypeError with a diagnostic referring to FigureBase.
- **matplotlib__matplotlib-24870** (main only (3))
  - Triangular tricontour() automatic levels.
  - Triangular tricontourf() automatic levels.
  - Regular contour() and contourf() with Python-list and masked-array boolean inputs.
- **matplotlib__matplotlib-24970** (main only (3))
  - A uint8 scalar zero produces the same correct colormap result as integer zero.
  - Signed-integer and floating-point scalar zero inputs preserve the expected colormap result after the common integer cast.
- **psf__requests-2931** (nearly complete (4))
  - Raw string or bytes query parameters are converted to a native string in `prepare_url` before query construction.
- **pydata__xarray-2905** (nearly complete (4))
  - A non-pandas object with a values property remains the object when used as Variable data during construction.
- **pydata__xarray-4075** (main only (3))
  - Boolean sum_of_weights() converts True weights to numeric counts.
- **pydata__xarray-6744** (main only (3))
  - center=True cases for sizes 1, 2, and 7, including the even-size centering case.
  - center=False trailing-window iteration for the tested sizes.
- **pylint-dev__pylint-7277** (main only (3))
  - Remove the first `sys.path` entry when it is `""`.
  - Remove the first `sys.path` entry when it is `"."`.
  - Remove the first `sys.path` entry when it is the current working directory.
- **scikit-learn__scikit-learn-9288** (main only (3))
  - The single-threaded and parallel KMeans execution branches produce identical cluster-label assignments for the same random_state.
- **sphinx-doc__sphinx-7462** (none (1))
  - The Python domain unparser renders an empty tuple annotation as the punctuation nodes "(" and ")".
  - The sphinx.pycode.ast unparser renders an empty tuple as the string "()".
- **sphinx-doc__sphinx-7590** (main only (3))
  - Hexadecimal floating-point user-defined literals are accepted.
  - Character user-defined literals are accepted with prefixes and escapes.
  - The complete integer, decimal-floating, and character suffix/prefix matrices are accepted.
- **sympy__sympy-19637** (none (1))
  - A no-space string "(2*x)/(x-1)" is parsed successfully as 2*x/(x-1) without UnboundLocalError.
  - A space-containing equivalent string continues through the space-handling branch and is parsed successfully as 2*x/(x-1).
- **sympy__sympy-20590** (main only (3))
  - Slotted SymPy instances reject assignment of undeclared attributes.
- **sympy__sympy-21596** (main only (3))
  - A solved imaginary-part condition over the integer domain filters out noninteger roots, producing FiniteSet(1).
  - A solved imaginary-part condition over Naturals0 respects that domain and produces FiniteSet(1).
  - An unsolved nonlinear imaginary condition is represented by an ImageSet over a ConditionSet.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
