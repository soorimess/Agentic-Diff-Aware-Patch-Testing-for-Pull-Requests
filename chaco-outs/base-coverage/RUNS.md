# Run status, per pull request

Last run in this table: 2026-10-12 19:23 UTC.

- **28** instances across **3** repositories
- **15/28** fail-to-pass, of those that reached a verdict
- **14/23** fail-to-pass without the 5 not-behavioural PRs (see PR groups at the end)
- **1** of those rescued by the second chance (no YES on the first attempt, YES after the restart); first attempts alone: **14/28**
- **Changed-line coverage (main): mean 69.7%** of the per-PR figures over the 15 measured YES PRs; median 75%
- **63%** of the changed lines those tests were measured against (329/524, pooled)
- **62%** pooled without the lines that run on import (320/515)
- **12%** of every source line all 28 patches change (329/2727), a fixed denominator (secondary; arms are compared on pooled lines over the PRs YES in both, in the compare report)

- \$4.56 and 63.1M tokens in total
- **26** of these had a stop refused at least once, and **13** of them ended fail-to-pass


### What the refused runs did next

Every refusal comes from `require-tools`; the last column says which part of the check the first reason was.

| told | runs | ended YES | ended NO | ended BROKEN | |
|---|---|---|---|---|---|
| `duties_open[mutation]` | 10 | 10 | 0 | 0 | checks after fail-to-pass |
| `passes_at_base` | 12 | 1 | 11 | 0 | not fail-to-pass yet |
| `verify_open` | 4 | 2 | 2 | 0 | not fail-to-pass yet |

Of the **16** first refused as not fail-to-pass yet, **3** ended fail-to-pass.


### The second chance

**Rescued 1** of 14 restarted run(s): 14 ended without a YES and were restarted with the record of their first attempt (14 after a NO, 0 after a BROKEN), and 1 ended fail-to-pass on the second attempt: `pandas-dev__pandas-60505`.


### Fail-to-pass, then lost

**15** run(s) had a test their own `verify` called fail-to-pass; **0** handed in a test that is not: none. Each such test is kept in the run's `f2p_snapshots/`.

Every row was produced with the same configuration: **`verify-tool+mutation-tool+guard+require-tools+second-chance`** &mdash; what the agent was given. `full` means every input shown and every add-on added; otherwise the name lists the add-ons present (`bare` for none) and any input withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

