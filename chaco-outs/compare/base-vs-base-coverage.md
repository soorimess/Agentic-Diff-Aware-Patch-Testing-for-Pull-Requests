# base vs base-coverage

Same 28 PRs, 12 YES in both. Coverage is compared on the **12 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

| | base | base-coverage |
|---|---|---|
| fail-to-pass | **16/28** | **15/28** |
| first attempts alone | 14/28 | 14/28 |
| rescued by the second chance | 2 | 1 |
| runs refused by the verify loop that still ended YES without a restart | 3 of 17 | 3 of 17 |
| **coverage, pooled over the 12 PRs YES in both (comparison)** | **80.4% (370/460)** | **62.6% (288/460)** |
| same, without `scipy__scipy-21700` (the PR that moves the gap most) | 79.3% (241/304) | 75.3% (229/304) |
| same, without import-time lines | 80.3% (366/456) | 62.3% (284/456) |
| coverage, mean of per-PR over own YES (each run's own) | 75.4% over 16 | 69.7% over 15 |
| mutants caught by the agent's test, pooled over 12 PRs YES in both | 57.8% (96/166) | 52.4% (87/166) |
| same, without `scipy__scipy-22549` (the PR that moves the gap most) | 62.3% (91/146) | 59.6% (87/146) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 2174 | 1916 |
| model cost | $5.98 | $4.56 |

## Verdicts that differ (7)

| PR | base | base-coverage | why base-coverage |
|---|---|---|---|
| `Qiskit__qiskit-12608` | NO | YES | 4 test(s) fail before the fix and pass after |
| `Qiskit__qiskit-13251` | NO | YES | 1 test(s) fail before the fix and pass after |
| `Qiskit__qiskit-14024` | YES | NO | passes before the fix too, so it does not test the change |
| `Qiskit__qiskit-14353` | YES | NO | passes before the fix too, so it does not test the change |
| `pandas-dev__pandas-59854` | NO | YES | 1 test(s) fail before the fix and pass after |
| `pandas-dev__pandas-60196` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `pandas-dev__pandas-60295` | YES | NO | still failing after the fix (['pandas/tests/internals/test_f2p_pandas_dev__pandas_60295.py |

## Coverage differences on PRs YES in both (8)

| PR | base | base-coverage |
|---|---|---|
| `Qiskit__qiskit-12483` | 96% | 98% |
| `Qiskit__qiskit-12561` | 80% | 60% |
| `Qiskit__qiskit-12579` | 100% | 88% |
| `pandas-dev__pandas-58893` | 53% | 47% |
| `pandas-dev__pandas-59626` | 10% | 0% |
| `scipy__scipy-20137` | 82% | 75% |
| `scipy__scipy-21700` | 83% | 38% |
| `scipy__scipy-21996` | 92% | 87% |

## Mutation differences on PRs YES in both (6)

| PR | base | base-coverage |
|---|---|---|
| `Qiskit__qiskit-12561` | 4/5 | 3/5 |
| `Qiskit__qiskit-12579` | 5/5 | 4/5 |
| `pandas-dev__pandas-58893` | 14/20 | 13/20 |
| `scipy__scipy-20137` | 6/20 | 8/20 |
| `scipy__scipy-21700` | 13/20 | 10/20 |
| `scipy__scipy-22549` | 5/20 | 0/20 |

## PR groups

Without the 5 not-behavioural PRs: fail-to-pass **15/23** (base) vs **14/23** (base-coverage); coverage pooled over the 11 PRs YES in both **83.8% (368/439)** vs **65.6% (288/439)**.

**not behavioural (no fail-to-pass test is meaningful)** (5): Agreed with the user 2026-10-12: a pure no-op or a change that only renames or reorganises private code; a test can only check spelling.

| PR | what | base | base-coverage |
|---|---|---|---|
| `pandas-dev__pandas-60541` | ruff cleanup: a no-op (`right_value = right_op` two lines above) plus reformatting | NO | NO |
| `scipy__scipy-20382` | `_np` -> `np` rename | NO | NO |
| `scipy__scipy-22616` | vecdot speed-up through a new private helper | NO | NO |
| `scipy__scipy-21485` | refactor into `_bary_rational` | NO | NO |
| `pandas-dev__pandas-59626` | private rename | YES | YES |

**not Python (excluded from runs)** (2): The change is in Rust; the image builds the Rust extension once, so the change cannot be applied and reverted by the harness.

| PR | what | base | base-coverage |
|---|---|---|---|
| `Qiskit__qiskit-13704` | Rust change | not run | not run |
| `Qiskit__qiskit-12495` | Rust change | not run | not run |

