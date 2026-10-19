# Run status, per pull request

Last run in this table: 2026-10-16 07:20 UTC.

- **23** instances across **3** repositories
- **14/23** fail-to-pass, of those that reached a verdict

- **3** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **11/23**
- **Changed-line coverage (main): mean 60.9%** of the per-PR figures over the 14 measured YES PRs; median 88%
- **51%** of the changed lines those tests were measured against (690/1362, pooled)
- **50%** pooled without the lines that run on import (662/1323)
- **16%** of every source line all 23 patches change (690/4400), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$7.49 and 104.5M tokens in total
- **23** of these had a stop refused at least once, and **14** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[coverage+mutation]` | 7 | 7 | 0 | 0 | checks after fail-to-pass |
| `duties_open[mutation]` | 2 | 2 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 9 | 0 | 9 | 0 | not fail-to-pass yet |
| `skipped_at_base` | 3 | 3 | 0 | 0 | not fail-to-pass yet |
| `verify_open` | 2 | 2 | 0 | 0 | not fail-to-pass yet |

Of the **14** first refused as not fail-to-pass yet, **5** ended fail-to-pass.


### The second chance

**Rescued 3** of 12 restarted run(s): 12 ended without a YES and were restarted with the record of their first attempt (12 after a NO, 0 after a BROKEN), and 3 ended fail-to-pass on the second attempt: `Qiskit__qiskit-13922`, `Qiskit__qiskit-14132`, `scipy__scipy-21700`.


### Fail-to-pass, then lost

**14** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`pandas-dev__pandas-59141`](./pandas-dev__pandas-59141/) |  | NO | — | — | — | 98 | `run` x38, `write_file` x18, `run_tests` x15, `verify` x9, `coverage` x2 | — | — | — | — | 2026-10-15 18:06 UTC |
| [`Qiskit__qiskit-12825`](./Qiskit__qiskit-12825/) |  | YES | 18% (55/307) | 3/20 | 17/20 | 87 | `run` x18, `write_file` x18, `verify` x15, `run_tests` x9, `coverage` x8, `mutation` x5  (+1 edit reverted) | — | — | — | — | 2026-10-16 06:32 UTC |
| [`Qiskit__qiskit-12474`](./Qiskit__qiskit-12474/) |  | YES | 5% (7/140); 0% (0/133) without import-time | 0/20 | 20/20 | 61 | `run` x15, `write_file` x12, `verify` x11, `run_tests` x6, `coverage` x5, `mutation` x3 | — | — | — | — | 2026-10-15 18:09 UTC |
| [`Qiskit__qiskit-12904`](./Qiskit__qiskit-12904/) |  | YES | 0% (0/104) | 0/20 | n/a | 100 | `run` x26, `write_file` x22, `run_tests` x15, `verify` x13, `coverage` x3, `mutation` x3 | — | — | — | — | 2026-10-16 05:57 UTC |
| [`Qiskit__qiskit-13922`](./Qiskit__qiskit-13922/) |  | YES | 98% (92/94) | 15/20 | 17/20 | 102 | `write_file` x22, `verify` x21, `run` x20, `coverage` x10, `mutation` x5, `run_tests` x3 | — | — | — | — | 2026-10-15 22:51 UTC |
| [`Qiskit__qiskit-12814`](./Qiskit__qiskit-12814/) |  | YES | 88% (69/78); 86% (54/63) without import-time | 12/20 | 14/20 | 83 | `write_file` x19, `run` x17, `verify` x16, `coverage` x10, `mutation` x6, `run_tests` x2 | — | — | — | — | 2026-10-15 21:59 UTC |
| [`Qiskit__qiskit-14024`](./Qiskit__qiskit-14024/) |  | YES | 3% (2/59); 4% (2/48) without import-time | 1/20 | n/a | 74 | `run` x26, `write_file` x16, `verify` x9, `coverage` x3, `run_tests` x3, `mutation` x2 | — | — | — | — | 2026-10-15 21:37 UTC |
| [`Qiskit__qiskit-12483`](./Qiskit__qiskit-12483/) |  | YES | 98% (50/51); 98% (49/50) without import-time | 14/20 | 13/20 | 69 | `verify` x18, `write_file` x18, `coverage` x8, `mutation` x8, `run` x7, `run_tests` x3 | — | — | — | — | 2026-10-16 06:02 UTC |
| [`Qiskit__qiskit-14132`](./Qiskit__qiskit-14132/) |  | YES | 96% (48/50); 96% (43/45) without import-time | 19/20 | 3/20 | 125 | `write_file` x27, `verify` x26, `run` x21, `coverage` x16, `run_tests` x11, `mutation` x7 | — | — | — | — | 2026-10-16 06:37 UTC |
| [`scipy__scipy-21700`](./scipy__scipy-21700/) |  | YES | 72% (113/156) | 11/20 | 14/20 | 124 | `run` x29, `write_file` x26, `verify` x22, `coverage` x13, `mutation` x10, `run_tests` x8 | — | — | — | — | 2026-10-15 23:59 UTC |
| [`scipy__scipy-21783`](./scipy__scipy-21783/) |  | NO | — | — | — | 90 | `run` x26, `run_tests` x23, `write_file` x23, `verify` x4 | — | — | — | — | 2026-10-16 05:42 UTC |
| [`scipy__scipy-21216`](./scipy__scipy-21216/) |  | NO | — | — | — | 80 | `run` x36, `write_file` x14, `run_tests` x13, `verify` x2, `coverage` x1 | — | — | — | — | 2026-10-15 21:38 UTC |
| [`scipy__scipy-21819`](./scipy__scipy-21819/) |  | NO | — | — | — | 95 | `run` x30, `write_file` x21, `run_tests` x20, `verify` x10, `coverage` x1 | — | — | — | — | 2026-10-15 21:44 UTC |
| [`scipy__scipy-21713`](./scipy__scipy-21713/) |  | NO | — | — | — | 98 | `run` x37, `run_tests` x18, `write_file` x18, `verify` x12 | — | — | — | — | 2026-10-15 21:56 UTC |
| [`scipy__scipy-22896`](./scipy__scipy-22896/) |  | NO | — | — | — | 114 | `run` x43, `run_tests` x23, `write_file` x23, `verify` x11, `coverage` x1 | — | — | — | — | 2026-10-15 21:54 UTC |
| [`scipy__scipy-21389`](./scipy__scipy-21389/) |  | YES | 100% (68/68) | 14/20 | 17/20 | 66 | `write_file` x16, `verify` x15, `run` x10, `mutation` x8, `coverage` x7, `run_tests` x3 | — | — | — | — | 2026-10-16 07:13 UTC |
| [`scipy__scipy-22983`](./scipy__scipy-22983/) |  | YES | 94% (74/79) | 18/20 | 17/20 | 74 | `run_tests` x14, `write_file` x14, `verify` x11, `run` x10, `coverage` x9, `mutation` x6  (+2 edits reverted) | — | — | — | — | 2026-10-15 18:25 UTC |
| [`scipy__scipy-22170`](./scipy__scipy-22170/) |  | NO | — | — | — | 108 | `run` x36, `write_file` x25, `run_tests` x20, `verify` x8, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-16 05:53 UTC |
| [`scipy__scipy-20137`](./scipy__scipy-20137/) |  | YES | 73% (56/77) | 10/20 | 9/20 | 97 | `run` x28, `write_file` x19, `verify` x18, `coverage` x12, `mutation` x5, `run_tests` x1 | — | — | — | — | 2026-10-16 07:20 UTC |
| [`scipy__scipy-20284`](./scipy__scipy-20284/) |  | NO | — | — | — | 88 | `run` x38, `run_tests` x18, `write_file` x17 | — | — | — | — | 2026-10-16 06:00 UTC |
| [`scipy__scipy-21777`](./scipy__scipy-21777/) |  | YES | 6% (3/46) | 0/20 | 14/20 | 94 | `run` x25, `verify` x16, `write_file` x16, `coverage` x14, `mutation` x6, `run_tests` x1 | — | — | — | — | 2026-10-16 07:16 UTC |
| [`scipy__scipy-21996`](./scipy__scipy-21996/) |  | YES | 100% (53/53) | 16/20 | 16/20 | 71 | `run` x29, `write_file` x11, `verify` x10, `coverage` x6, `mutation` x5, `run_tests` x4 | — | — | — | — | 2026-10-16 06:18 UTC |
| [`scipy__scipy-20753`](./scipy__scipy-20753/) |  | NO | — | — | — | 109 | `run` x34, `run_tests` x24, `write_file` x24, `verify` x10, `coverage` x1 | — | — | — | — | 2026-10-16 06:47 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
