# Where each run in this folder comes from

All 36 ran at `0e643e15` (experiment #7, 2026-10-06; results in `b4908241`) except the two below.

## Reruns at `e0d6c1c8` (2026-10-06, after reading no-verify)

The `run_tests` summary filtered a directory target as if it were a file (every real id dropped),
and pytest's skip summary (`SKIPPED [1] ...`) was read as a test named "[1]". Both runs saw
one of these; the earlier runs are in `out-v2/no-verify-second-runs/pre-e0d6c1c8/`:

- pylint-dev__pylint-4970, scikit-learn__scikit-learn-25232
