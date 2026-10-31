# Run status, per pull request

Last run in this table: 2026-10-31 10:39 UTC.

- **19** instances across **9** repositories
- **18/19** fail-to-pass, of those that reached a verdict

- **5** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **13/19**
- **Changed-line coverage (main): mean 35.0%** of the per-PR figures over the 18 measured YES PRs; median 39%
- **29%** of the changed lines those tests were measured against (388/1356, pooled)
- **26%** pooled without the lines that run on import (321/1223)
- **18%** of every source line all 19 patches change (388/2168), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)
- **11/18** of the judged YES tests are meaningful by the judge's first label
- \$3.18 and 44.3M tokens in total
- **13** of these had a stop refused at least once, and **12** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `passes_at_base` | 5 | 4 | 1 | 0 | not fail-to-pass yet |
| `skipped_at_base` | 1 | 1 | 0 | 0 | not fail-to-pass yet |
| `tricks_open` | 3 | 3 | 0 | 0 | — |
| `verify_open` | 4 | 4 | 0 | 0 | not fail-to-pass yet |

Of the **10** first refused as not fail-to-pass yet, **9** ended fail-to-pass.


### The second chance

**Rescued 5** of 6 restarted run(s): 6 ended without a YES and were restarted with the record of their first attempt (4 after a NO, 2 after a BROKEN), and 5 ended fail-to-pass on the second attempt: `pydata__xarray-6971`, `pydata__xarray-7444`, `pylint-dev__pylint-4551`, `sphinx-doc__sphinx-7590`, `sympy__sympy-14085`.


### Fail-to-pass, then lost

