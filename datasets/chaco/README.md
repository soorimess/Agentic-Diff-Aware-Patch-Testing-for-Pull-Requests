# ChaCo

The benchmark of *Change And Cover: Last-Mile, Pull Request-Based Regression Test
Augmentation* (Zhou, Paltenghi, Kim, Pradel; ICSE 2026), code at
[UCLA-SEAL/Change-Cover](https://github.com/UCLA-SEAL/Change-Cover).

## Where the data is

ChaCo publishes its benchmark as PR numbers only:
[`config/benchmark/rq_full.json`](https://github.com/UCLA-SEAL/Change-Cover/blob/d3be9a251d917a657a7675141728977c17aec117/config/benchmark/rq_full.json).
It lists 145 merged PRs from 2024–2025: 50 from `scipy/scipy`, 50 from `Qiskit/qiskit`
and 45 from `pandas-dev/pandas`. A copy, pinned at commit `d3be9a25`, is in
[`benchmark/rq_full.json`](benchmark/rq_full.json).

The repository has no instance file and publishes no images. Two other things are there
but not used here:
- **Dockerfiles** under `docker/<project>/`. They check out the PR head and run the whole
  suite for coverage.
- **Generated tests**, on figshare. These are only needed to reproduce the paper's own numbers.

## How a PR becomes an instance here

| step | what it does | result |
|---|---|---|
| `prepare` | Reads the PR from the GitHub API, cached in `.cache/github/`. Takes base = the merge commit's first parent and change = `diff(base, merge)` from a blobless mirror in `.cache/mirrors/`. Splits files under test directories into `test_patch` and the rest into `patch`. The problem statement is the issues the PR closes, then the PR's title and body. | a row in [`instances.json`](instances.json), a Dockerfile in [`dockerfiles/`](dockerfiles/) |
| `build` | Builds that Dockerfile: `/testbed` at base, dependencies resolved as of the base commit's date (`uv --exclude-newer`), the project installed editable | image `f2p-chaco/<id>`, archived in the image cache |
| `validate` | Runs the developer's test files at base+tests and at head+tests. `FAIL_TO_PASS` = failed before and passed after; `PASS_TO_PASS` = passed both times. Then `verify()` with the developer's test must reproduce the flip. | `status: runnable`, listed in [`prs.json`](prs.json) |

Only runnable rows are run. ChaCo's task is covering a PR's uncovered lines at head, with
no flip required, so some of its PRs have no fail-to-pass test: refactors, lint fixes, and
changes whose tests passed before. `validate` keeps those rows and records why they are
not runnable.

`status` values:
- `prepared`: awaiting build and validate.
- `runnable`: ready to run.
- `not-fail-to-pass`: no developer test flips.
- `broken-env`: the developer's tests collect nothing in the image.
- `oracle-mismatch`: the derived flip is not reproduced by `verify()`.
- `unsupported`: no Python source change, not merged, or a Qiskit Rust change, which the
  editable install does not rebuild.

## Per-project images

These are adapted from ChaCo's own Dockerfiles; `chaco.RECIPES` holds the recipes.

| project | Python | notes |
|---|---|---|
| pandas | 3.11 | meson-python editable (C extensions rebuilt on import, offline); X/GL libraries for `pytest-qt` |
| SciPy | 3.12 | meson-python editable, gfortran + OpenBLAS, submodules |
| Qiskit | 3.11 | Rust (rustup stable) via setuptools-rust; `pytest` added (Qiskit itself uses stestr) |

Build times on the server (16 cores) are 5–7 min per image. Archived images are 0.5–1.5 GB.

## Status

`python -m openhands_f2p.sources info chaco` prints the status of every row. So far
7 of the 145 are prepared. Preparing all of them needs a `GITHUB_TOKEN`, because the
unauthenticated GitHub API allows 60 calls an hour and a PR takes 2–3.

## Runs

| run | PR | verdict | changed-line coverage | mutants (agent / developer) | actions |
|---|---|---|---|---|---|
| [`chaco-outs/base`](../../chaco-outs/base/RUNS.md), 2026-10-08 | pandas-dev/pandas#60505 | YES | 100% (4/4) | 2/2 / 1/2 | 39 |

The configuration matches the out-v2 base run: qwen3-coder-30b, temperature 0.3, a cap
of 125 actions, all add-ons, 20 mutants, and no judge.
