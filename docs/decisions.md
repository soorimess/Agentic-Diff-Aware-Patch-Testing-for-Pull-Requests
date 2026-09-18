# Decisions, experiments and dead ends

[`system-design.md`](system-design.md) says what the system *is*. This file says how it
got there: the measurements that settled a design, the bugs that changed one, and the
things that were tried and removed. None of it is needed to understand the current system.
It is here so a decision already paid for is not re-litigated, and so the evidence behind
a number outlives the run that produced it.

## Metrics

### Why `BROKEN` is kept apart from `NO`

Collapsed together, every harness bug reads as a model failure. On the first full pass
over the twenty-six instances, **eleven distinct harness bugs each produced a plausible
number rather than an error** — each looked like a finding about the model and was a
finding about us. Keeping the two apart is what made them visible.

### Where changed-line coverage runs out

Two instances show the metric's edges, and both readings are correct rather than broken.

`scikit-learn-25747` reports **not measured — the changed lines are all comments or
blanks**. Its fix is a *deletion*: it removes two executable lines and its only added line
is a docstring sentence. There is nothing at any line number for a test to execute, so
changed-line coverage has no denominator. The test is genuinely fail-to-pass; the question
simply does not apply. Counting deleted lines would make full coverage unreachable, and
crediting the lines that surround the hole would measure the wrong thing — so the honest
answer is to decline. A patch whose whole behavioural change is a removal is invisible to
this metric, and that is a limitation of the definition, not a fault in the run.

`matplotlib-26208` reports **50% (1/2)**. Its fix applies the same one-line change in two
symmetric places, `twinx` and `twiny`, and the test exercises `twinx` only. That is the
metric doing exactly what it exists for: the test pins half of a symmetric bug, and the
number says so.

A third edge is the one a coverage number can never see. `seaborn-3187` under `gpt-5.5`
reports **100% (6/6)** for a test that cannot distinguish the fix from its absence. The
patch disables an additive offset and scientific notation on a legend's formatter; the
test's values run from 3e6 to 6e6, which makes matplotlib reach for scientific notation but
never for an offset. `set_useOffset(False)` executes, so it is covered — and flipping it to
`True` produces byte-identical labels for that data. Executing a line and discriminating on
it are different properties, and only the second is what a regression test is for. Mutation
caught it, the judge caught it independently, and coverage reported full marks. This is the
clearest case in the corpus for why the three instruments are not redundant.

### Mutation: why `mutmut` and not a model

An earlier version asked a frontier model for `{file, find, replace}` edits. It worked,
but it made the metric depend on a sampling temperature: re-running an instance could
produce a different denominator, and so a different score for an unchanged test. A
measurement that moves when nothing moved is not a measurement. `mutmut` 3.7.0 with
libcst 1.9.0 underneath is deterministic, and two runs of one instance producing
byte-identical mutants has been checked.

### Mutation: why the denominator is not filtered

| | agent test | developer test |
|---|---|---|
| `out/out_full_run/`, 23 instances, 90 mutants | 74 (82%) | 69 (77%) |
| `out/out_compare_repo_search/full`, 24 instances, 100 mutants | 75 | 79 |
| `out/out_compare_repo_search/repo-search`, same 100 mutants | 76 | 79 |

An earlier design filtered the denominator down to mutants the maintainer's test kills, on
the argument that the rest are unfair questions — equivalent mutants, or behaviour outside
what the pull request is about. That gate is gone by decision: it folded a judgement into
the number, and the raw pair says more. The developer column doubles as a control — the
same 100 mutants give 79 in both series, so an agent difference of 75 against 76 is a
like-for-like comparison and not two different exams.

The two corpora disagree about which test is stronger, and that is the honest finding:
across instances the agent's tests and the maintainer's are within a few points either
way, with real spread underneath. `sphinx-7454` went 10/10 against the maintainer's 9;
`flask-5014` killed 1 of 4.

### Mutation: the instances that score zero

Six of 23 instances produced **no mutants at all**. `mutmut`'s operators work on
expressions — comparisons, operators, constants, keywords — and a patch that only adds a
statement, a decorator or a framework declaration offers them nothing to change. A
statement-deletion operator would cover most of these; it is deliberately deferred, and
until then `0/0` is reported as what it is rather than counted as a perfect score.

