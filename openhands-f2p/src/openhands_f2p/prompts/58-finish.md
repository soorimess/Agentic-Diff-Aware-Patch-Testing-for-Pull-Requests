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
None of these is a score to push up. They are the same question asked from different
angles — is the behaviour I asserted really the behaviour this pull request changed — and
each answer is only worth what the test behind it is worth. Adding a call with no assertion
behind it answers nothing.
{/coverage-tool}

**Then: did you change the test after any check?** If you did, the checks above describe
a file that no longer exists. Run them again on what is actually on disk — that is the
loop, not a formality.
{?verify-tool}
The last thing you run before finishing should be `verify`: an assertion added to close
anything else can quietly stop the test failing on the old code.
{/verify-tool}

{?second-chance}
{?verify-tool}
**Before you can stop, the last `verify` must say fail-to-pass, and you must not have
edited the test since** — an answer about a file you have changed is an answer about a
file that no longer exists. Until it does say so, this is the only thing worth spending an
action on: rewrite the test and call `verify` again, as many times as it takes. This is
checked by its answer, not by whether you called it; a stop before it says fail-to-pass
is sent back with the reason.
{/verify-tool}
{/second-chance}
{?require-tools}

**Once `verify` says fail-to-pass, the checks after it are checked by their answers, in
this order.** Each is a question about a test that already flips, so work them in
sequence:
{?coverage-tool}
- `coverage`: aim for a test that runs every line the change touched. If it lists lines
  your test never runs, you must have acted on that — either made them run, or
  established that a line cannot be reached from a test. An assertion added only to
  execute a line is worth less than an honest reason the line stays unreached;
{/coverage-tool}
{?mutation-tool}
- `mutation`: every survivor answered — an assertion about the behaviour it breaks when
  that behaviour is part of what this pull request fixes, or one sentence saying why it
  is not.
{/mutation-tool}

Calling a tool once and stopping on an answer you did nothing with does not satisfy this.
If any of these is open you will be sent back with the reason, so closing it now is the
shorter path.
{/require-tools}

You are finished when the checks above have been run against the test as it now stands
and nothing any of them raised is still unanswered. Say in one sentence what behaviour your test pins down, and stop.
