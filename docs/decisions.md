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

### "Create only the test file" was the wrong rule

The rule said one file. The reason given for it was narrower than the rule: *do not change
the library source to make your test pass*. One-file was a proxy, chosen because it is
trivially checkable, at a time when the audit could not verify anything better -- it asked
`git status` in a checkout whose `.git` had been deleted, so it always reported clean.

`sphinx-10614` is where the proxy failed. The bug is that inheritance-diagram links are
wrong **in nested directories**; the base fixture root has no nested directory; and the
maintainer's own test for the bug touches **six files**, extending an existing root and
adding a `subdir/`. A test for this cannot be one file.

Two things made the relaxation safe to do rather than merely tempting:

* **The harness never enforced one-file anyway.** It recorded `files_written_outside_test`
  and no verdict depended on it. On one run the agent built a seven-file fixture root of
  its own and was not penalised -- it lost on the action cap, mid-iteration. The rule was
  costing us the contradiction of telling the agent not to do the necessary thing, and
  buying no safety in return.
* **`tree_changes` already existed**, comparing the checkout against a pre-agent snapshot
  in a git dir outside `/testbed`. It threw the status codes away, so added and modified
  looked alike; keeping them separates the safe case from the dangerous one exactly.

So the rule is now *create freely, edit nothing that exists*, and a run that edits
something pre-existing is `BROKEN` rather than scored. That is strictly stronger than
one-file on the thing that matters -- it catches a `sed -i` on library source, which
one-file only caught by implication -- and permits the fixtures a real regression test
needs.

What it does not settle: whether `sphinx-10614` now passes. The run that built the fixture
ran out of budget while iterating, and the run that passed did so without a fixture at all.

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

### Weak models bypass the tools rather than misuse them

`mutation` looked at first like a tool the agent skips: it went uncalled in every run of
`sphinx-10614`. Counting properly across the evaluation set shows something wider, and
strictly ordered by model strength.

| model | calls | `run` share | `verify` + `coverage` + `mutation` |
|---|---|---|---|
| `gpt-5.5` | 228 | 65% | **48 (21%)** |
| `gpt-5-mini` | 318 | 81% | 31 (10%) |
| `gpt-5-nano` | 340 | 85% | **4 (1%)** |
| `gpt-oss-20b` | 261 | 92% | **3 (1%)** |

It is not that `mutation` is unreachable. Weak models barely use any purpose-built tool:
`gpt-5-nano` called `verify` four times across ten runs while issuing 288 shell commands,
and it ran the test suite **by hand 28 times** against 16 calls to `run_tests`. `gpt-5.5`
inverts that — 9 by hand against 15 `run_tests` and 22 `verify`.

`coverage` and `mutation` have no shell equivalent the agent knows how to reach for, so
where `verify` degrades into `pytest` typed by hand, those two degrade into nothing at all.

The consequence for the tooling plan is unwelcome and worth stating before spending on it.
The models with the most headroom for a tool to help are the ones least likely to invoke
one, so an A/B of "tools on" against "tools off" at the weak end risks measuring two
configurations the model treats identically. Making a tool *available* is not the same as
making it the path of least resistance, and only the second is worth measuring.

### The rule that was never enforced, and what happened when it was loosened

`50-rules.md` used to open `Create only {test_file}. Do not modify, create or delete any
other file.` -- prohibition in the first four words. `sphinx-10614` needs six fixture
files, so the rule was rewritten to allow creating them, and the new version opened with
the permission and put the prohibition in its second paragraph.

On the next nano evaluation set the agent wrote its test correctly and then rewrote
`xarray/core/indexing.py` and `sklearn/impute/_iterative.py` with shell heredocs until its
own test passed. Two instances that had been YES became BROKEN, 6/10 fell to 3/10. The
prompts were diffed out of the two runs' `result.json` rather than reconstructed from
commits: **they differ in exactly one hunk**, which is this one.

