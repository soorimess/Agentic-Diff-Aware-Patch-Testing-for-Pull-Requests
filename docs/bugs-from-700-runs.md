# What 700 runs showed was wrong with the harness

Read out of the ten-arm series (`experiments/`, 70 instances × 10 arms) after a rerun of
the base arm's failures recovered 11 of 28 on an unchanged configuration. The question
was whether that was variance or a defect. It was both, and the defects were found by
reading tool logs, completions and the generated tests themselves, not by counting
verdicts.

The logic that produced the ten arms is preserved on branch `final-state-of-first-runs`.
Everything below is fixed on `main` unless marked otherwise.

## Fixed

### The stop was refused once, and then never again

`conversation.run()` was called a single time after the refusal message. The agent was
told *"You cannot finish while this is the answer"*, edited the test, and called `finish`
again -- and that second stop went through, because `finish` is the SDK's own tool and
nothing guarded it.

| across runs with a verify tool (630) | |
|---|---:|
| ended on an edit never re-verified | 162 (25%) |
| of those, after the refusal had already fired | 144 |
| edited after a verify that said NOT fail-to-pass | 103 → 75 NO, 27 BROKEN, 1 YES |
| held verify + the tool duty and never called verify at all | 30, all refused once, all ignored it |

This is why the second chance converted so unevenly by reason:

| refusal reason | runs | converted |
|---|---:|---:|
| `loop_open` -- one more verify was enough | 146 | 46% |
| `collects_nothing` | 55 | 23% |
| `passes_at_base` -- needs several rewrite→verify rounds | 156 | 3% |

The agent did try: 94% of `passes_at_base` continuations rewrote the test, averaging two
writes and one verify, with a median of 6 actions spent of 68 offered. It was not refused
a second time. **Fix:** every stop is checked; up to five refusals, ending early when the
gap closes or the agent does nothing but stop twice running.

### django's runner collects only `TestCase` methods, and nobody said so

`runtests.py` is unittest discovery. A module-level `def test_x():` prints
`Ran 0 tests ... OK`, exits 0, and scores as nothing collected.

- 44 of the 50 "collected nothing" failures in the series were django; 31 of those files
  defined only bare functions.
- **127 of 127** successful django runs used a `TestCase` class. No bare-function django
  test ever passed.
- The briefing said "no `import pytest`, no fixtures", asked for "one test function per
  behaviour", and never mentioned `TestCase` or `unittest`. Its one style example for
  django was `tests/test_sqlite.py`, a settings module.

django is 27 of the 70 instances. **Fix:** `repo_facts` states the collection rule for any
labels runner (keyed on the runner kind, not the repository); style samples are files that
define a test; the goal says "one test per behaviour", in whatever form the runner collects.

### `verify`'s supporting lines contradicted its headline

The headline always applied the harness rule. Everything under it keyed on "did anything
flip": the duty line, the coverage pointer, the pointer to `mutation`, and the error flag.
`scikit-learn-14087` wrote three tests, two flipped and one still failed; it read
*"NOT fail-to-pass ... still fail after the change"* followed by *"That it flips, and what
it reaches, are two of the three questions"*, with no duty line, five times, and scored NO.
21 of 700 runs ended holding a correctly flipping test beside a failing one.

(An earlier summary of this said the tool reported "Fail-to-pass: 2 test(s)". It did not;
the headline was right and the lines beneath it were wrong.) **Fix:** one `ok` -- something
flipped and nothing still fails -- drives every line.

### A negative verdict arrived as a tool error

`is_error=not flipped`, so "your test passes at base" was delivered prefixed
`[An error occurred during execution.]`. When a refusal began there was a median of five
of these already in context. Success fell from 85% with none to 27% with six or more --
confounded, since a struggling run calls `verify` more, so no causal claim; but the framing
was wrong regardless. **Fix:** a verdict is never an error.

### Coverage was both the agent's target and the published metric

The tool ended *"100% is the target"*; `58-finish.md` said *"none of these figures is a
target"*. The percentage the agent was told to push up is the one the report publishes as
an independent quality measure, which makes arms with the tool and arms without it measure
different things. **Fix:** the agent is shown the lines it misses and asked for a test that
runs every changed line; no percentage, no target. The harness computes the figure outside.

