# Run status, per pull request

Last run in this table: 2026-09-24 21:56 UTC.

- **70** instances across **12** repositories
- **38/66** fail-to-pass, of those that reached a verdict
- **38** measured for changed-line coverage: **mean 82%** per test, median 100%
- **69%** of the changed lines those tests were measured against (143/207, pooled)
- **28%** of every source line all 70 patches change (143/508) -- a fixed denominator, so this is the figure that compares across arms
- \$2.35 and 32.0M tokens in total
- **26** of these were sent a second-chance message after stopping with nothing to score, and **2** of them ended fail-to-pass; the other 44 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 5 | 1 | 1 | 3 | **added by the flag** |
| `passes_at_base` | 21 | 1 | 19 | 1 | **added by the flag** |

Of the **26** refused for a reason the flag itself adds, **2** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool+mutation-tool+require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 18 | `run` x8, `write_file` x5, `verify` x2 | — | — | — | 2026-09-24 21:35 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 7/7 | 7/7 | 32 | `run` x18, `write_file` x9, `verify` x2 | same | partial | acceptable | 2026-09-24 21:37 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 17 | `run` x12, `write_file` x2 | broader | complete | acceptable | 2026-09-24 21:32 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 0/9 | 9/9 | 20 | `run` x11, `write_file` x4, `verify` x3 | broader | partial | acceptable | 2026-09-24 21:35 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 48 | `run` x30, `write_file` x8, `run_tests` x3, `verify` x2 | — | — | — | 2026-09-24 21:35 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 31 | `run` x23, `write_file` x4, `verify` x2 | — | — | — | 2026-09-24 21:32 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 39 | `run` x20, `write_file` x8, `run_tests` x4, `verify` x1 | — | — | — | 2026-09-24 21:36 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 34 | `run` x14, `write_file` x7, `run_tests` x4, `verify` x2 | — | — | — | 2026-09-24 21:34 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 33 | `run` x20, `write_file` x8, `verify` x1 | — | — | — | 2026-09-24 21:32 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | BROKEN | — | — | — | 39 | `run` x23, `write_file` x8 | — | — | — | 2026-09-24 21:34 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 23 | `run` x13, `write_file` x5, `verify` x2 | narrower | partial | acceptable | 2026-09-24 21:30 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/10 | 8/10 | 38 | `run` x20, `write_file` x9, `verify` x4 | different | misses_the_point | acceptable | 2026-09-24 21:37 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | BROKEN | — | — | — | 49 | `run` x28, `write_file` x12, `verify` x2 | — | — | — | 2026-09-24 21:39 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | NO | — | — | — | 28 | `run` x17, `write_file` x6, `verify` x1 | — | — | — | 2026-09-24 21:35 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 26 | `run` x20, `write_file` x2, `verify` x1 | narrower | partial | acceptable | 2026-09-24 21:30 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 23 | `run` x16, `verify` x2, `write_file` x2 | broader | partial | good | 2026-09-24 21:32 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 30 | `run` x18, `write_file` x6, `verify` x3 | — | — | — | 2026-09-24 21:31 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 19 | `run` x11, `write_file` x3, `verify` x2 | same | complete | acceptable | 2026-09-24 21:34 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 50% (1/2) | no mutants | no mutants | 21 | `run` x16, `write_file` x2, `verify` x1 | narrower | partial | poor | 2026-09-24 21:32 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 51 | `run` x26, `write_file` x11, `verify` x5, `run_tests` x2 | — | — | — | 2026-09-24 21:37 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 30 | `run` x18, `write_file` x5, `verify` x2, `run_tests` x1 | broader | complete | good | 2026-09-24 21:36 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 27 | `run` x10, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 21:36 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 0/1 | 1/1 | 19 | `run` x11, `write_file` x5 | narrower | partial | poor | 2026-09-24 21:34 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 35 | `run` x18, `write_file` x9, `verify` x3 | — | — | — | 2026-09-24 21:38 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x15, `write_file` x4, `run_tests` x3, `verify` x2 | broader | complete | acceptable | 2026-09-24 21:35 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 48 | `run` x28, `write_file` x10, `verify` x4 | — | — | — | 2026-09-24 21:40 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | NO | — | — | — | 37 | `run` x20, `write_file` x11 | — | — | — | 2026-09-24 21:37 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 9/10 | 9/10 | 41 | `run` x20, `write_file` x9, `verify` x4, `run_tests` x3 | different | misses_the_point | poor | 2026-09-24 21:36 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 42% (10/24) | 2/10 | 0/10 | 21 | `run` x10, `verify` x3, `write_file` x3, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 21:31 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 26 | `run` x20, `write_file` x3, `verify` x1 | same | complete | acceptable | 2026-09-24 21:35 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | BROKEN | — | — | — | 36 | `run` x20, `write_file` x6, `verify` x3, `run_tests` x1 | — | — | — | 2026-09-24 21:37 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 10/10 | 10/10 | 19 | `run` x14, `write_file` x2 | narrower | complete | acceptable | 2026-09-24 21:38 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 17 | `run` x13, `verify` x1, `write_file` x1  (+1 edit reverted) | broader | partial | acceptable | 2026-09-24 21:36 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | YES | 59% (10/17) | no mutants | no mutants | 20 | `run` x14, `verify` x2, `write_file` x2 | narrower | partial | good | 2026-09-24 21:38 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 100% (6/6) | 3/10 | 1/10 | 20 | `run` x10, `write_file` x4, `verify` x2 | same | partial | poor | 2026-09-24 21:39 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 30 | `run` x11, `write_file` x7, `run_tests` x6, `verify` x1 | — | — | — | 2026-09-24 21:44 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 36 | `run` x22, `write_file` x6, `verify` x2 | — | — | — | 2026-09-24 21:42 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 17 | `run` x12, `write_file` x2 | broader | complete | good | 2026-09-24 21:37 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 67% (2/3) | 0/2 | 0/2 | 32 | `run` x22, `write_file` x4, `verify` x2 | same | partial | poor | 2026-09-24 21:40 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 17 | `run` x11, `write_file` x4 | same | partial | acceptable | 2026-09-24 21:40 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 10 | `run` x6, `verify` x1, `write_file` x1 | narrower | partial | acceptable | 2026-09-24 21:40 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 18 | `run` x13, `run_tests` x1, `verify` x1, `write_file` x1 | broader | complete | acceptable | 2026-09-24 21:40 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 27 | `run` x11, `write_file` x6, `run_tests` x4, `verify` x1 | — | — | — | 2026-09-24 21:41 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 18 | `run` x6, `write_file` x4, `run_tests` x3, `verify` x2 | narrower | partial | acceptable | 2026-09-24 21:43 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 0% (0/2) | 2/2 | 2/2 | 31 | `run` x18, `write_file` x6, `verify` x2 | different | misses_the_point | poor | 2026-09-24 21:45 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 6/7 | 7/7 | 15 | `run` x10, `write_file` x2, `verify` x1  (+1 edit reverted) | same | partial | poor | 2026-09-24 21:41 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | YES | 100% (5/5) | no mutants | no mutants | 22 | `run` x12, `write_file` x7 | narrower | partial | acceptable | 2026-09-24 21:45 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 29 | `run` x9, `run_tests` x6, `write_file` x6, `verify` x1 | — | — | — | 2026-09-24 21:43 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 22 | `run` x18, `run_tests` x1, `write_file` x1  (+1 edit reverted) | — | — | — | 2026-09-24 21:40 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 34 | `run` x17, `write_file` x8, `run_tests` x2, `verify` x1 | — | — | — | 2026-09-24 21:45 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 4/10 | 4/10 | 29 | `run` x20, `write_file` x5 | narrower | partial | poor | 2026-09-24 21:45 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 23 | `run` x14, `write_file` x5, `verify` x1 | narrower | complete | acceptable | 2026-09-24 21:45 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | NO | — | — | — | 39 | `run` x12, `write_file` x9, `run_tests` x7, `verify` x6 | — | — | — | 2026-09-24 21:46 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | NO | — | — | — | 37 | `run` x23, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 21:45 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 14 | `run` x8, `verify` x2, `write_file` x2 | same | complete | good | 2026-09-24 21:41 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 46 | `run` x31, `write_file` x8, `verify` x2 | — | — | — | 2026-09-24 21:46 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 34 | `run` x15, `write_file` x9, `verify` x4, `run_tests` x1 | — | — | — | 2026-09-24 21:45 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 44 | `run` x25, `write_file` x7, `verify` x3 | — | — | — | 2026-09-24 21:45 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 38 | `run` x21, `write_file` x9, `verify` x3 | — | — | — | 2026-09-24 21:47 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | YES | 43% (16/37) | 2/10 | 6/10 | 25 | `run` x14, `verify` x4, `write_file` x4 | narrower | partial | good | 2026-09-24 21:45 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 21 | `run` x13, `write_file` x3, `verify` x2 | — | — | — | 2026-09-24 21:42 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 6/10 | 10/10 | 26 | `run` x15, `write_file` x4, `run_tests` x3, `verify` x2 | narrower | partial | poor | 2026-09-24 21:45 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | NO | — | — | — | 28 | `run` x17, `write_file` x5, `verify` x3 | — | — | — | 2026-09-24 21:47 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 16 | `run` x9, `verify` x2, `write_file` x2, `run_tests` x1 | broader | partial | acceptable | 2026-09-24 21:56 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 21 | `run` x15, `write_file` x3, `verify` x1 | broader | complete | acceptable | 2026-09-24 21:44 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 42 | `run` x28, `write_file` x7 | — | — | — | 2026-09-24 21:48 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 19 | `run` x13, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 21:49 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 50% (1/2) | 1/4 | 3/4 | 23 | `run` x11, `write_file` x3, `run_tests` x2, `verify` x2 | narrower | partial | acceptable | 2026-09-24 21:46 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | NO | — | — | — | 35 | `run` x22, `write_file` x5, `verify` x2 | — | — | — | 2026-09-24 21:49 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 18 | `run` x10, `write_file` x3, `verify` x2 | narrower | partial | acceptable | 2026-09-24 21:47 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (partial)
  - The reported Q-format differences must identify the correct rows and values and produce correct aggregate and report details.