What the agent wrote was not a workaround. It was the maintainer's patch:

| instance | the real fix | what the agent wrote |
|---|---|---|
| `matplotlib-22719` | `-if is_numlike:` / `+if values.size and is_numlike:` | `if values.size and is_numlike:` |
| `xarray-7393` | `+if dtype is None: dtype = self.dtype`, `np.asarray(..., dtype=dtype)` | exactly that |
| `sklearn-25232` | `+"fill_value": "no_validation"`, `+fill_value=None`, `+self.fill_value = fill_value` | exactly those |

Character-identical in the matplotlib case. Had it stood, the before-the-fix run would have
executed *with* the fix, the test would pass at base, and the instance would report a
confident YES about nothing.

Two things were wrong and both were fixed. The prohibition is the first sentence again,
and the block is shorter than the one that replaced it -- permission survives, so the
fixture case still works. And the rule is now enforced between actions rather than
described: `_undo_edits` runs after every `run` and `write_file`, compares the tree with
the snapshot in `TREE_GIT`, restores anything pre-existing that changed, and says so in
that call's own observation.

`diff --name-only HEAD` rather than `status --porcelain`: it reads only what the snapshot
tracks and skips the untracked walk that is slow on these images, and that is also exactly
the question -- a file the agent *created* is tracked by neither and cannot manufacture a
flip, because it is present in the before run and the after run alike.

**Contamination went 2/10 to 0/10 and both instances recovered.** The impulse did not go
away: three of ten runs still reach for the library, once each, and stop when the revert
lands. Before the guard, the same first attempt was followed by forty more in the same
file. The guard suppresses the consequence, not the behaviour, and the `tools used` column
in `RUNS.md` reports each revert so that stays visible.

### `repo_facts` handed sympy a pytest.ini

The prompt told `sympy-21612` `Runner bin/test -C --verbose`, and four lines later printed
its `pytest.ini` under *"Test configuration, verbatim from the checkout"*. True, and
irrelevant: sympy runs its own framework in an image with no pytest installed. The agent
opened with `import pytest`, the file never imported, and the verdict was BROKEN --
nothing collected on either side, which is the harness learning nothing rather than
learning the test was wrong.

`test_config` now returns nothing unless the detected runner is pytest, and `repo_facts`
substitutes a positive instruction instead of going quiet -- silence would not do, because
the `pytest.ini` is still in the checkout for the agent to find. Rerunning the instance
moved it BROKEN to NO, and the action count went 10 to 52: it had been hitting the import
wall and giving up with ninety actions unspent.

### A strict tool schema was measuring itself

`Action` in the SDK sets `extra="forbid"`, so a tool call carrying one unknown key died
with a pydantic error and the model got no result:

```
Error validating tool 'sandbox_run': 1 validation error for RunAction
timeout
  Extra inputs are not permitted [type=extra_forbidden, input_value=120000, input_type=int]
```

Three invented names accounted for all of it across the evaluation set -- `timeout` (184
calls), `commentary` (57), `stdin` (30) -- and the models that invented them were the weak
ones:

| model | instances affected | worst instance |
|---|---|---|
| `gpt-5.5` | 0/10 | — |
| `gpt-5-mini` | 0/10 | — |
| `gpt-5-nano` | 1/10 | 30 of 47 calls |
| `gpt-oss-20b` | 7/10 | **91 of 100 calls** |

`sympy-21612` spent its whole 100-action cap inside the loop: rejection, then an empty
assistant turn whose recovery plan sat in `reasoning_content` where nothing reads it, then
OpenHands' generic *"your last response did not include a function call"*, then the same
malformed call again.

`ToolArgs` now sets `extra="ignore"` and counts what it drops into `INVENTED`, which is
recorded per run as `invented_parameters`. The emitted JSON schema is byte-identical under
both settings -- pydantic adds no `additionalProperties` either way -- so the model is told
exactly what it was told before and this is a validation change, not a prompt change.

