# base vs no-require-tools

Same 36 PRs, 27 YES in both. Coverage is compared on the **24 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `base`:** its runs come from several batches of the same system and some PRs keep the better of two runs, which favours it slightly (see its `REUSED.md`).

**Provenance of `no-require-tools`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | base | no-require-tools |
|---|---|---|
| fail-to-pass | **29/36** | **29/36** |
| first attempts alone | 27/36 | 27/36 |
| rescued by the second chance | 2 | 2 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | none refused |
| **coverage, pooled over the 24 PRs YES in both (comparison)** | **82.3% (51/62)** | **90.3% (56/62)** |
| same, without `mwaskom__seaborn-3069` (the PR that moves the gap most) | 98.0% (50/51) | 88.2% (45/51) |
| same, without import-time lines | 81.0% (47/58) | 89.7% (52/58) |
| coverage, mean of per-PR over own YES (each run's own) | 94.7% over 26 | 91.9% over 26 |
| mutants caught by the agent's test, pooled over 22 PRs YES in both | 63.8% (51/80) | 66.2% (53/80) |
| same, without `mwaskom__seaborn-3069` (the PR that moves the gap most) | 79.7% (51/64) | 65.6% (42/64) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1992 | 1550 |
| model cost | $3.76 | $2.42 |

## Verdicts that differ (4)

| PR | base | no-require-tools | why no-require-tools |
|---|---|---|---|
| `astropy__astropy-13398` | YES | NO | passes before the fix too, so it does not test the change |
| `pylint-dev__pylint-6903` | NO | YES | 2 test(s) fail before the fix and pass after |
| `pytest-dev__pytest-7982` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `sphinx-doc__sphinx-9602` | NO | YES (rescued) | 1 test(s) fail before the fix and pass after |

## Coverage differences on PRs YES in both (5)

| PR | base | no-require-tools |
|---|---|---|
| `django__django-13279` | 80% | 60% |
| `mwaskom__seaborn-3069` | 9% | 100% |
| `psf__requests-1142` | 100% | 50% |
| `pylint-dev__pylint-4970` | 100% | 0% |
| `scikit-learn__scikit-learn-25232` | 100% | 80% |

## Mutation differences on PRs YES in both (5)

| PR | base | no-require-tools |
|---|---|---|
| `django__django-13279` | 5/7 | 1/7 |
| `mwaskom__seaborn-3069` | 0/16 | 11/16 |
| `psf__requests-1142` | 4/5 | 2/5 |
| `scikit-learn__scikit-learn-25232` | 2/4 | 1/4 |
| `sphinx-doc__sphinx-7454` | 9/9 | 7/9 |
