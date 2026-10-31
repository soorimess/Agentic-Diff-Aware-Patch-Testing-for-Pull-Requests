# Run status, per pull request

Last run in this table: 2026-10-31 11:54 UTC.

- **19** instances across **9** repositories
- **19/19** fail-to-pass, of those that reached a verdict

- **4** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **15/19**
- **Changed-line coverage (main): mean 51.4%** of the per-PR figures over the 19 measured YES PRs; median 47%
- **47%** of the changed lines those tests were measured against (672/1416, pooled)
- **46%** pooled without the lines that run on import (582/1279)
- **31%** of every source line all 19 patches change (672/2168), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)
- **15/19** of the judged YES tests are meaningful by the judge's first label
- \$6.40 and 89.3M tokens in total
- **19** of these had a stop refused at least once, and **19** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[coverage+mutation]` | 8 | 8 | 0 | 0 | checks after fail-to-pass |
| `tricks_open` | 5 | 5 | 0 | 0 | — |
| `verify_open` | 6 | 6 | 0 | 0 | not fail-to-pass yet |

Of the **6** first refused as not fail-to-pass yet, **6** ended fail-to-pass.


### The second chance

**Rescued 4** of 4 restarted run(s): 4 ended without a YES and were restarted with the record of their first attempt (1 after a NO, 3 after a BROKEN), and 4 ended fail-to-pass on the second attempt: `pylint-dev__pylint-4551`, `sphinx-doc__sphinx-7234`, `sympy__sympy-14085`, `sympy__sympy-13236`.


### Fail-to-pass, then lost

**18** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

The three judge columns compare the generated test with the developer's, from 1 (the developer's clearly better) through 3 (on a par) to 5 (the generated clearly better), printed as `label (level)`:

| scale | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| concept -- which pins the fix's behaviour better? | developer's clearly better | developer's better | on a par | generated better | generated clearly better |
| issue -- which covers more of what the fix settles? | developer's covers clearly more | developer's covers more | same coverage | generated covers more | generated covers clearly more |
| readable -- which reads better? | clearly less readable | less readable | as readable | more readable | clearly more readable |

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14295`](./astropy__astropy-14295/) |  | YES | 40% (20/50) | 6/20 | 10/20 | 63 | `write_file` x17, `verify` x13, `run` x12, `run_tests` x4 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:30 UTC |
| [`astropy__astropy-7008`](./astropy__astropy-7008/) |  | YES | 82% (22/27); 100% (17/17) without import-time | 13/20 | 12/20 | 45 | `verify` x13, `write_file` x12, `run` x11, `run_tests` x1 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:00 UTC |
| [`django__django-16092`](./django__django-16092/) |  | YES | 13% (14/107); 14% (14/100) without import-time | 0/20 | 7/20 | 94 | `run` x35, `write_file` x19, `verify` x18, `run_tests` x4 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 14:41 UTC |
| [`django__django-11991`](./django__django-11991/) |  | YES | 47% (25/53); 53% (25/47) without import-time | 3/20 | 11/20 | 43 | `run` x15, `verify` x9, `write_file` x8, `run_tests` x2 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-30 16:24 UTC |
| [`matplotlib__matplotlib-25515`](./matplotlib__matplotlib-25515/) |  | YES | 8% (12/160); 5% (7/129) without import-time | 0/20 | 9/20 | 78 | `write_file` x22, `run` x19, `verify` x18, `run_tests` x3 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:51 UTC |
| [`matplotlib__matplotlib-19743`](./matplotlib__matplotlib-19743/) |  | YES | 43% (13/30) | 2/20 | 15/20 | 69 | `run` x30, `verify` x12, `write_file` x12, `run_tests` x7 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 10:26 UTC |
| [`matplotlib__matplotlib-20693`](./matplotlib__matplotlib-20693/) |  | YES | 57% (62/108) | 6/20 | 11/20 | 92 | `run` x27, `write_file` x20, `run_tests` x14, `verify` x14 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 10:46 UTC |
| [`pydata__xarray-6971`](./pydata__xarray-6971/) |  | YES | 87% (67/77); 89% (67/75) without import-time | 17/20 | 19/20 | 81 | `verify` x23, `write_file` x23, `run` x19, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-31 11:54 UTC |
| [`pydata__xarray-7444`](./pydata__xarray-7444/) |  | YES | 98% (50/51); 98% (46/47) without import-time | 15/20 | 16/20 | 53 | `run` x17, `write_file` x12, `verify` x11, `run_tests` x5 | yes | developer's better (2) | developer's covers more (2) | less readable (2) | 2026-10-28 18:23 UTC |
| [`pylint-dev__pylint-4551`](./pylint-dev__pylint-4551/) |  | YES | 18% (11/62); 11% (6/56) without import-time | 1/20 | 15/20 | 125 | `write_file` x36, `run_tests` x23, `verify` x23, `run` x20 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 13:16 UTC |
| [`pytest-dev__pytest-5787`](./pytest-dev__pytest-5787/) |  | YES | 97% (69/71) | 19/20 | 18/20 | 74 | `run` x27, `verify` x16, `write_file` x15, `run_tests` x4 | yes | developer's better (2) | same coverage (3) | clearly less readable (1) | 2026-10-28 12:03 UTC |
| [`scikit-learn__scikit-learn-14012`](./scikit-learn__scikit-learn-14012/) |  | YES | 98% (64/65); 98% (57/58) without import-time | 17/20 | 16/20 | 60 | `run` x22, `verify` x15, `write_file` x14, `run_tests` x2 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 15:04 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) |  | YES | 63% (34/54); 54% (24/44) without import-time | 2/20 | 10/20 | 106 | `run` x35, `write_file` x28, `verify` x23, `run_tests` x7 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 14:43 UTC |
| [`sphinx-doc__sphinx-7234`](./sphinx-doc__sphinx-7234/) |  | YES | 35% (28/80); 7% (4/56) without import-time | 5/20 | 18/20 | 124 | `run` x33, `verify` x30, `write_file` x29, `run_tests` x3 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 22:28 UTC |
| [`sphinx-doc__sphinx-7380`](./sphinx-doc__sphinx-7380/) |  | YES | 65% (87/134); 60% (70/117) without import-time | 5/20 | 10/20 | 77 | `verify` x22, `write_file` x22, `run` x12, `run_tests` x6 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 14:07 UTC |
| [`sympy__sympy-13091`](./sympy__sympy-13091/) |  | YES | 7% (4/56) | 3/20 | 4/20 | 96 | `verify` x29, `write_file` x29, `run` x24, `run_tests` x1 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 11:18 UTC |
| [`sympy__sympy-17512`](./sympy__sympy-17512/) |  | YES | 56% (48/85); 55% (45/82) without import-time | 8/20 | 16/20 | 88 | `write_file` x25, `verify` x23, `run` x21, `run_tests` x4 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-28 19:18 UTC |
| [`sympy__sympy-14085`](./sympy__sympy-14085/) |  | YES | 41% (24/58); 37% (20/54) without import-time | 4/20 | 4/20 | 123 | `run` x43, `write_file` x28, `verify` x18, `run_tests` x8 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 11:51 UTC |
| [`sympy__sympy-13236`](./sympy__sympy-13236/) |  | YES | 20% (18/88); 15% (12/82) without import-time | 2/20 | 13/20 | 125 | `run` x36, `write_file` x33, `verify` x26, `run_tests` x11 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 13:49 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14295** (developer's covers clearly more (1))
  - CAR-SIP transformation remains centered at the CRVAL coordinates.
  - Explicit -TPV CTYPE causes SIP distortion parameters to be discarded.
  - Pre-2012 TAN headers with high-order SCAMP PV parameters do not load SIP distortion parameters.
- **astropy__astropy-7008** (developer's covers clearly more (1))
  - A valid astropyconst13 context exposes the old CODATA2010/IAU2012 constant values.
  - Normal context exit restores the CODATA2014/IAU2015 default values.
  - Context exit restores the defaults even when the context body raises an exception.
- **django__django-16092** (developer's covers clearly more (1))
  - An omitted field receives its literal database default on model creation.
  - An omitted field receives an expression-derived database default.
  - A raw database insert uses db_default while an ORM insert can use the separate Python default.
- **django__django-11991** (developer's covers clearly more (1))
  - A supported backend generates and installs a normal covering index with the key and included columns, and can remove it.
  - A supported backend generates a covering partial index with INCLUDE before WHERE.
  - A supported backend creates a unique covering index whose key uniqueness is enforced.
- **matplotlib__matplotlib-25515** (developer's covers clearly more (1))
  - Each top-level plot produces both the normal-resolution image and its configured 2x companion.
  - The normal-resolution image remains available as the fallback image for each top-level plot.
  - Nested-page plots also produce correctly named 2x companion files.
- **matplotlib__matplotlib-19743** (developer's covers clearly more (1))
  - Outside upper figure legends reserve the correct top margin and have the expected upper placement.
  - Outside lower figure legends reserve the correct bottom margin and have the expected lower placement.
  - Outside left figure legends reserve the correct left margin and have the expected left placement.
- **matplotlib__matplotlib-20693** (developer's covers clearly more (1))
  - set_props updates the RectangleSelector selection artist's requested properties
  - set_handle_props updates the requested property on every RectangleSelector handle
  - set_props updates the SpanSelector selection artist's requested properties
- **pydata__xarray-6971** (developer's covers clearly more (1))
  - A custom Index class receives options passed through set_xindex.
  - set_xindex rejects an index class that is not an Index subclass.
  - Dataset.drop_indexes can remove multiple indexes in one call.
- **pydata__xarray-7444** (developer's covers more (2))
  - Legacy base is translated correctly for a pandas DatetimeIndex and produces the pandas-compatible resampling result.
  - Legacy base is translated correctly for a CFTimeIndex and produces the pandas-compatible resampling result.
  - loffset is applied to pandas resampling labels for supported offset types.
- **pylint-dev__pylint-4551** (developer's covers clearly more (1))
  - AnnAssign annotations are extracted, with a bare annotation and None default represented as Optional.
  - Existing Optional annotations and non-None AnnAssign defaults retain the declared annotation.
  - Constructor argument annotations are applied to instance attributes, including Optional handling.
- **pytest-dev__pytest-5787** (same coverage (3))
  - A chained CollectReport retains its exception chain after serialization and deserialization.
- **scikit-learn__scikit-learn-14012** (developer's covers clearly more (1))
  - A warm fit with equal max_iter leaves the existing ensemble unchanged.
  - Previously fitted trees retain their original max_depth when max_depth changes between warm fits.
  - New trees use the changed max_depth after a warm fit.
- **sphinx-doc__sphinx-7590** (developer's covers clearly more (1))
  - Character literals can have user-defined literal identifiers.
  - String literals can have user-defined literal identifiers.
  - A UDL's description/reference target is represented as operator"" followed by its identifier.
- **sphinx-doc__sphinx-7234** (developer's covers clearly more (1))
  - Function autodoc emits the registered int and str implementation signatures with inferred first-argument types.
  - The function autodoc header omits the default object implementation.
  - Method autodoc emits the registered int and str implementation signatures with inferred first-argument types.
- **sphinx-doc__sphinx-7380** (developer's covers clearly more (1))
  - Comma expressions are parsed as comma-expression ASTs and receive the expected encoding.
  - Parenthesized constant-expression template arguments with pack expansion are parsed and receive the expected IDs.
  - Type or function-pointer template arguments with pack expansion are parsed and receive the expected ID.
- **sympy__sympy-13091** (developer's covers clearly more (1))
  - Basic inequality uses operator equality and therefore observes reflected equality.
  - An unknown object with no reflected equality remains unequal to Basic.
  - Ordinary Number equality permits a custom reflected equality implementation.
- **sympy__sympy-17512** (developer's covers clearly more (1))
  - A positive infinite step produces the canonical singleton for a forward range.
  - A positive infinite step produces an empty range when the direction is invalid.
  - A negative infinite step produces the canonical singleton for a reverse range.
- **sympy__sympy-14085** (developer's covers clearly more (1))
  - Single and double factorial notation continues to produce the correct factorial expressions after switching tokenizers.
  - Repeating decimals such as 3.2[3] produce the exact corresponding Rational.
  - Repeating decimals with omitted integer or nonrepeating fractional parts, such as .[1], are supported.
- **sympy__sympy-13236** (developer's covers clearly more (1))
  - A factorial whose argument is known to exceed the modulus is divisible by that modulus.
  - An undecidable factorial/modulus boundary remains as Mod rather than being incorrectly simplified.
  - Modulo by zero raises ZeroDivisionError.
