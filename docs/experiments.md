# Experiments

A buffer of experiments worth running, each with what it would settle, what it costs, and
what result would change a decision. [`system-design.md`](system-design.md) says what the
system is; [`decisions.md`](decisions.md) records what past measurements settled. This file
is the queue in front of both.

Nothing here is scheduled. The order below is by what unblocks the most, not by appeal.

---

## What a run costs

Measured, not estimated. Per-instance figures are the totals from each run's `RUNS.md`
divided by its instance count.

| model | \$/instance | measured over | typical instance | slowest seen |
|---|---|---|---|---|
| `gpt-5.5` | **\$0.74** | eval-10, \$7.42 | 6m | 38m |
| `gpt-5-mini` | **\$0.05-\$0.14** | 26-set \$1.36, eval-10 \$0.89, weak-5 \$0.70 | 17m | 1h05 |
| `gpt-5-nano` | **\$0.034** | eval-10, \$0.34 | 13m | 25m |
| `gpt-oss-20b` | **\$0.024** | eval-10, \$0.24 | 8m | 1h26 |

Typical is the median of the ten evaluation instances. The slowest column is there so the
tail is on the record, not so you plan around it -- every model has one instance that runs
several times longer than its other nine.

`gpt-5-mini` has the wide range because cost tracks instance difficulty: \$0.05 across the
26, \$0.14 across the five weakest. Budget the high end for anything deliberately hard.

**gpt-5.5 is 8-15x mini and buys `issue complete` 7/10 against 4/10.** It is a diagnostic
instrument for one instance, not a way to run a corpus.

### Cost and wall clock by corpus size

One arm, `--parallel 10`. Cost is per-instance x n. Wall clock is bootstrapped from the
*measured* per-instance durations rather than multiplied from an average, because a batch
takes as long as its **slowest** member, not its mean. One figure per cell: the typical
run. Each model had a single instance that ran several times longer than its other nine
and it is excluded, so these are what a normal corpus costs in time, not a worst case.

| n | gpt-5.5 | gpt-5-mini | gpt-5-nano | gpt-oss-20b |
|---|---|---|---|---|
| **1** | \$0.74  /  5m | \$0.09  /  16m | \$0.03  /  14m | \$0.02  /  8m |
| **5** | \$3.71  /  6m | \$0.44  /  24m | \$0.17  /  22m | \$0.12  /  33m |
| **10** | \$7.42  /  6m | \$0.89  /  44m | \$0.34  /  25m | \$0.24  /  1h06 |
| **26** | \$19.29  /  19m | \$2.31  /  1h52 | \$0.88  /  1h10 | \$0.62  /  2h45 |
| **50** | \$37.10  /  32m | \$4.45  /  3h13 | \$1.70  /  1h58 | \$1.20  /  4h32 |
| **100** | \$74.20  /  1h03 | \$8.90  /  6h18 | \$3.40  /  3h58 | \$2.40  /  8h59 |

Up to n=10 everything runs in one batch, so the time is one instance's time and cost is
what scales. Past n=10 both scale.

**Multiply by the number of arms.** A two-arm A/B at n=26 on mini is \$4.60 and about four
hours; the same thing on gpt-5.5 is \$39 and under an hour.

Three things this table says that an average would have hidden:

* **gpt-oss-20b is the slowest model despite being the cheapest.** It is 30x cheaper than
  gpt-5.5 per instance and takes eight times as long at n=100, because it explores in the
  shell instead of using the tools. Cheap in dollars is not cheap in wall clock.
* **gpt-5-nano is the most predictable.** It is the only model whose ten instances have no
  outlier -- slowest 25m against a typical 13m. mini and gpt-oss have long tails where one
  instance can set the whole batch.
* **gpt-5.5 is faster per instance than mini**, despite costing 8x more. Fewer, better
  actions. If wall clock is the constraint rather than money, it is not the slow choice --
  100 instances on gpt-5.5 finish faster than 26 on mini.

Sample sizes are small: ten measured instances per model. Add roughly a third for a corpus
that happens to contain a pathological instance.

