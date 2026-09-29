---
needs: mutation-tool
name: tools-mutation
job: Says what `mutation` is for, and how to read a survivor without gaming it.

  This is the sharpest instrument in the set and the easiest to cheat, so the wording
  carries more weight than the others. A surviving mutant can always be killed: assert
  on the exact expression the mutant changed and it dies, whatever that assertion has to
  do with the behaviour. That test kills the mutant and tells a reader nothing.

  So the piece frames a survivor as a *question* rather than a defect -- "would a
  reviewer call this part of what the change fixes?" -- and says outright that the
  answer is sometimes no. An instruction that only said "kill them all" would produce
  tests shaped like the mutation operators.

  The honesty check this project uses: would this be correct advice if nobody were
  scoring? "Break the fix and see if your test notices" is what a careful developer does
  before opening a pull request. It survives the test.
---
- `mutation` — breaks the fix in small ways on purpose, runs your test against each
  broken version, and tells you which ones your test still passes on. A variant your test
  does not notice is a behaviour this change makes that your test does not check.

Use it, and act on what it says. A test can flip from failing to passing{?coverage-tool}, execute every
changed line,{/coverage-tool} and still be satisfied by a fix with a comparison inverted or a boundary off
by one{?coverage-tool} — coverage says the line *ran*, this says whether you would have *noticed* it going
wrong{/coverage-tool}. That is the difference between a test that documents the fix and a test that
merely accompanies it.

{?require-tools-with-score-report}
In this run it also reports your mutation score -- the share of wrong versions caught --
and that number is one of the two your test is scored on. Maximise it, by the route below
and no other: some survivors break nothing a test can observe, and no honest test catches
them -- an attempt that catches no more ends the loop. Asserting on the exact expression a
variant changed raises the number and makes the test worse.

{/require-tools-with-score-report}
Every survivor gets an answer. Read each one as a question, not as a defect to clear:

- **Would a reviewer call the behaviour it breaks part of what this pull request fixes?**
  If yes, your test is missing an assertion about that behaviour — add the one that
  asserts it (what the code returns, raises or does for an input that tells the right fix
  from this wrong one), and the variant dies as a consequence. Then run `verify` and
  `mutation` again.
- **Or does the variant break something the change was never about**, or nothing
  observable at all? Then say so, in one sentence, and leave it. Not every survivor is a
  gap, and a test stretched to cover one that is not gets worse, not better.

A survivor you have not answered either way is the one thing this tool exists to prevent:
a wrong fix your test would let through without anyone having decided that is acceptable.

What you must never do is write an assertion whose purpose is to kill a mutant. Pinning
the exact expression a variant happened to change — asserting on an internal value, or
restating the implementation — kills it and checks nothing a reader would recognise as
behaviour. A test like that passes every instrument here and is worthless to the next
person who has to maintain it, which is the only audience that matters.