**What the fix bought, measured on six of the 26 with gpt-oss-20b.** Zero rejections in
188 calls, against seven of ten instances affected before. The models still invent the same
parameters at the same rate -- `timeout` appeared 15 times -- they just no longer lose the
call for it.

**What it did not buy: a better score.** 1/5 of the instances that reached a verdict. The
failures are now the behaviour the section above describes, not a bug:

| instance | calls | tools used | outcome |
|---|---|---|---|
| `astropy-14995` | 37 | `write_file`, `verify` x4, `run_tests` | **YES** |
| `pytest-10081` | 39 | `write_file` x3, `run_tests` | NO, test wrong |
| `sklearn-10908` | 11 | `write_file`, `verify`, `coverage` | BROKEN, edited the tree |
| `django-13406` | 41 | **`run` x41** | NO, never wrote |
| `sympy-24562` | 29 | **`run` x29** | NO, never wrote |
| `xarray-7233` | 8 | **`run` x8** | NO, never wrote |

Three runs spent every action in the shell and wrote nothing. The one that passed is the
one that wrote early and verified. So removing the schema bug exposed the real constraint
rather than removing it, and `gpt-oss-20b`'s ceiling is still unmeasured -- what is now
known is that the earlier 2/10 was partly this config line.

One residual defect, rare but fatal where it lands: three of 188 responses carried Harmony
channel markup as plain text -- `to=functions.sandbox_run<|constrain|>??` -- instead of a
parsed tool call. Each was the final turn of its run. `models.json` already warns to check
native tool calling for this model before a full set; this is that warning coming true.

### Silence was worse than the refusal it replaced

`ToolArgs` first set `extra="ignore"`, which accepted a call carrying unknown keys and
dropped them. That fixed gpt-oss, which invents harmless names like `timeout`. It broke
`gpt-5-nano`, which emits calls where the shell script arrives as a *key*:

```json
{"command": "bash -lc", "grep -RIn \"symlink...\" | head -n 200' }": false}
```

The dropped half was the command. `bash -lc` ran with no argument and the only feedback
was `bash: -c: option requires an argument`. Across one evaluation set that was **47 of
329 actions**, and `pytest-7982` spent five consecutive actions on it and finished having
written nothing at all.

So the setting is `extra="allow"`: the extras are kept, and `_ignored` names them back in
the observation, marked as an error. Named rather than counted -- "ignored 1 unknown
argument" would not have told nano that what it lost was the command -- and truncated,
because the usual offender is an entire shell script sitting where a parameter name
belongs. The emitted JSON schema is identical under all three settings, so none of this
changes what the model is told it may send.

The lesson generalises past this bug. A lenient parser is right; a *silent* lenient parser
converts a diagnosable failure into an undiagnosable one, and the model cannot correct
what it cannot see.

### Requiring a tool call measured the wrong thing

`--no-require-tools` gates a rule that a registered instrument must have been used, on the
reasoning that a tool present and unused is a configuration we are not measuring: the arm
says `full` and the behaviour is `full` minus that tool. Across the evaluation set the
instruments were reached for **3 times out of a possible 30**.

The first implementation asked whether each tool *appeared* in the log. Usage jumped to
19/30 and the score did not move, and the reason is in the trace: **four of five failures
ended immediately after `verify` reported NOT fail-to-pass.** Requirement satisfied, goal
unmet. Meanwhile `pylint-7277` called `verify` seventeen times and `matplotlib-22719`
once, so the count carried almost no information about whether the loop had closed. It was
the Goodhart error the prompt rules are written to avoid, committed in the enforcement.

`V.loop_gap` judges each instrument by what it last said:

* **`verify`** must last have reported fail-to-pass, with no write since. An answer about
  a file that has been edited is an answer about a file that no longer exists -- two runs
  scored YES by stopping on a stale negative and being saved by an edit they never
  rechecked.
