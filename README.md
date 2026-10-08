# An agent that writes fail-to-pass tests

An OpenHands agent writes a regression test for a merged SWE-bench Verified pull request.
The test has to **fail at the base commit and pass once the fix is applied**. The
maintainer's own test for the same bug is held out: it is read once, at the end, to judge
the result, and never during generation.

The agent runs **on the host**; only its effects reach the container, each as a
`docker exec`. That is what makes `--network none` possible — see
[docs/system-design.md](docs/system-design.md) for the architecture, the diagrams and the
decisions behind them.

- **Results, per pull request:** [swe-bench-outs/out/out_full_run/RUNS.md](swe-bench-outs/out/out_full_run/RUNS.md)
- **Held-out evaluation, four models:** [swe-bench-outs/evaluation/RUNS.md](swe-bench-outs/evaluation/RUNS.md)
- **Design:** [docs/system-design.md](docs/system-design.md)
- **Why it is built that way:** [docs/decisions.md](docs/decisions.md) — the measurements, the bugs and the dead ends
- **What to measure next:** [docs/experiments.md](docs/experiments.md) — queued experiments, with costs and wall clock
- **Prompt design:** [openhands-f2p/src/openhands_f2p/prompts/README.md](openhands-f2p/src/openhands_f2p/prompts/README.md)

The twenty-six instances in `out/out_full_run/` are the ones every prompt here was written
while looking at. The ten in `swe-bench-outs/evaluation/` are not: one per repository, drawn by seed, run
through the same code with nothing special-cased. `gpt-5-mini` passes **10/10** of them,
which is the only evidence in this repository that the system works on instances nobody
tuned it against.

## Setup

Docker must be running, and the images are amd64 only — on Apple silicon they run under
emulation. Each is 1–5 GB, pulled once and cached.

```bash
cd openhands-f2p
uv sync
cp ../.env.example ../.env      # then fill in
```

**On Apple silicon, the interpreter must be native arm64.** `mutmut` 3 needs `libcst`,
which publishes a macOS wheel for `arm64` only — an x86_64 Python under Rosetta finds no
wheel, falls back to building from source, and needs a Rust toolchain to do it. `uv python
list` shows the architecture; `uv venv --python cpython-3.12-macos-aarch64-none` pins a
native one for this project without committing a platform into `.python-version`. The
images themselves stay amd64 and keep running under emulation either way — this is about
the harness, not the container.

The SWE-bench Verified rows are a download, not a source file, so they are not in the
repository. Put the dump at `data/swebench_verified.json` in the repository root or point `F2P_DATASET` at a copy
you have; `openhands_f2p/dataset.py` prints the fetch command if it cannot find one.

| var | note |
|---|---|
| `LLM_API_KEY` | falls back to `OPENAI_API_KEY` |
| `LLM_BASE_URL` | falls back to `OPENAI_BASE_URL` |
| `LLM_PROXY` | set if the endpoint needs an HTTP proxy. Given to litellm as an explicit client, so it never enters the environment the container inherits |
| `FALLBACK_LLM_*` | **fallbacks, not overrides.** `MODEL`, `API_MODE`, `TIMEOUT`, `MAX_OUTPUT_TOKENS`, `NUM_RETRIES`, `RETRY_MAX_WAIT`, `JUDGE_MODEL`, `JUDGE_TIMEOUT`. Each is consulted only where `models.json` says nothing — see below |
| `F2P_MODELS_FILE` | a model registry somewhere other than `models.json` at the project root |
| `F2P_MAX_PARALLEL` | PRs at once, default 5. Higher is not better: 30 exceeded the Docker VM's disk and rate-limited the gateway into failing four instances |
| `F2P_DATASET` | path to the SWE-bench Verified dump |
| `F2P_PRS_FILE` | a JSON list of instances to run instead of the twenty-six built in, e.g. `swe-bench-outs/evaluation/prs.json`. Same shape; nothing is special-cased for it |
| `F2P_IMAGE_CACHE` | where image archives are kept, default `image-cache/`. The evaluation set uses `image-cache-evaluation/` |
| `F2P_PROMPT_SKIP` | comma-separated prompt pieces to omit, e.g. `check-flips` |

To run the held-out set rather than the twenty-six:

