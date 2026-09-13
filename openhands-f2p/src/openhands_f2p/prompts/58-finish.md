---
name: finish
job: The stop condition, on its own so that changing when the agent stops does not mean
  editing what it checks.

  Rewritten twice. The first version ended the sequence at its first step -- "when you see
  that, finish" sat in the same file as the run_tests check -- and agents duly stopped
  there. The second said "when the checks agree", which a flip satisfies on its own: in a
  three-instance test every agent called verify last and stopped on the same turn, having
  been shown the lines its test never reached and having done nothing with them.

  So the condition is no longer "the checks came back". It is that nothing a check raised
  is still unanswered. That is a stopping rule, not an instruction to raise a number, and
  it stays true whether or not anyone is scoring the result.
---
A check that tells you something and gets no response was not worth running. If one shows
a failure, fix the test and run it again.
{?coverage-tool}
If one shows lines of the change your test never reached, decide what they are -- part of
the behaviour you set out to pin down and so worth another assertion, a separate case that
deserves its own test function, or genuinely outside what this test is for -- and act on
that decision.

None of these figures is a target. They are the same question asked from different angles
— is the behaviour I asserted really the behaviour this pull request changed — and a
number is only worth what the test behind it is worth. Adding a call with no assertion
behind it answers nothing.
{/coverage-tool}

You are finished when no check has raised something you have not answered. Say in one
sentence what behaviour your test pins down, and stop.
