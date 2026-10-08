# no-second-chance vs no-second-chance-no-require-tools

Same 36 PRs, 21 YES in both. Coverage is compared on the **19 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `no-second-chance`:** its runs come from several batches of the same system (see its `REUSED.md`).

**Provenance of `no-second-chance-no-require-tools`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | no-second-chance | no-second-chance-no-require-tools |
|---|---|---|
| fail-to-pass | **27/36** | **23/36** |
| first attempts alone | 27/36 | 23/36 |
| rescued by the second chance | 0 | 0 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | none refused |
| **coverage, pooled over the 19 PRs YES in both (comparison)** | **67.4% (89/132)** | **50.8% (67/132)** |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 94.4% (34/36) | 100.0% (36/36) |
| same, without import-time lines | 56.1% (55/98) | 33.7% (33/98) |
| coverage, mean of per-PR over own YES (each run's own) | 93.2% over 24 | 96.8% over 21 |
| mutants caught by the agent's test, pooled over 15 PRs YES in both | 51.7% (30/58) | 51.7% (30/58) |
| same, without `psf__requests-1142` (the PR that moves the gap most) | 47.2% (25/53) | 49.1% (26/53) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1538 | 1137 |
| model cost | $2.73 | $1.55 |

## Verdicts that differ (8)

| PR | no-second-chance | no-second-chance-no-require-tools | why no-second-chance-no-require-tools |
|---|---|---|---|
| `django__django-13279` | YES | NO | passes before the fix too, so it does not test the change |
| `django__django-15098` | YES | NO | still failing after the fix (['test_language_code_with_script_and_region_mixed_case (test_ |
| `matplotlib__matplotlib-26208` | NO | YES | 1 test(s) fail before the fix and pass after |
| `mwaskom__seaborn-3069` | NO | YES | 2 test(s) fail before the fix and pass after |
| `pylint-dev__pylint-6903` | YES | NO | passes before the fix too, so it does not test the change |
| `pytest-dev__pytest-10081` | YES | NO | passes before the fix too, so it does not test the change |
| `pytest-dev__pytest-7982` | YES | NO | still failing after the fix (['testing/test_f2p_pytest_dev__pytest_7982.py::test_visit_fun |
| `sphinx-doc__sphinx-7454` | YES | NO | passes before the fix too, so it does not test the change |

## Coverage differences on PRs YES in both (2)

| PR | no-second-chance | no-second-chance-no-require-tools |
|---|---|---|
| `astropy__astropy-13398` | 57% | 32% |
| `django__django-13406` | 0% | 100% |

## Mutation differences on PRs YES in both (2)

| PR | no-second-chance | no-second-chance-no-require-tools |
|---|---|---|
| `psf__requests-1142` | 5/5 | 4/5 |
| `scikit-learn__scikit-learn-25232` | 2/4 | 3/4 |