**There is no 100-instance set yet.** The corpus is 26 tuned-against plus 10 held out.
Reaching 100 means selecting and pulling ~64 more images - a day of bandwidth and roughly
130 GB of archives - before the bottom row applies.

---

## 0. The variance floor — run this before any A/B

**Question.** How large must a difference be before it means anything?

**Why first.** Every experiment below compares two arms, and we have no idea what the noise
is. `sphinx-10614` has returned YES, NO, YES, YES, YES, YES, YES, NO across near-identical
configurations. If per-instance variance is that high, a 26-instance A/B showing 20 vs 22
is indistinguishable from nothing, and we would draw a conclusion from a coin.

**Method.** Three repeats of the same 100 instances, one configuration, `gpt-5-mini`.
Report the standard deviation of the corpus-level count across the three repeats, and the
share of instances that did not return the same verdict all three times.

**Size / model / cost.** 100 x 3 repeats = 300 runs, mini, **~\$26.70**, ~19 h.

**What it changes.** It produces the minimum detectable effect for everything else. If the
corpus-level count has an SD of +/-2, an A/B must move at least 4-5 instances to be worth
reporting, and several experiments below are not worth running at all.

**What three repeats buys, and what it does not.** Three is enough for the number this
experiment exists to produce: an SD over 100 instances is estimated from the corpus counts,
and three of those give a usable figure -- wide confidence interval, right order of
magnitude. It is *not* enough to classify an individual instance. A triplet can only come
back 0, 1, 2 or 3, so "unstable" and "stable" are barely distinguishable per instance, and
a question like *is `sphinx-10614` reliably hard or just noisy* needs five or more. Two
consequences worth stating before the run rather than after: read the SD, not the
per-instance table; and treat the resulting minimum detectable effect as a floor, since a
three-sample SD is more likely to understate the spread than overstate it.

---

## 1. Do the tools do anything? *(the deferred coverage A/B, plus mutation)*

**Question.** Does giving the agent `coverage` and `mutation` produce better tests than
withholding them?

**Method.** Four arms on the same instances, `gpt-5-mini`:

| arm | flags |
|---|---|
| both | *(default)* |
| no coverage | `--no-coverage-tool` |
| no mutation | `--no-mutation` |
| neither | `--no-coverage-tool --no-mutation` |

**Read on.** Changed-line coverage and held-out mutation score — both measured by the
harness in every arm, so the withheld arms are still fully scored.

**Size / model / cost.** 100 x 4 arms = 400 runs, mini, **~\$35.60**, ~25 h.

**What would change our mind.** A gap of 4+ instances on `issue complete`, or a mutation
score difference outside the variance floor from experiment 0.

**Known risk, and it is serious.** Across 90 mutants in 23 instances there was exactly
**one** survivor the maintainer's test kills and the agent's does not. If the tools have
almost nothing to find on this corpus, all four arms will land on top of each other and
the experiment will have cost \$15 to measure a ceiling. Consider running experiment 2
first — it is cheaper and tells you whether there is anything here to detect.

---

## 2. Tool value against model strength

**Question.** Do the tools matter more for a weaker model, where there is headroom?

**Why this one is interesting.** At the top there is nothing for a tool to find. At the
bottom there should be — except that the weak models **do not call the tools**:

| model | `run` share of calls | `verify` + `coverage` + `mutation` |
|---|---|---|
| gpt-5.5 | 65% | 48 (21%) |
| gpt-5-mini | 81% | 31 (10%) |
| gpt-5-nano | 85% | **4 (1%)** |
| gpt-oss-20b | 92% | **3 (1%)** |

`gpt-5-nano` ran the test suite **by hand 28 times** against 16 `run_tests` calls and 4
`verify`. So a tools-on / tools-off A/B at the weak end risks comparing two configurations
the model treats identically, and returning a null result that means "it ignored them"
rather than "they do not help".

**Method.** Two arms (default, `--no-coverage-tool --no-mutation`) x two models
(`gpt-5-mini`, `gpt-5-nano`), 10 instances. **Report tool-call counts per arm first** — if
the nano arms are identical in behaviour, stop and go to experiment 3 instead.

