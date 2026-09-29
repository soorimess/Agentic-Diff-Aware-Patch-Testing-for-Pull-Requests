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
---
A check that tells you something and gets no response was not worth running. If one shows
a failure, fix the test and run it again.
{?coverage-tool}
If one shows lines of the change your test never reached, decide what they are -- part of
the behaviour you set out to pin down and so worth another assertion, a separate case that
deserves its own test, or genuinely outside what this test is for -- and act on
that decision.
{/coverage-tool}
{?mutation-tool}
If one shows a wrong version of the fix your test did not object to, decide whether that
behaviour is part of what the change fixes -- and if it is, assert it. If it is not, that
survivor is an answer, not an outstanding item.
{/mutation-tool}
{?coverage-tool}
{?!require-tools-with-score-report}
None of these is a score to push up. They are the same question asked from different
angles — is the behaviour I asserted really the behaviour this pull request changed — and
each answer is only worth what the test behind it is worth. Adding a call with no assertion
behind it answers nothing.
{/!require-tools-with-score-report}
{/coverage-tool}
{?require-tools-with-score-report}
**In this run your test is scored, and you are shown the score:**
{?coverage-tool}
- changed-line coverage, the share of the lines this pull request changed that your test
  runs, reported by `coverage`. **Its target is 100%**: raise it until every changed line
  runs, or until the lines left cannot be reached from a test;
{/coverage-tool}
{?mutation-tool}
- mutation score, the share of wrong versions of the fix your test catches, reported by
  `mutation`. **Maximise it**: catch every survivor that breaks behaviour a test can
  observe; the ones that break nothing observable are what is left when an honest attempt
  catches no more.
{/mutation-tool}

Raise a score the way a better test raises it: an input that takes the test somewhere it
did not go, an assertion about behaviour a wrong fix would break. A call with no assertion
behind it, or an assertion on an exact expression written only to move the number, is not
a better test.
{/require-tools-with-score-report}

**Then: did you change the test after any check?** If you did, the checks above describe
a file that no longer exists. Run them again on what is actually on disk — that is the
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

**Once `verify` says fail-to-pass, the checks after it are checked by their answers, in
this order.** Each is a question about a test that already flips, so work them in
sequence:
{?coverage-tool}
{?!require-tools-with-score-report}
- `coverage`, as a loop: while it lists lines your test never runs, change the test and
  call it again, until every changed line runs or an honest attempt reaches no more. An
  assertion added only to execute a line does not count;
{/!require-tools-with-score-report}
{?require-tools-with-score-report}
- `coverage`, as a loop with a score: your changed-line coverage must reach 100%. While it
  is below, change the test and call it again, until it does or an honest attempt raises
  it no further;
{/require-tools-with-score-report}
{/coverage-tool}
{?mutation-tool}
{?!require-tools-with-score-report}
- `mutation`, as a loop: while variants survive, add assertions about the behaviour they
  break and call it again, until none survives or an honest attempt catches no more.
{/!require-tools-with-score-report}
{?require-tools-with-score-report}
- `mutation`, as a loop with a score: maximise your mutation score. While variants
  survive, add assertions about the behaviour they break and call it again, until none
  survives or an honest attempt catches no more.
{/require-tools-with-score-report}
{/mutation-tool}

Calling a tool once and stopping on an answer you did nothing with does not satisfy this.
While any of these loops is open you will be sent back with the reason, so working it now
is the shorter path.
{/require-tools}

You are finished when the checks above have been run against the test as it now stands
and nothing any of them raised is still unanswered. Say in one sentence what behaviour your test pins down, and stop.
