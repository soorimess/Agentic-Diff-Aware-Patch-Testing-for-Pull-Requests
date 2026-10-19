# Checkpoint 4: the coverage tool

What the coverage tool adds, on a second dataset (ChaCo) and on large PRs. In every pair, `base`
is the full system with the coverage tool and `base-coverage` is the same system without it.

| folder | what it holds |
|---|---|
| `chaco-outs/base/`, `chaco-outs/base-coverage/` | 28 ChaCo PRs (SciPy, pandas, Qiskit), with and without the coverage tool |
| `chaco-outs/compare/` | their comparison |
| `swe-bench-outs/large/base/`, `base-coverage/` | large SWE-bench PRs (50+ executable changed lines), with and without the tool |
| `chaco-outs/large/base/`, `base-coverage/` | large ChaCo PRs, with and without the tool |

Only the experiment that marks this system version is kept here; tuning runs, retries and reruns
are not. The current system and its final experiment are on `main`.
