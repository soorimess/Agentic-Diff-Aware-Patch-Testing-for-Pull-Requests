# Run status, per pull request

Last run in this table: 2026-09-24 21:17 UTC.

- **70** instances across **12** repositories
- **29/64** fail-to-pass, of those that reached a verdict
- **29** measured for changed-line coverage: **mean 89%** per test, median 100%
- **76%** of the changed lines those tests were measured against (119/157, pooled)
- **23%** of every source line all 70 patches change (119/508) -- a fixed denominator, so this is the figure that compares across arms
- \$1.97 and 26.7M tokens in total
- **24** of these were sent a second-chance message after stopping with nothing to score, and **3** of them ended fail-to-pass; the other 46 finished or failed for a reason the agent could not have seen at base


### What the refused runs did next

`loop_open` belongs to `require-tools` and fires with or without `--second-chance`; the rows marked *added by the flag* are the ones this flag is answerable for.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `collects_nothing` | 9 | 3 | 0 | 6 | **added by the flag** |
| `passes_at_base` | 15 | 0 | 15 | 0 | **added by the flag** |

Of the **24** refused for a reason the flag itself adds, **3** ended fail-to-pass.

Every row was produced with the same configuration: **`no-verify-tool+coverage-tool+mutation-tool+require-tools`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14369`](./astropy__astropy-14369/) | 5.1 | NO | — | — | — | 25 | `run` x12, `write_file` x7 | — | — | — | 2026-09-24 21:02 UTC |
| [`astropy__astropy-14539`](./astropy__astropy-14539/) | 5.1 | YES | 100% (1/1) | 7/7 | 7/7 | 22 | `run` x15, `write_file` x4 | different | partial | poor | 2026-09-24 20:54 UTC |
| [`astropy__astropy-14598`](./astropy__astropy-14598/) | 5.2 | YES | 100% (2/2) | 3/4 | 3/4 | 11 | `run` x7, `write_file` x2 | narrower | partial | acceptable | 2026-09-24 20:53 UTC |
| [`astropy__astropy-7606`](./astropy__astropy-7606/) | 1.3 | YES | 83% (5/6) | 0/9 | 9/9 | 17 | `run` x12, `write_file` x3 | narrower | partial | poor | 2026-09-24 20:57 UTC |
| [`django__django-10914`](./django__django-10914/) | 3.0 | BROKEN | — | — | — | 39 | `run` x24, `write_file` x9, `run_tests` x2 | — | — | — | 2026-09-24 20:58 UTC |
| [`django__django-11179`](./django__django-11179/) | 3.0 | NO | — | — | — | 40 | `run` x19, `write_file` x10, `run_tests` x6 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-11477`](./django__django-11477/) | 3.0 | NO | — | — | — | 30 | `run` x22, `write_file` x5 | — | — | — | 2026-09-24 20:57 UTC |
| [`django__django-12308`](./django__django-12308/) | 3.1 | YES | 60% (3/5) | 1/6 | 4/6 | 34 | `run` x21, `write_file` x4, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 20:57 UTC |
| [`django__django-12965`](./django__django-12965/) | 3.2 | NO | — | — | — | 31 | `run` x22, `write_file` x6 | — | — | — | 2026-09-24 20:55 UTC |
| [`django__django-13012`](./django__django-13012/) | 3.2 | BROKEN | — | — | — | 39 | `run` x26, `write_file` x9 | — | — | — | 2026-09-24 20:57 UTC |
| [`django__django-13023`](./django__django-13023/) | 3.2 | YES | 100% (1/1) | no mutants | no mutants | 23 | `run` x16, `write_file` x5 | narrower | partial | acceptable | 2026-09-24 20:57 UTC |
| [`django__django-13449`](./django__django-13449/) | 3.2 | NO | — | — | — | 23 | `run` x14, `write_file` x5 | — | — | — | 2026-09-24 20:57 UTC |
| [`django__django-13513`](./django__django-13513/) | 3.2 | NO | — | — | — | 37 | `run` x20, `write_file` x11 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-13590`](./django__django-13590/) | 3.2 | YES | 100% (5/5) | 10/10 | 9/10 | 19 | `run` x11, `write_file` x5 | broader | complete | acceptable | 2026-09-24 20:56 UTC |
| [`django__django-13794`](./django__django-13794/) | 3.2 | BROKEN | — | — | — | 45 | `run` x30, `write_file` x11 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-14534`](./django__django-14534/) | 4.0 | YES | 100% (1/1) | no mutants | no mutants | 35 | `run` x24, `write_file` x6 | narrower | partial | poor | 2026-09-24 20:58 UTC |
| [`django__django-14559`](./django__django-14559/) | 4.0 | NO | — | — | — | 20 | `run` x12, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-24 20:54 UTC |
| [`django__django-14580`](./django__django-14580/) | 4.0 | YES | 100% (1/1) | 6/6 | 6/6 | 27 | `run` x19, `write_file` x5, `run_tests` x1 | same | complete | acceptable | 2026-09-24 20:54 UTC |
| [`django__django-14608`](./django__django-14608/) | 4.0 | BROKEN | — | — | — | 46 | `run` x32, `write_file` x9 | — | — | — | 2026-09-24 20:58 UTC |
| [`django__django-14725`](./django__django-14725/) | 4.1 | BROKEN | — | — | — | 28 | `run` x20, `write_file` x4 | — | — | — | 2026-09-24 20:58 UTC |
| [`django__django-14765`](./django__django-14765/) | 4.0 | YES | 100% (4/4) | 3/3 | 1/3 | 24 | `run` x13, `write_file` x6 | broader | complete | acceptable | 2026-09-24 20:57 UTC |
| [`django__django-14792`](./django__django-14792/) | 4.0 | NO | — | — | — | 30 | `run` x20, `write_file` x6 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-14915`](./django__django-14915/) | 4.1 | YES | 100% (2/2) | 0/1 | 1/1 | 20 | `run` x14, `run_tests` x2, `write_file` x2 | same | partial | poor | 2026-09-24 20:55 UTC |
| [`django__django-15252`](./django__django-15252/) | 4.1 | NO | — | — | — | 23 | `run` x13, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-15569`](./django__django-15569/) | 4.1 | BROKEN | — | — | — | 32 | `run` x24, `write_file` x4, `run_tests` x1 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-16136`](./django__django-16136/) | 4.2 | NO | — | — | — | 35 | `run` x26, `write_file` x5, `run_tests` x1 | — | — | — | 2026-09-24 20:56 UTC |
| [`django__django-16139`](./django__django-16139/) | 4.2 | YES | 100% (1/1) | 2/2 | 2/2 | 20 | `run` x14, `run_tests` x2, `write_file` x2 | narrower | complete | acceptable | 2026-09-24 20:56 UTC |
| [`django__django-16454`](./django__django-16454/) | 5.0 | YES | 100% (6/6) | 9/10 | 9/10 | 35 | `run` x24, `write_file` x8 | same | partial | acceptable | 2026-09-24 21:00 UTC |
| [`django__django-16560`](./django__django-16560/) | 5.0 | NO | — | — | — | 44 | `run` x31, `write_file` x8 | — | — | — | 2026-09-24 20:57 UTC |
| [`django__django-16642`](./django__django-16642/) | 5.0 | NO | — | — | — | 29 | `run` x21, `write_file` x5 | — | — | — | 2026-09-24 20:58 UTC |
| [`django__django-16667`](./django__django-16667/) | 5.0 | YES | 100% (2/2) | 1/1 | 1/1 | 17 | `run` x9, `run_tests` x3, `write_file` x3 | narrower | partial | acceptable | 2026-09-24 20:58 UTC |
| [`matplotlib__matplotlib-20676`](./matplotlib__matplotlib-20676/) | 3.4 | YES | 75% (3/4) | 9/10 | 10/10 | 27 | `run` x16, `write_file` x5, `run_tests` x2 | narrower | partial | acceptable | 2026-09-24 21:02 UTC |
| [`matplotlib__matplotlib-20859`](./matplotlib__matplotlib-20859/) | 3.4 | YES | 67% (2/3) | no mutants | no mutants | 17 | `run` x12, `write_file` x2 | narrower | partial | poor | 2026-09-24 20:59 UTC |
| [`matplotlib__matplotlib-24870`](./matplotlib__matplotlib-24870/) | 3.6 | NO | — | — | — | 29 | `run` x18, `write_file` x7 | — | — | — | 2026-09-24 21:06 UTC |
| [`matplotlib__matplotlib-24970`](./matplotlib__matplotlib-24970/) | 3.6 | YES | 33% (2/6) | 1/10 | 1/10 | 13 | `run` x7, `write_file` x3 | different | partial | poor | 2026-09-24 21:02 UTC |
| [`matplotlib__matplotlib-25960`](./matplotlib__matplotlib-25960/) | 3.7 | NO | — | — | — | 30 | `run` x16, `write_file` x8 | — | — | — | 2026-09-24 21:08 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 41 | `run` x26, `write_file` x9 | — | — | — | 2026-09-24 21:07 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 3/4 | 1/4 | 17 | `run` x8, `run_tests` x5, `write_file` x2 | broader | complete | acceptable | 2026-09-24 21:01 UTC |
| [`psf__requests-2931`](./psf__requests-2931/) | 2.9 | NO | — | — | — | 21 | `run` x12, `run_tests` x3, `write_file` x3 | — | — | — | 2026-09-24 21:02 UTC |
| [`pydata__xarray-2905`](./pydata__xarray-2905/) | 0.12 | NO | — | — | — | 22 | `run` x14, `write_file` x5 | — | — | — | 2026-09-24 21:04 UTC |
| [`pydata__xarray-4075`](./pydata__xarray-4075/) | 0.12 | YES | 67% (2/3) | 4/10 | 4/10 | 16 | `run` x11, `write_file` x3 | same | complete | acceptable | 2026-09-24 21:05 UTC |
| [`pydata__xarray-4629`](./pydata__xarray-4629/) | 0.12 | NO | — | — | — | 14 | `run` x9, `write_file` x3 | — | — | — | 2026-09-24 21:03 UTC |
| [`pydata__xarray-4687`](./pydata__xarray-4687/) | 0.12 | NO | — | — | — | 34 | `run` x22, `write_file` x7 | — | — | — | 2026-09-24 21:11 UTC |
| [`pydata__xarray-6744`](./pydata__xarray-6744/) | 2022.06 | YES | 100% (9/9) | 10/10 | 10/10 | 15 | `run` x9, `write_file` x4 | narrower | partial | acceptable | 2026-09-24 21:07 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | NO | — | — | — | 37 | `run` x19, `write_file` x6, `run_tests` x5 | — | — | — | 2026-09-24 21:06 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | NO | — | — | — | 11 | `run` x7, `write_file` x2 | — | — | — | 2026-09-24 21:00 UTC |
| [`pytest-dev__pytest-6197`](./pytest-dev__pytest-6197/) | 5.2 | NO | — | — | — | 26 | `run` x11, `write_file` x5, `run_tests` x4 | — | — | — | 2026-09-24 21:06 UTC |
| [`pytest-dev__pytest-6202`](./pytest-dev__pytest-6202/) | 5.2 | NO | — | — | — | 37 | `run` x22, `write_file` x11 | — | — | — | 2026-09-24 21:06 UTC |
| [`scikit-learn__scikit-learn-10297`](./scikit-learn__scikit-learn-10297/) | 0.20 | NO | — | — | — | 17 | `run` x13, `write_file` x2 | — | — | — | 2026-09-24 21:04 UTC |
| [`scikit-learn__scikit-learn-13124`](./scikit-learn__scikit-learn-13124/) | 0.21 | NO | — | — | — | 30 | `run` x10, `write_file` x7, `run_tests` x6 | — | — | — | 2026-09-24 21:13 UTC |
| [`scikit-learn__scikit-learn-14087`](./scikit-learn__scikit-learn-14087/) | 0.22 | NO | — | — | — | 20 | `run` x14, `write_file` x3 | — | — | — | 2026-09-24 21:04 UTC |
| [`scikit-learn__scikit-learn-9288`](./scikit-learn__scikit-learn-9288/) | 0.22 | YES | 100% (3/3) | 9/9 | 9/9 | 11 | `run` x7, `run_tests` x1, `write_file` x1 | same | complete | acceptable | 2026-09-24 21:02 UTC |
| [`sphinx-doc__sphinx-7462`](./sphinx-doc__sphinx-7462/) | 3.1 | YES | 70% (7/10) | 3/10 | 6/10 | 25 | `run` x19, `write_file` x4 | narrower | partial | poor | 2026-09-24 21:04 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) | 3.1 | YES | 55% (26/47) | 1/10 | 4/10 | 33 | `run` x23, `run_tests` x4, `write_file` x4 | narrower | partial | poor | 2026-09-24 21:07 UTC |
| [`sphinx-doc__sphinx-7757`](./sphinx-doc__sphinx-7757/) | 3.1 | YES | 81% (13/16) | 8/10 | 8/10 | 17 | `run` x14, `write_file` x1 | broader | complete | acceptable | 2026-09-24 21:02 UTC |
| [`sphinx-doc__sphinx-8035`](./sphinx-doc__sphinx-8035/) | 3.2 | NO | — | — | — | 34 | `run` x24, `write_file` x6 | — | — | — | 2026-09-24 21:10 UTC |
| [`sphinx-doc__sphinx-8459`](./sphinx-doc__sphinx-8459/) | 3.4 | NO | — | — | — | 39 | `run` x27, `write_file` x7 | — | — | — | 2026-09-24 21:11 UTC |
| [`sphinx-doc__sphinx-9591`](./sphinx-doc__sphinx-9591/) | 4.2 | NO | — | — | — | 33 | `run` x14, `write_file` x8, `run_tests` x6 | — | — | — | 2026-09-24 21:11 UTC |
| [`sphinx-doc__sphinx-9658`](./sphinx-doc__sphinx-9658/) | 4.3 | NO | — | — | — | 23 | `run` x12, `write_file` x6 | — | — | — | 2026-09-24 21:06 UTC |
| [`sympy__sympy-12489`](./sympy__sympy-12489/) | 1.0 | NO | — | — | — | 35 | `run` x16, `write_file` x8, `run_tests` x6 | — | — | — | 2026-09-24 21:08 UTC |
| [`sympy__sympy-13551`](./sympy__sympy-13551/) | 1.1 | NO | — | — | — | 17 | `run` x11, `write_file` x3 | — | — | — | 2026-09-24 21:04 UTC |
| [`sympy__sympy-14976`](./sympy__sympy-14976/) | 1.2 | NO | — | — | — | 27 | `run` x12, `write_file` x6, `run_tests` x5 | — | — | — | 2026-09-24 21:07 UTC |
| [`sympy__sympy-15349`](./sympy__sympy-15349/) | 1.4 | YES | 100% (1/1) | 6/7 | 6/7 | 21 | `run` x13, `write_file` x3, `run_tests` x2 | narrower | complete | acceptable | 2026-09-24 21:08 UTC |
| [`sympy__sympy-16450`](./sympy__sympy-16450/) | 1.5 | YES | 100% (1/1) | 2/7 | 7/7 | 13 | `run` x10, `write_file` x1 | broader | partial | acceptable | 2026-09-24 21:17 UTC |
| [`sympy__sympy-16766`](./sympy__sympy-16766/) | 1.5 | NO | — | — | — | 22 | `run` x17, `write_file` x3 | — | — | — | 2026-09-24 21:06 UTC |
| [`sympy__sympy-17318`](./sympy__sympy-17318/) | 1.5 | NO | — | — | — | 20 | `run` x14, `write_file` x3 | — | — | — | 2026-09-24 21:07 UTC |
| [`sympy__sympy-18189`](./sympy__sympy-18189/) | 1.6 | YES | 100% (1/1) | 5/7 | 5/7 | 12 | `run` x9, `write_file` x2 | same | complete | acceptable | 2026-09-24 21:11 UTC |
| [`sympy__sympy-19637`](./sympy__sympy-19637/) | 1.7 | YES | 100% (2/2) | 1/4 | 3/4 | 18 | `run` x8, `write_file` x4, `run_tests` x3 | narrower | partial | poor | 2026-09-24 21:08 UTC |
| [`sympy__sympy-20590`](./sympy__sympy-20590/) | 1.7 | YES | 100% (1/1) | 1/1 | 1/1 | 22 | `run` x16, `write_file` x2 | narrower | partial | poor | 2026-09-24 21:08 UTC |
| [`sympy__sympy-21596`](./sympy__sympy-21596/) | 1.9 | YES | 91% (10/11) | no mutants | no mutants | 29 | `run` x23, `write_file` x3 | narrower | partial | poor | 2026-09-24 21:11 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14539** (partial)
  - Q-format variable-length array columns with unequal contents produce the correct per-row differences and aggregate report.
- **astropy__astropy-14598** (partial)
  - A long FITS string containing `''` followed by a space and more value text round-trips unchanged.
- **astropy__astropy-7606** (partial)
  - UnrecognizedUnit equality with None evaluates to False.
  - UnrecognizedUnit inequality with None evaluates to True.
  - UnitBase's NotImplemented/reflected-comparison behaviour.
- **django__django-12308** (partial)
  - Truthy values that cannot be JSON-encoded fall back to ordinary display_for_value output instead of raising.
- **django__django-13023** (partial)
  - The decimal.InvalidOperation path for a nonnumeric string is not tested.
  - The ValueError path for a malformed tuple such as () is not tested.
- **django__django-14534** (partial)
  - The custom auto_id='prefix_%s' case that produces prefix_field_0 and prefix_field_1.
  - The second checkbox subwidget's id_for_label value.
  - The no-id case, where id_for_label should return None.
- **django__django-14915** (partial)
  - Its hash is derived from the wrapped value, so equal wrapped values have equal hashes and the tested different values have different hashes.
  - Membership lookup with a ModelChoiceIteratorValue against a dictionary keyed by its underlying scalar value succeeds and returns true.
- **django__django-16454** (partial)
  - The resulting command-line error must be rendered as the expected usage and error text rather than a traceback.
  - The explicit non-CommandParser parser_class branch must retain normal argparse error formatting.
- **django__django-16667** (partial)
  - A form using SelectDateWidget treats the oversized submission as an invalid date with "Enter a valid date." instead of allowing the request to crash.
- **matplotlib__matplotlib-20676** (partial)
  - Interactive horizontal initialization places edge handles at the existing x-axis bounds.
  - Interactive vertical initialization preserves the existing y-axis bounds.
  - Interactive vertical initialization places edge handles at the existing y-axis bounds.
- **matplotlib__matplotlib-20859** (partial)
  - The created legend is attached to the exact SubFigure that created it.
  - An ordinary Figure remains accepted as a FigureBase legend parent.
  - An unsupported parent raises TypeError with the updated `FigureBase` diagnostic.
- **matplotlib__matplotlib-24970** (partial)
  - The returned colormap value remains correct for the uint8 input.
  - The returned colormap value remains correct for the signed integer input.
  - The returned colormap value remains correct for float16 and float inputs.
- **pydata__xarray-6744** (partial)
  - center=True manual iteration for window sizes 1, 2, and 7, including the even-window alignment case
  - center=False manual iteration for window sizes 1, 2, and 7
- **sphinx-doc__sphinx-7462** (partial)
  - The exact doctree representation of `Tuple[()]` with `(` and `)` punctuation nodes.
  - The separate AST unparser result `"()"` for an empty tuple.
- **sphinx-doc__sphinx-7590** (partial)
  - The C-domain literal parser accepts valid integer and floating-point suffixes using the dedicated suffix regexes.
  - The C++-domain literal parser recognizes standard numeric suffixes while allowing a following UDL identifier.
  - C++ UDLs attach correctly to integer literals, including integer forms with suffix-like text.
- **sympy__sympy-16450** (partial)
  - Preservation of the other assumption types handled by the generic assumptions0 forwarding, such as rational, prime, even, and odd
  - Preservation of the complete inferred assumption set rather than only the selected finite and integer entries
- **sympy__sympy-19637** (partial)
  - The no-space parenthesized input must produce the correct parsed symbolic expression, not merely a non-None result.
  - The parenthesized-with-spaces branch is not exercised.
- **sympy__sympy-20590** (partial)
  - Assigning an undeclared attribute to a slotted SymPy object raises `AttributeError`.
- **sympy__sympy-21596** (partial)
  - The full reported intersection is exactly FiniteSet(-1, 1); the generated test only checks selected candidate values.
  - Noninteger-root filtering over Integers.
  - Domain-aware root filtering over Naturals0.

## Without a verdict

- **django__django-10914** — nothing collected on either side -- the file never ran
- **django__django-13012** — nothing collected on either side -- the file never ran
- **django__django-13794** — nothing collected on either side -- the file never ran
- **django__django-14608** — nothing collected on either side -- the file never ran
- **django__django-14725** — nothing collected on either side -- the file never ran
- **django__django-15569** — nothing collected on either side -- the file never ran