- **astropy__astropy-7606** (partial)
  - The UnitBase __eq__ path returning NotImplemented for invalid operands; the regular-unit test only checks the final False result, which does not distinguish this fix from the old implementation.
  - The valid UnrecognizedUnit type/name equality behaviour, including equality with "FOO" and inequality with u.m.
- **django__django-13023** (partial)
  - Values that cause decimal.Decimal() to raise ValueError are converted into ValidationError.
- **django__django-13449** (misses_the_point)
  - SQLite Window expressions with DecimalField output execute successfully by applying the numeric cast outside the window expression.
  - SQLite Window expressions with non-Decimal output continue to use the normal Window SQL path without the Decimal-specific cast.
- **django__django-13794** (partial)
  - The add filter concatenates two lazy strings (__add__ cooperating with __radd__).
  - Two lazy integer proxies can be added directly and produce 9.
- **django__django-14534** (partial)
  - When no ID is present in the subwidget attributes, id_for_label returns None instead of constructing an ID.
- **django__django-14608** (partial)
  - A ValidationError raised by `BaseFormSet.clean()` is converted from `e.error_list` into an ErrorList with `error_class='nonform'`.
- **django__django-14915** (partial)
  - The hash matches hash(self.value), including equal hashes for wrappers around the same underlying value.
  - Dictionary membership actually succeeds for a wrapper whose underlying value matches a dictionary key; the generated test allows `if value in show_fields` to be false.