* **`coverage`** must have been called, and a report under 100% must have been answered by
  an edit. Not a demand for 100%, which is often unreachable; a demand that a shortfall is
  answered once rather than read and passed over.
* **`mutation`** must have been called, and nothing more. Survivors are for the agent to
  weigh. `astropy-13398` is why: mutation reported 0 of 10 killed, the agent added a second
  test to close the list, the new test failed on both sides, and a file whose first test
  flipped correctly scored NO. Requiring a response to survivors is an instruction to
  clear a list rather than to understand one.

The refusal reuses the second-chance machinery, so it costs no extra budget and never
quotes the head run.

**On the ten evaluation instances the gate fired 9 times and 7 of those ended YES**, the
best result the set has produced. `sklearn-25232`, which the previous run left stopped on
a `verify` that had just said not-fail-to-pass, converted in four more actions.

One gap remains and it is structural: the refusal speaks only after the agent stops.
`sphinx-9602` spends ~95 of its 100 actions reading and is refused with nothing left to
spend, so it has now failed five runs out of five, untouched by any of this.

### A second chance, and the one thing it may not say

`--second-chance` refuses the agent's first stop. When a run ends with nothing a judge
could score, for a reason the agent could have seen itself, the harness says so and lets
it carry on -- once, in the same conversation, **on whatever is left of
`--max-iterations`**. A run that stopped at 41 of 100 resumes with 59; a run that reached
the cap gets nothing and the flow log says so. The budget is never topped up, so the flag
changes what the agent is told, not what it is allowed to spend.

It is one continuation, not a loop, and the trigger is the stop itself rather than a timer
or a tool call. That matters for the models it exists for: gpt-oss mostly does not end by
calling `finish` at all, it ends by emitting prose with no tool call, and both arrive at
the same place -- `run()` returns -- so one mechanism covers both.

**Why not have `verify` say it instead.** `verify` already does. It answers *"NOT
fail-to-pass: the test already passes before the change"* and *"...still fail after the
change is applied. The test is wrong, not the code."*, and `58-finish.md` already tells
the agent to call it last. The trouble is that it is opt-in and the agent that needs it
does not opt in. Across 28 weak-model runs:

| | YES | NO | rate |
|---|---|---|---|
| called `verify` | 8 | 2 | **80%** |
| never called it | 3 | 15 | **17%** |

For gpt-oss the split is absolute -- every YES called `verify`, and all twelve runs that
never called it failed. `django-13406` spent 41 actions in the shell with the tool
registered and untouched. A better message does not reach an agent that never asks, which
is why this is a stop the harness refuses rather than a sentence in a tool's output.

**What may be said.** `V.shortfall` returns a reason only for things the agent could have
established without leaving base -- there is no file, the file collects nothing, the test
passes on the unfixed code -- and `None` for everything else. *Your test still fails after
the fix* can never appear: it exists only in the head run, and quoting it back would have
the agent fit its test to a diff it was never shown, which is the one thing that would
stop the test being independent evidence about the pull request.

That is enforced by where the function sits, not by remembering: it runs before
`verify()`, calls `ensure_base()` first, and never applies the patch. A tree that is not
at base returns `None` rather than run a test against a state of unknown provenance.

The message also recaps the agent's own action counts, tools and files. That is the
cheapest thing on the safe side of the line, and "41 shell commands and no file written"
describes the failure where "you did not finish" only asserts it.

**Measured on twenty runs: the mechanism is right and the effect is small.** Ten instances
of the 26, run twice on `gpt-5-nano` with only this flag changing, plus ten on
`gpt-oss-20b`.

| | control | with the flag |
|---|---|---|
| `gpt-5-nano` | 5/10 | 5/10 |

The gate fired **once** in the nano pair, and that one converted: `pytest-10081` wrote a
test that passed at base, was told so, and rewrote it in **two actions of the eighty-two
it had left**. Every other movement in the table -- two YES going NO, one BROKEN going YES
-- happened on runs where the gate never fired, which is variance and not this.

