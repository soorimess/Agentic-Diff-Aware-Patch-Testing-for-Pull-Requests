# no-require-tools vs no-second-chance-no-require-tools

Same 36 PRs, 21 YES in both. Coverage is compared on the **19 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `no-require-tools`:** its runs come from several batches of the same system (see its `REUSED.md`).

**Provenance of `no-second-chance-no-require-tools`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | no-require-tools | no-second-chance-no-require-tools |
|---|---|---|
| fail-to-pass | **29/36** | **23/36** |
| first attempts alone | 27/36 | 23/36 |
| rescued by the second chance | 2 | 0 |
| runs refused by the verify loop that still ended YES without a restart | none refused | none refused |
| **coverage, pooled over the 19 PRs YES in both (comparison)** | **95.7% (45/47)** | **100.0% (47/47)** |
| same, without `psf__requests-1142` (the PR that moves the gap most) | 97.8% (44/45) | 100.0% (45/45) |
| same, without import-time lines | 95.3% (41/43) | 100.0% (43/43) |
| coverage, mean of per-PR over own YES (each run's own) | 91.9% over 26 | 96.8% over 21 |
| mutants caught by the agent's test, pooled over 16 PRs YES in both | 65.5% (36/55) | 72.7% (40/55) |
| same, without `scikit-learn__scikit-learn-25232` (the PR that moves the gap most) | 68.6% (35/51) | 72.5% (37/51) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1550 | 1137 |
| model cost | $2.42 | $1.55 |

## Verdicts that differ (10)

| PR | no-require-tools | no-second-chance-no-require-tools | why no-second-chance-no-require-tools |
|---|---|---|---|
| `astropy__astropy-13398` | NO | YES | 5 test(s) fail before the fix and pass after |
| `django__django-11119` | YES | NO | still failing after the fix (['test_render_to_string_honors_autoescape_true (test_f2p_djan |
| `django__django-13279` | YES | NO | passes before the fix too, so it does not test the change |
| `django__django-13406` | NO | YES | 1 test(s) fail before the fix and pass after |
| `django__django-15098` | YES | NO | still failing after the fix (['test_language_code_with_script_and_region_mixed_case (test_ |
| `pylint-dev__pylint-4970` | YES | NO | took 15 action(s) but wrote no test at tests/test_f2p_pylint_dev__pylint_4970.py |
| `pylint-dev__pylint-6903` | YES | NO | passes before the fix too, so it does not test the change |
| `pytest-dev__pytest-10081` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `sphinx-doc__sphinx-7454` | YES | NO | passes before the fix too, so it does not test the change |
| `sphinx-doc__sphinx-9602` | YES (rescued) | NO | passes before the fix too, so it does not test the change |

## Coverage differences on PRs YES in both (2)

| PR | no-require-tools | no-second-chance-no-require-tools |
|---|---|---|
| `psf__requests-1142` | 50% | 100% |
| `scikit-learn__scikit-learn-25232` | 80% | 100% |

## Mutation differences on PRs YES in both (2)

| PR | no-require-tools | no-second-chance-no-require-tools |
|---|---|---|
| `psf__requests-1142` | 2/5 | 4/5 |
| `scikit-learn__scikit-learn-25232` | 1/4 | 3/4 |
