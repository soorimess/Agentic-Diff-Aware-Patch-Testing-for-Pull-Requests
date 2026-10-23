---
name: finish
job: The stop condition, on its own so that changing when the agent stops does not mean
  editing what it checks.

  Rewritten twice. The first version ended the sequence at its first step -- "when you see
  that, finish" sat in the same file as the run_tests check -- and agents duly stopped
  there. The second said "when the checks agree", which a flip satisfies on its own: in a
  three-instance test every agent called verify last and stopped on the same turn, having
  been shown the lines its test never reached and having done nothing with them.

  So the condition became "nothing a check raised is still unanswered" -- and that had a
  hole in it, found on the first run with the `mutation` tool registered. A check that is
  never run raises nothing, so running *none* satisfied it: the agent wrote its test,
  called `verify`, and stopped after five actions having touched neither `coverage` nor
  `mutation`. Both were in the prompt, described, and numbered.

  So the condition now names both halves: run them, then answer what they raised. That is
  still a stopping rule rather than an instruction to raise a number -- "check your work
  before calling it done" is advice that holds with nobody scoring.

  The re-run step is phrased as another step for a reason found by watching. The agent
  follows the numbered sequence literally -- `run_tests`, `verify`, `coverage`,
  `mutation`, stop -- and two rewrites of the surrounding prose telling it to iterate
  changed nothing: same one call each, same survivor left alive. Prose does not compete
  with a numbered list. A step does.

  Since 2026-10-19 (user) coverage and mutation are reports of `verify`, and the score
  text is the default (the score-report flag is gone).
---
A check that tells you something and gets no response was not worth running. If one shows
a failure, fix the test and run it again.
{?coverage-tool}
If `verify` shows lines of the change your test never reached, decide what they are -- part
of the behaviour you set out to pin down and so worth another assertion, a separate case
that deserves its own test, or genuinely outside what this test is for -- and act on that
decision.
{/coverage-tool}
{?mutation-tool}
If `verify` shows a wrong version of the fix your test did not object to, decide whether
that behaviour is part of what the change fixes -- and if it is, assert it. If it is not,
that survivor is an answer, not an outstanding item.
{/mutation-tool}
{?verify-tool}
**Your test is scored on whether it is fail-to-pass{?coverage-tool}, on its changed-line
coverage{/coverage-tool}{?mutation-tool}, and on its mutation score{/mutation-tool}, and `verify`
shows you {?coverage-tool}each{/coverage-tool}{?!coverage-tool}{?mutation-tool}each{/mutation-tool}{?!mutation-tool}it{/!mutation-tool}{/!coverage-tool}.**
{?coverage-tool}
- Changed-line coverage, the share of the lines this pull request changed that your test
  runs. **Its target is 100%**: raise it until every changed line runs, or until the lines
  left cannot be reached from a test.
{/coverage-tool}
{?mutation-tool}
- Mutation score, the share of wrong versions of the fix your test catches. **Maximise
  it**: catch every survivor that breaks behaviour a test can observe; the ones that break
  nothing observable are what is left when an honest attempt catches no more.
{/mutation-tool}

Raise a score the way a better test raises it: an input that takes the test somewhere it
did not go, an assertion about behaviour a wrong fix would break. A call with no assertion
behind it, or an assertion on an exact expression written only to move the number, is not
a better test.
{/verify-tool}

**Then: did you change the test after any check?** If you did, {?verify-tool}the answers above describe{/verify-tool}{?!verify-tool}the check above describes{/!verify-tool}
a file that no longer exists. Run {?verify-tool}`verify`{/verify-tool}{?!verify-tool}it{/!verify-tool} again on what is actually on disk — that is the
loop, not a formality.
{?verify-tool}
The last thing you run before finishing should be `verify`: an assertion added to close
anything else can quietly stop the test failing on the old code.
{/verify-tool}

{?require-tools}
{?verify-tool}
**Before you can stop, the last `verify` must say fail-to-pass, and you must not have
edited the test since** — an answer about a file you have changed is an answer about a
file that no longer exists. Until it does say so, this is the only thing worth spending an
action on: rewrite the test and call `verify` again, as many times as it takes. This is
checked by its answer, not by whether you called it; a stop before it says fail-to-pass
is sent back with the reason.
{/verify-tool}

{?coverage-tool}
**Once `verify` says fail-to-pass, what it reports after that is checked too, in this
order:**
- coverage, as a loop with a score: your changed-line coverage must reach 100%. While it
  is below, change the test and call `verify` again, until it does or every part of the
  change (each function holding a missed line) has had its turns -- a part keeps its turns
  while each one runs more of its lines, and a first turn that runs none of them gets a
  second one;
{?mutation-tool}
- mutation, as a loop with a score: maximise your mutation score. While variants survive,
  add assertions about the behaviour they break and call `verify` again, until none
  survives or an honest attempt catches no more.
{/mutation-tool}

Reading a report and stopping on an answer you did nothing with does not satisfy this.
While any of these loops is open you will be sent back with the reason, so working it now
is the shorter path.
{/coverage-tool}
{?!coverage-tool}
{?mutation-tool}
**Once `verify` says fail-to-pass, what it reports after that is checked too, in this
order:**
- mutation, as a loop with a score: maximise your mutation score. While variants survive,
  add assertions about the behaviour they break and call `verify` again, until none
  survives or an honest attempt catches no more.

Reading a report and stopping on an answer you did nothing with does not satisfy this.
While any of these loops is open you will be sent back with the reason, so working it now
is the shorter path.
{/mutation-tool}
{/!coverage-tool}
{/require-tools}

You are finished when {?verify-tool}the checks above have{/verify-tool}{?!verify-tool}the check above has{/!verify-tool} been run against the test as it now stands
and nothing {?verify-tool}any of them{/verify-tool}{?!verify-tool}it{/!verify-tool} raised is still unanswered. Say in one sentence what behaviour your test pins down, and stop.
