# Run status, per pull request

Last run in this table: 2026-10-31 11:06 UTC.

- **19** instances across **9** repositories
- **18/19** fail-to-pass, of those that reached a verdict

- **3** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **15/19**
- **Changed-line coverage (main): mean 52.9%** of the per-PR figures over the 18 measured YES PRs; median 46%
- **50%** of the changed lines those tests were measured against (665/1328, pooled)
- **46%** pooled without the lines that run on import (555/1197)
- **31%** of every source line all 19 patches change (665/2168), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)
- **15/18** of the judged YES tests are meaningful by the judge's first label
- \$6.06 and 84.7M tokens in total
- **19** of these had a stop refused at least once, and **18** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[coverage]` | 6 | 6 | 0 | 0 | checks after fail-to-pass |
| `outputs_unread` | 2 | 2 | 0 | 0 | — |
| `passes_at_base` | 1 | 0 | 1 | 0 | not fail-to-pass yet |
| `tricks_open` | 4 | 4 | 0 | 0 | — |
| `verify_open` | 6 | 6 | 0 | 0 | not fail-to-pass yet |

Of the **7** first refused as not fail-to-pass yet, **6** ended fail-to-pass.


### The second chance

**Rescued 3** of 4 restarted run(s): 4 ended without a YES and were restarted with the record of their first attempt (0 after a NO, 4 after a BROKEN), and 3 ended fail-to-pass on the second attempt: `matplotlib__matplotlib-20693`, `pydata__xarray-6971`, `sphinx-doc__sphinx-7590`.


### Fail-to-pass, then lost

**16** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+coverage-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

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
| [`astropy__astropy-14295`](./astropy__astropy-14295/) |  | YES | 46% (23/50) | 5/20 | 10/20 | 61 | `write_file` x16, `verify` x13, `run` x10, `run_tests` x10 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:16 UTC |
| [`astropy__astropy-7008`](./astropy__astropy-7008/) |  | YES | 82% (22/27); 100% (17/17) without import-time | 13/20 | 12/20 | 50 | `run` x14, `verify` x13, `write_file` x13, `run_tests` x2, `compare` x1 | yes | developer's better (2) | same coverage (3) | less readable (2) | 2026-10-31 08:55 UTC |
| [`django__django-16092`](./django__django-16092/) |  | YES | 13% (14/107); 14% (14/100) without import-time | 0/20 | 7/20 | 85 | `run` x32, `verify` x17, `write_file` x17, `run_tests` x1 | yes | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 14:29 UTC |
| [`django__django-11991`](./django__django-11991/) |  | YES | 19% (10/53); 21% (10/47) without import-time | 3/20 | 11/20 | 79 | `run` x32, `verify` x16, `write_file` x14, `run_tests` x1 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-30 16:31 UTC |
| [`matplotlib__matplotlib-25515`](./matplotlib__matplotlib-25515/) |  | YES | 31% (49/160); 14% (18/129) without import-time | 5/20 | 9/20 | 71 | `write_file` x17, `run_tests` x16, `verify` x14, `run` x11 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:41 UTC |
| [`matplotlib__matplotlib-19743`](./matplotlib__matplotlib-19743/) |  | YES | 43% (13/30) | 2/20 | 15/20 | 49 | `run` x29, `verify` x6, `run_tests` x5, `write_file` x4 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-31 09:42 UTC |
| [`matplotlib__matplotlib-20693`](./matplotlib__matplotlib-20693/) |  | YES | 52% (56/108) | 8/20 | 11/20 | 124 | `write_file` x31, `run` x29, `verify` x29, `run_tests` x12, `compare` x1 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 11:00 UTC |
| [`pydata__xarray-6971`](./pydata__xarray-6971/) |  | YES | 1% (1/77); 1% (1/75) without import-time | 0/20 | 19/20 | 123 | `write_file` x35, `verify` x29, `run` x19, `run_tests` x17 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 11:06 UTC |
| [`pydata__xarray-7444`](./pydata__xarray-7444/) |  | YES | 98% (50/51); 98% (46/47) without import-time | 17/20 | 16/20 | 94 | `run` x35, `write_file` x16, `run_tests` x15, `verify` x15 | yes | on a par (3) | developer's covers more (2) | clearly less readable (1) | 2026-10-28 18:42 UTC |
| [`pylint-dev__pylint-4551`](./pylint-dev__pylint-4551/) |  | YES | 82% (51/62); 80% (45/56) without import-time | 12/20 | 15/20 | 63 | `run` x18, `verify` x16, `write_file` x15, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 13:11 UTC |
| [`pytest-dev__pytest-5787`](./pytest-dev__pytest-5787/) |  | YES | 100% (71/71) | 19/20 | 18/20 | 73 | `run` x27, `verify` x16, `write_file` x15, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 11:55 UTC |
| [`scikit-learn__scikit-learn-14012`](./scikit-learn__scikit-learn-14012/) |  | YES | 95% (62/65); 95% (55/58) without import-time | 16/20 | 16/20 | 66 | `verify` x21, `write_file` x19, `run` x11, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 15:05 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) |  | YES | 43% (23/54); 32% (14/44) without import-time | 2/20 | 10/20 | 123 | `run` x54, `write_file` x28, `run_tests` x10, `verify` x7 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 13:53 UTC |
| [`sphinx-doc__sphinx-7234`](./sphinx-doc__sphinx-7234/) |  | YES | 35% (28/80); 7% (4/56) without import-time | 8/20 | 18/20 | 99 | `write_file` x28, `run` x27, `verify` x27, `run_tests` x4 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 21:39 UTC |
| [`sphinx-doc__sphinx-7380`](./sphinx-doc__sphinx-7380/) |  | YES | 79% (106/134); 76% (89/117) without import-time | 7/20 | 10/20 | 92 | `write_file` x27, `verify` x26, `run` x22, `run_tests` x4 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 13:28 UTC |
| [`sympy__sympy-13091`](./sympy__sympy-13091/) |  | YES | 9% (5/56) | 3/20 | 4/20 | 79 | `write_file` x22, `run` x20, `verify` x20, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-29 10:45 UTC |
| [`sympy__sympy-17512`](./sympy__sympy-17512/) |  | YES | 34% (29/85); 32% (26/82) without import-time | 7/20 | 16/20 | 69 | `run` x26, `write_file` x15, `verify` x12, `run_tests` x4 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 18:42 UTC |
| [`sympy__sympy-14085`](./sympy__sympy-14085/) |  | YES | 90% (52/58); 89% (48/54) without import-time | 11/20 | 4/20 | 87 | `write_file` x26, `verify` x21, `run` x18, `run_tests` x7 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 11:25 UTC |
| [`sympy__sympy-13236`](./sympy__sympy-13236/) |  | NO | — | — | — | 106 | `run` x33, `write_file` x29, `verify` x15, `run_tests` x5 | — | — | — | — | 2026-10-29 12:17 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14295** (developer's covers clearly more (1))
  - The CAR-SIP case retains the SIP distortion object.
  - The CAR-SIP WCS maps CRPIX to the specified CRVAL.
  - Explicit -TPV CTYPE takes precedence over SIP and removes the SIP distortion.
- **astropy__astropy-7008** (same coverage (3))
  - Inside an astropyconst13 context, exported IAU constants also use their historical values.
  - After normal context exit, exported IAU constants are restored to their current values.
- **django__django-16092** (developer's covers clearly more (1))
  - A literal database default is applied when an object is created without an explicit value.
  - The database default is available after insertion both through RETURNING and after refresh on databases without RETURNING.
  - An expression database default is evaluated by the database.
- **django__django-11991** (developer's covers clearly more (1))
  - A supported backend emits INCLUDE columns for an ordinary covering index and can create, introspect, and remove it.
  - A supported backend combines INCLUDE columns with a partial index condition.
  - A covering unique constraint is created as a unique index and enforces uniqueness.
- **matplotlib__matplotlib-25515** (developer's covers clearly more (1))
  - A configured high-resolution image is generated for each root-level plot.
  - A configured high-resolution image is copied correctly for nested-page plots.
  - Root-level HTML contains the default and 2x image URLs with a 2.00x srcset descriptor.
- **matplotlib__matplotlib-19743** (developer's covers clearly more (1))
  - Figure legends are placed at the requested outside edge and corner for all supported location forms.
  - Constrained layout reserves the correct top or bottom margin for outside upper and lower locations.
  - Constrained layout reserves the correct left or right margin for outside left and right locations.
- **matplotlib__matplotlib-20693** (developer's covers clearly more (1))
  - set_props visibly updates a RectangleSelector's selection artist
  - set_props visibly updates a SpanSelector's selection artist
  - set_props visibly updates a PolygonSelector's selection artist
- **pydata__xarray-6971** (developer's covers clearly more (1))
  - A custom DataArray index can be created and receives constructor options.
  - Dataset.set_xindex with one coordinate creates the expected pandas index.
  - Dataset.set_xindex with multiple coordinates creates the expected pandas multi-index.
- **pydata__xarray-7444** (developer's covers more (2))
  - _convert_base_to_offset rejects indexes that are neither DatetimeIndex nor CFTimeIndex.
- **pylint-dev__pylint-4551** (developer's covers clearly more (1))
  - A non-Optional annotation on an attribute with a None default is labeled Optional[T].
  - When no annotation exists, successful inference still supplies the type set.
  - When inference raises InferenceError, the fallback type set is empty.
- **pytest-dev__pytest-5787** (developer's covers clearly more (1))
  - TestReport deserialization reconstructs an ExceptionChainRepr.
  - CollectReport serialization includes the exception chain.
  - CollectReport deserialization reconstructs an ExceptionChainRepr.
- **scikit-learn__scikit-learn-14012** (developer's covers clearly more (1))
  - Changing max_depth during warm-start preserves the old trees' depth and applies the new depth only to added trees.
  - Early stopping continues correctly when a second warm-start fit is performed.
  - A second fit with equal max_iter is a no-op and leaves the fitted ensemble unchanged.
- **sphinx-doc__sphinx-7590** (developer's covers clearly more (1))
  - An integer user-defined literal receives the correct AST identity and mangling.
  - Decimal floating-point user-defined literals, including the reported `q_J` case, receive the correct identity.
  - The other decimal floating-point forms support user-defined suffixes with the correct identity.
- **sphinx-doc__sphinx-7234** (developer's covers clearly more (1))
  - Autodoc renders the main singledispatch function and each non-default registered overload.
  - Autodoc renders the singledispatch method and each non-default registered overload.
  - The default object implementation is omitted from the displayed overload signatures.
- **sphinx-doc__sphinx-7380** (developer's covers clearly more (1))
  - Comma expressions receive the correct C++ domain ID encoding.
  - A type template argument followed by a pack expansion is parsed and receives the expected ID.
  - A parenthesized non-type template argument followed by a pack expansion is parsed with the expected IDs for versions 2 and 3.
- **sympy__sympy-13091** (developer's covers clearly more (1))
  - An unaware object compares unequal to a SymPy object when neither side supports the comparison.
  - Inequality uses operator-level equality dispatch so reflected custom equality remains symmetric.
  - Unsupported ordering comparisons with unknown numeric types raise TypeError.
- **sympy__sympy-17512** (developer's covers clearly more (1))
  - Sympifying a Python range still produces the equivalent SymPy Range.
  - An infinite positive step with a descending finite interval produces an empty Range.
  - Infinite positive and negative steps with finite intervals are canonicalized to the correct one-element Range.
- **sympy__sympy-14085** (developer's covers clearly more (1))
  - A Unicode identifier is parsed as the exact Symbol with that name.
  - A double factorial is parsed correctly.
  - Dot-only repeated decimals such as .[1] are accepted.
