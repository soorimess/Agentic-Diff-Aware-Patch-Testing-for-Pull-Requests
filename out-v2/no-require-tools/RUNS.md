# Run status, per pull request

Last run in this table: 2026-10-06 08:45 UTC.

**Not one launch:** these runs come from several batches of the same system -- see [REUSED.md](./REUSED.md) before comparing with other folders.

- **36** instances across **12** repositories
- **29/36** fail-to-pass, of those that reached a verdict
- **2** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **27/36**
- **Changed-line coverage (main): mean 91.9%** of the per-PR figures over the 26 measured YES PRs; median 100%
- **92%** of the changed lines those tests were measured against (65/71, pooled)
- **91%** pooled without the lines that run on import (61/67)
- **28%** of every source line all 36 patches change (65/229), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$2.42 and 33.5M tokens in total


### The second chance

**Rescued 2** of 9 restarted run(s): 9 ended without a YES and were restarted with the record of their first attempt (9 after a NO, 0 after a BROKEN), and 2 ended fail-to-pass on the second attempt: `pytest-dev__pytest-10081`, `sphinx-doc__sphinx-9602`.


### Fail-to-pass, then lost

**29** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+coverage-tool+mutation-tool+guard+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES | 100% (1/1) | 2/2 | 2/2 | 71 | `run` x39, `write_file` x12, `run_tests` x9, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-05 18:26 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | NO | — | — | — | 101 | `run` x43, `write_file` x23, `run_tests` x18, `verify` x5, `coverage` x4 | — | — | — | — | 2026-10-05 18:30 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | — | 1/1 | 1/1 | 25 | `run` x14, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2, `coverage` x1 | — | — | — | — | 2026-10-05 18:16 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | NO | — | — | — | 98 | `run` x37, `write_file` x25, `run_tests` x21, `verify` x6, `coverage` x1 | — | — | — | — | 2026-10-05 18:30 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | YES | — | no mutants | no mutants | 28 | `run` x14, `run_tests` x4, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-05 18:15 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 50% (1/2) | 2/5 | 2/5 | 27 | `run` x10, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-05 18:16 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 1/1 | 1/1 | 24 | `run` x11, `run_tests` x4, `verify` x2, `write_file` x2, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-05 18:12 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 23 | `run` x5, `verify` x4, `write_file` x4, `mutation` x3, `run_tests` x3, `coverage` x2 | — | — | — | — | 2026-10-05 18:13 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 0% (0/2) | 1/1 | 1/1 | 62 | `run` x32, `write_file` x9, `run_tests` x8, `verify` x4, `mutation` x3, `coverage` x2 | — | — | — | — | 2026-10-05 18:22 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | YES | 100% (1/1) | 2/2 | 1/2 | 21 | `run` x7, `run_tests` x5, `write_file` x3, `verify` x2, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-05 19:22 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (1/1) | 3/3 | 3/3 | 28 | `run` x11, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-05 18:16 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 5/5 | 5/5 | 57 | `run` x20, `write_file` x12, `run_tests` x11, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | — | 2026-10-06 08:42 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 100% (4/4) | 7/9 | 9/9 | 37 | `run` x20, `run_tests` x6, `write_file` x5, `coverage` x1, `mutation` x1, `verify` x1 | — | — | — | — | 2026-10-05 18:18 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | NO | — | — | — | 64 | `run` x25, `write_file` x14, `run_tests` x9, `verify` x6, `coverage` x2, `mutation` x1 | — | — | — | — | 2026-10-05 18:26 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | none held out | none held out | 28 | `run` x14, `run_tests` x3, `coverage` x2, `mutation` x2, `verify` x2, `write_file` x2 | — | — | — | — | 2026-10-05 18:16 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 3/3 | 3/3 | 31 | `run` x10, `write_file` x7, `run_tests` x6, `mutation` x2, `verify` x2, `coverage` x1 | — | — | — | — | 2026-10-05 18:19 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | none held out | none held out | 21 | `run` x7, `run_tests` x3, `write_file` x3, `coverage` x2, `mutation` x2, `verify` x2 | — | — | — | — | 2026-10-06 08:31 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | none held out | none held out | 22 | `run` x7, `run_tests` x3, `verify` x3, `write_file` x3, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-06 08:35 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 0/2 | 0/2 | 46 | `run` x17, `write_file` x12, `run_tests` x6, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-05 18:21 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | 4/5 | 4/5 | 29 | `run` x8, `write_file` x6, `run_tests` x5, `coverage` x2, `mutation` x2, `verify` x2 | — | — | — | — | 2026-10-05 18:23 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | YES | 100% (11/11); 100% (10/10) without import-time | 11/16 | 13/16 | 37 | `run` x11, `run_tests` x7, `write_file` x7, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-05 18:26 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | NO | — | — | — | 71 | `run` x27, `run_tests` x14, `write_file` x14, `verify` x7, `coverage` x1 | — | — | — | — | 2026-10-05 18:28 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | 1/1 | 1/1 | 30 | `run` x9, `mutation` x5, `verify` x4, `write_file` x4, `coverage` x3, `run_tests` x3 | — | — | — | — | 2026-10-05 18:18 UTC |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | YES | 100% (2/2) | 0/1 | 1/1 | 31 | `run` x13, `run_tests` x5, `write_file` x4, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | — | 2026-10-05 18:19 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 1/3 | 1/3 | 19 | `run` x9, `mutation` x2, `run_tests` x2, `coverage` x1, `verify` x1, `write_file` x1  (+1 edit reverted) | — | — | — | — | 2026-10-05 18:13 UTC |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | YES | — | no mutants | no mutants | 38 | `run` x18, `run_tests` x6, `write_file` x6, `verify` x3, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-05 18:19 UTC |
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | NO | — | — | — | 64 | `run` x24, `write_file` x12, `run_tests` x11, `verify` x6, `coverage` x1 | — | — | — | — | 2026-10-06 08:45 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | YES | 60% (3/5) | 1/7 | 7/7 | 45 | `run` x14, `write_file` x9, `verify` x7, `run_tests` x6, `coverage` x3, `mutation` x3 | — | — | — | — | 2026-10-05 18:25 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 0/1 | 0/1 | 35 | `run` x18, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-05 18:19 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | 1/2 | n/a | 22 | `run` x5, `coverage` x3, `mutation` x3, `run_tests` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-05 18:14 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 21 | `run` x10, `mutation` x2, `run_tests` x2, `verify` x2, `write_file` x2, `coverage` x1 | — | — | — | — | 2026-10-05 18:16 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 33 | `run` x15, `run_tests` x5, `write_file` x5, `verify` x3, `coverage` x1, `mutation` x1  (+1 edit reverted) | — | — | — | — | 2026-10-05 18:19 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | NO | — | — | — | 65 | `run` x20, `run_tests` x14, `write_file` x14, `verify` x4, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-06 08:42 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 80% (4/5); 50% (1/2) without import-time | 1/4 | 3/4 | 42 | `run` x17, `run_tests` x6, `write_file` x6, `verify` x5, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-05 18:21 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | YES | 100% (8/8) | 9/15 | 14/15 | 68 | `run` x21, `run_tests` x17, `write_file` x15, `verify` x3, `mutation` x2, `coverage` x1 | — | — | — | — | 2026-10-05 18:32 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | NO | — | — | — | 86 | `run` x37, `write_file` x15, `run_tests` x9, `coverage` x7, `verify` x7, `mutation` x1 | — | — | — | — | 2026-10-05 18:34 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
