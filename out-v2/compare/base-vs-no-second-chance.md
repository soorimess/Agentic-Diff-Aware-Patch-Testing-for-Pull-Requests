# base vs no-second-chance

Same 36 PRs, 25 YES in both. Coverage is compared on the **22 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `base`:** its runs come from several batches of the same system and some PRs keep the better of two runs, which favours it slightly (see its `REUSED.md`).

**Provenance of `no-second-chance`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | base | no-second-chance |
|---|---|---|
| fail-to-pass | **29/36** | **27/36** |
| first attempts alone | 27/36 | 27/36 |
| rescued by the second chance | 2 | 0 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | 1 of 10 |
| **coverage, pooled over the 22 PRs YES in both (comparison)** | **81.1% (116/143)** | **70.6% (101/143)** |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 97.9% (46/47) | 97.9% (46/47) |
| same, without import-time lines | 75.2% (82/109) | 61.5% (67/109) |
| coverage, mean of per-PR over own YES (each run's own) | 94.7% over 26 | 93.2% over 24 |
| mutants caught by the agent's test, pooled over 20 PRs YES in both | 71.6% (58/81) | 61.7% (50/81) |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 80.3% (49/61) | 80.3% (49/61) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1992 | 1538 |
| model cost | $3.76 | $2.73 |

## Verdicts that differ (6)

| PR | base | no-second-chance | why no-second-chance |
|---|---|---|---|
| `django__django-11119` | YES | NO | still failing after the fix (['test_engine_autoescape_setting_ignored (test_f2p_django__dj |
| `django__django-13406` | NO | YES | 1 test(s) fail before the fix and pass after |
| `matplotlib__matplotlib-26208` | YES | NO | still failing after the fix (['lib/matplotlib/tests/test_f2p_matplotlib__matplotlib_26208. |
| `mwaskom__seaborn-3069` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `pylint-dev__pylint-4970` | YES | NO | passes before the fix too, so it does not test the change |
| `pylint-dev__pylint-6903` | NO | YES | 4 test(s) fail before the fix and pass after |

## Coverage differences on PRs YES in both (1)

| PR | base | no-second-chance |
|---|---|---|
| `astropy__astropy-13398` | 73% | 57% |

## Mutation differences on PRs YES in both (3)

| PR | base | no-second-chance |
|---|---|---|
| `astropy__astropy-13398` | 9/20 | 1/20 |
| `django__django-13279` | 5/7 | 4/7 |
| `psf__requests-1142` | 4/5 | 5/5 |
