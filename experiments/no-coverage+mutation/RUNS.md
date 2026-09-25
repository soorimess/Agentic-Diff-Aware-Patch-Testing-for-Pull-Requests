# Run status, per pull request

Last run in this table: 2026-09-24 20:41 UTC.

- **70** instances across **12** repositories
- **38/65** fail-to-pass, of those that reached a verdict
- **38** measured for changed-line coverage: **mean 86%** per test, median 100%
- **73%** of the changed lines those tests were measured against (102/140, pooled)
- **20%** of every source line all 70 patches change (102/508) -- a fixed denominator, so this is the figure that compares across arms
- \$2.72 and 37.1M tokens in total
- **39** of these were sent a second-chance message after stopping with nothing to score, and **7** of them ended fail-to-pass; the other 31 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing+loop_open` | 5 | 0 | 2 | 3 | **added by the flag** |
| `loop_open` | 12 | 6 | 6 | 0 | from `require-tools` |
| `passes_at_base+loop_open` | 22 | 1 | 19 | 2 | **added by the flag** |

Of the **27** refused for a reason the flag itself adds, **1** ended fail-to-pass.

Every row was produced with the same configuration: **`no-coverage-tool+mutation-tool`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | YES | 100% (4/4) | 3/10 | 3/10 | 24 | `run` x13, `write_file` x5, `verify` x1 | same | partial | poor | 2026-09-24 20:21 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 4/7 | 7/7 | 31 | `run` x17, `write_file` x5, `verify` x4, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 20:17 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 22 | `run` x17, `verify` x1, `write_file` x1 | same | partial | acceptable | 2026-09-24 20:14 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 67% (4/6) | 0/9 | 9/9 | 18 | `run` x11, `write_file` x3, `verify` x1 | narrower | partial | poor | 2026-09-24 20:17 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 42 | `run` x22, `write_file` x8, `verify` x7 | — | — | — | 2026-09-24 20:21 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 37 | `run` x21, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 20:18 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 42 | `run` x22, `write_file` x11, `verify` x4 | — | — | — | 2026-09-24 20:18 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | NO | — | — | — | 40 | `run` x22, `write_file` x10 | — | — | — | 2026-09-24 20:20 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 29 | `run` x18, `write_file` x5, `verify` x3 | narrower | partial | acceptable | 2026-09-24 20:17 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | YES | 100% (2/2) | 0/1 | 0/1 | 28 | `run` x22, `write_file` x2, `verify` x1 | narrower | partial | acceptable | 2026-09-24 20:13 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 26 | `run` x17, `write_file` x3, `run_tests` x1, `verify` x1 | narrower | partial | poor | 2026-09-24 20:16 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | YES | 22% (2/9) | 0/10 | 8/10 | 31 | `run` x20, `write_file` x5, `run_tests` x2, `verify` x1 | unparsed | — | — | 2026-09-24 20:16 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 38 | `run` x10, `run_tests` x9, `write_file` x9, `verify` x3 | — | — | — | 2026-09-24 20:24 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | BROKEN | — | — | — | 39 | `run` x15, `write_file` x11, `verify` x6 | — | — | — | 2026-09-24 20:24 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | YES | 100% (4/4) | no mutants | no mutants | 34 | `run` x23, `write_file` x5, `verify` x1 | narrower | partial | poor | 2026-09-24 20:20 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 35 | `run` x26, `verify` x3, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 20:17 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 45 | `run` x18, `write_file` x12, `run_tests` x5, `verify` x1 | — | — | — | 2026-09-24 20:22 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 33 | `run` x21, `write_file` x7, `verify` x2 | same | complete | good | 2026-09-24 20:18 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | YES | 100% (2/2) | no mutants | no mutants | 21 | `run` x12, `write_file` x3, `run_tests` x2, `verify` x2 | broader | complete | acceptable | 2026-09-24 20:16 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | NO | — | — | — | 46 | `run` x26, `verify` x7, `write_file` x7 | — | — | — | 2026-09-24 20:22 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 17 | `run` x11, `verify` x2, `write_file` x2 | broader | complete | acceptable | 2026-09-24 20:12 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 44 | `run` x31, `write_file` x7, `verify` x1 | — | — | — | 2026-09-24 20:23 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | BROKEN | — | — | — | 35 | `run` x19, `write_file` x10, `verify` x1 | — | — | — | 2026-09-24 20:17 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 41 | `run` x27, `write_file` x8 | — | — | — | 2026-09-24 20:25 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | YES | 100% (1/1) | no mutants | no mutants | 20 | `run` x13, `verify` x2, `write_file` x2 | narrower | complete | acceptable | 2026-09-24 20:16 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 36 | `run` x17, `write_file` x8, `verify` x6 | — | — | — | 2026-09-24 20:26 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | NO | — | — | — | 46 | `run` x23, `write_file` x11, `verify` x5 | — | — | — | 2026-09-24 20:24 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | BROKEN | — | — | — | 43 | `run` x24, `write_file` x9, `verify` x5 | — | — | — | 2026-09-24 20:17 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | YES | 22% (4/18) | 0/10 | 0/10 | 27 | `run` x13, `write_file` x6, `verify` x2, `run_tests` x1 | narrower | partial | acceptable | 2026-09-24 20:16 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | YES | 100% (1/1) | 9/9 | 9/9 | 22 | `run` x13, `write_file` x3, `run_tests` x2, `verify` x2 | same | complete | acceptable | 2026-09-24 20:14 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | BROKEN | — | — | — | 41 | `run` x17, `write_file` x11, `verify` x4, `run_tests` x3 | — | — | — | 2026-09-24 20:22 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 100% (4/4) | 7/10 | 10/10 | 15 | `run` x11, `verify` x1, `write_file` x1 | narrower | complete | acceptable | 2026-09-24 20:18 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 26 | `run` x18, `write_file` x3, `verify` x2 | broader | partial | acceptable | 2026-09-24 20:20 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | NO | — | — | — | 28 | `run` x16, `write_file` x6, `run_tests` x1 | — | — | — | 2026-09-24 20:27 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 1/10 | 1/10 | 23 | `run` x15, `write_file` x3, `verify` x2 | narrower | partial | acceptable | 2026-09-24 20:27 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 41 | `run` x18, `write_file` x12, `verify` x5 | — | — | — | 2026-09-24 20:35 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 55 | `run` x30, `write_file` x13, `verify` x7 | — | — | — | 2026-09-24 20:32 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 16 | `run` x11, `verify` x2, `write_file` x1 | broader | complete | acceptable | 2026-09-24 20:21 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | YES | 33% (1/3) | 0/2 | 0/2 | 27 | `run` x17, `write_file` x4, `verify` x3 | same | partial | poor | 2026-09-24 20:25 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | YES | 50% (1/2) | 0/1 | 0/1 | 27 | `run` x14, `write_file` x7, `verify` x2 | same | partial | acceptable | 2026-09-24 20:29 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 21 | `run` x11, `write_file` x3, `verify` x2 | narrower | partial | acceptable | 2026-09-24 20:27 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | YES | 100% (1/1) | 2/2 | 1/2 | 19 | `run` x15, `verify` x1, `write_file` x1  (+1 edit reverted) | broader | complete | acceptable | 2026-09-24 20:23 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 27 | `run` x15, `write_file` x5, `verify` x2 | — | — | — | 2026-09-24 20:26 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 25 | `run` x17, `write_file` x4 | narrower | partial | good | 2026-09-24 20:28 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 35 | `run` x19, `write_file` x7, `verify` x4 | broader | complete | poor | 2026-09-24 20:31 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 7/7 | 7/7 | 20 | `run` x11, `write_file` x3, `verify` x2 | broader | complete | poor | 2026-09-24 20:27 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 38 | `run` x20, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 20:32 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 42 | `run` x20, `write_file` x11, `verify` x4 | — | — | — | 2026-09-24 20:29 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | YES | 100% (4/4) | 6/10 | 5/10 | 21 | `run` x14, `verify` x2, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 20:25 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 32 | `run` x16, `write_file` x8, `verify` x2 | — | — | — | 2026-09-24 20:31 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | YES | 60% (3/5) | 4/10 | 4/10 | 25 | `run` x17, `write_file` x3, `verify` x2 | narrower | partial | poor | 2026-09-24 20:29 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 27 | `run` x20, `write_file` x2, `verify` x1 | broader | complete | acceptable | 2026-09-24 20:29 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 3/10 | 6/10 | 32 | `run` x22, `write_file` x5 | narrower | partial | poor | 2026-09-24 20:29 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | NO | — | — | — | 39 | `run` x19, `write_file` x9, `verify` x6 | — | — | — | 2026-09-24 20:34 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | NO | — | — | — | 37 | `run` x17, `write_file` x11, `verify` x4 | — | — | — | 2026-09-24 20:31 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 44 | `run` x23, `write_file` x8, `verify` x4 | — | — | — | 2026-09-24 20:32 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 36 | `run` x19, `write_file` x9, `verify` x4 | — | — | — | 2026-09-24 20:32 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 36 | `run` x18, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 20:32 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 33 | `run` x16, `write_file` x8, `verify` x3 | — | — | — | 2026-09-24 20:34 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | NO | — | — | — | 38 | `run` x16, `write_file` x9, `verify` x5, `run_tests` x1 | — | — | — | 2026-09-24 20:34 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 32 | `run` x22, `write_file` x4, `verify` x1  (+1 edit reverted) | — | — | — | 2026-09-24 20:33 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | YES | 100% (2/2) | 10/10 | 10/10 | 20 | `run` x12, `verify` x3, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 20:30 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 18 | `run` x12, `write_file` x2, `verify` x1 | same | complete | acceptable | 2026-09-24 20:30 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 17 | `run` x13, `verify` x1, `write_file` x1 | broader | partial | acceptable | 2026-09-24 20:41 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | YES | 100% (4/4) | 10/10 | 10/10 | 18 | `run` x11, `run_tests` x1, `verify` x1, `write_file` x1 | broader | complete | acceptable | 2026-09-24 20:30 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 29 | `run` x17, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-24 20:33 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 15 | `run` x9, `verify` x1, `write_file` x1 | same | complete | acceptable | 2026-09-24 20:34 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 100% (2/2) | 1/4 | 3/4 | 18 | `run` x11, `verify` x3, `write_file` x2 | narrower | partial | poor | 2026-09-24 20:32 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | NO | — | — | — | 39 | `run` x23, `write_file` x7, `verify` x4 | — | — | — | 2026-09-24 20:36 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 23 | `run` x15, `write_file` x3, `verify` x2 | narrower | partial | poor | 2026-09-24 20:34 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14369** (partial)
  - `10+3J/m/s/kpc2` must produce the exact expected unit, because excluding `s / (kpc2 m)` does not establish the correct result.
  - `10-7J/s/kpc2` must produce the exact expected unit, because excluding `kpc2 / s` does not establish the correct result.
- **astropy__astropy-14539** (partial)
  - Comparing different Q-format variable-length-array values detects and reports the per-row differences and correct aggregate counts, ratio, and report.
- **astropy__astropy-14598** (partial)
  - A doubled-single-quote pair followed by a space and additional text survives serialization and reparsing.
- **astropy__astropy-7606** (partial)
  - Invalid operands in the general UnitBase.__eq__ path return NotImplemented so the other operand can attempt reflected equality.
  - An UnrecognizedUnit compared with None returns NotImplemented, making equality False instead of raising TypeError.
  - The corresponding inequality path yields True for comparison with None, including the not-in tuple regression case.
- **django__django-12965** (partial)
  - An unfiltered `Model.objects.all().delete()` emits a simple `DELETE FROM` statement without a self-referential `SELECT` subquery, preserving the affected MySQL lock and performance behaviour.
- **django__django-13012** (partial)
  - A non-constant expression wrapped in ExpressionWrapper preserves the wrapped expression's non-empty group-by columns.
- **django__django-13023** (partial)
  - Other unsupported TypeError inputs such as lists, sets, arbitrary objects, and complex numbers.
  - The ValueError path represented by malformed tuple input.
  - The InvalidOperation path represented by nonnumeric strings and bytes.
- **django__django-13794** (partial)
  - The add filter concatenates a normal string with a lazy string and produces the exact result `stringlazy`.
  - The add filter concatenates two lazy strings and produces the exact result `stringlazy`.
  - Two lazy integer proxies can be added and produce 9.
- **django__django-14534** (partial)
  - The no-ID branch, such as `auto_id=False`, returning `None`.
- **django__django-16560** (partial)
  - BaseConstraint includes a custom violation_error_code in deconstruction.
  - CheckConstraint reports the custom code when validation fails.
  - CheckConstraint equality and repr account for violation_error_code.
- **matplotlib__matplotlib-20859** (partial)
  - The TypeError path for an unsupported parent and its updated message, "Legend needs either Axes or FigureBase as parent".
- **matplotlib__matplotlib-24970** (partial)
  - The expected returned-color behavior for uint8 and signed int inputs is never asserted.
  - The expected returned-color behavior for float16 and Python-float inputs is never asserted.
- **psf__requests-2931** (partial)
  - `prepare_url` normalizes string or bytes query parameters with `to_native_string` before query encoding.
- **pydata__xarray-2905** (partial)
  - Pandas Series, Index, and DataFrame inputs continue to be normalized to their `.values` data.
- **pydata__xarray-4075** (partial)
  - sum_of_weights() converts boolean weights to integers and returns their numeric count.
- **pydata__xarray-6744** (partial)
  - center=False iteration retains trailing/right-aligned window semantics
  - window start and stop calculations work for sizes 1, 2, and 7, including even and oversized windows
- **scikit-learn__scikit-learn-10297** (partial)
  - Fitting with storage enabled produces cv_values_ with shape (n_samples, 1, n_alphas) for a one-dimensional target.
  - Fitting with storage enabled produces cv_values_ with shape (n_samples, n_targets, n_alphas) for a multi-target response.
- **scikit-learn__scikit-learn-14087** (partial)
  - The resolved OVR behaviour is reached by the generated test, but no assertion pins the successful result or absence of the error.
  - The multinomial coefficient-path behaviour is not exercised.
  - The non-elasticnet `l1_ratio_ = None` result is not asserted.
- **sphinx-doc__sphinx-7462** (partial)
  - The Python-domain annotation unparser renders the empty tuple in `Tuple[()]` as the expected doctree punctuation sequence; the generated assertions only check that a list exists.
  - `sphinx.pycode.ast.unparse` renders an empty AST tuple as the string `()`.
- **sympy__sympy-14976** (partial)
  - The mpmath lambdify path used by nsolve evaluates rational constants at the requested arbitrary precision.
- **sympy__sympy-16450** (partial)
  - The other assumption cases named in the report, such as rational=True, prime=True, even=True, and odd=True, are not tested.
  - The complete assumptions0 closure is not asserted; the real check is also weak evidence of preservation because positive=True already implies real=True.
- **sympy__sympy-19637** (partial)
  - The bug-report string must be parsed into the exact expression 2*x/(x-1), rather than merely producing a non-None expression-like object.
  - Parenthesized strings containing spaces must continue through the existing kern-replacement branch with hit computed from the replacement.
- **sympy__sympy-21596** (partial)
  - The assertion that the motivating intersection is exactly {-1, 1} with no other members.
  - The shifted-factor Integer case.
  - The factored Naturals0 case.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-13590** — nothing collected on either side -- the file never ran
- **django__django-14915** — nothing collected on either side -- the file never ran
- **django__django-16454** — nothing collected on either side -- the file never ran
- **django__django-16667** — nothing collected on either side -- the file never ran
