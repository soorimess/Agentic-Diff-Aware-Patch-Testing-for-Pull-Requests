# An agent that writes fail-to-pass tests

An OpenHands agent writes a regression test for a merged SWE-bench Verified pull request.
The test has to **fail at the base commit and pass once the fix is applied**. The
maintainer's own test for the same bug is held out: it is read once, at the end, to judge
the result, and never during generation.

The agent runs **on the host**; only its effects reach the container, each as a
`docker exec`. That is what makes `--network none` possible — see
[docs/system-design.md](docs/system-design.md) for the architecture, the diagrams and the
decisions behind them.

- **Results, per pull request:** [out/RUNS.md](out/RUNS.md)
- **Design:** [docs/system-design.md](docs/system-design.md)
- **Prompt design:** [openhands-f2p/src/openhands_f2p/prompts/README.md](openhands-f2p/src/openhands_f2p/prompts/README.md)

## Setup

Docker must be running, and the images are amd64 only — on Apple silicon they run under
emulation. Each is 1–5 GB, pulled once and cached.

```bash
cd openhands-f2p
uv sync
cp ../.env.example ../.env      # then fill in
```

The SWE-bench Verified rows are a download, not a source file, so they are not in the
repository. Put the dump at `data/swebench_verified.json` in the repository root or point `F2P_DATASET` at a copy
you have; `openhands_f2p/dataset.py` prints the fetch command if it cannot find one.

| var | note |
|---|---|
| `LLM_API_KEY` | falls back to `OPENAI_API_KEY` |
| `LLM_BASE_URL` | falls back to `OPENAI_BASE_URL` |
| `LLM_MODEL` | prefix with `litellm_proxy/` behind a LiteLLM gateway, or litellm strips the provider and the gateway 400s |
| `LLM_PROXY` | set if the endpoint needs an HTTP proxy. Given to litellm as an explicit client, so it never enters the environment the container inherits |
| `LLM_API_MODE` | `chat`. `auto` picks the Responses API for gpt-5-mini, which hangs against some gateways |
| `LLM_TIMEOUT` | seconds; litellm's own default of 300 is too low once test logs are in context |
| `LLM_MAX_OUTPUT_TOKENS` | reasoning models spend this before emitting anything; too low returns empty content |
| `LLM_NUM_RETRIES`, `LLM_RETRY_MAX_WAIT` | how long to wait out a rate-limited gateway |
| `LLM_JUDGE_MODEL`, `LLM_JUDGE_TIMEOUT` | the final comparison, deliberately a stronger model than the agent's |
| `F2P_MAX_PARALLEL` | PRs at once, default 5. Higher is not better: 30 exceeded the Docker VM's disk and rate-limited the gateway into failing four instances |
| `F2P_DATASET` | path to the SWE-bench Verified dump |
| `F2P_PROMPT_SKIP` | comma-separated prompt pieces to omit, e.g. `check-flips` |

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
| `--blind` | withhold the diff. Harder task; drops the `verify` and `coverage` tools with it |
| `--compare-coverage` | each PR twice, with and without the coverage tool, into `out_compare_coverage/` |
| `--no-compare` | skip the final judgement against the maintainer's test |
| `--max-iterations N` | cap on agent steps, default 100. Highest observed use: 62 |

The instances are in `src/openhands_f2p/prs.py`: 26 across 12 repositories, five django
versions from 3.0 to 5.0, and for every other repository one old and one recent — the
oldest is `psf/requests` at 1.1, from 2013.

## Read what happened

```bash
uv run python -m openhands_f2p.trace 3            # the flow, summarised
uv run python -m openhands_f2p.trace 3 --tools    # tool calls only
uv run python -m openhands_f2p.trace 3 --full     # nothing truncated
uv run python -m openhands_f2p.trace 3 --llm 2    # the raw 2nd LLM exchange
```

`out/<id>/flow.log` is the same run as aligned text, top to bottom. For the visual
timeline, upload `out/<id>/trajectory.json` at
[trajectory-visualizer.vercel.app](https://trajectory-visualizer.vercel.app/).

[out/RUNS.md](out/RUNS.md) is the index: one row per pull request with its verdict,
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
docker images | grep sweb            # ~3 GB per instance, evicted automatically
rm -rf .cache                        # SDK workspaces and event log, never read
uv run python -m openhands_f2p.docs --check    # is the design doc current
```

## Known limits

- **One run per instance.** Same-instance variance is visible at n=1 — sympy took 3
  actions on one run and 4 on another. Action counts are a range, not a measurement.
- **Four instances have no verdict.** The gateway key reached its budget mid-run;
  a pre-flight check now says so in 0.3 s instead of letting each instance wait twenty
  minutes and fail having written nothing.
- **The coverage A/B has not been run.** `--compare-coverage` works, but 26 PRs twice
  needs the budget for it.
- **Isolation rests on discipline, not a process boundary.** The host has a network. The
  guarantee is that every executor takes `box` and has no other exit; a fourth tool
  written carelessly would undo it.
- **Memorisation is not addressed.** `psf/requests` is among the most-copied Python
  repositories on the internet. That can be disclosed, not closed.
