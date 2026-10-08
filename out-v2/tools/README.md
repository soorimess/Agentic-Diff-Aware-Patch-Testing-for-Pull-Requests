# Analysis helpers for out-v2

Run from `openhands-f2p/` with `F2P_PRS_FILE=../evaluation/local-36-prs.json uv run python ../out-v2/tools/<script> ...`
(the replay scripts import the harness); the plain ones run with `python3` anywhere (server copies live in `/root/`).

| script | what it does |
|---|---|
| `replay_stop_checks.py <folder>` | replays `verify_gap`/`duty_gap` of the *current* code at every recorded refusal and conversation end; prints runs whose decision or refusal text would differ -- decides which runs a code change forces to rerun |
| `replay_gates.py <folder>` | same idea for the mutation gate and verify's headline (flipped + backwards) |
| `progress.py <exp>` | live phase counts and verdicts of a running experiment (server paths) |
| `table.py <exp>` | one line per run: verdict, actions, coverage, mutants, tool counts, refusals, restart, f2p_history |
| `nos.py <exp>` | the NO runs with their refusal reasons and restart |
| `trace_loop.py <run dir>` | a run's writes (sha), verify/coverage/mutation results and refusals in order |
| `randtable.py` | the six astropy-13398 randomness runs side by side |
| `pick_extremes.py` | best base against worst arms (user, 2026-10-06): per PR the best/worst run of the same system and config, linked into `out-v2/extreme-*/` with `PICKED.md`; RUNS.md and compare reports then say "picked runs" up top |
| `dashboard_data.py [folder]` | one JSON document per experiment for the comparison page: writes `out-v2/dashboard/<folder>.json`; upload with `ArtifactData` `set` (collection `experiments`, doc id = folder, `file_path`). The page computes every comparison itself |
| `replay_texts.py <folder>...` | which runs saw tool text a later fix changes (astropy header, child-process note, backwards, pytester ids, directory filter, phantom ids) |
| `baseline_probe.py` | coverage of an EMPTY test per PR (the environment-baseline probe, no model calls) |

`out-v2/audit_outage.py <folder>` (gateway damage) and `out-v2/compare.py <a> <b>` (comparison report) sit one level up.
