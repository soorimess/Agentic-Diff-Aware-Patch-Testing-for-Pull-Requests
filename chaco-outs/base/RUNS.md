# Run status, per pull request

Last run in this table: 2026-10-12 16:07 UTC.

- **28** instances across **3** repositories
- **16/28** fail-to-pass, of those that reached a verdict
- **15/23** fail-to-pass without the 5 not-behavioural PRs (see PR groups at the end)
- **2** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **14/28**
- **Changed-line coverage (main): mean 75.4%** of the per-PR figures over the 16 measured YES PRs; median 92%
- **75%** of the changed lines those tests were measured against (404/540, pooled)
- **74%** pooled without the lines that run on import (389/525)
- **15%** of every source line all 28 patches change (404/2727), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$5.98 and 83.1M tokens in total
- **27** of these had a stop refused at least once, and **15** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[coverage+mutation]` | 9 | 9 | 0 | 0 | checks after fail-to-pass |
| `duties_open[coverage]` | 1 | 1 | 0 | 0 | checks after fail-to-pass |
| `duties_open[mutation]` | 2 | 2 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 13 | 1 | 12 | 0 | not fail-to-pass yet |
| `skipped_at_base` | 1 | 1 | 0 | 0 | not fail-to-pass yet |
| `verify_open` | 1 | 1 | 0 | 0 | not fail-to-pass yet |

Of the **15** first refused as not fail-to-pass yet, **3** ended fail-to-pass.


### The second chance

**Rescued 2** of 14 restarted run(s): 14 ended without a YES and were restarted with the record of their first attempt (14 after a NO, 0 after a BROKEN), and 2 ended fail-to-pass on the second attempt: `scipy__scipy-21700`, `pandas-dev__pandas-60196`.


### Fail-to-pass, then lost

**16** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`scipy__scipy-21700`](./scipy__scipy-21700/) |  | YES | 83% (129/156) | 13/20 | 14/20 | 112 | `run` x40, `write_file` x19, `verify` x14, `coverage` x7, `run_tests` x5, `mutation` x4 | — | — | — | — | 2026-10-12 16:07 UTC |
| [`scipy__scipy-21713`](./scipy__scipy-21713/) |  | NO | — | — | — | 106 | `run` x33, `run_tests` x23, `write_file` x22, `verify` x11 | — | — | — | — | 2026-10-12 14:53 UTC |
| [`scipy__scipy-22549`](./scipy__scipy-22549/) |  | YES | 40% (8/20) | 5/20 | 10/20 | 69 | `run` x30, `write_file` x11, `verify` x10, `coverage` x4, `mutation` x4, `run_tests` x4 | — | — | — | — | 2026-10-12 14:30 UTC |
| [`scipy__scipy-21996`](./scipy__scipy-21996/) |  | YES | 92% (49/53) | 15/20 | 16/20 | 84 | `run` x27, `write_file` x16, `verify` x13, `coverage` x9, `run_tests` x4, `mutation` x3 | — | — | — | — | 2026-10-12 15:20 UTC |
| [`scipy__scipy-21485`](./scipy__scipy-21485/) |  | NO | — | — | — | 77 | `run` x26, `write_file` x15, `run_tests` x12, `verify` x4, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 14:46 UTC |
| [`scipy__scipy-20137`](./scipy__scipy-20137/) |  | YES | 82% (63/77) | 6/20 | 9/20 | 49 | `run` x12, `verify` x10, `write_file` x10, `coverage` x4, `mutation` x4, `run_tests` x2 | — | — | — | — | 2026-10-12 15:12 UTC |
| [`scipy__scipy-22616`](./scipy__scipy-22616/) |  | NO | — | — | — | 93 | `run` x26, `write_file` x22, `run_tests` x19, `verify` x13 | — | — | — | — | 2026-10-12 14:48 UTC |
| [`scipy__scipy-21462`](./scipy__scipy-21462/) |  | YES | 95% (41/43); 95% (38/40) without import-time | 15/20 | 15/20 | 49 | `run` x20, `write_file` x8, `run_tests` x6, `coverage` x3, `verify` x3, `mutation` x2  (+1 edit reverted) | — | — | — | — | 2026-10-12 14:14 UTC |
| [`scipy__scipy-20382`](./scipy__scipy-20382/) |  | NO | — | — | — | 89 | `run` x30, `write_file` x16, `run_tests` x15, `verify` x12, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 14:42 UTC |
| [`scipy__scipy-21332`](./scipy__scipy-21332/) |  | NO | — | — | — | 110 | `run` x33, `write_file` x25, `run_tests` x24, `verify` x8, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 14:44 UTC |
| [`pandas-dev__pandas-58893`](./pandas-dev__pandas-58893/) |  | YES | 53% (10/19) | 14/20 | 13/20 | 57 | `run` x11, `verify` x10, `write_file` x10, `coverage` x8, `mutation` x7, `run_tests` x2 | — | — | — | — | 2026-10-12 14:38 UTC |
| [`pandas-dev__pandas-60196`](./pandas-dev__pandas-60196/) |  | YES | 100% (4/4) | 5/8 | n/a | 95 | `run` x41, `write_file` x15, `run_tests` x10, `verify` x9, `mutation` x4, `coverage` x3 | — | — | — | — | 2026-10-12 13:01 UTC |
| [`pandas-dev__pandas-59626`](./pandas-dev__pandas-59626/) |  | YES | 10% (2/21) | 0/12 | n/a | 71 | `run` x23, `write_file` x12, `verify` x11, `coverage` x8, `mutation` x7, `run_tests` x4 | — | — | — | — | 2026-10-12 14:24 UTC |
| [`pandas-dev__pandas-60505`](./pandas-dev__pandas-60505/) |  | YES | 100% (4/4) | 2/2 | 1/2 | 32 | `run` x13, `write_file` x5, `run_tests` x4, `verify` x3, `coverage` x2, `mutation` x1 | — | — | — | — | 2026-10-12 13:43 UTC |
| [`pandas-dev__pandas-59141`](./pandas-dev__pandas-59141/) |  | NO | — | — | — | 93 | `run` x43, `write_file` x15, `run_tests` x11, `verify` x5, `coverage` x2, `mutation` x1 | — | — | — | — | 2026-10-12 14:36 UTC |
| [`pandas-dev__pandas-60295`](./pandas-dev__pandas-60295/) |  | YES | 50% (2/4) | 2/8 | 4/8 | 75 | `run` x36, `verify` x10, `write_file` x10, `run_tests` x6, `coverage` x4, `mutation` x3 | — | — | — | — | 2026-10-12 14:12 UTC |
| [`pandas-dev__pandas-59854`](./pandas-dev__pandas-59854/) |  | NO | — | — | — | 91 | `run` x27, `write_file` x18, `run_tests` x17, `verify` x7, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 14:41 UTC |
| [`pandas-dev__pandas-60713`](./pandas-dev__pandas-60713/) |  | YES | 100% (3/3) | 2/2 | 0/2 | 36 | `run` x12, `mutation` x4, `run_tests` x4, `verify` x4, `write_file` x4, `coverage` x3 | — | — | — | — | 2026-10-12 13:44 UTC |
| [`pandas-dev__pandas-60541`](./pandas-dev__pandas-60541/) |  | NO | — | — | — | 84 | `run` x35, `write_file` x14, `run_tests` x13, `verify` x6, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 14:25 UTC |
| [`pandas-dev__pandas-59928`](./pandas-dev__pandas-59928/) |  | NO | — | — | — | 102 | `write_file` x32, `run` x21, `run_tests` x21, `verify` x8, `coverage` x2, `mutation` x2 | — | — | — | — | 2026-10-12 14:46 UTC |
| [`Qiskit__qiskit-12483`](./Qiskit__qiskit-12483/) |  | YES | 96% (49/51); 96% (48/50) without import-time | 15/20 | 13/20 | 86 | `write_file` x21, `verify` x20, `run` x12, `coverage` x9, `mutation` x8, `run_tests` x3 | — | — | — | — | 2026-10-12 14:54 UTC |
| [`Qiskit__qiskit-12561`](./Qiskit__qiskit-12561/) |  | YES | 80% (4/5) | 4/5 | n/a | 47 | `run` x19, `verify` x5, `write_file` x5, `coverage` x4, `run_tests` x4, `mutation` x3  (+1 edit reverted) | — | — | — | — | 2026-10-12 14:13 UTC |
| [`Qiskit__qiskit-12579`](./Qiskit__qiskit-12579/) |  | YES | 100% (8/8) | 5/5 | 4/5 | 32 | `run` x10, `verify` x5, `write_file` x5, `run_tests` x4, `mutation` x3, `coverage` x1 | — | — | — | — | 2026-10-12 15:24 UTC |
| [`Qiskit__qiskit-12608`](./Qiskit__qiskit-12608/) |  | NO | — | — | — | 106 | `run` x34, `write_file` x25, `run_tests` x16, `verify` x6, `coverage` x2  (+1 edit reverted) | — | — | — | — | 2026-10-12 14:50 UTC |
| [`Qiskit__qiskit-13251`](./Qiskit__qiskit-13251/) |  | NO | — | — | — | 85 | `run` x39, `write_file` x15, `run_tests` x8, `verify` x5, `coverage` x1 | — | — | — | — | 2026-10-12 14:32 UTC |
| [`Qiskit__qiskit-13343`](./Qiskit__qiskit-13343/) |  | NO | — | — | — | 110 | `run` x34, `run_tests` x24, `write_file` x22, `verify` x11, `coverage` x1, `mutation` x1 | — | — | — | — | 2026-10-12 13:02 UTC |
| [`Qiskit__qiskit-14024`](./Qiskit__qiskit-14024/) |  | YES | 25% (15/59); 8% (4/48) without import-time | 2/20 | n/a | 49 | `run` x16, `write_file` x6, `verify` x5, `coverage` x4, `mutation` x4, `run_tests` x4 | — | — | — | — | 2026-10-12 14:13 UTC |
| [`Qiskit__qiskit-14353`](./Qiskit__qiskit-14353/) |  | YES | 100% (13/13) | 16/19 | n/a | 85 | `run` x31, `write_file` x11, `run_tests` x10, `verify` x10, `coverage` x7, `mutation` x4 | — | — | — | — | 2026-10-12 14:53 UTC |

Mutation cells: *none held out* -- the only mutant(s) went to the half shown by the agent's `mutation` tool, so none were left to score on; *no mutants* -- mutmut offers none on the changed lines; *n/a* -- none of the developer's tests pass offline here, so its column is not measured.

Coverage cells: the second figure leaves out changed lines that run on import (imports, module constants, decorators, `def` and class lines) -- any test that imports the module runs them.

## PR groups

**not behavioural (no fail-to-pass test is meaningful)** (5): Agreed with the user 2026-10-12: a pure no-op or a change that only renames or reorganises private code; a test can only check spelling.

- `pandas-dev__pandas-60541` -- ruff cleanup: a no-op (`right_value = right_op` two lines above) plus reformatting -- **NO** here
- `scipy__scipy-20382` -- `_np` -> `np` rename -- **NO** here
- `scipy__scipy-22616` -- vecdot speed-up through a new private helper -- **NO** here
- `scipy__scipy-21485` -- refactor into `_bary_rational` -- **NO** here
- `pandas-dev__pandas-59626` -- private rename -- **YES** here

**not Python (excluded from runs)** (2): The change is in Rust; the image builds the Rust extension once, so the change cannot be applied and reverted by the harness.

- `Qiskit__qiskit-13704` -- Rust change -- not run
- `Qiskit__qiskit-12495` -- Rust change -- not run

