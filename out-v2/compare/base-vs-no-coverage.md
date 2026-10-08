# base vs no-coverage

Same 36 PRs, 27 YES in both. Coverage is compared on the **25 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `base`:** its runs come from several batches of the same system and some PRs keep the better of two runs, which favours it slightly (see its `REUSED.md`).

| | base | no-coverage |
|---|---|---|
| fail-to-pass | **29/36** | **28/36** |
| first attempts alone | 27/36 | 27/36 |
| rescued by the second chance | 2 | 1 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | 1 of 10 |
| **coverage, pooled over the 25 PRs YES in both (comparison)** | **81.8% (121/148)** | **52.0% (77/148)** |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 98.1% (51/52) | 88.5% (46/52) |
| same, without import-time lines | 76.3% (87/114) | 37.7% (43/114) |
| coverage, mean of per-PR over own YES (each run's own) | 94.7% over 26 | 90.5% over 26 |
| mutants caught by the agent's test, pooled over 23 PRs YES in both | 71.8% (61/85) | 54.1% (46/85) |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 80.0% (52/65) | 69.2% (45/65) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1992 | 1781 |
| model cost | $3.76 | $3.09 |

## Verdicts that differ (3)

| PR | base | no-coverage | why no-coverage |
|---|---|---|---|
| `django__django-13406` | NO | YES | 1 test(s) fail before the fix and pass after |
| `django__django-17029` | YES | NO | passes before the fix too, so it does not test the change |
| `mwaskom__seaborn-3069` | YES (rescued) | NO | passes before the fix too, so it does not test the change |

## Coverage differences on PRs YES in both (4)

| PR | base | no-coverage |
|---|---|---|
| `astropy__astropy-13398` | 73% | 32% |
| `django__django-13279` | 80% | 20% |
| `matplotlib__matplotlib-26208` | 100% | 50% |
| `psf__requests-1142` | 100% | 50% |

## Mutation differences on PRs YES in both (3)

| PR | base | no-coverage |
|---|---|---|
| `astropy__astropy-13398` | 9/20 | 1/20 |
| `django__django-13279` | 5/7 | 0/7 |
| `psf__requests-1142` | 4/5 | 2/5 |
