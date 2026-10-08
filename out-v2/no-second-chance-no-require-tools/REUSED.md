# Where each run in this folder comes from

All 36 ran at `43b809ff` (experiment #4, 2026-10-06; results in `edfb126a`) except the five below.

## Reruns at `252dd3aa` (2026-10-06, after reading no-second-chance-no-require-tools)

Four text fixes: astropy's report header and pytest's own traceback frames are dropped from
`verify`/`run_tests` output (astropy-13398's failure line had been clipped away); `verify`
and `coverage` say when a test starts a child process; "backwards" names tests failing on
both sides; the `run_tests` summary lists the agent's own ids only. Every run whose shown
text these change was rerun (`out-v2/tools/replay_texts.py`); the earlier runs are in
`out-v2/no-second-chance-no-require-tools-second-runs/pre-252dd3aa/`:

- astropy__astropy-13398, astropy__astropy-14995, astropy__astropy-7336, pytest-dev__pytest-10081, psf__requests-1142