**16** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

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
| [`astropy__astropy-14295`](./astropy__astropy-14295/) |  | YES | 54% (27/50) | 5/20 | 10/20 | 18 | `run` x9, `run_tests` x2, `verify` x2, `write_file` x2 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-31 08:45 UTC |
| [`astropy__astropy-7008`](./astropy__astropy-7008/) |  | YES | 82% (22/27); 100% (17/17) without import-time | 12/20 | 12/20 | 46 | `run` x16, `write_file` x13, `verify` x9, `run_tests` x3  (+2 edits reverted) | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 08:49 UTC |
| [`django__django-16092`](./django__django-16092/) |  | YES | 13% (14/107); 14% (14/100) without import-time | 0/20 | 7/20 | 19 | `run` x10, `verify` x3, `write_file` x3, `run_tests` x1 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 13:36 UTC |
| [`django__django-11991`](./django__django-11991/) |  | YES | 36% (19/53); 40% (19/47) without import-time | 3/20 | 11/20 | 21 | `run` x12, `verify` x3, `run_tests` x2, `write_file` x2 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 14:23 UTC |
| [`matplotlib__matplotlib-25515`](./matplotlib__matplotlib-25515/) |  | YES | 8% (12/160); 5% (7/129) without import-time | 0/20 | 9/20 | 30 | `run` x10, `run_tests` x6, `write_file` x6, `verify` x4 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 09:03 UTC |
| [`matplotlib__matplotlib-19743`](./matplotlib__matplotlib-19743/) |  | YES | 43% (13/30) | 2/20 | 15/20 | 72 | `run` x22, `write_file` x17, `run_tests` x10, `verify` x9 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-31 09:27 UTC |
| [`matplotlib__matplotlib-20693`](./matplotlib__matplotlib-20693/) |  | YES | 13% (14/108) | 5/20 | 11/20 | 83 | `run` x21, `write_file` x18, `run_tests` x14, `verify` x14 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 10:01 UTC |
| [`pydata__xarray-6971`](./pydata__xarray-6971/) |  | YES | 1% (1/77); 1% (1/75) without import-time | 0/20 | 19/20 | 123 | `write_file` x33, `verify` x27, `run_tests` x25, `run` x12 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-31 10:39 UTC |
| [`pydata__xarray-7444`](./pydata__xarray-7444/) |  | YES | 80% (41/51); 79% (37/47) without import-time | 10/20 | 16/20 | 123 | `write_file` x36, `run_tests` x23, `run` x20, `verify` x17 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-28 18:06 UTC |
| [`pylint-dev__pylint-4551`](./pylint-dev__pylint-4551/) |  | YES | 16% (10/62); 9% (5/56) without import-time | 1/20 | 15/20 | 95 | `run` x29, `run_tests` x23, `write_file` x23, `verify` x9 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 13:01 UTC |
| [`pytest-dev__pytest-5787`](./pytest-dev__pytest-5787/) |  | YES | 59% (42/71) | 14/20 | 18/20 | 20 | `run` x9, `write_file` x4, `verify` x3, `run_tests` x2 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 11:16 UTC |
| [`scikit-learn__scikit-learn-14012`](./scikit-learn__scikit-learn-14012/) |  | YES | 65% (42/65); 60% (35/58) without import-time | 9/20 | 16/20 | 28 | `write_file` x8, `verify` x7, `run` x6, `run_tests` x3 | yes | developer's better (2) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 13:45 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) |  | YES | 43% (23/54); 32% (14/44) without import-time | 1/20 | 10/20 | 96 | `run` x39, `write_file` x23, `run_tests` x16, `verify` x7 | yes | developer's better (2) | developer's covers more (2) | less readable (2) | 2026-10-28 13:30 UTC |
| [`sphinx-doc__sphinx-7234`](./sphinx-doc__sphinx-7234/) |  | YES | 7% (5/76); 5% (3/56) without import-time | 0/20 | 18/20 | 53 | `run` x16, `write_file` x12, `run_tests` x11, `verify` x9 | no | developer's clearly better (1) | developer's covers clearly more (1) | clearly less readable (1) | 2026-10-28 18:56 UTC |
| [`sphinx-doc__sphinx-7380`](./sphinx-doc__sphinx-7380/) |  | YES | 39% (52/134); 30% (35/117) without import-time | 1/20 | 10/20 | 68 | `run` x18, `write_file` x15, `verify` x14, `run_tests` x7 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 12:40 UTC |
| [`sympy__sympy-13091`](./sympy__sympy-13091/) |  | NO | — | — | — | 83 | `write_file` x28, `run` x18, `run_tests` x15, `verify` x7 | — | — | — | — | 2026-10-29 07:18 UTC |
| [`sympy__sympy-17512`](./sympy__sympy-17512/) |  | YES | 25% (21/85); 22% (18/82) without import-time | 5/20 | 16/20 | 23 | `run` x14, `write_file` x3, `run_tests` x2, `verify` x2 | no | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-28 18:14 UTC |
| [`sympy__sympy-14085`](./sympy__sympy-14085/) |  | YES | 41% (24/58); 37% (20/54) without import-time | 4/20 | 4/20 | 117 | `write_file` x38, `run` x23, `verify` x20, `run_tests` x12 | yes | developer's better (2) | developer's covers clearly more (1) | less readable (2) | 2026-10-29 10:59 UTC |
| [`sympy__sympy-13236`](./sympy__sympy-13236/) |  | YES | 7% (6/88); 0% (0/82) without import-time | 1/20 | 13/20 | 68 | `write_file` x21, `run` x20, `run_tests` x15, `verify` x6 | no | developer's clearly better (1) | developer's covers clearly more (1) | as readable (3) | 2026-10-29 12:36 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **astropy__astropy-14295** (developer's covers clearly more (1))
  - The CAR-SIP reference pixel still transforms to the declared CRVAL values after PV preservation.
  - All-SIP TAN headers with high-index SCAMP PV terms retain SIP rather than discarding it.
  - All-SIP TAN headers with high-index SCAMP PV terms emit the redundant-SCAMP warning.
- **astropy__astropy-7008** (developer's covers clearly more (1))
  - Inside a supported context, CODATA constants use their astropyconst13 values.
  - Inside a supported context, IAU constants use their astropyconst13 values.
  - After the context exits, CODATA constants are restored to the current values.
- **django__django-16092** (developer's covers clearly more (1))
  - An omitted literal database default is applied by the database on creation.
  - A database expression default is evaluated by the database.
  - An ordinary Python default takes precedence when an explicit ordinary default is also defined.
- **django__django-11991** (developer's covers clearly more (1))
  - A covering partial index combines INCLUDE and WHERE clauses correctly.
  - Covering indexes are created, introspected with their key and included columns, and removed correctly on supporting databases.
  - Unsupported databases omit INCLUDE from generated SQL rather than emitting unsupported syntax.
- **matplotlib__matplotlib-25515** (developer's covers clearly more (1))
  - The normal-resolution plot image remains available when plot_srcset is enabled.
  - A requested 2x plot image is generated alongside the normal-resolution image.
  - Responsive image assets are copied correctly for nested documentation pages.
- **matplotlib__matplotlib-19743** (developer's covers clearly more (1))
  - Figure legends accept and correctly interpret the six outside upper/lower location forms.
  - An outside upper figure legend causes constrained layout to reserve top space and positions the axes below it.
  - An outside lower figure legend causes constrained layout to reserve bottom space and positions the axes above it.
- **matplotlib__matplotlib-20693** (developer's covers clearly more (1))
  - SpanSelector selection artist properties change through set_props.
  - RectangleSelector selection artist properties change through set_props.
  - PolygonSelector selection artist properties change through set_props.
- **pydata__xarray-6971** (developer's covers clearly more (1))
  - DataArray set_xindex can construct a custom index and forward options.
  - Dataset set_xindex can construct a custom index and forward options.
  - Dataset set_xindex creates the expected default single-coordinate pandas index.
- **pydata__xarray-7444** (developer's covers clearly more (1))
  - Base is converted to an offset and produces the correct pandas/CFTime resampling result.
  - Base-to-offset conversion agrees for pandas and CFTime tick frequencies.
  - Valid loffset values shift pandas resampling labels correctly.
- **pylint-dev__pylint-4551** (developer's covers clearly more (1))
  - A Subscript annotation retains its complete label, such as Optional[str].
  - AnnAssign annotations produce their declared labels, including explicit Optional annotations.
  - An AnnAssign annotation with a None default is normalized to Optional[str].
- **pytest-dev__pytest-5787** (developer's covers clearly more (1))
  - The innermost chained traceback retains its expected exception text.
  - The outermost chained traceback retains its expected exception text.
  - The direct-cause description is preserved exactly.
- **scikit-learn__scikit-learn-14012** (developer's covers clearly more (1))
  - A regressor warm-start fit with a larger max_iter reuses the previous ensemble and matches a one-shot fit to the final iteration count.
  - A classifier warm-start fit with a larger max_iter reuses the previous ensemble and matches a one-shot fit to the final iteration count.
  - A classifier rejects a smaller max_iter during warm starting.
- **sphinx-doc__sphinx-7590** (developer's covers more (2))
  - Character UDLs are consumed and represented with the correct UDL identity.
- **sphinx-doc__sphinx-7234** (developer's covers clearly more (1))
  - Autodoc documents a singledispatch function with its registered int and str overload signatures.
  - Autodoc documents a singledispatch method with its registered int and str overload signatures.
  - Registered implementation types are added as first-argument annotations in the rendered overload signatures.
- **sphinx-doc__sphinx-7380** (developer's covers clearly more (1))
  - Braced initializer lists work as assignment-expression initializer clauses and receive the expected representation.
  - Type template-argument pack expansions are accepted and encoded correctly.
  - Parenthesized constant template-argument pack expansions are accepted and retain the correct versioned identifiers.
- **sympy__sympy-17512** (developer's covers clearly more (1))
  - Explicit sympification of a native Python range still produces a SymPy Range.
  - Symbolic Range arguments are accepted and preserved as arguments.
  - Invalid noninteger symbolic Range arguments are rejected.
- **sympy__sympy-14085** (developer's covers clearly more (1))
  - Single factorial notation continues to parse correctly after the tokenizer change.
  - Double factorial notation continues to parse correctly.
  - More than two consecutive factorial markers are rejected.
- **sympy__sympy-13236** (developer's covers clearly more (1))
  - Modulo by zero raises `ZeroDivisionError`.
  - An unknown-type symbolic power is not unsafely reduced modulo its symbolic base.
  - A positive integer power of a symbolic multiple is divisible by its symbolic factor.
