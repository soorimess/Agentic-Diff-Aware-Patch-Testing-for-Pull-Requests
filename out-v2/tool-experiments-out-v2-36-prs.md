# Tool experiments — out-v2, 36 PRs

What each add-on of the F2P agent is worth, measured by taking it away from the full
system (`base`) one at a time (and in a few pairs), on the same 36 PRs.

The plan is iterative: run one experiment, analyse its trajectories for bugs, flaws and
logic problems in the harness or the agent's instructions, fix what is found, and rerun
what the fix touches before moving on. The order below is the order of work; `base` is
always rerun first when the system changes.

## Fixed for every experiment

| Setting | Value |
|---|---|
| Instances | the 36 in `evaluation/local-36-prs.json` (26 development, 10 evaluation) |
| Where | the server, `<repo>`, `--parallel 36` |
| Model | `openrouter/qwen/qwen3-coder-30b-a3b-instruct`, temperature 0.3 |
| Action cap | **125** per run (`--max-iterations`, up from 100 on 2026-10-04) |
| Inputs | issue, patch and repo facts shown in every experiment |
| Mutation | `--mutants 20`, scored on the held-out half |
| Judge | **off by default**. Added afterwards, on request, with `run_exp.py --judge <experiment>` |
| Results | `out-v2/<folder>/`, committed on the server and pulled to the laptop after each run |

## Largest possible effect (user, 2026-10-06)

Beside the fair one-sample comparison, each finished arm is also reported as base's *best*
run per PR against the arm's *worst*, picked from every run of the same system and
configuration (official folder and `rerun8-*`; the astropy randomness runs left the pool after the `252dd3aa` fixes):
`out-v2/extreme-base-best/`, `extreme-no-second-chance-worst/`, `extreme-no-require-tools-worst/`
(each with `PICKED.md`), reports in `out-v2/compare/extreme-*.md`, built by
`out-v2/tools/pick_extremes.py`. It shows the largest effect a flag can make, not the expected one.

## The add-ons

| Add-on | Flag | What it does |
|---|---|---|
| verify | `--add-verify-tool` | the `verify` tool: runs the test before and after the change |
| coverage | `--add-coverage-tool` | the `coverage` tool: which changed lines the test never runs (needs verify) |
| mutation | `--add-mutation-tool` | the `mutation` tool: wrong versions of the fix the test does not notice (needs verify) |
| guard | `--add-guard` | puts back edits to files that existed before the agent started |
| require tools | `--add-require-tools` | stop checks: the verify loop, then the coverage and mutation loops (needs verify) |
| require tools with score | `--add-require-tools-with-score-report` | the same loops with coverage and mutation scores shown as targets (implies require tools) |
| second chance | `--add-second-chance` | a restart with the first attempt's record when the run ends without a YES |

`base` has verify, coverage, mutation, guard, require tools and second chance.

## Experiments

