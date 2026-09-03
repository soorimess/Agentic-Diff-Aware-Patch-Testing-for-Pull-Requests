---
name: finish
job: The stop condition, on its own so that changing when the agent stops does not mean
  editing what it checks. The previous wording ended the sequence at its first step --
  "when you see that, finish" sat in the same file as the run_tests check -- and agents
  duly stopped there: sixteen of twenty-two never called `coverage` at all.
---
Fix and re-run a check whenever it tells you something is wrong, rather than moving on.

None of these figures is a target. They are the same question asked from different angles
— is the behaviour I asserted really the behaviour this pull request changed — and a
number is only worth what the test behind it is worth.

When the checks agree, say in one sentence what behaviour your test pins down, and finish.