### Mutation: two bugs in the held-out split

The halving happens at the *candidate* level, inside each `(file, line)` group. Splitting
`_spread`'s output instead looked equivalent and was not: `_spread` round-robins across
groups, so consecutive entries come from different lines, and taking every other one
divides the pool by line. On `requests-1142` that gave the developer's own test **0 of 5**,
its half being entirely on a line that test does not exercise. A denominator built that way
measures which line landed where.

Splitting by line was the first bug in the halving. The second was subtler and lived for
several runs: the side each group *started* on was always the same one, so index 0 of every
group went to the agent. mutmut's order within a literal is fixed — `False -> None` before
`False -> True` — which meant one half systematically collected the type-changing mutants
and the other the value-changing ones.

Those ask different questions. On `seaborn-3187` the agent was shown
`set_useOffset(None)`, which raises a `TypeError` inside matplotlib and therefore dies
against any test whatsoever, and was scored on `set_useOffset(True)`, which formats
*identically* to the fix unless the data is in the range where an offset would appear. The
agent recorded a kill it had not earned, learned nothing about the line, and its test was
then measured on the one mutant that would have told it the truth. The fix is one counter:
the starting side rotates with the group's position, so both halves draw from the same mix
of operators. A held-out number means nothing if the two halves are not samples of the
same thing.

### What the mutation tool can be worth

**How much it can help is bounded, and worth stating.** Across 90 mutants in 23 instances
there is exactly one survivor the maintainer's test kills and the agent's does not. Nearly
every survivor is one neither test kills, and `47-tools-mutation.md` tells the agent to
leave those alone. On most instances the tool correctly has nothing to ask for.

### Coverage and the judge agree by different routes

On `matplotlib-26208` the judge returned `issue partial` and named the missing behaviour
as "the twiny/shared-y symmetric case" — the same gap the 50% changed-line figure found by
executing lines. Two instruments, two routes, one answer.
## Which model answers

### Why the registry moved out of the code

Every model-specific decision used to be a global default in `llm_config.py` with a
comment naming the model it was tuned for: `api_mode="chat"` because `"auto"` resolved
gpt-5-mini to an endpoint that hung for the full 300 seconds, a token ceiling because a
reasoning model spent its whole budget and emitted no tool call, a timeout and retry count
measured against one gateway. Changing model meant editing environment variables and
hoping.

### The precedence was written backwards

It was written the other way round first, with the environment above the profile, on the reasoning that an explicit override should win. That reasoning is wrong
here, and the shape of the bug says why: an environment variable is *global* while a
profile is *per-model*, so `LLM_TIMEOUT=600` in a `.env` overrode the 900 that `gpt-5.5`
asks for, and every profile value was inert for as long as a variable named the same
field. A registry nothing consults is not a registry. Inverting it made the variables what
they always should have been — a floor under a model with no entry of its own — and the
`FALLBACK_` prefix says so in the one file where the mistake was easy to make.

Two things follow. Profile tuning fields default to `None` rather than to a real value,
because a field with a default can never fall through to a fallback; `None` is how an
entry says *this one has no opinion*. And `describe()` prints resolved values with a star
on the ones the file actually names, since a table full of `None` would answer a different
question than the one being asked.

### What a profile cannot fix

`gpt-5.5` through the LiteLLM gateway answers with two choices: a text preamble in
`choices[0]`, the tool call in `choices[1]`. The SDK reads the first, finds no tool calls,
and treats the reply as final -- so the agent records zero actions in twelve seconds and
looks like a model that cannot call tools. It is not; the tool call is right there in the
second choice.

No value in `models.py` reaches that, because the choice is made inside the SDK. It is
recorded on the profile as `picks_first_choice=False` so the failure has a name and the
next person does not spend a run rediscovering it, and fixing it means wrapping the SDK's
`LLM` rather than adding a field.

## What the agent is given

### The `repo_info` sub-agent, and why it was deleted

There is no sub-agent for repository knowledge any more. There used to be: `repo_info`,
a second model call per instance that read the tree and reported how tests are written
here. It was removed because the same question was being answered in three places at
once -- its own `find` over the test directories, `run_tests` building the command, and
the runner detection in `runners` -- and the three could disagree. Once it was asked to
report the runner without being handed the answer it called `pytest` "the canonical
runner" for sympy, which does not use it.