```bash
F2P_PRS_FILE=swe-bench-outs/evaluation/prs.json F2P_IMAGE_CACHE=image-cache-evaluation \
  uv run python -m openhands_f2p.agent all --model gpt-5-mini \
  --out-root swe-bench-outs/evaluation/out_gpt5mini --mutants 10 --parallel 10
```

Results are kept per dataset. Everything run on SWE-bench is under `swe-bench-outs/`
(`out/`, `out-v2/`, `experiments*/`, `evaluation/`), and ChaCo's runs are under
`chaco-outs/` (see [datasets/README.md](datasets/README.md)). `swe-bench-outs/out/` holds
one folder per run, e.g. `out/out_full_run/` and `out/out_compare_repo_search/`, plus
`out/default/` for a run given no `--out-root`. Evaluation runs live apart, under
`swe-bench-outs/evaluation/`.

### Which model answers

`--model gpt-5-mini`, `--judge-model gpt-5.5`, `--provider anthropic`. The name is matched
against the profile registry in **`models.json`** at the project root, which supplies the
API mode, token ceiling, timeout and retry policy that model needs, and which credentials
to look for. `python -m openhands_f2p.models` prints the table.

Adding a model or a gateway is an edit to that file -- no Python, no reinstall, and
`F2P_MODELS_FILE` points at a different one so a machine can carry its own:

```json
{ "match": "claude-*", "provider": "anthropic", "max_output_tokens": 32000,
  "note": "why these values -- this is the only place the reason survives" }
```

Profiles match by glob against the bare model id, first match wins, so exact names go
above their wildcards and a `"*"` entry stays last. Unknown fields are refused by name
rather than ignored, which is the check a JSON file would otherwise lack.

**Precedence is CLI flag, then `models.json`, then `FALLBACK_LLM_*`, then the built-in
defaults.** The registry sits above the environment on purpose. A variable is *global* and
a profile is *per-model*, so while the variable won, `LLM_TIMEOUT=600` in a `.env` silently
overrode the 900 that `gpt-5.5`'s profile asks for — and no profile could be trusted to
mean anything. The `FALLBACK_` prefix is the rename that makes that visible in `.env`
itself. Nothing about a model is read from the environment first any more; the flags and
the registry are the two places to look.

A profile field left out is `None`, and that is what makes a fallback reachable at all: a
field with a real default can never fall through to one. So an entry says only what it has
a reason to say, and `python -m openhands_f2p.models` stars the values that came from the
file to keep the difference visible.

One profile records a gateway bug rather than a preference: through the LiteLLM gateway
`gpt-5.5` answers with a text preamble in `choices[0]` and the tool call in `choices[1]`,
and the SDK reads the first, so the run recorded zero actions. `picks_first_choice: false`
routes it through `MultiChoiceLLM`, which reorders the choices — a wrapper around the
SDK's `LLM`, because no value could have expressed it. With that in place `gpt-5.5` runs
as the agent.

All commands below run from `openhands-f2p/`.

## Check the instrument first

```bash
uv run python -m openhands_f2p.oracle                  # every instance
uv run python -m openhands_f2p.oracle django           # one repository
uv run python -m openhands_f2p.oracle sympy__sympy-24562
```

Feeds the **maintainer's own test** through the same verifier the agent's test goes
through. That test is fail-to-pass by construction, so anything but `ORACLE : OK` is a bug
in this harness, not a result about a model. It also runs a `PASS_TO_PASS` gate and checks
isolation (`dns=False`, `git_present=False`).

This matters more than it sounds. On the first full pass over all 26 instances, eleven
distinct harness bugs each produced a plausible *number* rather than an error — six false
`NO` verdicts and five `BROKEN`. Re-judging the same saved tests turned all of them into
`YES`.

## Run the agent

```bash
uv run openhands-f2p                         # all 26
uv run openhands-f2p django                  # one repository
uv run openhands-f2p django__django-17029    # one instance
uv run openhands-f2p old                     # oldest version of each repository
uv run openhands-f2p 1,7,12                  # or a comma-separated selection
uv run openhands-f2p --parallel 5
uv run openhands-f2p 4 --dry-run             # target path and runner, no LLM call
```

