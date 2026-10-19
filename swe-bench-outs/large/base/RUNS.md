# Run status, per pull request

Last run in this table: 2026-10-16 10:29 UTC.

- **35** instances across **10** repositories
- **29/35** fail-to-pass, of those that reached a verdict

- **2** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **27/35**
- **Changed-line coverage (main): mean 39.6%** of the per-PR figures over the 29 measured YES PRs; median 42%
- **30%** of the changed lines those tests were measured against (912/3040, pooled)
- **27%** pooled without the lines that run on import (756/2803)
- **16%** of every source line all 35 patches change (912/5649), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$12.45 and 174.7M tokens in total
- **2 of 3207** model replies arrived empty -- no text and no tool call, and three of those in a row trip OpenHands' stuck detector, which ends the run. A run losing turns at that rate is bounded by its transport rather than by the model, and the verdicts below should be read with that in mind
- **35** of these had a stop refused at least once, and **29** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[coverage+mutation]` | 26 | 26 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 7 | 2 | 5 | 0 | not fail-to-pass yet |
| `verify_open` | 2 | 1 | 1 | 0 | not fail-to-pass yet |

Of the **9** first refused as not fail-to-pass yet, **3** ended fail-to-pass.


### The second chance

**Rescued 2** of 8 restarted run(s): 8 ended without a YES and were restarted with the record of their first attempt (8 after a NO, 0 after a BROKEN), and 2 ended fail-to-pass on the second attempt: `matplotlib__matplotlib-25515`, `sphinx-doc__sphinx-7590`.


### Fail-to-pass, then lost

**29** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14295`](./astropy__astropy-14295/) |  | YES | 28% (14/50) | 7/20 | 10/20 | 73 | `run` x22, `write_file` x12, `verify` x11, `run_tests` x10, `coverage` x6, `mutation` x4 | — | — | — | — | 2026-10-15 21:52 UTC |
| [`astropy__astropy-7008`](./astropy__astropy-7008/) |  | YES | 82% (22/27); 100% (17/17) without import-time | 12/20 | 12/20 | 53 | `run` x14, `write_file` x11, `verify` x7, `coverage` x6, `mutation` x5, `run_tests` x3  (+1 edit reverted) | — | — | — | — | 2026-10-16 05:21 UTC |
| [`django__django-11885`](./django__django-11885/) |  | NO | — | — | — | 111 | `run` x41, `write_file` x26, `run_tests` x22, `verify` x4 | — | — | — | — | 2026-10-15 18:02 UTC |
| [`django__django-16092`](./django__django-16092/) |  | YES | 13% (14/107); 14% (14/100) without import-time | 0/20 | 7/20 | 84 | `run` x20, `write_file` x20, `run_tests` x13, `verify` x10, `coverage` x3, `mutation` x2  (+2 edits reverted) | — | — | — | — | 2026-10-15 21:51 UTC |
| [`django__django-13207`](./django__django-13207/) |  | YES | 19% (16/86); 22% (16/74) without import-time | 6/20 | 7/20 | 75 | `run` x16, `write_file` x14, `verify` x13, `coverage` x11, `run_tests` x5, `mutation` x4 | — | — | — | — | 2026-10-16 06:20 UTC |
| [`django__django-11991`](./django__django-11991/) |  | YES | 45% (24/53); 51% (24/47) without import-time | 3/20 | 11/20 | 125 | `run` x29, `write_file` x26, `verify` x24, `coverage` x14, `mutation` x9, `run_tests` x6 | — | — | — | — | 2026-10-16 06:53 UTC |
| [`matplotlib__matplotlib-24013`](./matplotlib__matplotlib-24013/) |  | YES | 13% (104/825); 13% (104/807) without import-time | 6/20 | 7/20 | 95 | `run` x21, `write_file` x17, `run_tests` x15, `verify` x13, `coverage` x7, `mutation` x7 | — | — | — | — | 2026-10-16 10:29 UTC |
| [`matplotlib__matplotlib-25515`](./matplotlib__matplotlib-25515/) |  | YES | 3% (5/160); 0% (0/129) without import-time | 0/20 | 9/20 | 124 | `run` x28, `write_file` x28, `run_tests` x27, `verify` x17, `coverage` x6, `mutation` x5 | — | — | — | — | 2026-10-16 06:15 UTC |
| [`matplotlib__matplotlib-19743`](./matplotlib__matplotlib-19743/) |  | YES | 43% (13/30) | 2/20 | 15/20 | 61 | `run` x26, `verify` x8, `write_file` x8, `coverage` x7, `mutation` x4, `run_tests` x1 | — | — | — | — | 2026-10-16 05:38 UTC |
| [`matplotlib__matplotlib-20693`](./matplotlib__matplotlib-20693/) |  | YES | 55% (59/108) | 9/20 | 11/20 | 116 | `run` x36, `write_file` x20, `verify` x18, `coverage` x15, `mutation` x9, `run_tests` x7 | — | — | — | — | 2026-10-16 07:22 UTC |
| [`mwaskom__seaborn-2766`](./mwaskom__seaborn-2766/) |  | NO | — | — | — | 95 | `run` x29, `run_tests` x22, `write_file` x21, `verify` x6 | — | — | — | — | 2026-10-15 21:44 UTC |
| [`pydata__xarray-7179`](./pydata__xarray-7179/) |  | YES | 6% (6/97); 6% (6/95) without import-time | 5/20 | 6/20 | 95 | `run` x27, `run_tests` x14, `write_file` x14, `verify` x13, `coverage` x8, `mutation` x6 | — | — | — | — | 2026-10-16 07:24 UTC |
| [`pydata__xarray-6971`](./pydata__xarray-6971/) |  | YES | 39% (30/77); 37% (28/75) without import-time | 3/20 | 19/20 | 83 | `verify` x18, `write_file` x18, `coverage` x15, `run` x10, `mutation` x6, `run_tests` x2 | — | — | — | — | 2026-10-16 06:59 UTC |
| [`pydata__xarray-7444`](./pydata__xarray-7444/) |  | YES | 92% (47/51); 92% (43/47) without import-time | 12/20 | 16/20 | 71 | `write_file` x17, `run` x14, `verify` x13, `coverage` x7, `run_tests` x5, `mutation` x2 | — | — | — | — | 2026-10-16 06:10 UTC |
| [`pydata__xarray-2922`](./pydata__xarray-2922/) |  | YES | 97% (35/36) | 14/20 | 17/20 | 41 | `run` x8, `coverage` x6, `run_tests` x6, `verify` x6, `write_file` x6, `mutation` x4 | — | — | — | — | 2026-10-16 05:57 UTC |
| [`pylint-dev__pylint-4551`](./pylint-dev__pylint-4551/) |  | YES | 10% (6/62); 0% (0/56) without import-time | 0/20 | 15/20 | 104 | `run` x23, `run_tests` x19, `write_file` x19, `verify` x13, `coverage` x11, `mutation` x5 | — | — | — | — | 2026-10-16 06:17 UTC |
| [`pylint-dev__pylint-5136`](./pylint-dev__pylint-5136/) |  | YES | 0% (0/62) | 1/20 | 0/20 | 88 | `write_file` x18, `run` x17, `verify` x17, `coverage` x12, `mutation` x5, `run_tests` x5 | — | — | — | — | 2026-10-16 09:02 UTC |
| [`pylint-dev__pylint-4492`](./pylint-dev__pylint-4492/) |  | YES | 2% (1/55) | 0/20 | 15/20 | 100 | `run_tests` x20, `write_file` x20, `verify` x17, `coverage` x12, `run` x12, `mutation` x5 | — | — | — | — | 2026-10-16 06:04 UTC |
| [`pytest-dev__pytest-5787`](./pytest-dev__pytest-5787/) |  | YES | 61% (43/71) | 14/20 | 18/20 | 71 | `run` x15, `write_file` x11, `run_tests` x10, `verify` x8, `coverage` x7, `mutation` x6 | — | — | — | — | 2026-10-15 21:53 UTC |
| [`pytest-dev__pytest-10442`](./pytest-dev__pytest-10442/) |  | NO | — | — | — | 101 | `run` x27, `write_file` x26, `run_tests` x20, `verify` x10  (+1 edit reverted) | — | — | — | — | 2026-10-16 05:59 UTC |
| [`scikit-learn__scikit-learn-25969`](./scikit-learn__scikit-learn-25969/) |  | YES | 64% (54/85); 49% (30/61) without import-time | 8/20 | 4/20 | 93 | `write_file` x17, `run_tests` x16, `run` x15, `verify` x15, `coverage` x12, `mutation` x4 | — | — | — | — | 2026-10-16 06:24 UTC |
| [`scikit-learn__scikit-learn-24145`](./scikit-learn__scikit-learn-24145/) |  | YES | 2% (1/63) | 1/20 | 5/20 | 104 | `write_file` x27, `run_tests` x20, `verify` x15, `run` x12, `coverage` x8, `mutation` x8 | — | — | — | — | 2026-10-16 06:19 UTC |
| [`scikit-learn__scikit-learn-14012`](./scikit-learn__scikit-learn-14012/) |  | YES | 65% (42/65); 60% (35/58) without import-time | 9/20 | 16/20 | 46 | `verify` x13, `write_file` x13, `coverage` x5, `run` x5, `mutation` x4, `run_tests` x1 | — | — | — | — | 2026-10-15 23:17 UTC |
| [`scikit-learn__scikit-learn-25363`](./scikit-learn__scikit-learn-25363/) |  | NO | — | — | — | 93 | `run` x30, `write_file` x23, `run_tests` x18, `verify` x4, `coverage` x1 | — | — | — | — | 2026-10-16 06:05 UTC |
| [`scikit-learn__scikit-learn-10483`](./scikit-learn__scikit-learn-10483/) |  | YES | 63% (99/158); 55% (73/132) without import-time | 7/20 | 12/20 | 101 | `write_file` x21, `run` x18, `verify` x16, `run_tests` x15, `coverage` x8, `mutation` x6 | — | — | — | — | 2026-10-16 06:09 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) |  | YES | 52% (28/54); 43% (19/44) without import-time | 1/20 | 10/20 | 125 | `run` x58, `write_file` x18, `run_tests` x15, `verify` x10, `coverage` x6, `mutation` x4 | — | — | — | — | 2026-10-16 06:28 UTC |
| [`sphinx-doc__sphinx-10360`](./sphinx-doc__sphinx-10360/) |  | NO | — | — | — | 104 | `run` x43, `write_file` x21, `run_tests` x19, `verify` x8 | — | — | — | — | 2026-10-15 18:06 UTC |
| [`sphinx-doc__sphinx-7234`](./sphinx-doc__sphinx-7234/) |  | YES | 56% (45/80); 38% (21/56) without import-time | 8/20 | 18/20 | 95 | `run` x21, `verify` x18, `write_file` x18, `coverage` x14, `mutation` x7, `run_tests` x1 | — | — | — | — | 2026-10-16 06:41 UTC |
| [`sphinx-doc__sphinx-7380`](./sphinx-doc__sphinx-7380/) |  | YES | 42% (57/134); 34% (40/117) without import-time | 1/20 | 10/20 | 90 | `run` x27, `write_file` x19, `verify` x16, `coverage` x8, `mutation` x3, `run_tests` x3 | — | — | — | — | 2026-10-16 09:21 UTC |
| [`sphinx-doc__sphinx-10807`](./sphinx-doc__sphinx-10807/) |  | YES | 9% (14/157); 0% (0/139) without import-time | 2/20 | 9/20 | 76 | `run` x15, `run_tests` x12, `write_file` x12, `verify` x10, `coverage` x9, `mutation` x4 | — | — | — | — | 2026-10-16 06:09 UTC |
| [`sympy__sympy-13091`](./sympy__sympy-13091/) |  | YES | 11% (6/56) | 3/20 | 4/20 | 121 | `run` x27, `run_tests` x18, `verify` x18, `write_file` x18, `coverage` x16, `mutation` x10 | — | — | — | — | 2026-10-16 07:09 UTC |
| [`sympy__sympy-17512`](./sympy__sympy-17512/) |  | YES | 51% (43/85); 49% (40/82) without import-time | 7/20 | 16/20 | 90 | `run` x20, `write_file` x19, `verify` x18, `coverage` x9, `mutation` x8, `run_tests` x3 | — | — | — | — | 2026-10-16 06:18 UTC |
| [`sympy__sympy-12472`](./sympy__sympy-12472/) |  | NO | — | — | — | 89 | `run` x23, `write_file` x23, `run_tests` x19, `verify` x10 | — | — | — | — | 2026-10-16 05:32 UTC |
| [`sympy__sympy-14085`](./sympy__sympy-14085/) |  | YES | 95% (55/58); 94% (51/54) without import-time | 11/20 | 4/20 | 79 | `run` x20, `write_file` x13, `coverage` x12, `verify` x12, `run_tests` x10, `mutation` x4 | — | — | — | — | 2026-10-16 06:05 UTC |
| [`sympy__sympy-13236`](./sympy__sympy-13236/) |  | YES | 33% (29/88); 28% (23/82) without import-time | 4/20 | 13/20 | 121 | `run` x27, `run_tests` x20, `write_file` x20, `verify` x19, `coverage` x14, `mutation` x6 | — | — | — | — | 2026-10-16 08:02 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
