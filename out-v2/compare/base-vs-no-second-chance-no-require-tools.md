# base vs no-second-chance-no-require-tools

Same 36 PRs, 22 YES in both. Coverage is compared on the **20 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `base`:** its runs come from several batches of the same system and some PRs keep the better of two runs, which favours it slightly (see its `REUSED.md`).

**Provenance of `no-second-chance-no-require-tools`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | base | no-second-chance-no-require-tools |
|---|---|---|
| fail-to-pass | **29/36** | **23/36** |
| first attempts alone | 27/36 | 23/36 |
| rescued by the second chance | 2 | 0 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | none refused |
| **coverage, pooled over the 20 PRs YES in both (comparison)** | **74.8% (107/143)** | **54.5% (78/143)** |
| same, without `astropy__astropy-13398` (the PR that moves the gap most) | 78.7% (37/47) | 100.0% (47/47) |
| same, without import-time lines | 66.7% (72/108) | 39.8% (43/108) |
| coverage, mean of per-PR over own YES (each run's own) | 94.7% over 26 | 96.8% over 21 |
| mutants caught by the agent's test, pooled over 17 PRs YES in both | 49.3% (37/75) | 54.7% (41/75) |
| same, without `mwaskom__seaborn-3069` (the PR that moves the gap most) | 62.7% (37/59) | 50.8% (30/59) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1992 | 1137 |
| model cost | $3.76 | $1.55 |

## Verdicts that differ (8)

| PR | base | no-second-chance-no-require-tools | why no-second-chance-no-require-tools |
|---|---|---|---|
| `django__django-11119` | YES | NO | still failing after the fix (['test_render_to_string_honors_autoescape_true (test_f2p_djan |
| `django__django-13279` | YES | NO | passes before the fix too, so it does not test the change |
| `django__django-13406` | NO | YES | 1 test(s) fail before the fix and pass after |
| `django__django-15098` | YES | NO | still failing after the fix (['test_language_code_with_script_and_region_mixed_case (test_ |
| `pylint-dev__pylint-4970` | YES | NO | took 15 action(s) but wrote no test at tests/test_f2p_pylint_dev__pylint_4970.py |
| `pytest-dev__pytest-10081` | YES | NO | passes before the fix too, so it does not test the change |
| `pytest-dev__pytest-7982` | YES (rescued) | NO | still failing after the fix (['testing/test_f2p_pytest_dev__pytest_7982.py::test_visit_fun |
| `sphinx-doc__sphinx-7454` | YES | NO | passes before the fix too, so it does not test the change |

## Coverage differences on PRs YES in both (2)

| PR | base | no-second-chance-no-require-tools |
|---|---|---|
| `astropy__astropy-13398` | 73% | 32% |
| `mwaskom__seaborn-3069` | 9% | 100% |

## Mutation differences on PRs YES in both (3)

| PR | base | no-second-chance-no-require-tools |
|---|---|---|
| `astropy__astropy-13398` | 9/20 | 1/20 |
| `mwaskom__seaborn-3069` | 0/16 | 11/16 |
| `scikit-learn__scikit-learn-25232` | 2/4 | 3/4 |
