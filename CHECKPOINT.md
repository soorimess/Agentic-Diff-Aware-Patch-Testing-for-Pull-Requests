# Checkpoint 1: the first system

The harness as first built: the agent writes a fail-to-pass test with `verify`, the coverage and
mutation tools, a guard against editing the project, and a second chance.

| folder | what it holds |
|---|---|
| `out/out_full_run/` | the first full run on the 26 development PRs; `RUNS.md` is the index |
| `evaluation/` | ten held-out PRs, one per repository, run with several models; `RUNS.md` compares them |
| `experiments/` | ten configurations on 70 SWE-bench Verified PRs, each withholding one component; `comparison/` has the write-up |

Only the experiment that marks this system version is kept here; tuning runs, retries and reruns
are not. The current system and its final experiment are on `main`.