### The trajectory hid every refusal

The refusal was sent to the model (it is in `completions/`) and logged in `flow.log`, but
`trajectory.json` was rebuilt from the opening task alone and showed one user message. This
is how the single-shot refusal stayed invisible through a whole series. **Fix:**
`injected_messages.json`, placed in the trajectory at the tool-log position it arrived.

### The guard statistic was mostly false positives

`files_edited_outside_test` compared raw path strings, so the agent's own test written as
`/testbed/tests/x.py` or `./tests/x.py` counted as a write outside the test. 296 of 700 runs
populated it. **Fix:** paths are normalised (`testbed/tests/x.py` without the slash is kept,
because it really does create a stray directory), and scratch files the agent created are
listed apart from edits to files that existed at base.

### A missing target file did not say what was written instead

`seaborn-3069` wrote `..._3269.py` -- one digit off -- and the record read *"wrote no test
at ..._3069.py"*. Correct, but it looked like the agent wrote nothing. (An earlier summary
called this a substantive NO; it was not.) **Fix:** the message names the test files it did
write.

## Found while testing the new system

A 26-instance run of the new system (`experiments-tests/new-system-26`) checked every fix
above against what the model actually received. All held. It surfaced two more:

- **django's summary line parsed as a test.** `FAILED (errors=1)` fits the pytest
  short-summary pattern, so the agent read `['test_x', '(errors=1)'] still fail after the
  change`. Verdict-neutral -- it only appears beside a real failure -- but misleading.
  Fixed: no test id starts with a parenthesis.
- **The judge's trailing comma.** `matplotlib-13989` came back complete (concept 5,
  issue 5) with `"reasoning": "...",` as its last line and was recorded as `unparsed`.
  Fixed: a trailing comma is tolerated, only after a strict parse fails.

And one behaviour, not a bug: under repeated refusal the model's policy is **write →
verify → finish** every round. It reads `verify`'s "NOT fail-to-pass ... you cannot
finish" and finishes anyway; the loop turns that into up to five attempts instead of one.
`django-13406` recovered this way (YES after five refusals); `django-11119` and
`pylint-4970` exhausted the cap still passing at base.

That behaviour led to three more rules on the refusal loop (see "Refusing a stop" in
`docs/system-design.md`):

- A `passes_at_base` refusal now says **which** mistake it is, measured the way the
  `coverage` tool measures it (only when the agent holds that tool): the test never runs
  the changed lines (move the input), or it runs them and still passes (keep the input,
  change the assertion). The old message could not tell these apart, and the agent
  rewrote blindly every round.
- `passes_at_base` is refused at most two rounds running; a test that already flips is
  reminded of an open coverage/mutation duty at most once. Replayed on the 26-PR run,
  these drop 25 of 55 rounds and lose none of its three conversions.

The live check (`experiments-tests/diag-smoke`) showed both diagnoses reaching the model
and the two-round stop firing. It also caught one gap: a test that never imports the
changed file leaves no entry in the coverage report, the metric calls that
*unmeasurable*, and the first refusal went out with no diagnosis at all -- the plainest
case of not reaching the change. The diagnosis now reads that reason as "runs none of
the changed lines". The published coverage metric is unchanged.

## Found in the temperature test (control-26, temp-0.3-26)

Reading both runs' trajectories and completions (details in
`experiments-tests/temperature-0.3.md`):

- **Tool names did not match the prompt** -- `sandbox_verify` to the model, `verify` in every
  message. Fixed: tools are named as the prompt names them.
- **Source-text tests pass the verdict.** Eight across all runs (six in the ten-arm series,
  none in the base arm). Fixed: the stop is refused, the prompt forbids it, results record
  `reads_source`.
- **`verify` hid a partly working test**, and **the refusal claimed "not changed since"
  after an edit**. Fixed.
- **The audit filed `/tmp/fix.patch` as a pre-existing file.** Fixed: asked of the base
  snapshot.
- **A deletion-only fix read "all comments or blanks".** Fixed: says the fix only removes
  code.
- Not changed: `think` called with `summary` instead of `thought` is rejected by the SDK
  (eight wasted actions in one run); and no reach diagnosis when coverage records nothing,
  since that can be a subprocess the tracer does not follow.