All of it now comes from one place. `repo_facts(box, test_file)` in `runners` reads the
checkout directly -- runner, target directory, the project's own pytest configuration
verbatim, and the names of neighbouring tests -- and that text becomes the `15-repo.md`
prompt piece. It is measurement, not inference: no model call, nothing to disagree with,
and the same code path that `run_tests` uses to build the command. Style is the one thing
it does not try to answer, because it cannot be answered generally; the agent is told to
read one to three neighbouring tests and see for itself.

### Withholding a component can mean adding an instruction

`--repo-search` (also spelled `--no-repo-facts`) is the first feature where taking a
component away is not enough. The other four make the prompt shorter and nothing else:
drop the diff and there is simply no diff. Drop the briefing on how this project tests
and the agent has to be *told* to work it out, or the run measures a missing instruction
rather than a missing input — a distinction the whole point of these switches depends on.

So `prompt.py` grew a negated condition. `needs: !repo-facts` keeps a piece only while
that feature is off, and `16-explore.md` uses it to ask the same questions `15-repo.md`
answers: where a new test file has to live to be collected, what the test configuration
enforces, how the tests already there are written. It answers none of them — an answer
would be the per-repository advice that was deleted from `prompts/` once already.

Two things about it are worth stating plainly, because they bound what the flag measures.

**The runner is not really withheld.** `run_tests` picks this project's runner in every
configuration and converts a path to whatever form it wants, and the agent could always
have read a configuration file with `run`. What the briefing uniquely supplied is the
*destination*: the shallowest directory named `tests`, `testing` or `test`, which is the
one fact that took twelve repositories to get right.

**So the destination moves to the agent, and the harness follows it.** The filename stays
ours — it is not repo knowledge, it keeps the file findable afterwards, and it stops the
agent overwriting a test that was already there — while the directory becomes the agent's
to establish. `written_test_path` resolves it: the write log first, confirmed against the
container, then a `find`, then the path the harness would have chosen. It runs before
`audit`, which flags every write that is not the test file; left later, the agent's own
chosen path would be reported as a stray write on every run.

Resolving it once is not enough, and finding that out cost a run. `verify` derived the
path itself from `gen_test_path`, so an agent that put its test in django's
`tests/auth_tests/` — beside the model it imports, where django's own developers keep
this test — wrote `from .models import ...`, correct there, and the harness relocated the
file to `tests/`, where there is no parent package. The verdict came back *"still failing
after the fix — the test is wrong, not the code"* about an ImportError the harness had
manufactured. `verify` now takes `test_path`, `recheck` passes what the run recorded, and
`mutate_saved` prefers it over re-deriving. Re-judging that run with no LLM call turned it
from `NO` to `YES` at 100% coverage.

The line that broke already carried a comment about the same class of bug one
configuration earlier: pytest keeps its tests in `testing/`, the briefing said so
correctly, and a verdict computed at `tests/` reported "nothing collected on either side"
for a test that was fine. A derived path is the bug; the parameter is the fix.

**The runner leaked through a channel the prompt scan cannot see.** `run_tests` built its
description from `runner_for(box)["cmd"]`, so every `--repo-search` run handed django's
`./tests/runtests.py --verbosity 2` to the model in the tool schema — before it took a
single action — while the briefing that was supposed to be withheld sat unused. The
observation echoed `$ <command>` too, which taught the dotted-label conversion on first
use. `prompt.build` had guaranteed for months that no assembled prompt names an
unregistered tool; tool *descriptions* had no such guarantee, and that is exactly where
the leak was.

Now the runner is named only when the briefing names it. `reveal_runner` controls both the
description and the echo, and `_check_no_leak` refuses to register a tool whose
description contains the runner command while `repo-facts` is withheld. The capability is
identical either way — `run_tests` still builds and runs the right command — and only the
knowledge differs. The first A/B measured before this fix; the second, after.

Both paths are recorded, always, as `test_path` and `test_path_default`. A test in a
directory the runner never collects from fails for a reason that has nothing to do with
how good the test is, and without the pair on record those two failures are
indistinguishable in the table.

### The audit that could not have caught anything