- **django__django-16454** (misses_the_point)
  - Default CommandParser subparser errors are rendered as the expected human-facing CLI error output.
  - Explicit argparse.ArgumentParser subparser errors retain their normal argparse formatting.
- **django__django-16560** (partial)
  - BaseConstraint accepts and stores a non-None violation_error_code.
  - BaseConstraint.deconstruct() includes a non-None violation_error_code.
  - CheckConstraint equality distinguishes constraints with different violation_error_code values.
- **matplotlib__matplotlib-20859** (partial)
  - A legend created for a SubFigure is attached to that exact SubFigure as its figure.
  - An unsupported parent still raises TypeError with the updated FigureBase wording.
- **matplotlib__matplotlib-24870** (partial)
  - tricontour() defaulting boolean data to [0.5].
  - tricontourf() defaulting boolean data to [0, 0.5, 1].
  - The list and masked-array forms of the regular contour and contourf cases are not checked.
- **matplotlib__matplotlib-24970** (partial)
  - The generated test never checks that the returned colormap values are correct across uint8, signed int, float16, and native float inputs.
- **psf__requests-2931** (partial)
  - String or bytes supplied as URL `params` are normalized with `to_native_string` before query-string encoding.
- **pydata__xarray-2905** (partial)
  - Pandas Series, Index, and DataFrame inputs continue to be converted to their `.values` data.