## Found in the source-check run

- **A failed `coverage` install did not stop the run.** Docker Desktop's proxy stopped
  answering; `pip install coverage` timed out three times (109 s each), flow.log said
  `FAILED after 3 attempts`, and the run went on with the `coverage` tool registered but
  unable to measure, no reach diagnosis, and no coverage figure. It had happened before
  unnoticed: four instances of `control-26` and one of `fix-smoke`. Fixed: the wheel is
  fetched on the host and copied in, the container never has a network, and any failure
  is fatal. (Server runs of the ten arms all recorded `coverage: ok`, 70 of 70 in base.)

## Found in the ten-arm check on five evaluation instances (eval5-arms)

Each arm was run on five instances the system was never tuned on, to check that a removed
feature is removed and nothing else changes. Batch 1 (base, −second-chance, −guard,
−require-tools) showed three places where it was not:

- **−second-chance got more refusals than base.** The two-rounds-running limit keyed on the
  reason `passes_at_base`, which only the flag produces. Without the flag the same state
  arrives as `loop_open` and ran to five rounds: 20 refusals against base's 4, none
  converting after the second. Fixed: those rounds count toward the same limit.
- **−guard was told the guard exists.** The rules said every edit to an existing file "is
  reverted" -- false in that arm, and a threat can deter without enforcement. Fixed: that
  sentence is gated on `guard`.