`uv run python -m openhands_f2p.agent …` is the same thing; from the repository
root, `openhands-f2p/.venv/bin/python main.py 3` also works.

| flag | what it is for |
|---|---|
| `--parallel N` | N PRs at once, as separate processes |
| `--recheck` | re-judge the saved tests under the current harness, with **no model call** — how a harness fix is verified against the whole set for free |
| `--retry-broken` | rerun only the instances with no usable result |
| `--mutants N` | after the verdict, generate N mutants of the patch with `mutmut` and report how many the agent's test kills and how many the maintainer's does, on the same set |
| `--no-compare` | skip the final judgement against the maintainer's test |
| `--out-root DIR` | write results here instead of `swe-bench-outs/out/default/` (`chaco-outs/default/` for ChaCo). Each run gets its own folder |
| `--label NAME` | a name for this run, recorded in every result |
| `--max-iterations N` | cap on agent steps, default 100. One instance has reached it: `sphinx-7454` spent 91 of its 100 steps in `run`, searching rather than looping |

The configuration flags are listed in the next section.

The instances are in `src/openhands_f2p/prs.py`: 26 across 12 repositories, five django
versions from 3.0 to 5.0, and for every other repository one old and one recent — the
oldest is `psf/requests` at 1.1, from 2013.

## Choose what the agent has

Two kinds of flag (since 2026-09-28). What the agent is **shown** is on unless withheld;
what is **added** to a bare agent is off unless asked for. With no flags at all the agent
is shown the report, the diff and the briefing, holds `run`, `write_file` and `run_tests`,
and its first stop is final.

| shown -- on unless withheld | added -- off unless asked for |
|---|---|
| `--no-issue` the bug report | `--add-verify-tool` the `verify` tool |
| `--no-patch` the pull request diff | `--add-coverage-tool` the `coverage` tool (needs verify-tool, patch) |
| `--no-repo-facts` (`--repo-search`) the briefing on how this project tests | `--add-mutation-tool` the `mutation` tool (needs verify-tool, patch) |
| | `--add-guard` edits to pre-existing files reverted between actions |
| | `--add-require-tools` three loops: `verify` until the test is fail-to-pass, then `coverage` until no changed line is missed and `mutation` until no variant survives, each ending early when an honest attempt stops improving it (needs verify-tool) |
| | `--add-require-tools-with-score-report` the same loops with the scores shown: coverage to 100%, mutation score maximised (implies `--add-require-tools`) |
| | `--add-second-chance` a restart: a run that ended without a YES starts again with its first attempt's record and the rest of its budget |

An add-on whose need is missing is refused with the flag that fixes it, never quietly
dropped. The harness measures the same things in every configuration, so runs made with
different flags are comparable:

```bash
FULL="--add-verify-tool --add-coverage-tool --add-mutation-tool --add-guard --add-require-tools --add-second-chance"
uv run openhands-f2p $FULL                              # everything: the reference configuration
uv run openhands-f2p ${FULL/--add-coverage-tool /}      # the tool goes; the measurement stays
uv run openhands-f2p $FULL --no-patch                   # refused: coverage and mutation need the diff
uv run openhands-f2p --no-issue                         # only the diff says what the bug is
uv run openhands-f2p $FULL --repo-search                # no briefing; the agent works the repo out
```

`--repo-search` is the same switch as `--no-repo-facts`, spelled for what the run is for.
It withholds the briefing on how the project tests — the target convention, where a test
file has to live to be collected, the neighbouring tests, the configuration — and the
agent establishes them itself with `run`. The destination becomes the agent's: the harness
names the filename, the agent picks the directory, and `test_path` and
`test_path_default` are both recorded so a test in a directory the runner never collects
from can be told apart from a weak test.

Measured on 24 instances against `full`: **24/24 fail-to-pass either way**, mean coverage
95.0% against 97.1%, mutation 75/100 against 76/100 on identical mutant sets. Eleven of
the 24 chose a different directory from the harness heuristic, every one of them beside
the code under test, and all passed. It costs about 11% more.

`--no-issue --no-patch` is refused rather than run: with neither, nothing tells the agent
which bug to write a test for, and the run would still produce a verdict.

