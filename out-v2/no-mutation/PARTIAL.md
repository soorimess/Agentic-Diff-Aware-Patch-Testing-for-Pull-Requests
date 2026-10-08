# Partial run: experiment #9, base − mutation tool

Configuration: verify, coverage, guard, require tools, second chance (no `mutation` tool),
run 2026-10-07 at `3ca9b026` on the 36 PRs of `evaluation/local-36-prs.json`.

**Only 23 of the 36 PRs finished.** The model gateway's key reached its spending limit
mid-run (HTTP 429 `budget_exceeded`); the remaining 13 never got a verdict, and the
experiment plan was ended (2026-10-08) before they were run again. All 23 finished runs are
YES, but they are the quicker, easier PRs -- the 13 missing ones include most of the PRs
other experiments fail -- so this folder must not be compared with full experiments as if
it were one.

Never finished (no result here):
astropy__astropy-13398, django__django-11119, django__django-13279, django__django-13406,
django__django-16333, matplotlib__matplotlib-22719, mwaskom__seaborn-3069,
mwaskom__seaborn-3187, pylint-dev__pylint-6903, pytest-dev__pytest-10081,
sphinx-doc__sphinx-10614, sphinx-doc__sphinx-9602, sympy__sympy-21612