- **−require-tools was told the coverage duty is enforced** ("it is checked ... will be sent
  back"). Fixed: gated on `require-tools`.

Batch 2 (the three fixed arms rerun, plus −repo-facts):

- **−repo-facts was told two contradictory things.** Its exploration piece said "that one
  file is the only thing you may add"; the rules, in every arm, say fixture files may be
  created. And the rules and goal said "your test goes in `test_f2p_x.py`" -- in this arm
  a bare file name, since choosing the directory is the agent's job -- which reads as the
  repository root. Both failing −repo-facts runs that never collected had put the file
  there. Fixed: "in the directory you chose", and the exploration piece defers to the
  rules on creating files. Only this arm's prompt changes.
- **`collects_nothing` was refused five times running** with nothing changing. Now under
  the same two-rounds-running limit as `passes_at_base`.
- The source-text refusal fired live for the first time (−repo-facts django-13279:
  `inspect.getsource(SessionBase.encode)`); the agent rewrote it as a behaviour test and
  ended YES with full coverage.

Batch 3 (−repo-facts rerun, −coverage, −mutation, −cov −mut):

- **The −second-chance limit was wider than base's.** It counted any `loop_open` round whose
  own verify said "not fail-to-pass", which also takes in a test failing on both sides --
  a state base never caps, and one that converts (four recorded runs recovered after a
  third refusal). Narrowed to exactly what base caps: the agent's own last `verify` shows
  everything passing before the fix, or nothing collected.
- Checked and left alone: three −cov −mut runs never called `verify` although told to
  twice (v1's same arm: 64 of 70 did, so this is variance on five); the guard reverted two
  `sed` edits to library source and said so; a pytest test that drives pytest through a
  subprocess flipped with 0 changed lines covered, got the soft "if coverage cannot follow
  the path, say so" refusal once, and kept its YES.

Batch 4 (−verify, −cov −mut −duty, and base and −second-chance rerun on the final code)
found nothing to change: every arm registers exactly its tools, no refusal names a tool
the arm lacks, and the two refusal paths stop at the same point. Final five-instance
tally, one run each: base 2, −second-chance 2, −guard 2, −require-tools 2, −repo-facts 2,
−coverage 1, −mutation 3, −cov −mut 2, −verify 0, −cov −mut −duty 2 -- five instances
say nothing about the arms' effects; they were run to check that each removal is clean.

Both prompt leaks were also in the ten-arm series, so those arms remain comparable with each
other; the −guard and −require-tools arms there measured the enforcement, not the stated
rule. Base's prompt is byte-identical after the change. `prompt.py` gained inline blocks
(`...sentence.{?guard} Next sentence.{/guard}`), which keep or drop one sentence without
disturbing the paragraph around it.

## Found in experiments-v2's first pass (base and −second-chance, 140 runs)

The one fix round the v2 plan allows, after reading every trajectory of the first two arms.
The OpenRouter key ran out of credit about two-thirds of the way through, which is what
exposed the first two.

- **A run cut off by the gateway was scored as a finding.** 35 runs lost the model
  mid-conversation to `402 ... requires more credits` and were judged on whatever test was
  on disk -- 22 NO, 13 YES -- with the stop never checked. v1 had no agent errors at all,
  so this never showed. Fixed: an agent error from outside the run (402, 429, 5xx,
  connection, timeout, gateway budget) makes the verdict BROKEN, with what the partial
  test would have scored in the reason; `--retry-broken` reruns it. A context-window
  overflow is the run's own length and keeps its verdict, like the action cap.
- **The job pool did not recognise exhausted credit.** The gateway's own "Budget has been
  exceeded" stopped a run; OpenRouter's "requires more credits" did not, so every remaining
  job started and died. Both now stop it.
- **The refusal loop and the verdict scored different files.** With repo-facts on, the
  loop, like the agent's own `verify`, follows the test wherever it was written; the
  verdict read only the path the agent was given. django-14915 moved its test into
  `tests/forms_tests/tests/`, verified it fail-to-pass there, had its stop accepted on that
  file, and was scored "wrote no test". Fixed: the verdict scores the file the agent ended
  with, in every configuration (`test_path_default` keeps the named one). Two runs in about
  nine hundred were affected, one of them in v1 (−cov −mut django-15252).
- **One judgement in about fifty could not be read** -- django-14792: the judge left the
  `readability` object unclosed. Fixed: asked once more with the identical prompt, and an
  answer that still cannot be read is kept whole in `raw`.

Checked and correct: every run that ran five refusals was a test failing on both sides,
which is uncapped by design; no refusal message named a missing tool; no YES read source;
coverage, mutation and judge were recorded on every YES but one, whose developer test does
not pass on the fixed code.

## Found reading all 700 experiments-v2 runs

Every trajectory of the ten arms was read (five readers, two arms each, flagged cases
checked by hand). No crash, harness traceback, killed process or hung step in any run;
every run had its arm's tools, the model, temperature 0.3, a sealed network and
`coverage` installed; the refusal limits held everywhere; the guard never touched a test.

### Fixed: the django output parser dropped a test whose status came on a later line

`runners.parse_output` read a django result only as `name ... status` on one line. When a
test printed something in between -- argparse usage, a coroutine warning -- the test was
dropped. Three verdicts were wrong, and were re-scored offline from the saved logs by the
harness's own `verify._decide` (`experiments-v2/rescore.py`; the runs keep their old
verdict in `rescored_from`):

| run | recorded | re-scored |
|---|---|---|
| −coverage / django-16454 | YES | NO (a test still errors after the fix) |
| −cov −mut −duty / django-16454 | YES | NO (same) |
| −repo-facts / django-16136 | NO | YES (coverage, mutation, judge not measured: rescored offline) |

Checked over all 1,292 django logs in v1 and v2: every status-on-a-later-line case now
parses. No v1 verdict was affected.

### Fixed after the audit (2026-09-27; left in place for the v2 results)

These reached the agent during the v2 runs, so the v2 results stand with them in place;
the system as it ran is on branch `final-state-of-second-runs`. Every fix below was
checked offline against the saved v1 and v2 runs; none of it has run live yet.

**Verdict path**

- *A django test file that does not import counted as a failing test.* django reports a
  module it cannot import as one erroring test, `unittest.loader._FailedTest`; it is now
  dropped, so the file reads as collecting nothing, like pytest's collection error, and
  `--second-chance` refuses it as `collects_nothing`. Replayed: 3 v2 runs (−repo-facts
  django-14534, 16454, 16560) and 11 v1 runs move NO -> BROKEN; no YES changes.
- *The django parser in the agent's `verify` / `run_tests`.* Both call the same
  `parse_output`, so the v2 fix already covers them.
- *sympy tests that print showed "no tests ran" to the agent.* The status arrives alone
  on a later line, as in django; now read. 15 of the 29 such `run_tests` outputs in v2
  parse; the other 14 genuinely ran 0 tests.
- *A test skipped at base got no refusal* (no-cov+mut+require django-16560). New
  `skipped_at_base` reason, capped with `passes_at_base` / `collects_nothing`; `verify`
  and the verdict say "skipped" rather than "passes before the fix".
- *django tests sharing a docstring collapsed, subTest lines merged* (django-14765, 16667,
  13023, and v1 14792). Keyed on the test id with the docstring as an alias; a test left
  open by failing subTests takes its status from its traceback header.

**Refusal loop**

- *`loop_gap` trusted the last `verify` whatever file it ran on* (6 runs, 4 NO). All three
  instruments are now read on the scored file only, and a refusal names the file verified
  and the file scored. The `verify` tool notes when its target is not the scored file.
  Replayed over v2's final tool logs: the loop is now open at the end in 7 runs -- the 4
  side-file cases, 2 −repo-facts runs whose `mutation` only ever ran on a side file, and
  sphinx-7757, whose loop had looked closed only because a scratch file came after
  `coverage`.
- *`wrote_after` counted any `write_file`* (2 runs). Writes to the scored file only.
- *A corrupted library file under −guard kept drawing "call `verify`"* (sklearn-10297).
  The loop stops when the tree is off base; telling the agent to restore the file would be
  the guard the arm removes.
- *`reads_source` fired on a fixture write* (`open(path, 'w')`; sphinx-9591, 8459). A
  write, append or create mode exempts the line. The 19 final tests it flagged across both
  series are unchanged.

**Features not cleanly removed**

- *Without `coverage`, `verify` still reported whether every changed line ran* (the
  design note below). That sentence now goes out only with `coverage` registered.
- *"You cannot finish having read that" went out in arms without `coverage`*, where nothing
  enforced it. Gone with the sentence above.

**Reports**

- The mutation tool's own revert is no longer logged as "patch left applied by the agent".
- A held-out pool emptied because its one mutant went to the agent's half says so, instead
  of "mutmut offers no mutations".
- `guard` reverts are listed apart from the agent's tools in the refusal recap.
- A test written and then moved is `test_moved_from` in the audit, not a stray write.
- A `verify` call on a tree off base is in `tool_log` (with `error`).
- "Still failing after the fix" is no longer said of a test that passed before and fails
  after: it reads "backwards". A file that stops importing once the fix is applied reads
  "nothing collected after the fix".
- RUNS.md labels each refusal reason by its source: `no_test` and `skipped_at_base` are the
  second chance's, `reads_source` every configuration's, `runs_no_change` the coverage
  tool's.

**The second chance hands back the file and the run.** Under `--second-chance` a refusal
now carries the test file as it is on disk and what running it at base printed. This is
the "hand the agent its own failing test" item below, done within the same conversation
and budget.

### A design point the coverage arms should be read with

`verify` measured changed-line coverage itself and said whether every changed line ran
(`_reach`). Arms without the coverage tool got that yes/no as often as base (−coverage:
42 outputs in 18 runs; base 45 in 16); what they lost was *which* lines and their code. So
v1's and v2's −coverage measured "no line-level detail", not "no coverage feedback". Fixed
for future runs (above); the published v1/v2 comparisons are to be read this way.

## Found in the loop check (6 runs, 2026-09-29)

Three instances (sphinx-9602, django-11119, matplotlib-22719) under base and under
`--add-require-tools-with-score-report`, before the 36-instance base run. All fixed.

- **`verify` clipped away the reason.** Each side of its output was cut to its first and
  last few hundred characters; pytest's session header and warnings summary filled both
  ends. matplotlib-22719 (base) wrote `with pytest.warns() as w: ...; assert len(w) == 0`,
  which fails after the fix with `DID NOT WARN` -- a line that fell in the omitted middle
  in all four verifies. The agent decided `verify` could not work "in this environment",
  took ten `verify_open` refusals without calling it again, and ended NO after a restart.
  Now the runner's own lines are dropped (`_condense`, also for `run_tests`) and the side
  that explains the answer gets 2400 characters.
- **`coverage` said "runs every line" about a test that fails after the fix.** Read as
  "done" eight times in the same run. It now adds that the test did not pass with the
  change applied and that only `verify` decides fail-to-pass.
- **The `verify_open` refusal was one fixed sentence.** It now quotes the last `verify`
  headline and says `run_tests` and `coverage` do not answer it.
- **"It does reach the change -- keep the input" at partial reach.** sphinx-9602 ran 7 of
  8 changed lines; the message now lists the missed ones.
- **Trajectory order.** Tool calls were timed off every agent flow row (think, finish,
  stop checks included), so the harness's own events could not be placed among them and
  were all drawn after the last tool call -- a restart's first-attempt probes after the
  restart. Now timed off the tool rows only, refusals off their stop-check rows, and the
  whole trajectory sorted by time. The probe rows are named `stop-check probe` / `stop-check
  reach` (they were `second-chance …`, from before require-tools owned the stop checks).

- **A refusal with 1 action left.** Found in the re-check (sphinx-9602): too few to
  rewrite the test and call `verify`. No refusal and no restart now below 3 actions left
  (`MIN_USEFUL_ACTIONS`); the stop check records the gap still open instead.

Re-check after the fixes (`_fix-check`, same two base NOs): matplotlib-22719 YES in 32
actions, no refusals (its `verify` now showed the failing assertion after the change);
sphinx-9602 NO again at the 100-action cap -- two passes-at-base refusals (reaching all 8
changed lines, so "keep the input" was right), the restart spent on the same assertion.

- **The first 36-instance base run filled the laptop's disk** (13 of 36 done, all
  before the failure and kept). The load guard checked 14 GB free per load and nothing
  for the containers already running; fourteen of them wrote the host to 0, Docker
  Desktop stopped, the rest hung. Now 1.5 GB is reserved per running container and a load
  short of room waits for a job to finish. The 23 unfinished were cleared, not rerun yet.

