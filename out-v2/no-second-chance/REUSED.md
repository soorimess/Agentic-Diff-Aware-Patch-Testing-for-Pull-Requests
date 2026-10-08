# Where each run in this folder comes from

All 36 ran at `dbfcc71c`/`d9362d0e` except `astropy__astropy-13398`, rerun at `85a0586e` after
the function-level coverage refusal (its only change; no other run here got a coverage
refusal with 10+ missed lines).

## Reruns at `fd63cdf4` (2026-10-05)

After the full trajectory audit: the prompt no longer cuts the issue or the fix, staleness is judged by content, verify names flipped and backwards tests together, a tool typed in bash gets a hint, and coverage leaves out changed lines an empty test also runs (environment baseline, user A'). Every run whose agent-visible text these change was rerun:

- matplotlib__matplotlib-22719, scikit-learn__scikit-learn-25747, django__django-15098, pylint-dev__pylint-4970, django__django-17029, pylint-dev__pylint-6903, pytest-dev__pytest-5262, pytest-dev__pytest-10081, django__django-13279
- `astropy__astropy-13398`: run 1 of the randomness set `out-v2/rand-astropy-nsc-1/` (three runs each of base and no-second-chance)

These replace the earlier entries for the same PRs, including best-of-two picks.

## Reruns at `0a15f5d8` (2026-10-05, after reading no-require-tools)

Two harness bugs: the subprocess hedge matched the word "multiprocessing" in a docstring
(pylint-6903 was told falsely that its test "starts a child process"), and the coverage
environment probe ran pytest's unittest plugin, the code pytest-10081 changes, so that PR
could never be measured. Both PRs rerun; the earlier runs are in `out-v2/no-second-chance-second-runs/`:

- pylint-dev__pylint-6903, pytest-dev__pytest-10081

## Reruns at `252dd3aa` (2026-10-06, after reading no-second-chance-no-require-tools)

Four text fixes: astropy's report header and pytest's own traceback frames are dropped from
`verify`/`run_tests` output (astropy-13398's failure line had been clipped away); `verify`
and `coverage` say when a test starts a child process; "backwards" names tests failing on
both sides; the `run_tests` summary lists the agent's own ids only. Every run whose shown
text these change was rerun (`out-v2/tools/replay_texts.py`); the earlier runs are in
`out-v2/no-second-chance-second-runs/pre-252dd3aa/`:

- astropy__astropy-13398, astropy__astropy-14995, astropy__astropy-7336, pytest-dev__pytest-10081
