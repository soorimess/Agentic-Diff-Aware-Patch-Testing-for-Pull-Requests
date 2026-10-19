# Run status, per pull request

Last run in this table: 2026-10-16 13:09 UTC.

- **35** instances across **10** repositories
- **25/35** fail-to-pass, of those that reached a verdict

- **1** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **24/35**
- **Changed-line coverage (main): mean 32.5%** of the per-PR figures over the 25 measured YES PRs; median 25%
- **30%** of the changed lines those tests were measured against (566/1879, pooled)
- **25%** pooled without the lines that run on import (414/1686)
- **10%** of every source line all 35 patches change (566/5649), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$6.02 and 83.7M tokens in total
- **35** of these had a stop refused at least once, and **25** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[mutation]` | 23 | 23 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 11 | 2 | 9 | 0 | not fail-to-pass yet |
| `verify_open` | 1 | 0 | 1 | 0 | not fail-to-pass yet |

Of the **12** first refused as not fail-to-pass yet, **2** ended fail-to-pass.


### The second chance

**Rescued 1** of 11 restarted run(s): 11 ended without a YES and were restarted with the record of their first attempt (11 after a NO, 0 after a BROKEN), and 1 ended fail-to-pass on the second attempt: `pytest-dev__pytest-10442`.


### Fail-to-pass, then lost

**25** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+mutation-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`astropy__astropy-14295`](./astropy__astropy-14295/) |  | YES | 54% (27/50) | 6/20 | 10/20 | 35 | `run` x11, `write_file` x6, `verify` x5, `mutation` x4, `run_tests` x4 | — | — | — | — | 2026-10-16 08:44 UTC |
| [`astropy__astropy-7008`](./astropy__astropy-7008/) |  | YES | 82% (22/27); 100% (17/17) without import-time | 12/20 | 12/20 | 43 | `run` x17, `verify` x7, `write_file` x7, `mutation` x4, `run_tests` x1 | — | — | — | — | 2026-10-16 10:57 UTC |
| [`django__django-11885`](./django__django-11885/) |  | YES | 7% (3/45) | 2/20 | 9/20 | 61 | `run` x22, `write_file` x10, `run_tests` x9, `verify` x5, `mutation` x4 | — | — | — | — | 2026-10-16 10:59 UTC |
| [`django__django-16092`](./django__django-16092/) |  | YES | 13% (14/107); 14% (14/100) without import-time | 0/20 | 7/20 | 35 | `run` x14, `write_file` x6, `verify` x5, `mutation` x3, `run_tests` x3 | — | — | — | — | 2026-10-16 08:37 UTC |
| [`django__django-13207`](./django__django-13207/) |  | YES | 16% (14/86); 19% (14/74) without import-time | 4/20 | 7/20 | 45 | `run` x14, `write_file` x8, `verify` x7, `mutation` x5, `run_tests` x3 | — | — | — | — | 2026-10-16 12:02 UTC |
| [`django__django-11991`](./django__django-11991/) |  | YES | 0% (0/53); 0% (0/47) without import-time | 0/20 | 11/20 | 46 | `run` x13, `verify` x8, `mutation` x7, `write_file` x6, `run_tests` x4 | — | — | — | — | 2026-10-16 12:00 UTC |
| [`matplotlib__matplotlib-24013`](./matplotlib__matplotlib-24013/) |  | NO | — | — | — | 125 | `write_file` x42, `run_tests` x40, `verify` x16, `run` x13, `mutation` x1 | — | — | — | — | 2026-10-16 11:21 UTC |
| [`matplotlib__matplotlib-25515`](./matplotlib__matplotlib-25515/) |  | YES | 24% (39/160); 6% (8/129) without import-time | 12/20 | 9/20 | 53 | `run` x13, `write_file` x10, `run_tests` x8, `verify` x8, `mutation` x5 | — | — | — | — | 2026-10-16 12:14 UTC |
| [`matplotlib__matplotlib-19743`](./matplotlib__matplotlib-19743/) |  | YES | 43% (13/30) | 2/20 | 15/20 | 58 | `run` x32, `write_file` x6, `mutation` x5, `verify` x5, `run_tests` x4 | — | — | — | — | 2026-10-16 11:59 UTC |
| [`matplotlib__matplotlib-20693`](./matplotlib__matplotlib-20693/) |  | NO | — | — | — | 91 | `run` x28, `write_file` x21, `run_tests` x19, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-16 12:07 UTC |
| [`mwaskom__seaborn-2766`](./mwaskom__seaborn-2766/) |  | NO | — | — | — | 79 | `run` x26, `write_file` x19, `run_tests` x14, `verify` x6, `mutation` x1  (+1 edit reverted) | — | — | — | — | 2026-10-16 11:13 UTC |
| [`pydata__xarray-7179`](./pydata__xarray-7179/) |  | NO | — | — | — | 103 | `run` x34, `write_file` x23, `run_tests` x20, `verify` x9, `mutation` x1 | — | — | — | — | 2026-10-16 11:18 UTC |
| [`pydata__xarray-6971`](./pydata__xarray-6971/) |  | YES | 25% (19/77); 25% (19/75) without import-time | 6/20 | 19/20 | 44 | `run` x11, `verify` x11, `write_file` x11, `mutation` x4, `run_tests` x1 | — | — | — | — | 2026-10-16 09:04 UTC |
| [`pydata__xarray-7444`](./pydata__xarray-7444/) |  | YES | 80% (41/51); 79% (37/47) without import-time | 14/20 | 16/20 | 75 | `run` x20, `write_file` x16, `run_tests` x13, `verify` x9, `mutation` x8 | — | — | — | — | 2026-10-16 12:22 UTC |
| [`pydata__xarray-2922`](./pydata__xarray-2922/) |  | YES | 92% (33/36) | 14/20 | 17/20 | 32 | `run` x10, `mutation` x6, `verify` x4, `write_file` x4, `run_tests` x2  (+1 edit reverted) | — | — | — | — | 2026-10-16 12:17 UTC |
| [`pylint-dev__pylint-4551`](./pylint-dev__pylint-4551/) |  | YES | 16% (10/62); 9% (5/56) without import-time | 0/20 | 15/20 | 50 | `run` x21, `run_tests` x8, `write_file` x8, `verify` x4, `mutation` x3 | — | — | — | — | 2026-10-16 11:01 UTC |
| [`pylint-dev__pylint-5136`](./pylint-dev__pylint-5136/) |  | YES | 6% (4/62) | 1/20 | 0/20 | 86 | `run` x24, `write_file` x16, `mutation` x14, `verify` x14, `run_tests` x5 | — | — | — | — | 2026-10-16 12:16 UTC |
| [`pylint-dev__pylint-4492`](./pylint-dev__pylint-4492/) |  | YES | 0% (0/55) | 1/20 | 15/20 | 47 | `run` x10, `run_tests` x9, `write_file` x9, `mutation` x6, `verify` x6 | — | — | — | — | 2026-10-16 11:54 UTC |
| [`pytest-dev__pytest-5787`](./pytest-dev__pytest-5787/) |  | NO | — | — | — | 101 | `write_file` x27, `run` x24, `run_tests` x23, `verify` x13, `mutation` x1 | — | — | — | — | 2026-10-16 08:39 UTC |
| [`pytest-dev__pytest-10442`](./pytest-dev__pytest-10442/) |  | YES | 0% (0/31) | 5/20 | 7/20 | 125 | `write_file` x34, `run_tests` x26, `run` x20, `verify` x18, `mutation` x7 | — | — | — | — | 2026-10-16 11:25 UTC |
| [`scikit-learn__scikit-learn-25969`](./scikit-learn__scikit-learn-25969/) |  | YES | 64% (54/85); 49% (30/61) without import-time | 5/20 | 4/20 | 46 | `run` x14, `run_tests` x7, `write_file` x7, `mutation` x6, `verify` x6 | — | — | — | — | 2026-10-16 11:15 UTC |
| [`scikit-learn__scikit-learn-24145`](./scikit-learn__scikit-learn-24145/) |  | YES | 25% (16/63) | 3/20 | 5/20 | 73 | `run` x18, `verify` x12, `write_file` x12, `mutation` x8, `run_tests` x7 | — | — | — | — | 2026-10-16 12:10 UTC |
| [`scikit-learn__scikit-learn-14012`](./scikit-learn__scikit-learn-14012/) |  | YES | 51% (33/65); 45% (26/58) without import-time | 9/20 | 16/20 | 44 | `write_file` x11, `verify` x10, `run` x8, `mutation` x7, `run_tests` x2 | — | — | — | — | 2026-10-16 10:37 UTC |
| [`scikit-learn__scikit-learn-25363`](./scikit-learn__scikit-learn-25363/) |  | NO | — | — | — | 125 | `write_file` x42, `run_tests` x36, `run` x21, `verify` x12 | — | — | — | — | 2026-10-16 12:09 UTC |
| [`scikit-learn__scikit-learn-10483`](./scikit-learn__scikit-learn-10483/) |  | YES | 47% (74/158); 36% (48/132) without import-time | 4/20 | 12/20 | 64 | `write_file` x14, `run` x11, `run_tests` x11, `verify` x11, `mutation` x6 | — | — | — | — | 2026-10-16 12:13 UTC |
| [`sphinx-doc__sphinx-7590`](./sphinx-doc__sphinx-7590/) |  | YES | 20% (11/54); 2% (1/44) without import-time | 0/20 | 10/20 | 61 | `run` x27, `write_file` x11, `mutation` x6, `run_tests` x6, `verify` x6 | — | — | — | — | 2026-10-16 11:21 UTC |
| [`sphinx-doc__sphinx-10360`](./sphinx-doc__sphinx-10360/) |  | NO | — | — | — | 125 | `run` x36, `write_file` x34, `run_tests` x31, `verify` x9 | — | — | — | — | 2026-10-16 12:06 UTC |
| [`sphinx-doc__sphinx-7234`](./sphinx-doc__sphinx-7234/) |  | NO | — | — | — | 107 | `run` x43, `write_file` x24, `run_tests` x19, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-16 12:05 UTC |
| [`sphinx-doc__sphinx-7380`](./sphinx-doc__sphinx-7380/) |  | YES | 42% (57/134); 34% (40/117) without import-time | 2/20 | 10/20 | 38 | `write_file` x8, `run` x7, `verify` x7, `mutation` x5, `run_tests` x4 | — | — | — | — | 2026-10-16 12:20 UTC |
| [`sphinx-doc__sphinx-10807`](./sphinx-doc__sphinx-10807/) |  | YES | 6% (10/157); 0% (0/139) without import-time | 1/20 | 9/20 | 44 | `run` x13, `write_file` x9, `verify` x7, `mutation` x5, `run_tests` x4 | — | — | — | — | 2026-10-16 12:03 UTC |
| [`sympy__sympy-13091`](./sympy__sympy-13091/) |  | NO | — | — | — | 116 | `run_tests` x29, `write_file` x29, `run` x20, `verify` x12, `mutation` x1 | — | — | — | — | 2026-10-16 11:19 UTC |
| [`sympy__sympy-17512`](./sympy__sympy-17512/) |  | YES | 35% (30/85); 33% (27/82) without import-time | 5/20 | 16/20 | 54 | `run` x20, `write_file` x9, `verify` x8, `mutation` x6, `run_tests` x3 | — | — | — | — | 2026-10-16 12:01 UTC |
| [`sympy__sympy-12472`](./sympy__sympy-12472/) |  | NO | — | — | — | 83 | `write_file` x26, `run` x17, `run_tests` x16, `verify` x8, `mutation` x1 | — | — | — | — | 2026-10-16 11:58 UTC |
| [`sympy__sympy-14085`](./sympy__sympy-14085/) |  | YES | 41% (24/58); 37% (20/54) without import-time | 4/20 | 4/20 | 51 | `run` x22, `verify` x7, `run_tests` x5, `write_file` x5, `mutation` x4 | — | — | — | — | 2026-10-16 11:51 UTC |
| [`sympy__sympy-13236`](./sympy__sympy-13236/) |  | YES | 20% (18/88); 15% (12/82) without import-time | 4/20 | 13/20 | 64 | `run` x16, `run_tests` x12, `verify` x11, `write_file` x11, `mutation` x8 | — | — | — | — | 2026-10-16 13:09 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