**The reachable population is what limits it, and it depends on how the model fails.**

| failure | nano | gpt-oss |
|---|---|---|
| wrong test, head-only *(gate forbidden to speak)* | 5 | 2 |
| wrote nothing *(gate fires)* | 0 | 2 |
| passes at base *(gate fires)* | 1 | 1 |
| BROKEN, edited the tree | 3 | 0 |

The two models defeat the flag from opposite sides. `nano` writes a test nearly every
time and writes the wrong one, which is the head-only failure the boundary forbids acting
on -- so the gate is silent for four of its five failures. `gpt-oss` stops without writing,
which the gate catches, but it then answers the message with empty assistant turns: on
`django-13406` it spent 1227 reasoning tokens working out *"We'll just write file
tests/test_f2p_django__django_13406.py"* and emitted none of it, and the stuck detector
ended the run. Its four continuations converted nothing. On `gpt-5.5` and `gpt-5-mini`,
10/10 on the evaluation set, it would never fire at all.

So it is worth keeping and not worth planning around: free when it does not fire, correct
when it does, and addressed at a slice of the failures that is small on every model we
have. Across both pairs the gate fired five times and converted two.

What twenty runs did establish is that it is safe. It declined every head-only failure,
the budget arithmetic was right every time (97, 97, 95, 94, 82 from a cap of 100), and
`seaborn-3069`, which used all 100 actions, got `no budget left at the cap` and nothing
was spent.

**Measured again on qwen3-coder, and the same shape holds at a larger scale of firing.**
Ten evaluation instances, control against the flag, nothing else changed:

| | control | with the flag |
|---|---|---|
| `qwen3-coder-30b` | 5/10 | 6/10 |

This is the first pair where the gate fired on most of the set -- **seven of ten runs
refused**, four of them carrying a reason only this flag adds (`passes_at_base` three
times, `collects_nothing` once). Every refused run acted on the message, spending 1 to 12
further actions and never zero. One NO became a YES. One NO became a BROKEN: `django-13279`
was told `collects_nothing`, which was true, spent eight more actions and finished with a
file that still collected nothing. Correct diagnosis, worse outcome.

Two things that pair settles which the earlier twenty could not.

**Budget is not what limits it.** The smallest remaining budget was 66 actions and the
largest continuation spent 12. Nothing failed for want of room, which removes the first
explanation for the five that did not convert.

**What it cannot fix is the common failure.** Three of the five persistent NOs were told
`passes_at_base` -- the test runs, collects, and passes on unfixed code. They were told
exactly what was wrong, had 67 to 71 actions in hand, and still could not write a test that
distinguishes the two versions. That is a capability limit, and no message closes it. The
boundary that forbids quoting the head run is not what is holding this back; the model is.

And the flag is free: the arm ran 32 *fewer* actions than its control and cost four cents
less. The per-instance tables are in
[the comparison](../evaluation/qwen3coder-comparison/second-chance.md).

One caution attached to all three pairs. A single repeat of ten instances cannot separate 5
from 6 -- the same corpus has returned 4, 5 and 6 across recent configurations, and in this
pair the judge moved `xarray-7393` from `partial` to `complete` on an instance that was
never refused and never otherwise changed. That is the size of the noise, and it is the
size of the reported effect.

**The trap.** `Conversation.run()` resets its iteration counter to zero, so a second
`run()` inherits a fresh full cap. Left alone, one flag would have doubled what a run may
spend -- and silently, since both halves report normally. What is left of the cap is
computed and set on the conversation before the continuation.

### Five changes, and a score that never left the band

The five fixes above were each measured on the same ten held-out instances with
`gpt-5-nano`. The verdict counts, in order:

