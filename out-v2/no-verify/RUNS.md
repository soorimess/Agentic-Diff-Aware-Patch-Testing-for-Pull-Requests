# Run status, per pull request

Last run in this table: 2026-10-06 12:58 UTC.

**Not one launch:** these runs come from several batches of the same system -- see [REUSED.md](./REUSED.md) before comparing with other folders.

- **36** instances across **12** repositories
- **25/36** fail-to-pass, of those that reached a verdict
- **5** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **20/36**
- **Changed-line coverage (main): mean 95.0%** of the per-PR figures over the 24 measured YES PRs; median 100%
- **95%** of the changed lines those tests were measured against (53/56, pooled)
- **94%** pooled without the lines that run on import (50/53)
- **23%** of every source line all 36 patches change (53/229), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$1.30 and 17.7M tokens in total


### The second chance

**Rescued 5** of 16 restarted run(s): 16 ended without a YES and were restarted with the record of their first attempt (16 after a NO, 0 after a BROKEN), and 5 ended fail-to-pass on the second attempt: `pytest-dev__pytest-5262`, `pytest-dev__pytest-10081`, `astropy__astropy-7336`, `astropy__astropy-14995`, `sphinx-doc__sphinx-9602`.

Every row was produced with the same configuration: **`guard+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES | 100% (1/1) | 2/2 | 2/2 | 47 | `run` x22, `write_file` x13, `run_tests` x10 | — | — | — | — | 2026-10-06 11:31 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | NO | — | — | — | 62 | `run` x27, `write_file` x16, `run_tests` x13 | — | — | — | — | 2026-10-06 11:34 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | NO | — | — | — | 34 | `run` x12, `run_tests` x9, `write_file` x9 | — | — | — | — | 2026-10-06 11:30 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | YES | 100% (2/2) | 3/3 | 3/3 | 34 | `run` x23, `write_file` x5, `run_tests` x4 | — | — | — | — | 2026-10-06 11:28 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | NO | — | — | — | 58 | `run` x27, `run_tests` x12, `write_file` x12 | — | — | — | — | 2026-10-06 11:33 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 50% (1/2) | 2/5 | 2/5 | 11 | `run` x5, `run_tests` x2, `write_file` x2 | — | — | — | — | 2026-10-06 11:25 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 1/1 | 1/1 | 23 | `run` x10, `run_tests` x5, `write_file` x5 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 2/2 | 0/2 | 15 | `run` x8, `run_tests` x4, `write_file` x1 | — | — | — | — | 2026-10-06 11:24 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 1/1 | 1/1 | 23 | `run` x10, `run_tests` x6, `write_file` x4 | — | — | — | — | 2026-10-06 12:58 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | NO | — | — | — | 40 | `run` x15, `run_tests` x10, `write_file` x9 | — | — | — | — | 2026-10-06 11:32 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (1/1) | 3/3 | 3/3 | 33 | `run` x18, `write_file` x5, `run_tests` x4 | — | — | — | — | 2026-10-06 11:30 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 5/5 | 5/5 | 44 | `run` x18, `write_file` x11, `run_tests` x9 | — | — | — | — | 2026-10-06 11:31 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 100% (4/4) | 6/9 | 9/9 | 18 | `run` x12, `run_tests` x2, `write_file` x2 | — | — | — | — | 2026-10-06 11:27 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | NO | — | — | — | 46 | `run` x25, `run_tests` x11, `write_file` x5 | — | — | — | — | 2026-10-06 11:31 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | none held out | none held out | 19 | `run` x15, `run_tests` x1, `write_file` x1 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 3/3 | 3/3 | 19 | `run` x9, `run_tests` x4, `write_file` x4 | — | — | — | — | 2026-10-06 11:27 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | none held out | none held out | 23 | `run` x10, `run_tests` x4, `write_file` x4 | — | — | — | — | 2026-10-06 11:28 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | none held out | none held out | 34 | `run` x21, `run_tests` x4, `write_file` x4 | — | — | — | — | 2026-10-06 11:30 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 0/2 | 0/2 | 20 | `run` x11, `write_file` x4, `run_tests` x3 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | 4/5 | 4/5 | 23 | `run` x13, `write_file` x4, `run_tests` x3 | — | — | — | — | 2026-10-06 11:32 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | NO | — | — | — | 47 | `run` x25, `run_tests` x8, `write_file` x8 | — | — | — | — | 2026-10-06 11:32 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | NO | — | — | — | 59 | `run` x31, `run_tests` x11, `write_file` x11 | — | — | — | — | 2026-10-06 11:35 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | 1/1 | 1/1 | 18 | `run` x10, `run_tests` x3, `write_file` x3 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | YES | 50% (1/2) | 0/1 | 1/1 | 17 | `run` x10, `run_tests` x2, `write_file` x2 | — | — | — | — | 2026-10-06 11:27 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 1/3 | 1/3 | 19 | `run` x13, `run_tests` x2, `write_file` x2 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | YES | — | no mutants | no mutants | 19 | `run` x11, `run_tests` x3, `write_file` x2 | — | — | — | — | 2026-10-06 11:27 UTC |
| [`astropy__astropy-13398`](./astropy__astropy-13398/) | 5.0 | NO | — | — | — | 57 | `run` x20, `run_tests` x14, `write_file` x14 | — | — | — | — | 2026-10-06 11:38 UTC |
| [`django__django-13279`](./django__django-13279/) | 3.2 | NO | — | — | — | 54 | `run` x23, `run_tests` x12, `write_file` x12 | — | — | — | — | 2026-10-06 11:33 UTC |
| [`matplotlib__matplotlib-22719`](./matplotlib__matplotlib-22719/) | 3.5 | YES | 100% (2/2) | 0/1 | 0/1 | 18 | `run` x9, `run_tests` x3, `write_file` x3 | — | — | — | — | 2026-10-06 11:26 UTC |
| [`psf__requests-1766`](./psf__requests-1766/) | 2.0 | YES | 100% (1/1) | 1/2 | n/a | 15 | `run` x8, `run_tests` x4, `write_file` x1 | — | — | — | — | 2026-10-06 11:24 UTC |
| [`pydata__xarray-7393`](./pydata__xarray-7393/) | 2022.09 | YES | 100% (3/3) | 3/3 | 3/3 | 30 | `run` x19, `write_file` x6, `run_tests` x2 | — | — | — | — | 2026-10-06 11:29 UTC |
| [`pylint-dev__pylint-7277`](./pylint-dev__pylint-7277/) | 2.15 | YES | 100% (3/3) | 3/3 | 3/3 | 22 | `run` x7, `run_tests` x6, `write_file` x6 | — | — | — | — | 2026-10-06 11:29 UTC |
| [`pytest-dev__pytest-7982`](./pytest-dev__pytest-7982/) | 6.2 | NO | — | — | — | 49 | `run` x16, `run_tests` x13, `write_file` x13 | — | — | — | — | 2026-10-06 11:36 UTC |
| [`scikit-learn__scikit-learn-25232`](./scikit-learn__scikit-learn-25232/) | 1.3 | YES | 80% (4/5); 50% (1/2) without import-time | 0/4 | 3/4 | 20 | `run` x12, `run_tests` x3, `write_file` x2 | — | — | — | — | 2026-10-06 12:57 UTC |
| [`sphinx-doc__sphinx-9602`](./sphinx-doc__sphinx-9602/) | 4.2 | YES | 100% (8/8) | 9/15 | 14/15 | 52 | `run` x21, `write_file` x12, `run_tests` x11 | — | — | — | — | 2026-10-06 11:35 UTC |
| [`sympy__sympy-21612`](./sympy__sympy-21612/) | 1.9 | NO | — | — | — | 39 | `run` x17, `run_tests` x7, `write_file` x7 | — | — | — | — | 2026-10-06 11:31 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
