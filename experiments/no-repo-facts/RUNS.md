# Run status, per pull request

Last run in this table: 2026-09-24 16:49 UTC.

- **70** instances across **12** repositories
- **31/63** fail-to-pass, of those that reached a verdict
- **31** measured for changed-line coverage: **mean 82%** per test, median 100%
- **66%** of the changed lines those tests were measured against (148/225, pooled)
- **29%** of every source line all 70 patches change (148/508) -- a fixed denominator, so this is the figure that compares across arms
- \$4.15 and 57.3M tokens in total
- **49** of these were sent a second-chance message after stopping with nothing to score, and **15** of them ended fail-to-pass; the other 21 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 1 | 0 | 0 | 1 | **added by the flag** |
| `collects_nothing+loop_open` | 7 | 1 | 0 | 6 | **added by the flag** |
| `loop_open` | 23 | 13 | 10 | 0 | from `require-tools` |
| `no_test+loop_open` | 1 | 1 | 0 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 17 | 0 | 17 | 0 | **added by the flag** |

Of the **25** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`no-repo-facts`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

The agent held the `mutation` tool in this run, so the mutants scored here are the **held-out half** of the pool &mdash; the agent was shown the other half and never these. That keeps the number a measurement rather than a mark for revising against the sample, but it also halves the denominator, so a per-instance figure is noisier than one from a run without the tool. The two are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 38 | `run` x15, `write_file` x8, `verify` x5, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 16:36 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | NO | — | — | — | 49 | `run` x26, `write_file` x9, `verify` x6, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:34 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 2/2 | 2/2 | 36 | `run` x23, `write_file` x4, `coverage` x2, `mutation` x2, `verify` x2 | same | partial | acceptable | 2026-09-24 16:29 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 3/4 | 4/4 | 32 | `run` x16, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x1 | same | partial | poor | 2026-09-24 16:32 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 42 | `run` x25, `write_file` x6, `run_tests` x3, `verify` x3, `coverage` x1 | — | — | — | 2026-09-24 16:30 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 34 | `run` x24, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1  (+1 edit reverted) | — | — | — | 2026-09-24 16:26 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 49 | `run` x33, `write_file` x9, `verify` x2 | — | — | — | 2026-09-24 16:29 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 57 | `run` x37, `write_file` x12, `verify` x1 | — | — | — | 2026-09-24 16:33 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 53 | `run` x38, `write_file` x6 | — | — | — | 2026-09-24 16:31 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | NO | — | — | — | 49 | `run` x25, `write_file` x9, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-24 16:33 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 28 | `run` x17, `run_tests` x2, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | narrower | partial | acceptable | 2026-09-24 16:25 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/9 | 7/9 | 49 | `run` x31, `write_file` x6, `verify` x4, `coverage` x1, `mutation` x1 | different | misses_the_point | poor | 2026-09-24 16:32 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 52 | `run` x17, `write_file` x12, `run_tests` x8, `verify` x6, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:31 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 5/5 | 4/5 | 37 | `run` x26, `write_file` x4 | broader | complete | acceptable | 2026-09-24 16:26 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | NO | — | — | — | 40 | `run` x29, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:27 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | NO | — | — | — | 61 | `run` x36, `write_file` x10, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:37 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 37 | `run` x18, `verify` x5, `write_file` x5, `coverage` x3, `mutation` x3 | — | — | — | 2026-09-24 16:29 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 3/3 | 3/3 | 49 | `run` x32, `write_file` x8, `verify` x2, `coverage` x1, `mutation` x1 | same | complete | acceptable | 2026-09-24 16:31 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 44 | `run` x31, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 16:27 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 51 | `run` x33, `write_file` x7, `verify` x5 | — | — | — | 2026-09-24 16:31 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 1/1 | 0/1 | 28 | `run` x17, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | broader | complete | acceptable | 2026-09-24 16:27 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 43 | `run` x30, `write_file` x8 | — | — | — | 2026-09-24 16:29 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | no mutants | no mutants | 41 | `run` x24, `write_file` x6, `verify` x3, `coverage` x2, `mutation` x2 | narrower | partial | acceptable | 2026-09-24 16:31 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 41 | `run` x24, `write_file` x5, `run_tests` x3, `verify` x1 | — | — | — | 2026-09-24 16:30 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | NO | — | — | — | 44 | `run` x28, `run_tests` x5, `write_file` x5, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 16:28 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 37 | `run` x19, `write_file` x5, `verify` x4, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 16:32 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | NO | — | — | — | 46 | `run` x30, `write_file` x7, `verify` x3, `mutation` x2, `coverage` x1 | — | — | — | 2026-09-24 16:28 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | NO | — | — | — | 48 | `run` x33, `write_file` x7, `run_tests` x1 | — | — | — | 2026-09-24 16:28 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 31 | `run` x20, `write_file` x5, `run_tests` x1, `verify` x1 | — | — | — | 2026-09-24 16:28 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 4/4 | 4/4 | 32 | `run` x17, `run_tests` x4, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | broader | complete | acceptable | 2026-09-24 16:27 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | NO | — | — | — | 39 | `run` x27, `write_file` x5, `verify` x2 | — | — | — | 2026-09-24 16:33 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 4/5 | 5/5 | 21 | `run` x12, `coverage` x2, `verify` x2, `write_file` x2, `mutation` x1 | unparsed | — | — | 2026-09-24 16:33 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 43 | `run` x29, `verify` x3, `coverage` x2, `write_file` x2, `mutation` x1 | broader | partial | poor | 2026-09-24 16:39 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 44 | `run` x28, `verify` x5, `write_file` x4, `coverage` x2, `mutation` x1 | unparsed | — | — | 2026-09-24 16:43 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 2/10 | 2/10 | 29 | `run` x14, `write_file` x4, `coverage` x3, `verify` x3, `mutation` x1 | different | partial | acceptable | 2026-09-24 16:40 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 45 | `run` x26, `write_file` x7, `verify` x5, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:45 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 60 | `run` x38, `write_file` x8, `verify` x3, `coverage` x1 | — | — | — | 2026-09-24 16:42 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 31 | `run` x16, `coverage` x3, `mutation` x3, `verify` x3, `write_file` x3 | broader | complete | acceptable | 2026-09-24 16:35 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 100% (3/3) | 0/1 | 0/1 | 54 | `run` x26, `coverage` x8, `verify` x7, `write_file` x7, `mutation` x1 | broader | partial | poor | 2026-09-24 16:43 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | no mutants | no mutants | 40 | `run` x17, `write_file` x7, `verify` x6, `coverage` x5, `mutation` x1 | broader | partial | acceptable | 2026-09-24 16:42 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 100% (3/3) | 6/10 | 3/10 | 23 | `run` x13, `write_file` x3, `coverage` x2, `verify` x2, `mutation` x1 | broader | complete | acceptable | 2026-09-24 16:38 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 1/1 | 0/1 | 29 | `run` x11, `coverage` x4, `mutation` x4, `verify` x4, `write_file` x4 | broader | complete | good | 2026-09-24 16:39 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 28 | `run` x19, `write_file` x2, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | 2026-09-24 16:37 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 9/10 | 9/10 | 25 | `run` x15, `write_file` x4, `verify` x2, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 16:41 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 50 | `run` x26, `write_file` x9, `run_tests` x4, `verify` x4 | — | — | — | 2026-09-24 16:43 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 33 | `run` x20, `write_file` x3, `mutation` x2, `verify` x2, `coverage` x1 | same | partial | poor | 2026-09-24 16:39 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 36 | `run` x23, `write_file` x4, `verify` x3, `coverage` x1, `mutation` x1 | narrower | partial | poor | 2026-09-24 16:42 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 54 | `run` x29, `write_file` x10, `verify` x5, `coverage` x2, `mutation` x1 | — | — | — | 2026-09-24 16:43 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 3/6 | 3/6 | 33 | `run` x19, `verify` x3, `write_file` x3, `coverage` x2, `run_tests` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 16:40 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 38 | `run` x15, `write_file` x8, `verify` x6, `coverage` x1, `mutation` x1 | — | — | — | 2026-09-24 16:46 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 40 | `run` x19, `write_file` x7, `verify` x5, `coverage` x4, `mutation` x1 | — | — | — | 2026-09-24 16:44 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 5/5 | 5/5 | 34 | `run` x24, `write_file` x3, `coverage` x1, `mutation` x1, `verify` x1 | same | complete | acceptable | 2026-09-24 16:41 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 20% (2/10) | 1/10 | 6/10 | 35 | `run` x18, `verify` x5, `write_file` x5, `coverage` x3, `mutation` x1 | narrower | partial | poor | 2026-09-24 16:41 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 57% (27/47) | 1/10 | 4/10 | 30 | `run` x23, `write_file` x3 | narrower | partial | poor | 2026-09-24 16:44 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 31 | `run` x22, `coverage` x1, `mutation` x1, `verify` x1, `write_file` x1 | broader | complete | acceptable | 2026-09-24 16:41 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 35 | `run` x26, `write_file` x4 | — | — | — | 2026-09-24 16:40 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 50 | `run` x34, `write_file` x10 | — | — | — | 2026-09-24 16:44 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 58 | `run` x25, `write_file` x14, `verify` x8, `run_tests` x5 | — | — | — | 2026-09-24 16:47 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 34 | `run` x18, `write_file` x7, `verify` x4 | — | — | — | 2026-09-24 16:46 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 38% (14/37) | 1/10 | 5/10 | 39 | `run` x17, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x2, `mutation` x1 | narrower | partial | acceptable | 2026-09-24 16:45 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 39 | `run` x26, `write_file` x5, `verify` x3 | — | — | — | 2026-09-24 16:43 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | BROKEN | — | — | — | 33 | `run` x21, `write_file` x5, `run_tests` x2, `mutation` x1 | — | — | — | 2026-09-24 16:43 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | BROKEN | — | — | — | 45 | `run` x21, `write_file` x7, `run_tests` x4, `verify` x3, `coverage` x2, `mutation` x2 | — | — | — | 2026-09-24 16:48 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | BROKEN | — | — | — | 37 | `run` x25, `write_file` x4, `verify` x3 | — | — | — | 2026-09-24 16:44 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 6/6 | 6/6 | 33 | `run` x20, `verify` x4, `write_file` x3, `coverage` x2, `mutation` x2 | broader | complete | acceptable | 2026-09-24 16:47 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | BROKEN | — | — | — | 35 | `run` x25, `write_file` x5 | — | — | — | 2026-09-24 16:45 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | BROKEN | — | — | — | 46 | `run` x29, `write_file` x6, `verify` x2 | — | — | — | 2026-09-24 16:47 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 0/2 | 1/2 | 36 | `run` x23, `write_file` x4, `run_tests` x2 | broader | partial | poor | 2026-09-24 16:47 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | BROKEN | — | — | — | 29 | `run` x22, `write_file` x3 | — | — | — | 2026-09-24 16:45 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 49 | `run` x40, `write_file` x5 | narrower | partial | acceptable | 2026-09-24 16:49 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14598** (partial)
  - Doubled single quotes followed by whitespace do not cause partial string matching or quote loss at the string/comment boundary.