The measurement rests on the agent not having edited the library: the "before the fix" run
happens in the container as the agent left it, so a source edit makes that run a fact about
something other than the pull request. `50-rules.md` says so, and for a long time the
checking was a fiction. `audit` asked `git status`; `strip_git` had already deleted the
repository, so the answer was always "not a repository" and the tree always read clean. It
could not have caught anything. The other check, `files_written_outside_test`, reads the
tool log — which sees `write_file` calls and is blind to `sed -i` or a shell redirect.

The tree is now compared against a snapshot taken before the agent is let in. The
repository holding that snapshot lives **outside the checkout**:

    git --git-dir=/tmp/f2p_tree.git --work-tree=/testbed

Putting `.git` back under `/testbed` would have changed what we measure — `setuptools_scm`
and friends compute a package version from git, and every verdict on record was taken with
no repository there, so one untagged commit could change a version string and break tests
for reasons unrelated to the agent. Outside, the checkout still has no `.git`, the single
commit holds only the base state so there is no history to leak, and `tree_changes()`
still returns an exact list of what moved.

Verified on a live container: an agent editing `django/forms/models.py` with a shell
redirect is invisible to the tool log and appears immediately in the tree diff. Across the
48 runs of the first A/B, every run created exactly one file and changed nothing else —
which is now a checked fact rather than an assumption.

### An input is not its tool

The diff and `verify` were one switch to begin with, on the reasoning that a check against
the change is only possible once the change has been shown. That was wrong. The harness
holds the patch in *every* configuration — it applies it and reverts it itself — so
`verify` can report whether the agent's test flips without the agent seeing a line of the
diff. It leaks nothing: the verdict is a fact about the agent's own test.

Coupling them was also a methodological mistake. If `--no-patch` withheld the feedback
loop as well as the input, a drop in the result could not be attributed to either — which
defeats the purpose of having the switches at all. They are separate features now.

The one that genuinely cannot be separated is `coverage`. It prints the source of the lines
a test missed, and those lines *are* the diff, so it needs `patch`. What survives the split
is a graded scale of information:

| what the agent gets | leaks the diff? |

### Why there is no pair-comparison code

There is no pair-comparison code. There was: an `arms.py` that ran every pull request
twice, once with the coverage tool and once without, and reported the paired difference.
It is gone, because a pair is the wrong unit — the interesting comparisons are between
*series* of runs whose configurations differ, and a paired harness fixes the axis at two
values chosen when it was written.

What replaces it is bookkeeping. Every result records `features.config`; `RUNS.md` states
which configuration produced its rows and warns when they came from more than one. A
series is a directory:

```bash
uv run openhands-f2p --out-root out_full
uv run openhands-f2p --out-root out_nocov --no-coverage-tool
```
## The prompt

### What watching the `mutation` tool changed

Watching it be used produced two prompt fixes and one non-fix worth recording. The stop
condition read "you are finished when no check has raised something you have not
answered", which a run that calls *no* checks satisfies: an agent wrote its test, called
`verify`, and stopped after five actions. And nothing pointed at `mutation` -- `verify`
already reports coverage itself, so skipping `coverage` was reasonable, but `mutation` is
the one question nothing else answers. `verify` now names it, the way it already named
`coverage`.

The non-fix: three rewrites of the surrounding prose telling the agent to iterate changed
nothing. It calls the checks in numbered order and stops, in roughly three runs in five.
The one time iteration appeared -- `seaborn-3187`, coverage 33%, a rewrite, then 100% --
it was because there was something to iterate on; four earlier instances were at 100% on
the first measurement, where a loop would have been a no-op.

### Reading is not the work

Two instructions changed after `sphinx-10614` failed, and the second is the only prompt
change in this project with a repeated measurement behind it.

The failure: 98 of 100 actions were `sed`, `grep` and `ls`; one was a write, one was a
test run; the budget ran out holding a test that did not flip. The agent was obeying the
last line of `50-rules.md`, which read, in full, "Read the source before you write." On a
repository the size of sphinx that instruction has no stopping point.

Ranking every run of that instance by outcome ranks them by how often the agent *revised*,
and not at all by how much it read:

| write / verify / coverage | outcome | `run` commands |
|---|---|---|
| 4 / 2 / 2 | 100% coverage, 9 of 10 mutants | 91 |
| 3 / 2 / 1 | 100% coverage, 10 of 10 | 66 |
| 1 / 1 / 1 | 80% coverage, judged `different` | 50 |
| 1 / 1 / 0 | **NO** | 98 |