- **pydata__xarray-4075** (partial)
  - Boolean weights produce an integer count in the public sum_of_weights() result rather than a boolean reduction.
- **pydata__xarray-6744** (partial)
  - center=True for window sizes 1, 2, and 7, including the even-window and boundary cases.
  - center=False iteration for window sizes 1, 2, 3, and 7.
- **pylint-dev__pylint-4970** (misses_the_point)
  - With `min-similarity-lines` set to zero, the duplicate-code checker must stop without reporting similarities and complete successfully.
- **pylint-dev__pylint-7277** (partial)
  - Removal of an empty-string first entry is not pinned: `assert sys.path[0] != ""` also passes with the old unconditional pop and does not assert the resulting list.
  - Removal of a dot first entry is not pinned: `assert sys.path[0] != "."` is the same weak check.
  - Removal of an os.getcwd() first entry is not tested.
- **pytest-dev__pytest-6197** (partial)
  - Pytest does not add a src directory to sys.path merely while collecting tests.
- **scikit-learn__scikit-learn-14087** (partial)
  - The multinomial coefficient-averaging result is not pinned; assert len(clf.C_) >= 1 only checks that C_ is nonempty.
  - The non-elasticnet result is not asserted to set l1_ratio_ to None.
  - The elasticnet l1-ratio selection branch is never exercised.
- **sympy__sympy-12489** (partial)
  - Constructing a subclass from multiple cycle arguments or an ordinary sequence returns an instance of that subclass.
  - Constructing from an existing subclass, including size adjustment, preserves or creates the requested subclass.
  - Binary and composition operations such as __mul__, __rmul__, mul_inv, and rmul_with_af preserve the receiver's subclass type.
- **sympy__sympy-14976** (partial)
  - MpmathPrinter emits the exact mpmath.mpf(numerator)/mpmath.mpf(denominator) representation; the substring assertion permits incomplete or otherwise malformed output.
  - High-precision nsolve returns the correctly precise rational root.
- **sympy__sympy-16450** (partial)
  - The complete assumptions0 set is not asserted for the replacement, so preservation of inferred assumptions such as real, complex, hermitian, nonzero, and infinite=False is not pinned.
- **sympy__sympy-19637** (partial)
  - The no-space input must return the correctly parsed expression `2*x/(x-1)`.
- **sympy__sympy-21596** (partial)
  - Nonintegral roots of the imaginary part are discarded when the parameter set is Integers, producing {1}.
  - The same imaginary-root filtering works over Naturals0, producing {1}.
  - An unsolved nonlinear imaginary condition is represented with a ConditionSet inside the resulting ImageSet.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-13012** — nothing collected on either side -- the file never ran
- **django__django-13513** — nothing collected on either side -- the file never ran
- **django__django-16667** — nothing collected on either side -- the file never ran