- **astropy__astropy-7606** (partial)
  - The UnitBase.__eq__ invalid-operand/reflected-comparison branch, including the recognized-unit side of the membership check.
  - The changed type(self) compatibility distinction for different UnrecognizedUnit types.
- **django__django-13023** (partial)
  - Values such as malformed tuples that make decimal.Decimal() raise ValueError are converted into ValidationError.
- **django__django-13449** (misses_the_point)
  - SQLite Window expressions with DecimalField output, including Lag, execute successfully with the numeric cast outside OVER and return correct results instead of raising a syntax error.
  - SQLite Window expressions with non-Decimal output continue through the ordinary Window SQL path without the Decimal-specific cast.
- **django__django-14608** (partial)
  - The default non-form ErrorList created during formset cleaning uses the nonform class, so accumulated formset-level errors such as min/max violations render with it.
- **django__django-14915** (partial)
  - The wrapper's hash matches the hash of its raw underlying value for the reported dictionary-membership path.
  - Wrappers containing the distinct primary keys exercised by the fix produce distinct hashes.
- **matplotlib__matplotlib-20859** (partial)
  - An invalid non-Axes, non-FigureBase parent is rejected with the updated FigureBase error message.
- **matplotlib__matplotlib-24970** (partial)
  - The floating-point path continues to scale, clip, and convert to correct integer indices after the cast is moved to the common path.
