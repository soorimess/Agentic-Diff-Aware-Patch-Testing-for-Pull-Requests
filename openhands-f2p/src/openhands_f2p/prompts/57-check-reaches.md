---
needs: coverage-tool
name: check-reaches
job: Step three, plus how to read a low figure. Present only with `--add-coverage-tool`, which needs the diff.

  Rewritten twice. The first version said "iterate until both answer well" -- an
  instruction to maximise the numbers we score by, which makes a high number evidence of
  obedience rather than of a good test. The second went too far the other way: "neither is
  a score to raise" was nearly all it said, and reads as a reason not to bother.

  Since 2026-10-19 (user) coverage and mutation are reports of `verify`, not tools.
---
**3. Coverage — does it reach the change?** A test can flip while running only part of
what the change touched: it gets to the new code by a route that skips a branch. That test
passes today and will still pass tomorrow if that branch breaks again. Once your test
flips, every `verify` reports its changed-line coverage and lists the changed lines it
never runs, by function; the conditions above each one, read in the diff, say what your
input has to satisfy to get there.

**Read the missed lines, and change the test before you stop.** The target is 100%: a test
that runs every line the change touched.{?require-tools} That is a loop, and it is checked:
while coverage is below 100% you will be sent back to change the test and call `verify`
again, one part of the change at a time -- each function holding a missed line gets one
turn -- until it reaches 100% or every part has had its turn.{/require-tools} It is not a
demand that every line runs whatever it takes — sometimes a line is genuinely outside what
this test is for — it is a demand that each missed line gets an answer rather than being
noted and passed over. Decide what the missed lines are, change the test, call `verify`
again. Keep going until what remains is missed for a reason you can state in a sentence.

Missed lines are not a bad mark. They are a description of your test, usually a precise one:
the change has more than one path through it and you took one. So ask whether the missed
lines are the same behaviour reached another way -- one more assertion normally covers
that -- or a genuinely separate case the same pull request also fixed, which deserves a
second test rather than an assertion stretched to reach it.

What you must not do is add code whose only purpose is to execute a line. A call with no
assertion after it makes a line run and tests nothing, and it hides the gap from
everyone who reads the test afterwards, including you.