So the rule now says what the reading is *for* and hands the stopping point to the test:
read enough to know what to assert, then get a test running and let what it does correct
the rest. Three repeats afterwards, on the instance that had been the noisiest thing in
the corpus:

| | four runs before | three runs after |
|---|---|---|
| verdict | YES, **NO**, YES, YES | YES, YES, YES |
| coverage | 100, --, 80, 100 | 100, 100, 100 |
| readability | **poor, poor, poor, poor** | **acceptable, acceptable, acceptable** |
| actions | 72, 100, 57, 100 | 66, 66, 71 |

Readability had never once been `acceptable` on this instance, including under the
original prompts. The variance is the other half: two cap-hits and a 57--100 spread became
66/71 with none. What did *not* move is `issue coverage`, still `partial` in two of three
-- the change buys reliability and legibility, not behavioural breadth.

The other change, in `20-goal.md`, is breadth and is **not** yet measured. "One test"
became "one test function per behaviour the change settles separately -- as many as the
change has, and no more", after `astropy-13398`: 93 changed executable lines where the
rest of the evaluation set has one to eight, a whole module of coordinate transforms, and
both gpt-5-mini and gpt-5.5 wrote exactly one test function and left most of it untested.
The five instances it has been run against are all one- and two-line patches, where one
function is the right answer and the instruction is never exercised. It needs
`astropy-13398` itself to be worth anything.

## Structure

### The module split

`swebench_env.py` was 1091 lines holding four subjects that barely touched each other, and
`agent.py` was 807 holding six. Both are split:

| was | is now |
|---|---|
| `swebench_env` 1091 | `images` 282 &middot; `runners` 315 &middot; `sandbox` 238 &middot; `coverage_metric` 398 &middot; facade 89 |
| `agent` 807 | `agent` 470 &middot; `parallel` 211 &middot; `checks` 107 |

`runners` grew past its extracted size on purpose: it absorbed `repo_facts`, `test_config`
and `example_tests` when the `repo_info` sub-agent was deleted, so everything the system
knows about how a repository is tested is now in one file.

Three things made it safe. `swebench_env` stays as a re-export facade, so every existing
`from openhands_f2p import swebench_env as E` keeps working and none of its six dependents
changed. The move was done by slicing exact line ranges rather than retyping. And
`--recheck` re-ran the saved tests through the whole verdict and coverage path afterwards,
with no model call, to show nothing moved.

## Results

### The held-out evaluation set

Every prompt and heuristic here was written while looking at the twenty-six in
`out/out_full_run/`, which makes them useless for the one question that matters most:
whether any of this works on instances nobody saw. So `evaluation/prs.json` holds ten
more -- one per repository, drawn by seed, tier taken from SWE-bench's own `difficulty`
-- and `F2P_PRS_FILE` points the same code at them with nothing special-cased.

Four models, the same ten instances:

| model | fail-to-pass | issue complete | cost | per instance |
|---|---|---|---|---|
| `gpt-5.5` | 10/10 | 7/10 | $7.42 | $0.74 |
| `gpt-5-mini` | 10/10 | 4/10 | $0.89 | $0.09 |
| `gpt-5-nano` | 6/10 | 3/10 | $0.34 | $0.03 |
| `gpt-oss-20b` | 2/10 | 2/10 | $0.24 | $0.02 |

**The system is not the limiting factor at the top.** gpt-5-mini passes all ten held-out
instances, and the gap to gpt-5.5 is entirely in `issue coverage` -- whether the test
reaches every behaviour the pull request settles -- not in anything mechanical. Tier for
tier the held-out set matches the tuned-against one: 9/9 versus 20/21 on tiers 2--4, with
coverage at 100% on 8 of 9 either way.

The per-instance matrix nests perfectly: every instance a weaker model passes, every
stronger model passes too, with no inversions. That says the set grades models rather
than sampling noise, which is the property an evaluation set has to have before any
number taken from it means anything.

**The weak models fail differently, and only one of those differences is about test
quality.** Six of gpt-oss-20b's eight failures are *wrote no test at all* -- it explores
and stops, once after a single action. gpt-5-nano writes real tests, and five of its six
passes are at 100% coverage. That distinction decides which rung is usable for measuring
tooling: a tool that reports on a test can only help a model that writes one.