**An input and a tool are separate switches even when they are about the same thing.**
`--no-patch` withholds the diff from the *prompt*; the harness still holds it, applies it
and reverts it, so `verify` keeps working and reports whether the agent's test flips
without quoting a line of the diff. These were one switch at first, and that was wrong
twice over: it was not technically necessary, and it confounded the very comparison the
flags exist for &mdash; if withholding the diff also withheld the feedback loop, a drop in
the result could not be attributed to either.

What genuinely cannot be separated is `coverage`: it prints the source of the lines a test
missed, which *is* the diff. So it needs `patch`, and `--add-coverage-tool --no-patch` is
refused: "--add-coverage-tool needs patch: drop --no-patch".

**To compare configurations, give each its own directory and compare the series:**

```bash
uv run openhands-f2p --out-root out_full  $FULL
uv run openhands-f2p --out-root out_nocov ${FULL/--add-coverage-tool /}
```

Each `result.json` records `features.config`, and `RUNS.md` says which configuration its
rows came from &mdash; and warns when they came from more than one.

Adding a switch is one entry in `FEATURES` in `openhands_f2p/features.py`. That gets it a
flag, a line in `--help`, dependency handling, a place in every recorded result, and the
ability to gate a prompt piece. The prompt adapts two ways: `needs:` in a piece's header
drops the whole piece, and `{?feature} ... {/feature}` inside a body drops a paragraph
&mdash; because most instructions are not all-or-nothing. Withholding the diff should not
delete the goal, only the clause telling the agent to work out what the code will do
*after* the change.

That the finished prompt never mentions a tool the agent does not have is checked, not
hoped for: `prompt.build` scans the assembled text for the names of tools that were not
registered and raises, naming the piece to fix. Ask for the assembled prompt in any
configuration:

```bash
uv run python -m openhands_f2p.prompt --explain --no-patch        # which pieces, and why
uv run python -m openhands_f2p.prompt --add-verify-tool --add-coverage-tool   # the text itself
```

## Would the test notice a wrong fix?

```bash
uv run openhands-f2p 3 --mutants 5
```

`mutmut` generates five mutants — single edits to the *fixed* code, confined to the lines
the pull request changed and spread across them rather than clustered on one expression.
Each is applied in turn and the test is run against it. A mutant the test fails on is
killed; one it still passes is a survivor, and each survivor names a behaviour the test
does not pin down.

Deterministic, and no model call: two runs of the same instance produce byte-identical
mutants, so a score only moves when the test moves.

**Both columns, raw.** Every mutant is run against the maintainer's test as well, and both
numbers are reported side by side rather than one being filtered by the other. Across 24
instances and 100 mutants the agent's tests killed 75 and the maintainer's 79 — close, with
real spread underneath: `sphinx-7454` scored 10/10 against the maintainer's 9, `flask-5014`
killed 1 of 4. The maintainer's column doubles as a control, since it is the same mutant
set in every run.

Six of 23 instances produced **no mutants at all** — `mutmut` works on expressions, and a
patch that only adds a statement or a framework declaration offers nothing to change. That
reports as `0/0`, not as a perfect score. A statement-deletion operator would cover most of
them and is deferred.

### The agent can ask the same question

`mutation` is also a tool the agent holds, alongside `verify` and `coverage`: it breaks
the fix in small ways, runs the agent's test against each, and reports the ones it does
not notice. It is there only with `--add-mutation-tool`; without it nothing in the prompt
mentions it.

Giving the agent the tool would ordinarily destroy the measurement — an agent that tunes
its test until those ten mutants die, scored on those ten mutants, is being marked on its
own revision. So when the tool is registered the pool is **split**: the agent is shown one
half, the harness scores the other, and results record `held_out: true`. The halves are
drawn alternately *within* each changed line rather than across lines, because splitting
`_spread`'s output divides the pool by line — the first attempt gave the maintainer's own
test 0 of 5, its half being entirely on a line that test never exercises.

The tool changes tests, but rarely, and the reason is worth knowing before expecting more:
across 90 mutants in 23 instances there is exactly **one** survivor the maintainer's test
kills and the agent's does not. Almost every survivor is one *neither* test kills — an
equivalent mutant — and the prompt tells the agent to leave those alone. On most instances
the honest answer is that there is nothing to fix.