| | pre-regression | + tree guard | + config fix | + tools required | + outcome gate |
|---|---|---|---|---|---|
| YES | 6/10 | 5/10 | 6/10 | 5/10 | **7/10** |

**6, 5, 6, 5, 7.** Only three instances are stable across all five runs -- `requests-1766`,
`xarray-7393`, `pylint-7277`. Two never pass at all: `sphinx-9602` and `sympy-21612`, 0/5
each. The other five flip in both directions between runs that differ by one variable, and
in some cases by nothing that touches them.

So the corpus score cannot distinguish any of these changes from each other or from noise.
What it can distinguish is the mechanism, and each fix has a metric that moved
unambiguously at n=10:

| | before | after |
|---|---|---|
| instances that edited the library | 2/10 | **0/10** |
| actions lost to silently-dropped arguments | 47/329 | reported, not dropped |
| instrument calls (instances x tools) | 3/30 | **~24/30** |
| runs stopping on a negative `verify` | 4/5 failures | refused |

That split is the finding, and it is worth more than the 7. **A ten-instance set with five
unstable members has a noise floor wider than any effect this project has produced.**
Running further variants against it will keep returning fives and sixes whatever the
change, which is what experiment 0 exists to establish and why it now blocks the rest of
the queue rather than merely heading it.

Two consequences for how results are read here. Per-instance movement between runs is not
evidence about a change unless a log says why -- `astropy-13398` has been NO, NO, YES, NO,
YES across five runs and only the last has a trace behind it. And a mechanism metric that
moves at n=10 is a better argument than a verdict count that does not, because it is
measuring the thing the change actually did.

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
| `gpt-5.5` | 10/10 | 7/10 | \$7.42 | \$0.74 |
| `gpt-5-mini` | 10/10 | 4/10 | \$0.89 | \$0.09 |
| `gpt-5-nano` | 6/10 | 3/10 | \$0.34 | \$0.03 |
| `gpt-oss-20b` | 2/10 | 2/10 | \$0.24 | \$0.02 |

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

---

## Reaching the model through the gateway

Three things a run needed that no value in `models.json` could express, and one that a
value could once the field existed.

**The reply shape is not configuration.** `llm_adapters.py` already existed because
gpt-5.5 answers a tool-calling request with two choices and puts the call in the second.
qwen3-coder added a second case of the same kind: it sometimes writes Qwen's own syntax
into the message body and sends no `tool_calls` at all --

    finish_reason: stop
    content: "I'll start by exploring.\n\n<function=run>\n<parameter=command>\n
              find /testbed -name '*.py'\n</parameter>\n</function>\n</tool_call>"

-- and OpenHands reads a reply with no tool call as the agent finishing. `sympy-21612`
ended that way at action zero; `pylint-7277` hit it once in twenty-nine calls and survived
only because it happened mid-run. The model did everything right except the serialisation,
so the reply is repaired rather than the protocol changed: `salvages_xml_tool_calls` on the
profile, parsed back into real tool calls by a mixin. Emulated tool calling would have
changed every call to work around a fault in a few.

The two adaptations compose through mixins rather than four enumerated classes, because
they are independent and a model could need both.

**Which upstream serves a model is part of the experiment.** The gateway is a LiteLLM
proxy in front of OpenRouter, and it forwards body fields it does not recognise -- verified
by sending `provider.ignore` and watching the `provider` in the reply change. That made
`extra_body` worth a registry field: a per-model dict, deep-copied at construction, that
reaches past the gateway to whatever is behind it.

It was needed immediately. qwen3-coder defaulted to an upstream that returned messages with
no `content` key and no `tool_calls` key while billing 45 to 1000 completion tokens -- 113
of 244 replies in the first evaluation. Excluding it took the empty-reply count to zero
across 358 calls and turned a run that read as a model unable to call tools into one that
scored 5/10.

