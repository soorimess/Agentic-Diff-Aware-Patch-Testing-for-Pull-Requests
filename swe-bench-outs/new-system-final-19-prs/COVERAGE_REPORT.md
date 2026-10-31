# How far can the coverage tool raise coverage?

18 held-out large SWE-bench PRs, qwen3-coder-30b. Charts: [coverage.html](coverage.html).

Mean changed-line coverage goes from **35.0%** without the coverage tool to **62.7%** with it (**+27.7 points**), higher on 14 of 18 PRs.

| | without the tool | with the tool |
|---|---:|---:|
| Mean changed-line coverage | 35.0% | 62.7% |
| PRs at 100% | 0 | 1 |
| PRs at 80% or more | 2 | 7 |
| PRs under 20% | 7 | 1 |

## Every pull request

| PR | lines | without | with | gain |
|---|---:|---:|---:|---:|
| xarray 6971 | 83 | 1.3% | 87.0% | +85.7 |
| pylint 4551 | 58 | 16.1% | 82.3% | +66.2 |
| sympy 14085 | 58 | 41.4% | 89.7% | +48.3 |
| matplotlib 20693 | 118 | 13.0% | 57.4% | +44.4 |
| pytest 5787 | 74 | 59.2% | 100.0% | +40.8 |
| sphinx 7380 | 134 | 38.8% | 79.1% | +40.3 |
| scikit-learn 14012 | 58 | 64.6% | 98.5% | +33.9 |
| sympy 17512 | 82 | 24.7% | 56.5% | +31.8 |
| sphinx 7234 | 73 | 6.6% | 35.0% | +28.4 |
| matplotlib 25515 | 160 | 7.5% | 30.6% | +23.1 |
| sphinx 7590 | 52 | 42.6% | 63.0% | +20.4 |
| xarray 7444 | 56 | 80.4% | 98.0% | +17.6 |
| sympy 13236 | 88 | 6.8% | 20.5% | +13.7 |
| django 11991 | 50 | 35.8% | 47.2% | +11.4 |
| astropy 7008 | 56 | 81.5% | 81.5% | +0.0 |
| django 16092 | 128 | 13.1% | 13.1% | +0.0 |
| matplotlib 19743 | 55 | 43.3% | 43.3% | +0.0 |
| astropy 14295 | 51 | 54.0% | 46.0% | -8.0 |

## How this was measured

- 18 large SWE-bench PRs (50 to 160 executable changed lines), none used while the tools were built or tuned. Same harness, model and settings in every run: qwen3-coder-30b, temperature 0.3, at most 125 actions; the agent must call `verify` itself, and a guard undoes any edit outside the test file.
- Coverage is measured after the run on the handed-in test with the change applied, over the executable lines the PR adds. Only fail-to-pass tests are counted.
