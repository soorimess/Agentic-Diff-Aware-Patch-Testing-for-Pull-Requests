# Run status, per pull request

Last run in this table: 2026-10-16 13:09 UTC.

- **23** instances across **3** repositories
- **16/23** fail-to-pass, of those that reached a verdict

- **1** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **15/23**
- **Changed-line coverage (main): mean 62.3%** of the per-PR figures over the 16 measured YES PRs; median 70%
- **52%** of the changed lines those tests were measured against (828/1606, pooled)
- **51%** pooled without the lines that run on import (800/1578)
- **19%** of every source line all 23 patches change (828/4400), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$4.30 and 59.6M tokens in total
- **1 of 1573** model replies arrived empty -- no text and no tool call, and three of those in a row trip OpenHands' stuck detector, which ends the run. A run losing turns at that rate is bounded by its transport rather than by the model, and the verdicts below should be read with that in mind
- **23** of these had a stop refused at least once, and **16** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[mutation]` | 11 | 11 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 9 | 2 | 7 | 0 | not fail-to-pass yet |
| `skipped_at_base` | 1 | 1 | 0 | 0 | not fail-to-pass yet |
| `verify_open` | 2 | 2 | 0 | 0 | not fail-to-pass yet |

Of the **12** first refused as not fail-to-pass yet, **5** ended fail-to-pass.


### The second chance

**Rescued 1** of 8 restarted run(s): 8 ended without a YES and were restarted with the record of their first attempt (8 after a NO, 0 after a BROKEN), and 1 ended fail-to-pass on the second attempt: `scipy__scipy-20284`.


### Fail-to-pass, then lost

**16** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+mutation-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`pandas-dev__pandas-59141`](./pandas-dev__pandas-59141/) |  | NO | — | — | — | 92 | `run` x30, `write_file` x20, `run_tests` x18, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-16 11:10 UTC |
| [`Qiskit__qiskit-12825`](./Qiskit__qiskit-12825/) |  | YES | 21% (64/307) | 9/20 | 17/20 | 45 | `run` x15, `write_file` x9, `verify` x7, `mutation` x5, `run_tests` x2 | — | — | — | — | 2026-10-16 08:56 UTC |
| [`Qiskit__qiskit-12474`](./Qiskit__qiskit-12474/) |  | YES | 68% (95/140); 66% (88/133) without import-time | 2/20 | 20/20 | 28 | `run` x10, `run_tests` x4, `mutation` x3, `verify` x3, `write_file` x3 | — | — | — | — | 2026-10-16 11:00 UTC |
| [`Qiskit__qiskit-12904`](./Qiskit__qiskit-12904/) |  | YES | 70% (73/104) | 7/20 | n/a | 53 | `verify` x13, `write_file` x13, `run` x12, `mutation` x8, `run_tests` x2 | — | — | — | — | 2026-10-16 11:12 UTC |
| [`Qiskit__qiskit-13922`](./Qiskit__qiskit-13922/) |  | YES | 97% (91/94) | 15/20 | 17/20 | 44 | `run` x11, `verify` x8, `write_file` x8, `mutation` x7, `run_tests` x1 | — | — | — | — | 2026-10-16 09:18 UTC |
| [`Qiskit__qiskit-12814`](./Qiskit__qiskit-12814/) |  | YES | 35% (27/78); 19% (12/63) without import-time | 8/20 | 14/20 | 45 | `run` x11, `write_file` x10, `verify` x8, `mutation` x7, `run_tests` x3  (+1 edit reverted) | — | — | — | — | 2026-10-16 11:00 UTC |
| [`Qiskit__qiskit-14024`](./Qiskit__qiskit-14024/) |  | NO | — | — | — | 105 | `run` x37, `run_tests` x21, `write_file` x21, `verify` x10 | — | — | — | — | 2026-10-16 11:17 UTC |
| [`Qiskit__qiskit-12483`](./Qiskit__qiskit-12483/) |  | YES | 98% (50/51); 98% (49/50) without import-time | 13/20 | 13/20 | 35 | `run` x12, `mutation` x5, `verify` x5, `write_file` x5, `run_tests` x2 | — | — | — | — | 2026-10-16 11:02 UTC |
| [`Qiskit__qiskit-14132`](./Qiskit__qiskit-14132/) |  | YES | 80% (40/50); 78% (35/45) without import-time | 12/20 | 3/20 | 53 | `write_file` x13, `verify` x11, `run` x9, `mutation` x6, `run_tests` x5 | — | — | — | — | 2026-10-16 12:05 UTC |
| [`scipy__scipy-21700`](./scipy__scipy-21700/) |  | YES | 31% (49/156) | 13/20 | 14/20 | 82 | `write_file` x20, `verify` x15, `mutation` x13, `run` x11, `run_tests` x7 | — | — | — | — | 2026-10-16 10:32 UTC |
| [`scipy__scipy-21783`](./scipy__scipy-21783/) |  | YES | 14% (22/153) | 7/20 | 15/20 | 61 | `run` x24, `verify` x10, `write_file` x10, `mutation` x6, `run_tests` x5  (+1 edit reverted) | — | — | — | — | 2026-10-16 08:56 UTC |
| [`scipy__scipy-21216`](./scipy__scipy-21216/) |  | NO | — | — | — | 93 | `run` x34, `write_file` x20, `run_tests` x19, `verify` x4, `mutation` x1 | — | — | — | — | 2026-10-16 11:16 UTC |
| [`scipy__scipy-21819`](./scipy__scipy-21819/) |  | NO | — | — | — | 90 | `run` x29, `write_file` x18, `run_tests` x17, `verify` x8, `mutation` x1 | — | — | — | — | 2026-10-16 11:15 UTC |
| [`scipy__scipy-21713`](./scipy__scipy-21713/) |  | NO | — | — | — | 107 | `run` x30, `run_tests` x22, `write_file` x22, `verify` x15, `mutation` x1 | — | — | — | — | 2026-10-16 11:19 UTC |
| [`scipy__scipy-22896`](./scipy__scipy-22896/) |  | NO | — | — | — | 77 | `run` x37, `write_file` x13, `run_tests` x7, `verify` x4, `mutation` x2 | — | — | — | — | 2026-10-16 11:14 UTC |
| [`scipy__scipy-21389`](./scipy__scipy-21389/) |  | YES | 100% (68/68) | 12/20 | 17/20 | 52 | `verify` x12, `write_file` x12, `mutation` x10, `run` x10, `run_tests` x1 | — | — | — | — | 2026-10-16 13:09 UTC |
| [`scipy__scipy-22983`](./scipy__scipy-22983/) |  | YES | 68% (54/79) | 12/20 | 17/20 | 52 | `write_file` x13, `run` x10, `run_tests` x10, `verify` x6, `mutation` x4  (+1 edit reverted) | — | — | — | — | 2026-10-16 09:21 UTC |
| [`scipy__scipy-22170`](./scipy__scipy-22170/) |  | YES | 11% (8/75) | 0/20 | n/a | 70 | `run` x23, `write_file` x16, `run_tests` x15, `verify` x6, `mutation` x3 | — | — | — | — | 2026-10-16 12:04 UTC |
| [`scipy__scipy-20137`](./scipy__scipy-20137/) |  | YES | 66% (51/77) | 6/20 | 9/20 | 53 | `run` x29, `write_file` x7, `verify` x6, `run_tests` x4, `mutation` x3 | — | — | — | — | 2026-10-16 12:36 UTC |
| [`scipy__scipy-20284`](./scipy__scipy-20284/) |  | YES | 71% (53/75) | 2/20 | 12/20 | 124 | `run` x36, `write_file` x25, `verify` x20, `run_tests` x18, `mutation` x5 | — | — | — | — | 2026-10-16 13:04 UTC |
| [`scipy__scipy-21777`](./scipy__scipy-21777/) |  | YES | 74% (34/46) | 12/20 | 14/20 | 42 | `run` x12, `mutation` x7, `verify` x7, `write_file` x7, `run_tests` x2 | — | — | — | — | 2026-10-16 12:29 UTC |
| [`scipy__scipy-21996`](./scipy__scipy-21996/) |  | YES | 92% (49/53) | 14/20 | 16/20 | 69 | `run` x18, `mutation` x12, `write_file` x12, `verify` x11, `run_tests` x5 | — | — | — | — | 2026-10-16 13:03 UTC |
| [`scipy__scipy-20753`](./scipy__scipy-20753/) |  | NO | — | — | — | 97 | `run` x30, `run_tests` x21, `write_file` x21, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-16 12:25 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.