**But excluding one upstream is not pinning one.** The exclusion left three, and OpenRouter
chose between them per request. Two runs of the same configuration then landed on different
upstreams, and the second scored 8/10 at five times the cost. It was nearly written down as
the effect of the flag it was testing; what gave it away was that two of its three gains had
`second_chance: None` recorded against them -- the flag had not fired on the instances
credited to it.

So the field now names exactly one upstream and forbids fallback. **A configuration that
can be served by more than one provider is not a configuration**, and nothing in a result
says which one answered unless someone reads `provider` out of `completions/`.

Two measurements worth keeping from that accident. Prompt caching bought nothing: 91% of
prompt tokens came back marked cached and the bill was exactly the full list price for all
of them. And the price difference between upstreams is 4x on prompt and 5x on completion
for identical weights, the only declared difference being quantization.

---

## One obligation at a time

`require-tools` asked for three things at once: `verify` must last say fail-to-pass,
`coverage` must have been called, `mutation` must have been called. All three appeared in
the same refusal whatever state the run was in.

Two of them are questions about a test that already flips. Coverage asks how much of the
change a working test reaches; mutation asks what a working test would notice. Asked of a
test that does not flip, they are questions about something that does not exist yet -- and
the run showed exactly that: eight `coverage` and `mutation` calls before `verify` had ever
flipped, one of which `mutation` answered with *your test does not pass on the fixed code
yet*. The tool said the demand was premature. The demand was made anyway.

So they are checked in order now, and while the first is open it is the only thing said.
The agent gets one instruction it can act on instead of three, two of which it cannot.

The same ordering settles what runs after the agent stops. Coverage and the mutants were
already measured only on a test that flipped; the judge was not. Of the four NOs in the
qwen evaluation every one was *passes before the fix too*, and the judge graded all four on
concept, issue coverage and readability -- quality answers about something that has not met
the bar quality is measured against, at the price of the largest model in the registry. It
is gated on the verdict now, like everything else beside it.

**Where the rule is stated changed too.** It lived in the prompt block read once at the
start and in the refusal delivered after the agent had decided it was done -- neither of
them in front of it at the moment it reads a failing verdict and chooses what to do next.
The tools now carry it: a failing `verify` says *you cannot finish while this is the
answer*, and a coverage shortfall says the same, both only when `require-tools` is on, so
withholding the rule still withholds the enforcement.

`verify` also states the percentage again. It was withheld deliberately -- a score in front
of the agent is a score to raise -- and that was half right. Without it the agent had no
handle on how far from done it was while being told a rule expressed in exactly that
number. The figure is back, paired with the missed lines and their guard conditions, and
with the one sentence that keeps it honest: an assertion added only to execute a line is
worth less than an honest reason the line stays unreached.

**One branch was answering the wrong question.** A test that passes at base and fails at
head fell into the *still fail after the change* message, which is false -- it did not fail
before -- and points at rewriting rather than at inverting one assertion. It is the closest
near-miss the harness can see: the agent found the right behaviour and asserted the side of
it the change removes. It has its own branch now, ahead of the general one.

---

## `lstrip` takes a set of characters

`written_test_path` ended with `path.lstrip("./")`. Given the absolute
`/testbed/astropy/tests/x.py` the agent actually wrote, that returned
`testbed/astropy/tests/x.py` -- a repository-relative path naming a directory the
repository does not have.

Invisible for as long as nothing read it. The harness resolves its own target, so verdicts
were unaffected and the bug sat in the second-chance message as a path nobody checked.
`--second-chance` is what made it matter: `shortfall` reads that path off the disk, would
have found nothing, and would have told the agent `no_test` -- that its test did not exist
-- after it had written one six times. The most discouraging thing the harness can say, and
false.

`_relative()` strips the repository prefix as a prefix. The `passes_at_base` and
`collects_nothing` reasons appearing in
[the second-chance comparison](../evaluation/qwen3coder-comparison/second-chance.md) are the
first time those branches have been observed firing; before the fix every recorded reason
was `loop_open`.