**Size / model / cost.** 100 x 2 arms x 2 models = 400 runs, **~\$24.60**, ~21 h (mini 200 at \$17.80 and 12h36, nano 200 at \$6.80 and 7h51, one after the other).

---

## 3. Make the tools reachable

**Question.** Can a weak model be made to use the tools at all — and does using them help?

**Method.** One prompt change (candidates: naming the finishing sequence earlier, or
having `run_tests` say what `verify` would add), then nano on 10 instances, comparing
tool-call counts before and after. Only if usage moves does the quality question become
answerable.

**Size / model / cost.** 100 x 2 arms = 200 runs, nano, **~\$6.80**, ~8 h.

**Dependency.** Do this before experiment 1 if experiment 2 shows the weak arms are
behaviourally identical. It is the cheapest item in the file and it gates the most
expensive one.

---

## 4. Does the action cap bind?

**Question.** `--max-iterations` is 100. Its stated rationale — *"observed use ranges from
12 to 65, so the headroom is deliberate"* — was measured before the mutation tool, the
coverage loop and `--repo-search` existed. Recent runs hit 100.

**Method.** The 8-10 instances with the highest observed action counts, two arms: cap 100
and cap 150.

**Read on.** How many runs in the 150 arm exceed 100 actions *and* end YES — that is the
number the current cap is costing.

**Size / model / cost.** 100 x 2 arms = 200 runs, mini, **~\$17.80**, ~13 h.

**Caveat.** On `sphinx-10614` the evidence says the cap is not the binding constraint:
the failing runs and the passing runs differ by *strategy*, not budget. Expect a small
effect and size the conclusion accordingly.

---

## 5. Fixtures allowed — did the rule change help?

**Question.** The rule changed from "create only the test file" to "create freely, edit
nothing that exists", enforced by voiding any run that alters a pre-existing file. Does it
improve instances whose bug needs a fixture?

**Method.** Identify instances whose `test_patch` touches more than one file — that is the
population the change is for, and it is a property of the dataset, computable offline for
free. Run those instances before and after the rule.

**Read on.** Verdict, and `tree_added` versus `tree_altered` — the second must stay empty,
or the enforcement is rejecting work it should permit.

**Size / model / cost.** Population unknown until counted; on the 26 it looked like 5-10, so budget 20-40 of the 100. At 40 x 2 arms on mini that is 80 runs, **~\$7.10**, ~5 h.
**~\$1-3**, ~1-2 h.

**Do the offline count first.** If only one instance in the corpus needs fixtures, the
change is still right but the experiment is not worth running.

---

## 6. `--repo-search` as the default

**Question.** The first A/B found it costs nothing: 24/24 YES both ways, coverage
95.0% -> 97.1%, mutation 75 vs 76 on identical sets, +11% cost, and 11 of 24 chose a better
directory than the harness default. On `sphinx-10614` it produced the best test of three
configurations while hitting the cap.

**Method.** Re-run the A/B under current prompts — the original predates the write-early
rule, the goal change and the mutation tool.

**Size / model / cost.** 100 x 2 arms = 200 runs, mini, **~\$17.80**, ~13 h.

**What it decides.** Whether the briefing should be withheld by default, making
`--repo-search` the normal mode and `--repo-facts` the ablation.

---

## 7. Re-baseline the 26

**Question.** What does the reference corpus look like under the current system?

**Why it is not optional forever.** `out/out_full_run/` predates the mutation tool,
`--repo-search`, the input-choice paragraph, the write-early rule, the goal change and the
fixtures rule. Every "before" comparison against it silently attributes six changes to
whichever one is being tested — which already cost one extra run during the goal-change
test, when a fresh baseline had to be taken first.

**Size / model / cost.** 100 runs, mini, **~\$8.90**, ~6 h.

**Not an experiment.** It is the maintenance that makes the others cheap, and the single
highest value-per-dollar item in this file.

---

## 8. `--no-patch`: the harder task

