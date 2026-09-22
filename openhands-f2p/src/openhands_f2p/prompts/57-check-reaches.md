---
needs: coverage-tool
name: check-reaches
job: Step three, plus how to read a low figure. Dropped with the diff, and by `--no-coverage-tool` on its own.

  Rewritten twice. The first version said "iterate until both answer well" -- an
  instruction to maximise the numbers we score by, which makes a high number evidence of
  obedience rather than of a good test. The second went too far the other way: "neither is
  a score to raise" was nearly all it said, and reads as a reason not to bother.
---
**3. `coverage` — does it reach the change?** A test can flip while running only part of
what the change touched: it gets to the new code by a route that skips a branch. That test
passes today and will still pass tomorrow if that branch breaks again. The missed lines
are the inputs you did not think of, and the conditions printed above each one say what
your input has to satisfy to get there.

**Call `coverage`, and if it comes back under 100%, change the test before you stop.**
That is the rule, and it is checked: a run that reads a shortfall and does nothing about
it will be sent back. It is not a demand for 100% — often the remaining lines are
genuinely outside what this test is for — it is a demand that a shortfall gets answered
once rather than noted and passed over. Decide what the missed lines are, change the test,
call `coverage` again; you do not need to re-run the earlier checks in between. Keep going
until what remains is missed for a reason you can state in a sentence.

A low figure is not a bad mark. It is a description of your test, usually a precise one:
the change has more than one path through it and you took one. So ask whether the missed
lines are the same behaviour reached another way -- one more assertion normally covers
that -- or a genuinely separate case the same pull request also fixed, which deserves a
second test function rather than an assertion stretched to reach it.

What you must not do is add code whose only purpose is to execute a line. A call with no
assertion after it raises the number and tests nothing, and it makes the figure useless to
everyone who reads it afterwards, including you.
