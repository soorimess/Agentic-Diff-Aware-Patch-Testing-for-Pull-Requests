# Datasets

The harness runs on instances from more than one dataset. Each dataset has an adapter in
[`openhands-f2p/src/openhands_f2p/sources/`](../openhands-f2p/src/openhands_f2p/sources/).
The adapter turns that dataset into the **standard row** the harness reads, and says how
each instance's Docker image is obtained. Nothing downstream changes per dataset: the
agent, `verify`, the coverage metric, mutation and the oracle all read the same row.

| dataset | instances | rows | images |
|---|---|---|---|
| `swebench` | SWE-bench Verified, 500 (we run 36) | `data/swebench_verified.json` (a download, git-ignored) | pulled from Docker Hub (`swebench/sweb.eval.*`) |
| `chaco` | ChaCo benchmark (ICSE 2026), 145 PRs of SciPy, Qiskit, pandas | [`chaco/instances.json`](chaco/instances.json), made here | built here (`f2p-chaco/*`), from [`chaco/dockerfiles/`](chaco/dockerfiles/) |

```bash
cd openhands-f2p
uv run python -m openhands_f2p.sources list                 # every dataset, what is prepared
uv run python -m openhands_f2p.sources info chaco           # per-instance status
uv run python -m openhands_f2p.sources prepare chaco <ids|all>   # rows + Dockerfiles, no Docker
uv run python -m openhands_f2p.sources build chaco <ids>         # images
uv run python -m openhands_f2p.sources validate chaco <ids>      # FAIL_TO_PASS, oracle -> runnable
uv run python -m openhands_f2p.agent --dataset chaco <id> --model ...   # a run
uv run python ../swe-bench-outs/out-v2/run_exp.py --dataset chaco --only <ids> <name>  # -> chaco-outs/<name>/
```

A run always names its dataset. It is set by `--dataset` or by `F2P_DATASET_NAME`, and the
default is `swebench`. The run prints the dataset in its header, and every `result.json`
records it.

## The standard row

The SWE-bench Verified row, because the harness was built and audited on it:

| field | meaning |
|---|---|
| `instance_id` | `owner__repo-number` |
| `repo` | `owner/repo` |
| `base_commit` | the tree the agent works in, before the change |
| `patch` | the change without its tests (unified diff), applied by the harness for "after" |
| `test_patch` | the developer's tests for it, held out, read only to judge |
| `problem_statement` | the text the agent may be given (`--no-issue` withholds it) |
| `FAIL_TO_PASS` | JSON list: developer tests that fail at base and pass with `patch` |
| `PASS_TO_PASS` | JSON list: developer tests that pass on both sides (the environment gate) |
| `dataset`, `image`, `image_source` | which adapter made the row, its image, `pull` or `build` |

The image contract is also SWE-bench's:
- the checkout sits at `/testbed`, at `base_commit`;
- the project is installed so its tests run with `python` under `bash -lc`, as root;
- `git` and coreutils `timeout` are present;
- nothing needs a network once the container starts, since every run uses `--network none`.

## Adding a dataset

1. Write `sources/<name>.py` with an object that has `name`, `description`, `load(id)` and
   `prs()`, plus `image_for(id)`, `owns_image(image)` and `summary()`. If its images
   are built rather than pulled, it also needs `recipe(image) -> (id, Dockerfile path)`.
2. Register it in `sources/__init__.py` (`_registry`).
3. Make its rows satisfy `sources.REQUIRED_FIELDS`. Derive `FAIL_TO_PASS` by running
   the developer's tests on both sides, as `chaco.validate` does, rather than trusting
   a label.

The image builder ([`image_build.py`](../openhands-f2p/src/openhands_f2p/image_build.py))
is generic:
- `images.pull_image` hands it any image whose adapter has a recipe;
- builds run under their own slots (`F2P_BUILD_CONCURRENCY`, default 2);
- each build is logged to `.cache/builds/<image>/build.log`;
- every built image is archived to the image cache even under `F2P_NO_ARCHIVE`, because a rebuild takes tens of minutes, not the thirty seconds of a re-pull.

## ChaCo

See [chaco/README.md](chaco/README.md).
