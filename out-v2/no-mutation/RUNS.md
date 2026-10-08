# Run status, per pull request

**Partial run:** 23 of 36 PRs finished; the other 13 were cut off by the model gateway's spending limit and never rerun -- see [PARTIAL.md](./PARTIAL.md).

Last run in this table: 2026-10-07 10:47 UTC.

- **23** instances across **11** repositories
- **23/23** fail-to-pass, of those that reached a verdict
- **0** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **23/23**
- **Changed-line coverage (main): mean 100.0%** of the per-PR figures over the 20 measured YES PRs; median 100%
- **100%** of the changed lines those tests were measured against (41/41, pooled)
- **100%** pooled without the lines that run on import (38/38)
- **72%** of every source line all 23 patches change (41/57), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$0.64 and 8.8M tokens in total


### The second chance

**Rescued 0** of 0 restarted run(s): 0 ended without a YES and were restarted with the record of their first attempt (0 after a NO, 0 after a BROKEN), and 0 ended fail-to-pass on the second attempt: none.


### Fail-to-pass, then lost

**23** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+coverage-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | — | 1/1 | 1/1 | 34 | `run` x18, `write_file` x5, `run_tests` x4, `verify` x4, `coverage` x1 | — | — | — | — | 2026-10-07 10:44 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | YES | — | no mutants | no mutants | 22 | `run` x11, `run_tests` x3, `write_file` x3, `verify` x2, `coverage` x1 | — | — | — | — | 2026-10-07 10:39 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 100% (2/2) | 4/5 | 2/5 | 14 | `run` x5, `coverage` x2, `run_tests` x2, `verify` x2, `write_file` x1 | — | — | — | — | 2026-10-07 10:36 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 1/1 | 1/1 | 44 | `run` x25, `verify` x6, `write_file` x6, `run_tests` x3, `coverage` x1  (+1 edit reverted) | — | — | — | — | 2026-10-07 10:44 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 19 | `run` x9, `run_tests` x3, `verify` x2, `coverage` x1, `write_file` x1 | — | — | — | — | 2026-10-07 10:35 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 1/1 | 1/1 | 21 | `run` x7, `run_tests` x5, `write_file` x3, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:40 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (1/1) | 3/3 | 3/3 | 19 | `run` x5, `coverage` x3, `verify` x3, `write_file` x3, `run_tests` x2 | — | — | — | — | 2026-10-07 10:38 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 100% (4/4) | 7/9 | 9/9 | 20 | `run` x10, `run_tests` x4, `write_file` x2, `coverage` x1, `verify` x1 | — | — | — | — | 2026-10-07 10:38 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | no mutants | no mutants | 27 | `run` x19, `run_tests` x2, `write_file` x2, `coverage` x1, `verify` x1 | — | — | — | — | 2026-10-07 10:39 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 3/3 | 3/3 | 22 | `run` x8, `run_tests` x4, `write_file` x4, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:43 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | no mutants | no mutants | 14 | `run` x6, `coverage` x2, `verify` x2, `run_tests` x1, `write_file` x1 | — | — | — | — | 2026-10-07 10:36 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | no mutants | no mutants | 22 | `run` x8, `write_file` x4, `run_tests` x3, `verify` x3, `coverage` x2 | — | — | — | — | 2026-10-07 10:43 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 0/2 | 0/2 | 32 | `run` x16, `run_tests` x6, `write_file` x4, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:44 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | 4/5 | 4/5 | 27 | `run` x13, `run_tests` x3, `write_file` x3, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:47 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | 1/1 | 1/1 | 29 | `run` x11, `verify` x5, `write_file` x5, `coverage` x3, `run_tests` x3 | — | — | — | — | 2026-10-07 10:44 UTC |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | YES | 100% (2/2) | 0/1 | 1/1 | 18 | `run_tests` x4, `write_file` x4, `run` x3, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:42 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 1/3 | 1/3 | 26 | `run` x18, `run_tests` x2, `verify` x2, `coverage` x1, `write_file` x1  (+2 edits reverted) | — | — | — | — | 2026-10-07 10:37 UTC |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | YES | — | no mutants | no mutants | 29 | `run` x15, `run_tests` x4, `write_file` x4, `verify` x2, `coverage` x1 | — | — | — | — | 2026-10-07 10:41 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | 1/2 | n/a | 24 | `run` x9, `write_file` x4, `coverage` x3, `run_tests` x3, `verify` x3 | — | — | — | — | 2026-10-07 10:39 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 17 | `run` x7, `coverage` x2, `run_tests` x2, `verify` x2, `write_file` x2 | — | — | — | — | 2026-10-07 10:40 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 30 | `run` x10, `run_tests` x7, `write_file` x5, `verify` x4, `coverage` x1 | — | — | — | — | 2026-10-07 10:43 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | YES | 100% (1/1) | 1/1 | 1/1 | 28 | `run` x15, `run_tests` x4, `write_file` x3, `coverage` x2, `verify` x2 | — | — | — | — | 2026-10-07 10:40 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 100% (5/5); 100% (2/2) without import-time | 1/4 | 3/4 | 21 | `run` x9, `verify` x3, `write_file` x3, `run_tests` x2, `coverage` x1 | — | — | — | — | 2026-10-07 10:40 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
