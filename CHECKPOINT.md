# Checkpoint 3: tool ablations on 36 PRs

The system with stop duties (verify, coverage, mutation), a restart as the second chance and the
coverage and mutation loops, run on the 36 locally cached PRs. `base` has every add-on; each other
folder removes one.

| folder | what it holds |
|---|---|
| `out-v2/base/` | every add-on |
| `out-v2/no-coverage/`, `no-mutation/`, `no-verify/`, `no-require-tools/`, `no-second-chance/`, `no-second-chance-no-require-tools/` | base minus that add-on (`no-mutation` is partial: 23 of 36 PRs) |
| `out-v2/compare/` | one comparison per pair of configurations |
| `out-v2/comparison/` | the page built from all of them |

Only the experiment that marks this system version is kept here; tuning runs, retries and reruns
are not. The current system and its final experiment are on `main`.