| # | Experiment | Folder | Add-ons on | Status |
|---|---|---|---|---|
| 1 | base | `base` | verify, coverage, mutation, guard, require tools, second chance | done 2026-10-05 (system `fd63cdf4`; pylint-6903, pytest-10081 rerun at `0a15f5d8`, results `519aeaed`): **29/36 YES**, 2 rescued (27/36 first attempts), coverage mean 94.7% (after the 2026-10-06 reruns); batches + best-of-two in `base/REUSED.md` |
| 2 | base − second chance | `no-second-chance` | verify, coverage, mutation, guard, require tools | done 2026-10-05 (pylint-6903, pytest-10081 rerun at `0a15f5d8`, `519aeaed`): **27/36 YES**, coverage mean 93.2% (after the 2026-10-06 reruns); vs base: `compare/base-vs-no-second-chance.md` |
| 3 | base − require tools | `no-require-tools` | verify, coverage, mutation, guard, second chance | done 2026-10-05 (system `a5dabefe`; two PRs rerun at `0a15f5d8`, `519aeaed`): **29/36 YES**, 2 rescued (27/36 first attempts), coverage mean 91.9% (after the 2026-10-06 reruns); vs base: `compare/base-vs-no-require-tools.md` -- the verify loop converts almost nothing (base: 1 of 11 refused runs), the coverage/mutation loops do lift quality (without seaborn-3069: coverage 98.1% vs 86.5%, mutants 80.0% vs 66.2%) |
| 4 | base − second chance − require tools | `no-second-chance-no-require-tools` | verify, coverage, mutation, guard | done 2026-10-06 (`edfb126a`; 5 PRs rerun after the `252dd3aa` text fixes): **23/36 YES**, coverage mean 96.8%; vs base: `compare/base-vs-no-second-chance-no-require-tools.md` |
| 5 | base − guard | `no-guard` | verify, coverage, mutation, require tools, second chance | planned |
| 6 | base, require tools → require tools with score | `require-tools-with-score` | verify, coverage, mutation, guard, require tools with score, second chance | planned |
| 7 | base − verify | `no-verify` | guard, second chance (see below) | done 2026-10-06 (`b4908241`; 2 PRs rerun at `e0d6c1c8`): **25/36 YES** (20 first attempts, 5 after the restart); vs base: `compare/base-vs-no-verify.md` |
| 8 | base − coverage | `no-coverage` | verify, mutation, guard, require tools, second chance | done 2026-10-07 (`550f6ca6`): **28/36 YES**, coverage mean 90.5%; vs base: `compare/base-vs-no-coverage.md` -- quality falls without the tool (PRs YES in both, without astropy-13398: lines 98.1% vs 88.5%, mutants 80.0% vs 69.2%) |
| 9 | base − mutation | `no-mutation` | verify, coverage, guard, require tools, second chance | planned |
| 10 | base − coverage − mutation | `no-coverage-no-mutation` | verify, guard, require tools, second chance | planned |
| 11 | base − coverage − mutation − require tools | `no-coverage-no-mutation-no-require-tools` | verify, guard, second chance | planned |

### What "− verify" means

coverage, mutation and require tools each **need** verify, and the harness refuses a
configuration with a missing need. So "− verify" removes verify and everything that
depends on it, as the v1/v2 `no-verify-tool` arm did: #7 runs with guard and second chance
only. "− verify − require tools" would be the same run, so it is not in the plan (user,
2026-10-04).

## Commands

From `openhands-f2p/` on the server (each spec is `folder` or `folder=--flag,--flag`):

```bash
uv run python ../out-v2/run_exp.py base
uv run python ../out-v2/run_exp.py \
  no-second-chance=--add-verify-tool,--add-coverage-tool,--add-mutation-tool,--add-guard,--add-require-tools
uv run python ../out-v2/run_exp.py \
  no-require-tools=--add-verify-tool,--add-coverage-tool,--add-mutation-tool,--add-guard,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-second-chance-no-require-tools=--add-verify-tool,--add-coverage-tool,--add-mutation-tool,--add-guard
uv run python ../out-v2/run_exp.py \
  no-guard=--add-verify-tool,--add-coverage-tool,--add-mutation-tool,--add-require-tools,--add-second-chance
uv run python ../out-v2/run_exp.py \
  require-tools-with-score=--add-verify-tool,--add-coverage-tool,--add-mutation-tool,--add-guard,--add-require-tools,--add-require-tools-with-score-report,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-verify=--add-guard,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-coverage=--add-verify-tool,--add-mutation-tool,--add-guard,--add-require-tools,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-mutation=--add-verify-tool,--add-coverage-tool,--add-guard,--add-require-tools,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-coverage-no-mutation=--add-verify-tool,--add-guard,--add-require-tools,--add-second-chance
uv run python ../out-v2/run_exp.py \
  no-coverage-no-mutation-no-require-tools=--add-verify-tool,--add-guard,--add-second-chance

# the judge, afterwards, when asked for:
uv run python ../out-v2/run_exp.py --judge base no-coverage
```

`--retry-broken` reruns only runs that the model gateway or the machine cut off.
