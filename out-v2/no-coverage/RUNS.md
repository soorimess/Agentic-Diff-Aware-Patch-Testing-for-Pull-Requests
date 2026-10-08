# Run status, per pull request

Last run in this table: 2026-10-07 07:30 UTC.

- **36** instances across **12** repositories
- **28/36** fail-to-pass, of those that reached a verdict
- **1** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **27/36**
- **Changed-line coverage (main): mean 90.5%** of the per-PR figures over the 26 measured YES PRs; median 100%
- **53%** of the changed lines those tests were measured against (79/150, pooled)
- **39%** pooled without the lines that run on import (45/116)
- **34%** of every source line all 36 patches change (79/229), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$3.09 and 42.8M tokens in total
- **18** of these had a stop refused at least once, and **10** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[mutation]` | 8 | 8 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 9 | 1 | 8 | 0 | not fail-to-pass yet |
| `verify_open` | 1 | 1 | 0 | 0 | not fail-to-pass yet |

Of the **10** first refused as not fail-to-pass yet, **2** ended fail-to-pass.


### The second chance

**Rescued 1** of 9 restarted run(s): 9 ended without a YES and were restarted with the record of their first attempt (9 after a NO, 0 after a BROKEN), and 1 ended fail-to-pass on the second attempt: `pylint-dev__pylint-4970`.


### Fail-to-pass, then lost

**28** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+mutation-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES | 100% (1/1) | 2/2 | 2/2 | 91 | `write_file` x26, `run` x22, `run_tests` x16, `verify` x13, `mutation` x5 | — | — | — | — | 2026-10-07 07:23 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | YES | 100% (2/2) | none held out | none held out | 48 | `run` x32, `run_tests` x5, `write_file` x4, `verify` x2, `mutation` x1 | — | — | — | — | 2026-10-07 07:14 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | — | 1/1 | 1/1 | 41 | `run` x18, `write_file` x7, `run_tests` x6, `verify` x4, `mutation` x3 | — | — | — | — | 2026-10-07 07:15 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | NO | — | — | — | 111 | `write_file` x40, `run` x34, `run_tests` x14, `verify` x7, `mutation` x2 | — | — | — | — | 2026-10-07 07:27 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | NO | — | — | — | 85 | `run` x30, `write_file` x19, `run_tests` x13, `verify` x6, `mutation` x1  (+1 edit reverted) | — | — | — | — | 2026-10-07 07:24 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 50% (1/2) | 2/5 | 2/5 | 39 | `mutation` x8, `run` x8, `verify` x7, `write_file` x6, `run_tests` x4 | — | — | — | — | 2026-10-07 07:14 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 1/1 | 1/1 | 31 | `run` x14, `run_tests` x5, `verify` x3, `write_file` x3, `mutation` x2 | — | — | — | — | 2026-10-07 07:11 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 22 | `run` x8, `run_tests` x4, `mutation` x3, `verify` x3, `write_file` x2 | — | — | — | — | 2026-10-07 07:08 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 1/1 | 1/1 | 76 | `run` x30, `write_file` x18, `run_tests` x8, `verify` x5, `mutation` x4 | — | — | — | — | 2026-10-07 07:23 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | NO | — | — | — | 85 | `run` x24, `write_file` x20, `run_tests` x19, `verify` x4, `mutation` x1 | — | — | — | — | 2026-10-07 07:26 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (1/1) | 3/3 | 3/3 | 26 | `run` x9, `run_tests` x6, `verify` x4, `write_file` x3, `mutation` x2 | — | — | — | — | 2026-10-07 07:09 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 5/5 | 5/5 | 19 | `run` x10, `run_tests` x3, `write_file` x2, `mutation` x1, `verify` x1 | — | — | — | — | 2026-10-07 07:08 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 100% (4/4) | 9/9 | 9/9 | 30 | `run` x12, `verify` x4, `write_file` x4, `mutation` x3, `run_tests` x3 | — | — | — | — | 2026-10-07 07:14 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | NO | — | — | — | 124 | `run` x43, `write_file` x43, `run_tests` x19, `verify` x5, `mutation` x1 | — | — | — | — | 2026-10-07 07:28 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | none held out | none held out | 31 | `run` x15, `run_tests` x4, `write_file` x4, `mutation` x3, `verify` x3 | — | — | — | — | 2026-10-07 07:11 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 3/3 | 3/3 | 33 | `run` x13, `run_tests` x5, `write_file` x5, `verify` x4, `mutation` x3 | — | — | — | — | 2026-10-07 07:15 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | none held out | none held out | 18 | `run` x9, `run_tests` x2, `write_file` x2, `mutation` x1, `verify` x1 | — | — | — | — | 2026-10-07 07:08 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | none held out | none held out | 11 | `run` x6, `mutation` x1, `run_tests` x1, `verify` x1, `write_file` x1 | — | — | — | — | 2026-10-07 07:07 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 0/2 | 0/2 | 44 | `run` x17, `write_file` x8, `run_tests` x5, `mutation` x4, `verify` x4 | — | — | — | — | 2026-10-07 07:16 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | 4/5 | 4/5 | 29 | `run` x13, `run_tests` x5, `write_file` x4, `mutation` x2, `verify` x2 | — | — | — | — | 2026-10-07 07:19 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 102 | `run` x44, `write_file` x30, `run_tests` x6, `verify` x3, `mutation` x1 | — | — | — | — | 2026-10-07 07:26 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | NO | — | — | — | 104 | `run` x28, `run_tests` x23, `write_file` x23, `verify` x11, `mutation` x2 | — | — | — | — | 2026-10-07 07:29 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | 1/1 | 1/1 | 29 | `run` x8, `mutation` x5, `verify` x5, `write_file` x5, `run_tests` x3 | — | — | — | — | 2026-10-07 07:12 UTC |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | YES | 50% (1/2) | 0/1 | 1/1 | 29 | `run` x14, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-07 07:11 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 1/3 | 1/3 | 35 | `run` x10, `verify` x6, `write_file` x6, `mutation` x4, `run_tests` x4 | — | — | — | — | 2026-10-07 07:14 UTC |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | YES | — | no mutants | no mutants | 26 | `run` x13, `write_file` x4, `mutation` x2, `run_tests` x2, `verify` x2 | — | — | — | — | 2026-10-07 07:11 UTC |
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | YES | 32% (31/96); 0% (0/65) without import-time | 1/20 | 18/20 | 50 | `run` x13, `write_file` x11, `verify` x8, `mutation` x6, `run_tests` x6 | — | — | — | — | 2026-10-07 07:30 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | YES | 20% (1/5) | 0/7 | 7/7 | 58 | `run` x16, `write_file` x13, `verify` x9, `run_tests` x8, `mutation` x7 | — | — | — | — | 2026-10-07 07:22 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 0/1 | 0/1 | 30 | `run` x13, `write_file` x7, `run_tests` x4, `mutation` x1, `verify` x1 | — | — | — | — | 2026-10-07 07:12 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | 1/2 | n/a | 17 | `run` x4, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x2 | — | — | — | — | 2026-10-07 07:07 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 19 | `run` x10, `run_tests` x4, `mutation` x1, `verify` x1, `write_file` x1 | — | — | — | — | 2026-10-07 07:09 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 25 | `run` x14, `write_file` x3, `run_tests` x2, `verify` x2, `mutation` x1  (+1 edit reverted) | — | — | — | — | 2026-10-07 07:10 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | YES | 100% (1/1) | 1/1 | 1/1 | 25 | `run` x7, `run_tests` x6, `write_file` x4, `verify` x3, `mutation` x2 | — | — | — | — | 2026-10-07 07:11 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 100% (5/5); 100% (2/2) without import-time | 2/4 | 3/4 | 43 | `run` x13, `verify` x8, `write_file` x8, `run_tests` x7, `mutation` x3 | — | — | — | — | 2026-10-07 07:21 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | NO | — | — | — | 91 | `run` x38, `write_file` x18, `run_tests` x11, `verify` x5, `mutation` x1 | — | — | — | — | 2026-10-07 07:26 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | NO | — | — | — | 104 | `run` x33, `write_file` x24, `run_tests` x20, `verify` x7, `mutation` x2 | — | — | — | — | 2026-10-07 07:29 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
