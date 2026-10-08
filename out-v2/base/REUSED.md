# Where each run in this folder comes from

The base is one system, run in three batches to save budget (user, 2026-10-04). Each run
below was made by code whose agent-visible behaviour is identical to the final one
(`d882f246`) for that run: every refusal, acceptance and tool text was replayed and would
be the same (`docs/bugs-from-700-runs.md`, "Found reading the base at c1d704b2").

- Run at `d882f246` (rerun after the rule-B fixes): django__django-11119, django__django-13279, matplotlib__matplotlib-13989, pytest-dev__pytest-7982
- Run at `acb9fff7` (rerun after the rewind): scikit-learn__scikit-learn-25232
- Run at `85a0586e` (rerun after the function-level coverage refusal): astropy__astropy-13398 (its earlier run is in `out-v2/base-second-runs/`)
- Run at `c1d704b2`: the other 25 not listed below
- Reused from `out-v2/fix-check-2/` (`7e79f68a`): django__django-13406,
  matplotlib__matplotlib-26208, mwaskom__seaborn-3069, psf__requests-1142,
  sphinx-doc__sphinx-7454

## Best of two runs (user, 2026-10-05)

Three PRs were run twice: at `c1d704b2` (YES) and again at `d882f246` after the rule-B
fixes (NO each time, stuck on passes-at-base -- sampling, not the fixes). The YES run is
kept here, the NO run is in `out-v2/base-second-runs/`:

- `django__django-11119` -- YES (87 actions); the pre-fix run took one refusal the fixed
  loop would not have sent.
- `django__django-13279` -- YES (54 actions); its coverage loop closed at 83% without a
  shortfall refusal (the rule-B bug), so its coverage figure comes from the old loop.
- `pytest-dev__pytest-7982` -- YES (96 actions, rescued by the second chance); it was told
  "does not reach" about a subprocess the fixed diagnosis now hedges.

Picking the better of two samples favours base slightly in comparisons with arms run once.
`django__django-13279` was later replaced by its `fd63cdf4` rerun (below), so the best-of-two
picks still in this folder are `django__django-11119` and `pytest-dev__pytest-7982`.

## Reruns at `fd63cdf4` (2026-10-05)

After the full trajectory audit: the prompt no longer cuts the issue or the fix, staleness is judged by content, verify names flipped and backwards tests together, a tool typed in bash gets a hint, and coverage leaves out changed lines an empty test also runs (environment baseline, user A'). Every run whose agent-visible text these change was rerun:

- matplotlib__matplotlib-22719, scikit-learn__scikit-learn-25747, scikit-learn__scikit-learn-25232, django__django-15098, django__django-17029, pylint-dev__pylint-6903, pytest-dev__pytest-5262, pytest-dev__pytest-10081, django__django-13279
- `astropy__astropy-13398`: run 1 of the randomness set `out-v2/rand-astropy-base-1/` (three runs each of base and no-second-chance)

These replace the earlier entries for the same PRs, including best-of-two picks.

## Reruns at `0a15f5d8` (2026-10-05, after reading no-require-tools)

Two harness bugs: the subprocess hedge matched the word "multiprocessing" in a docstring
(pylint-6903 was told falsely that its test "starts a child process"), and the coverage
environment probe ran pytest's unittest plugin, the code pytest-10081 changes, so that PR
could never be measured. Both PRs rerun; the earlier runs are in `out-v2/base-second-runs/`:

- pylint-dev__pylint-6903, pytest-dev__pytest-10081

## Reruns at `252dd3aa` (2026-10-06, after reading no-second-chance-no-require-tools)

Four text fixes: astropy's report header and pytest's own traceback frames are dropped from
`verify`/`run_tests` output (astropy-13398's failure line had been clipped away); `verify`
and `coverage` say when a test starts a child process; "backwards" names tests failing on
both sides; the `run_tests` summary lists the agent's own ids only. Every run whose shown
text these change was rerun (`out-v2/tools/replay_texts.py`); the earlier runs are in
`out-v2/base-second-runs/pre-252dd3aa/`:

- astropy__astropy-13398, astropy__astropy-14995, astropy__astropy-7336, pytest-dev__pytest-10081, pytest-dev__pytest-7982

`pytest-dev__pytest-7982` was one of the two best-of-two picks; its new run replaces it, so `django__django-11119` is now the only best-of-two pick here.