Mutants are scored on the **held-out half** of each instance's pool, in every configuration, so runs with and without the `mutation` tool are scored on the same mutants &mdash; the agent held the tool here and was shown the other half, never these. Results from before 2026-09-28 scored runs without the tool on the whole pool and are not comparable row for row.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a model that wrote none of these tests, comparing the generated test with the developer's: which pins the behaviour the fix establishes better, which covers more of what the pull request settles, and which reads better. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | tools used | meaningful | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`scipy__scipy-21700`](./scipy__scipy-21700/) |  | YES | 38% (59/156) | 10/20 | 14/20 | 40 | `run` x12, `verify` x8, `write_file` x7, `mutation` x6, `run_tests` x2 | — | — | — | — | 2026-10-12 17:20 UTC |
| [`scipy__scipy-21713`](./scipy__scipy-21713/) |  | NO | — | — | — | 97 | `run` x30, `run_tests` x21, `write_file` x21, `verify` x9, `mutation` x1 | — | — | — | — | 2026-10-12 18:27 UTC |
| [`scipy__scipy-22549`](./scipy__scipy-22549/) |  | YES | 40% (8/20) | 0/20 | 10/20 | 69 | `run` x21, `run_tests` x12, `verify` x12, `write_file` x12, `mutation` x7 | — | — | — | — | 2026-10-12 18:12 UTC |
| [`scipy__scipy-21996`](./scipy__scipy-21996/) |  | YES | 87% (46/53) | 15/20 | 16/20 | 74 | `run` x18, `write_file` x17, `verify` x16, `mutation` x9, `run_tests` x3 | — | — | — | — | 2026-10-12 19:08 UTC |
| [`scipy__scipy-21485`](./scipy__scipy-21485/) |  | NO | — | — | — | 65 | `write_file` x18, `run` x13, `verify` x12, `run_tests` x7, `mutation` x1  (+1 edit reverted) | — | — | — | — | 2026-10-12 18:22 UTC |
| [`scipy__scipy-20137`](./scipy__scipy-20137/) |  | YES | 75% (58/77) | 8/20 | 9/20 | 32 | `verify` x7, `write_file` x7, `mutation` x5, `run` x5, `run_tests` x2 | — | — | — | — | 2026-10-12 18:48 UTC |
| [`scipy__scipy-22616`](./scipy__scipy-22616/) |  | NO | — | — | — | 103 | `run` x37, `write_file` x24, `run_tests` x22, `verify` x6 | — | — | — | — | 2026-10-12 18:21 UTC |
| [`scipy__scipy-21462`](./scipy__scipy-21462/) |  | YES | 95% (41/43); 95% (38/40) without import-time | 15/20 | 15/20 | 45 | `run` x20, `run_tests` x6, `write_file` x6, `verify` x5, `mutation` x3 | — | — | — | — | 2026-10-12 17:51 UTC |
| [`scipy__scipy-20382`](./scipy__scipy-20382/) |  | NO | — | — | — | 72 | `write_file` x17, `run_tests` x15, `run` x12, `verify` x12, `mutation` x1 | — | — | — | — | 2026-10-12 18:09 UTC |
| [`scipy__scipy-21332`](./scipy__scipy-21332/) |  | NO | — | — | — | 102 | `run` x31, `write_file` x23, `run_tests` x15, `verify` x8, `mutation` x1 | — | — | — | — | 2026-10-12 18:20 UTC |
| [`pandas-dev__pandas-58893`](./pandas-dev__pandas-58893/) |  | YES | 47% (9/19) | 13/20 | 13/20 | 33 | `run` x7, `run_tests` x6, `verify` x5, `write_file` x5, `mutation` x4 | — | — | — | — | 2026-10-12 18:00 UTC |
| [`pandas-dev__pandas-60196`](./pandas-dev__pandas-60196/) |  | NO | — | — | — | 124 | `run` x46, `write_file` x28, `run_tests` x26, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-12 16:56 UTC |
| [`pandas-dev__pandas-59626`](./pandas-dev__pandas-59626/) |  | YES | 0% (0/21) | 0/12 | n/a | 31 | `run` x15, `verify` x4, `write_file` x4, `mutation` x2, `run_tests` x1 | — | — | — | — | 2026-10-12 17:39 UTC |
| [`pandas-dev__pandas-60505`](./pandas-dev__pandas-60505/) |  | YES | 100% (4/4) | 2/2 | 1/2 | 104 | `run` x30, `write_file` x23, `verify` x13, `run_tests` x12, `mutation` x8 | — | — | — | — | 2026-10-12 18:19 UTC |
| [`pandas-dev__pandas-59141`](./pandas-dev__pandas-59141/) |  | NO | — | — | — | 78 | `run` x28, `write_file` x14, `run_tests` x11, `verify` x8, `mutation` x2 | — | — | — | — | 2026-10-12 18:08 UTC |
| [`pandas-dev__pandas-60295`](./pandas-dev__pandas-60295/) |  | NO | — | — | — | 115 | `run` x28, `write_file` x26, `run_tests` x25, `verify` x12, `mutation` x2 | — | — | — | — | 2026-10-12 18:27 UTC |
| [`pandas-dev__pandas-59854`](./pandas-dev__pandas-59854/) |  | YES | 100% (2/2) | 2/2 | 2/2 | 27 | `run` x9, `run_tests` x4, `verify` x4, `write_file` x4, `mutation` x3 | — | — | — | — | 2026-10-12 17:36 UTC |
| [`pandas-dev__pandas-60713`](./pandas-dev__pandas-60713/) |  | YES | 100% (3/3) | 2/2 | 0/2 | 36 | `run` x8, `verify` x6, `write_file` x6, `mutation` x5, `run_tests` x4 | — | — | — | — | 2026-10-12 17:42 UTC |
| [`pandas-dev__pandas-60541`](./pandas-dev__pandas-60541/) |  | NO | — | — | — | 81 | `run` x30, `write_file` x15, `run_tests` x14, `verify` x5, `mutation` x1 | — | — | — | — | 2026-10-12 18:02 UTC |
| [`pandas-dev__pandas-59928`](./pandas-dev__pandas-59928/) |  | NO | — | — | — | 93 | `run` x28, `run_tests` x20, `write_file` x20, `verify` x7, `mutation` x1 | — | — | — | — | 2026-10-12 18:13 UTC |
| [`Qiskit__qiskit-12483`](./Qiskit__qiskit-12483/) |  | YES | 98% (50/51); 98% (49/50) without import-time | 15/20 | 13/20 | 46 | `verify` x10, `write_file` x10, `mutation` x9, `run` x5, `run_tests` x4 | — | — | — | — | 2026-10-12 18:12 UTC |
| [`Qiskit__qiskit-12561`](./Qiskit__qiskit-12561/) |  | YES | 60% (3/5) | 3/5 | n/a | 35 | `run` x9, `run_tests` x7, `write_file` x7, `verify` x6, `mutation` x4  (+1 edit reverted) | — | — | — | — | 2026-10-12 17:44 UTC |
| [`Qiskit__qiskit-12579`](./Qiskit__qiskit-12579/) |  | YES | 88% (7/8) | 4/5 | 4/5 | 31 | `run` x10, `mutation` x5, `verify` x5, `write_file` x5, `run_tests` x1 | — | — | — | — | 2026-10-12 19:23 UTC |
| [`Qiskit__qiskit-12608`](./Qiskit__qiskit-12608/) |  | YES | 74% (29/39); 74% (28/38) without import-time | 13/20 | n/a | 50 | `run` x11, `write_file` x11, `verify` x10, `mutation` x9, `run_tests` x2 | — | — | — | — | 2026-10-12 16:51 UTC |
| [`Qiskit__qiskit-13251`](./Qiskit__qiskit-13251/) |  | YES | 44% (10/23); 32% (6/19) without import-time | 4/20 | n/a | 50 | `write_file` x13, `run` x11, `run_tests` x10, `verify` x4, `mutation` x3 | — | — | — | — | 2026-10-12 18:01 UTC |
| [`Qiskit__qiskit-13343`](./Qiskit__qiskit-13343/) |  | NO | — | — | — | 91 | `run` x24, `write_file` x20, `run_tests` x19, `verify` x11, `mutation` x1 | — | — | — | — | 2026-10-12 18:11 UTC |
| [`Qiskit__qiskit-14024`](./Qiskit__qiskit-14024/) |  | NO | — | — | — | 98 | `run` x36, `write_file` x23, `run_tests` x20, `verify` x3  (+1 edit reverted) | — | — | — | — | 2026-10-12 18:15 UTC |
| [`Qiskit__qiskit-14353`](./Qiskit__qiskit-14353/) |  | NO | — | — | — | 94 | `run` x30, `write_file` x23, `run_tests` x17, `verify` x6, `mutation` x1 | — | — | — | — | 2026-10-12 18:20 UTC |

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