**Question.** How much does the agent lose when it must infer the intended behaviour from
the issue alone? This is the configuration comparable to TDD-Bench baselines, so it is the
one that makes an external comparison possible.

**Method.** Default versus `--no-patch`, same instances. Note that `coverage` cascades off
with the diff, so the arms differ by input *and* one tool — a confound to state, not to
fix, since `coverage` genuinely cannot work without the patch.

**Size / model / cost.** 100 x 2 arms = 200 runs, mini, **~\$17.80**, ~13 h.

---

## 9. Judge reliability

**Question.** `verdict`, `issue_coverage` and `readability` are one call to one model. How
repeatable are they?

**Method.** Re-judge the *same saved tests* five times. No agent, no container, no
generation — `--recheck` territory, so it costs only judge calls.

**Size / model / cost.** 100 tests x 5 judgements on gpt-5.5, **~\$8-15**, ~2 h. Judgements, not agent runs -- no containers, so this is the one item whose wall clock is set by the API rather than by the test suites.

**Why it matters.** `issue complete` is the metric separating gpt-5.5 from mini (7/10 vs
4/10) and the one every prompt experiment reads. If it is not stable to +/-1, several
conclusions in `decisions.md` need weakening.

---

## 10. Growing the corpus to 100

**Question.** Do the findings hold at four times the size?

**What it takes before any run.** Selecting ~64 more SWE-bench Verified instances,
balanced across repositories and difficulty, then pulling and archiving their images:
roughly 130 GB and a day of bandwidth. That is the real cost; the tokens are cheap.

**Size / model / cost.** 100 runs, mini, **~\$8.90**, ~6 h once the images exist. This one was already sized at 100 because it is the item that *builds* the 100.

**Judgement.** Worth doing *after* experiment 0 says what the noise floor is. A larger
corpus is the only way to detect a small effect, and right now we do not know whether the
effects we care about are small or absent.

---

## 11. The second-chance prompt

**Question.** When a run ends with no fail-to-pass test, the agent is simply told nothing
and the run is scored. Would one more message -- *the task is not finished, here is what
is missing* -- turn a NO into a YES?

**Why it is plausible.** Most failures are not the agent running out of road. Across the
four evaluation runs the thirteen non-YES verdicts break down as:

| failure | count | can the agent check this itself at base? |
|---|---|---|
| wrote no test at all | 7 | yes -- the file is not there |
| test passes before the fix too | 1 | yes -- run it and watch it pass |
| test file collects nothing | 1 | yes -- run the collector |
| still fails after the fix | 4 | **no** |

Nine of thirteen fail on something the agent could have verified without leaving the base
commit. It stopped while holding the evidence that it was not done.

**The line this experiment must not cross.** The verdict comes from running the test at
base *and* at head. The agent only ever sees base. So the nudge may state base-observable
facts -- there is no file at `{test_file}`, your test passes at base, your file collected
nothing -- because each is something the agent could have established on its own, and each
is equally correct advice whether or not a judge exists. It may **not** say *your test
still fails after the fix*. That fact exists only in the head run. Feeding it back turns
generation into fitting-to-the-fix, and the test stops being independent evidence about
the pull request.

That boundary is also what decides the reachable population: the base-observable nudge can
fire on 9 of the 13 failures and is silent on the other 4 by construction.

**The flag exists.** `--second-chance` implements arm B: it refuses the agent's first stop
and lets it carry on once, on what is left of `--max-iterations`, so an arm costs no more
budget than its control. See `decisions.md`, *A second chance, and the one thing it may not
say*. A small pilot on ten instances suggested the effect is modest and that the reachable
population depends heavily on which model is running, which is a reason to size the real
measurement properly rather than a substitute for it.

**Method.** Three arms, same instances:

* **A** control, current system.
* **B** on a finish with no F2P, re-enter the same conversation with one message naming
  only the base-observable fact, and allow up to 25 more actions. Nudge at most once.
* **C** the same, with the head result included. **Measurement only -- its tests are
  discarded and never enter a corpus.** It exists to price what the boundary costs.

`Conversation` is still live when `run()` returns, so B is `send_message()` plus a second
`run()` inside `run_agent()` -- the agent keeps its full context, and the retry costs
nothing on runs that already passed.