Working as designed, for the record: the verify loop ran to the cap of 10 (matplotlib
base); the passes-at-base cap ended the first attempt after two rounds and the restart
took the rest of the budget (sphinx both modes; NO -> YES under score report); the
mutation loop refused twice and closed on an attempt that did not improve (django score,
sphinx score); matplotlib score scored 0% on the held-out half with 1/1 on its own -- one
held-out mutant (`and` -> `or` guarding a log call) that the developer's test misses too.

## Found in the first base run's 13 finished runs (2026-09-30)

12 YES, 1 NO (django-15098). Two measurement bugs, both fixed:

- **mutmut never mutated decorated code.** Its rule (skip decorated functions and whole
  decorated classes) exists for its own runner. pytest-5262 (an `@property`) and
  astropy-7336 (inside a `@wraps` wrapper) scored "mutmut offers no mutations"; the
  agent's tool told pytest-5262 the same three times. Fixed in `mutants._allow_decorated`;
  files with no decorators give byte-identical pools (checked on twelve modules).
- **A module-level change counts as reached by any import.** django-15098's patch is a
  module-level regex. The test copied the regex into itself; coverage said it runs every
  changed line and the passes-at-base refusal said "It does reach the change ... Keep the
  input", twice. Now `coverage`, `verify` and the refusal say when every line run is an
  import-time line, and the refusal asks for the code that uses it.

