# base vs no-verify

Same 36 PRs, 23 YES in both. Coverage is compared on the **22 of them with coverage measured**: covered / all changed lines, pooled (user, 2026-10-04). A pooled figure weights each line, so a PR with many changed lines moves it most -- the per-PR differences are listed below.

**Provenance of `base`:** its runs come from several batches of the same system and some PRs keep the better of two runs, which favours it slightly (see its `REUSED.md`).

**Provenance of `no-verify`:** its runs come from several batches of the same system (see its `REUSED.md`).

| | base | no-verify |
|---|---|---|
| fail-to-pass | **29/36** | **25/36** |
| first attempts alone | 27/36 | 20/36 |
| rescued by the second chance | 2 | 5 |
| runs refused by the verify loop that still ended YES without a restart | 1 of 10 | none refused |
| **coverage, pooled over the 22 PRs YES in both (comparison)** | **100.0% (46/46)** | **93.5% (43/46)** |
| same, without `matplotlib__matplotlib-26208` (the PR that moves the gap most) | 100.0% (44/44) | 95.5% (42/44) |
| same, without import-time lines | 100.0% (43/43) | 93.0% (40/43) |
| coverage, mean of per-PR over own YES (each run's own) | 94.7% over 26 | 95.0% over 24 |
| mutants caught by the agent's test, pooled over 19 PRs YES in both | 80.4% (45/56) | 67.9% (38/56) |
| same, without `sphinx-doc__sphinx-7454` (the PR that moves the gap most) | 76.6% (36/47) | 68.1% (32/47) |
| meaningful (judge) | not judged | not judged |
| actions, all PRs | 1992 | 1161 |
| model cost | $3.76 | $1.30 |

## Verdicts that differ (8)

| PR | base | no-verify | why no-verify |
|---|---|---|---|
| `astropy__astropy-13398` | YES | NO | backwards: passes before the fix and fails after (['astropy/tests/test_f2p_astropy__astrop |
| `django__django-13279` | YES | NO | passes before the fix too, so it does not test the change |
| `django__django-15098` | YES | NO | backwards: passes before the fix and fails after (['test_language_code_prefix_regex_limita |
| `django__django-16333` | NO | YES | 1 test(s) fail before the fix and pass after |
| `django__django-17029` | YES | NO | passes before the fix too, so it does not test the change |
| `mwaskom__seaborn-3069` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `pytest-dev__pytest-7982` | YES (rescued) | NO | passes before the fix too, so it does not test the change |
| `sphinx-doc__sphinx-9602` | NO | YES (rescued) | 2 test(s) fail before the fix and pass after |

## Coverage differences on PRs YES in both (3)

| PR | base | no-verify |
|---|---|---|
| `matplotlib__matplotlib-26208` | 100% | 50% |
| `psf__requests-1142` | 100% | 50% |
| `scikit-learn__scikit-learn-25232` | 100% | 80% |

## Mutation differences on PRs YES in both (3)

| PR | base | no-verify |
|---|---|---|
| `psf__requests-1142` | 4/5 | 2/5 |
| `scikit-learn__scikit-learn-25232` | 2/4 | 0/4 |
| `sphinx-doc__sphinx-7454` | 9/9 | 6/9 |