- **psf__requests-2931** (partial)
  - String or byte query parameters are converted to native text before URL query encoding after _encode_params stops coercing payloads.
- **pydata__xarray-2905** (partial)
  - Pandas Series, Index, and DataFrame inputs continue to be converted through their `.values` attributes.
- **pydata__xarray-6744** (partial)
  - Centered leading and trailing boundary results and the rest of the centered output sequence.
  - The center=False branch.
  - Window sizes 1, 2, and 7, including the even-sized window case.
- **pylint-dev__pylint-7277** (partial)
  - Remove a leading entry equal to `os.getcwd()`.
- **pytest-dev__pytest-6197** (partial)
  - Collecting a package beneath src does not add src to sys.path.
- **scikit-learn__scikit-learn-10297** (partial)
  - With store_cv_values=True, fitting single-target data creates cv_values_ with shape (n_samples, 1, n_alphas).
  - With store_cv_values=True, fitting multi-target data creates cv_values_ with shape (n_samples, n_targets, n_alphas).
- **sphinx-doc__sphinx-7462** (partial)
  - The low-level `sphinx.pycode.ast.unparse` path returning `()` for an empty tuple.
  - The exact punctuation-node output for the domain-level `Tuple[()]` annotation.
- **sphinx-doc__sphinx-7590** (partial)
  - Hexadecimal floating-point UDLs.
  - Binary, hexadecimal, and octal integer UDLs.
- **sympy__sympy-12489** (partial)
  - Construction from multiple cycle arguments preserves the subclass type.
  - Construction from a Cycle preserves the subclass type.
  - Construction from an integer size preserves the subclass type.
- **sympy__sympy-19637** (partial)
  - The space-containing path that computes `hit = kern in s`.
- **sympy__sympy-21596** (partial)
  - Factored imaginary parts with nonintegral roots are filtered against the source set, including the Naturals0 case.
  - An imaginary-part equation that cannot be solved linearly is represented with a ConditionSet.
  - Parameters that make denominators zero are excluded while valid real image values remain.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **sympy__sympy-14976** — nothing collected on either side -- the file never ran
- **sympy__sympy-15349** — nothing collected on either side -- the file never ran
- **sympy__sympy-16450** — nothing collected on either side -- the file never ran
- **sympy__sympy-17318** — nothing collected on either side -- the file never ran
- **sympy__sympy-18189** — nothing collected on either side -- the file never ran
- **sympy__sympy-20590** — nothing collected on either side -- the file never ran