Each mutant is saved to `out/<run>/<instance>/mutations/NN-<name>.diff`, so a survivor can be
read rather than taken on trust.

Runs after the verdict and only for a `YES`, in the same position as the judge, since it
reads the held-out test. The agent is never told it exists.

## Read what happened

```bash
uv run python -m openhands_f2p.trace 3            # the flow, summarised
uv run python -m openhands_f2p.trace 3 --tools    # tool calls only
uv run python -m openhands_f2p.trace 3 --full     # nothing truncated
uv run python -m openhands_f2p.trace 3 --llm 2    # the raw 2nd LLM exchange
```

`out/<run>/<id>/flow.log` is the same run as aligned text, top to bottom. For the visual
timeline, upload `out/<run>/<id>/trajectory.json` at
[trajectory-visualizer.vercel.app](https://trajectory-visualizer.vercel.app/).

[swe-bench-outs/out/out_full_run/RUNS.md](swe-bench-outs/out/out_full_run/RUNS.md) is the index: one row per pull request with its verdict,
coverage, and when it last ran. It is regenerated from the results on disk at the end of
every run, so it cannot drift.

## Inspect the prompt

```bash
uv run python -m openhands_f2p.prompt --explain  # what each piece is for
uv run python -m openhands_f2p.prompt django     # the assembled prompt
```

One file per instruction in `src/openhands_f2p/prompts/`, so a result that moves can be
attributed to the instruction that moved it, and a piece can be dropped for one arm and
kept for another:

```bash
F2P_PROMPT_SKIP=check-flips,check-reaches uv run openhands-f2p 3
```

The `5x` check files are the ones to drop first when comparing against a pipeline: they
hand the agent a workflow it might not have found alone, so leaving them in means part of
what looks like agency was instruction.

## Housekeeping

```bash
docker ps -a --filter name=f2p-      # removed on exit; none should linger
rm -rf .cache                        # SDK workspaces and event log, never read
uv run python -m openhands_f2p.docs --check    # is the design doc current
```

### Images are pulled once, ever

The registry link here has been measured at **0.3 MB/s** — about three hours for one
3-4 GB image, and two runs have already died mid-pull. So every image is kept as a
gzipped `docker save` on the host and loaded from there instead:

```bash
uv run python -m openhands_f2p.image_cache list           # what is stored
uv run python -m openhands_f2p.image_cache archive-all    # archive what Docker holds
uv run python -m openhands_f2p.image_cache load <id>      # one, by hand
```

Nothing is automatic about the pull path: it checks Docker, then the archive, then the
registry — and archives whatever it had to pull, while it still holds the pull lock.
Measured on `requests-1142`: 2.67 GB in Docker, **1.1 GB** archived, 52 s to write,
**26 s to load**. Sixteen images are 19.7 GB on disk against ~36 GB in Docker.

The archive is the durable copy, so Docker's is dropped when a run finishes with it —
otherwise the space is spent twice. Two rules make that safe: nothing is deleted before
its archive has been read back and verified (`gzip -t` plus a `manifest.json` check), and
an image another worker has claimed is never touched. `F2P_KEEP_IMAGES=1` keeps Docker's
copy, which is what you want while iterating on one instance. `F2P_IMAGE_CACHE` moves the
directory.

## Known limits

- **One run per instance.** Same-instance variance is visible at n=1 — sympy took 3
  actions on one run and 4 on another. Action counts are a range, not a measurement.
- **Two instances have no verdict.** Both are infrastructure, not results:
  `matplotlib-26208` lost the Docker socket 76 minutes into its image pull when Docker
  Desktop restarted, and `scikit-learn-25747` was still downloading at 0.3 MB/s when the
  run was stopped. Neither started an agent. `out/<run>/<id>/result.json` says so, and
  `--retry-broken` picks up exactly these.
- **No configuration has been compared against another yet.** The switches to do it
  exist and every result records which were in force, but the runs cost what they cost,
  so every number here comes from the full configuration.
- **Isolation rests on discipline, not a process boundary.** The host has a network. The
  guarantee is that every executor takes `box` and has no other exit; a sixth tool
  written carelessly would undo it.
- **Memorisation is not addressed.** `psf/requests` is among the most-copied Python
  repositories on the internet. That can be disclosed, not closed.