Not bugs, for the record:
- 5 of 13 had no mutation score: the 2 above, django-17029 (a bare `cache_clear()` call:
  no operator applies) and 2 with a pool of one mutant, which goes to the agent's half.
- Readability was "developer's better" in 11 of 12: long docstrings, comments, unused
  imports. The judge's readings were grounded (e.g. django-17029: a mock asserting
  `cache_clear` was called, against the developer's check that the cache is empty).
- 4 runs left scratch scripts at the repository root (`debug_test.py`, `simple_test.py`,
  `poc_test.py`, a urls module); the audit records them; none is imported by the test.
- The refusal fixes from the loop check worked: requests-6028 called `verify` right after
  the quoted `verify_open` refusal and flipped; requests-1142 and sympy-12096's mutation
  loops closed on a non-improving attempt.

## Found in the second base run (36 instances, 2026-09-30): 27/36 YES

Ran 1.3 h at parallel 18; the disk never went below 39 GB free (the per-container reserve
held). Fixed:

- **mutmut never mutates `__new__`, `__getattribute__`, `__setattr__`** -- the same
  trampoline-only rule as the decorator one. sympy-24562's patch is all in
  `Rational.__new__` and still had "no mutations". Lifted with the decorator rule.
- **A developer test that cannot pass here dropped both mutation columns.** requests'
  tests call httpbin and astropy's refraction tests fetch IERS data; the sandbox has no
  network, so the "both tests must pass on the fix" check returned early and
  requests-1766 and astropy-13398 had no score for the agent's passing test either. The
  developer column now uses the developer tests that pass here and lists the rest
  (`excluded`); it reads "not measured" only when none pass.