**Read on.** NO to YES conversions in B over A. Then B against C: if C rescues the four
head-only failures and B rescues nothing extra, the boundary is costing exactly those
four and the number is worth knowing.

**One confound.** **OpenHands already nudges.** An empty assistant turn is answered with
*"Your last response did not include a function call or a message. Please use a tool to
proceed with the task."* So the honest null hypothesis is not "nudging does nothing" -- it
is "a specific, base-grounded nudge beats the generic one". Report the comparison that
way.

**A second confound was found while sizing this, fixed, and measured.** A strict tool
schema was rejecting invented parameters outright; `ToolArgs` in `sandbox_tools.py` now
drops unknown fields instead of failing the call. Six of the 26 re-run on gpt-oss-20b
afterwards: zero rejections in 188 calls, and **still 1/5**. Three of the four failures
spent every action in the shell and wrote nothing at all. So the schema was real but it
was not what caps this model, and these three are exactly the population arm B fires on --
this experiment now has its cleanest test case. See `decisions.md`, *A strict tool schema
was measuring itself*.

**Size / model / cost.** 100 x 2 arms (A, B) on nano = 200 runs, **~\$6.80**, ~8 h. Arm C
runs only on the instances that failed -- budget 40 of the 100, so 40 more runs, **~\$1.40**,
~2 h. gpt-5.5 and mini pass 10/10 on the evaluation set, so they have nothing to rescue;
this experiment needs the weak end of the ladder.

---

## Suggested order

Everything below is sized at **n = 100**, one arm meaning 100 runs. Nothing here has been
run. Experiment **10 comes first by necessity** -- it is the item that builds the
hundred-instance corpus every other line assumes, and until it exists these are estimates
against a set that does not yet exist.

| | experiment | runs | cost | wall clock | why here |
|---|---|---|---|---|---|
| 1 | **10** grow the corpus to 100 | 100 | ~\$8.90 | ~6 h | every row below is priced against a corpus that does not exist yet |
| 2 | **0** variance floor | 300 | ~\$26.70 | ~19 h | nothing below is interpretable without it |
| 3 | **7** re-baseline the 100 | 100 | ~\$8.90 | ~6 h | makes every later comparison single-variable |
| 4 | **3** make tools reachable | 200 | ~\$6.80 | ~8 h | cheapest real arm, and it gates the most expensive |
| 5 | **11** the second-chance prompt | 240 | ~\$8.20 | ~10 h | if a message recovers the failures, the tools are being asked to fix something a sentence already fixes |
| 6 | **9** judge reliability | -- | ~\$8-15 | ~2 h | validates the metric the others are read through |
| 7 | **2** tool value x model | 400 | ~\$24.60 | ~21 h | tells you whether the next line is worth \$36 |
| 8 | **1** the tool A/B | 400 | ~\$35.60 | ~25 h | only once 4 and 7 say there is signal to find |

**The first five: ~\$60 and about 49 hours.** The full eight: **~\$131, 1,740 agent runs
and about 97 hours** -- four days of continuous running at `--parallel 10`.

Two things that table makes obvious and the 26-instance version hid:

* **Experiment 0 is the third most expensive item**, at three repeats of 100. Five would
  have made it the second, at ~\$44.50 and ~31 h; three is the deliberate choice, and it
  buys a corpus-level SD but not a per-instance stability verdict. The reasoning is under
  experiment 0.
* **Wall clock, not money, is the binding constraint.** \$131 is not much; 97 hours is
  most of a week. Anything that shortens it -- a larger `--parallel`, or running the
  cheap arms concurrently on different models -- buys more than anything that shortens the
  bill. The costing above assumes `--parallel 10` throughout and arms run one after the
  other.

Everything is priced on `gpt-5-mini` unless the experiment names another model, at
\$0.089 an instance. The same 1,740 runs on `gpt-5.5` would be **~\$1,290**, and on
`gpt-5-nano` **~\$59**. The per-model figures are in *Cost and wall clock by corpus size*
above.
