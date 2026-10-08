# Where each run in this folder comes from

All 36 ran at `a5dabefe` (experiment #3, 2026-10-05; results in `86845e06`) except the
two below.

## Reruns at `0a15f5d8` (2026-10-05, after reading no-require-tools)

Two harness bugs: the subprocess hedge matched the word "multiprocessing" in a docstring
(pylint-6903 was told falsely that its test "starts a child process"), and the coverage
environment probe ran pytest's unittest plugin, the code pytest-10081 changes, so that PR
could never be measured. Both PRs rerun; the earlier runs are in `out-v2/no-require-tools-second-runs/`:

- pylint-dev__pylint-6903, pytest-dev__pytest-10081

Both reruns run code whose agent-visible behaviour differs from the first launch only in
those two fixes; no other run here received the hedge or has environment lines that
changed (re-probed on all 36).

## Reruns at `252dd3aa` (2026-10-06, after reading no-second-chance-no-require-tools)

Four text fixes: astropy's report header and pytest's own traceback frames are dropped from
`verify`/`run_tests` output (astropy-13398's failure line had been clipped away); `verify`
and `coverage` say when a test starts a child process; "backwards" names tests failing on
both sides; the `run_tests` summary lists the agent's own ids only. Every run whose shown
text these change was rerun (`out-v2/tools/replay_texts.py`); the earlier runs are in
`out-v2/no-require-tools-second-runs/pre-252dd3aa/`:

- astropy__astropy-13398, astropy__astropy-14995, astropy__astropy-7336, pytest-dev__pytest-10081, pytest-dev__pytest-7982