- **"You never called `verify`" said nothing about what `verify` does.** astropy-13398
  wrote "let me run `verify`" fourteen times, believed it "cannot apply the change in this
  environment", never called it, and took all ten refusals (it scored YES anyway, with
  32% changed-line coverage). The refusal now says `verify` applies and reverts the change
  itself and names the call.

Observed, not changed:
- All 9 NOs ended on the passes-at-base cap, then a restart; 2 of 11 restarts converted
  (django-17029, sphinx-9602). Reach diagnoses split: 3 "does not reach", 4 "does reach",
  2 "reaches part". pytest-7982 alternated passes-at-base and verify-open refusals, so the
  two-running cap never fired and it used all ten.
- A coverage or mutation loop can close with no refusal at all: `V._no_better` also counts
  an attempt made before the agent first stopped (requests-1142: coverage 50%, mutation
  3/5, "not needed"). Working as written; a design question for the user.
- sympy-21612: the image lacks `antlr4`, but the patch is in `printing/str.py` and is
  testable without the LaTeX parser -- a model failure, not an environment one.

## Changed after the fact

- **2026-09-29:** the judge answers five labelled questions per subject before each
  level (`rubric: questions-v1`); its prompt is the folder `judge_prompts/`, questions
  and labels read from the pieces; the judge decides the levels itself, with no rule tying
  them to the labels.
- **2026-09-29:** require-tools' coverage and mutation duties are loops (until no missed
  line / no survivor, or an attempt that does not improve them), in both modes; refusal cap 10.
- **2026-09-28, second revision:** require-tools holds every stop refusal (the base run,
  the `verify` loop, the duties); the second chance is a restart with the first attempt's
  record; `--add-require-tools-with-score-report` adds scores to the duties; flags are
  `--add-<add-on>` / `--no-<input>`; model calls go through `LLM_PROXY` (the gateway resets
  direct connections from the laptop).
- **2026-09-28, from the tool and gate analysis of experiments-v2** (details in
  system-design.md): the second chance is the stop gate (verify loop included) and a
  default-on feature; `require-tools` is only the coverage/mutation duties, and surviving
  mutants must now be answered; every configuration is scored on the same held-out mutant
  half, `--mutants 20`; the judge compares the two tests on a symmetric 1-5 scale (scale
  6); one prompt leak closed (the mutation paragraph named `coverage` in −coverage). Why:
  a withheld tool was already fully gone (no shell workarounds in 700 runs); `coverage`
  and `mutation` are only called after the test flips, so they cannot move fail-to-pass
  through their output; all 40 second-chance rounds in v2 base co-fired with the verify
  loop; the mutation tool did not change the mutation score (0.66 vs 0.66, 31 pairs), and
  its score was taken on a different pool from the arm without it.

- **Sampling temperature 0.3 is the default** since 2026-09-26. One run at 0.3 scored
  20/26 against 16/26 with none sent (p = 0.22; 20 vs 15 genuine, p = 0.06). Adopted on
  that evidence; the ten arms all ran with none sent.

## Not changed yet, on purpose

- ~~A second chance that hands the agent its own failing test~~ -- done 2026-09-27 (see
  "Fixed after the audit"). Not yet tested on its own; a base-twice run on the laptop's 36
  instances is the planned noise-floor check before any arm comparison.

## What this does to the ten-arm results

The ten arms ran identical verdict-path code, so they remain comparable with each other.
But the refusal and django fixes change verdicts, so the new system's numbers are not
comparable with the old ones, and no conclusion should mix the two.
