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

ChaCo has four PR lists. We use two of them; both are kept in [`benchmark/`](benchmark/):

| list | PRs | what it is | here |
|---|---|---|---|
| `rq_full.json` | 145 | the benchmark (RQ1) | `full` |
| `rq_ablation.json` | 30, 10 per project, all in `full` | what the ablation study ran on (RQ3) | `ablation`, **the list we run** |
| `pr-test-reviews/reviews/004/` | 27; 4 of its SciPy PRs are not in `full` | tests reviewed by hand (RQ2) | not used |
| `scipy_example.json` | 10 SciPy, not in `full` | the README demo | not used |

Every command takes a list name in place of ids (`prepare chaco ablation`,
`run_exp.py --only ablation`), and each row records its lists in `chaco_lists`.

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
- `broken-env`: the developer's tests collect nothing in the image, or pytest did not
  finish (a crash or timeout). A run without pytest's closing summary line is never read
  as a result.
- `oracle-mismatch`: the derived flip is not reproduced by `verify()`.
- `no-developer-test`: the PR adds or changes no test. FAIL_TO_PASS cannot be derived, and
  both the developer column of mutation and the judge need a developer test, so these
  rows are not built or run. 9 of the 30 ablation PRs are in this state.
- `unsupported`: no Python source change, not merged, or a Qiskit Rust change, which the
  editable install does not rebuild.

Two SWE-bench fields are filled in at prepare and validate time:
- `hints_text`: comments on the closed issues that were posted before the PR was opened.
- `version`: the installed package's major.minor.

Two cannot be filled: `difficulty` and the "Verified" human screening are judgements
specific to SWE-bench Verified.

## Checking a PR by hand

`python -m openhands_f2p.sources review chaco ablation` writes [`review/`](review/). It has
one page per PR, linking to the PR, the base and merge commits, the closed issues and the
Dockerfile. Each page shows FAIL_TO_PASS, PASS_TO_PASS, the problem statement, the hints,
`patch` and `test_patch` in full, so every derived field can be checked against GitHub.
The pages are generated from `instances.json` and are never edited by hand.

## Per-project images

These are adapted from ChaCo's own Dockerfiles; `chaco.RECIPES` holds the recipes.

| project | Python | notes |
|---|---|---|
| pandas | 3.11 | meson-python editable (C extensions rebuilt on import, offline); X/GL libraries for `pytest-qt` |
| SciPy | 3.12 | meson-python editable, gfortran + OpenBLAS, submodules |

Every image sets `OPENBLAS_CORETYPE=Haswell`. On the server's QEMU virtual CPU, OpenBLAS
autodetects a kernel that uses an instruction the CPU lacks. SciPy's `test_lapack.py` died
with "Illegal instruction" after 8 of its 1927 tests until the core type was pinned.
| Qiskit | 3.11 | Rust (rustup stable) via setuptools-rust; `pytest` added (Qiskit itself uses stestr) |

Build times on the server (16 cores) are 5–7 min per image. Archived images are 0.5–1.5 GB.

## Status

`python -m openhands_f2p.sources info chaco` prints the status of every row, and
[`review/README.md`](review/README.md) is the table for the ablation list. Preparing needs
a `GITHUB_TOKEN`, because the unauthenticated GitHub API allows 60 calls an hour and a PR
takes 2–4.

## Runs

| run | PR | verdict | changed-line coverage | mutants (agent / developer) | actions |
|---|---|---|---|---|---|
| [`chaco-outs/base`](../../chaco-outs/base/RUNS.md), 2026-10-08 | pandas-dev/pandas#60505 | YES | 100% (4/4) | 2/2 / 1/2 | 39 |

The configuration matches the out-v2 base run: qwen3-coder-30b, temperature 0.3, a cap
of 125 actions, all add-ons, 20 mutants, and no judge.
