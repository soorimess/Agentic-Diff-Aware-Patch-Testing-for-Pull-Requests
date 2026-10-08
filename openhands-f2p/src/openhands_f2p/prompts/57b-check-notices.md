---
needs: mutation-tool
name: check-notices
job: The mutation step of the finishing sequence. Numbered between `coverage` and the
  stop condition because it is the last and strictest of the three questions, and it is
  only answerable once the test passes on the fixed code.

  Deliberately does not say "until none survive". Some survivors are not gaps, and an
  instruction to clear the board would turn the reasonable ones into padding.
---
**{?coverage-tool}4{/coverage-tool}{?!coverage-tool}3{/!coverage-tool}. `mutation` — would it notice a wrong fix?** Break the fix in small ways and see
whether your test objects. Whatever survives is a version of this change that is wrong in
a way your test cannot tell apart from the right one.

**Call it, and read what comes back.** It is the only check that asks whether your
assertions have any force, and a test that flips{?coverage-tool} and covers every line{/coverage-tool} can still pass
against a fix that is subtly wrong.

**Work every survivor.** For each, decide whether the behaviour it breaks is part of what
this pull request fixes. If it is, add the assertion about that behaviour and call
`verify` and `mutation` again. If it is not, leave it.{?require-tools} This is a loop, and
it is checked: while survivors remain you will be sent back to work them and call
`mutation` again, until none survives or an honest attempt catches no more -- what is left
then breaks nothing a test here can observe. A survivor you judged out of scope still brings
that one attempt: change the test to try to catch it and call `mutation`; if it catches no
more, the loop ends.{/require-tools} What you must not do is close
the list for its own sake: a run once answered `0 killed` by adding a
second test that failed on both sides, which turned a file whose first test flipped
correctly into no result at all. Keep `verify` saying fail-to-pass while you work.

Call it again after you change the test — a new assertion that closes one survivor often
closes others, and it can reveal ones the earlier version never reached.

Work through the survivors and decide about each, rather than trying to clear the list.
Where the broken behaviour is part of what the pull request fixes, add the assertion that
covers it; where it is not, say so to yourself and move on. Ending with survivors you have
considered and rejected is a good result. Ending with none because you asserted on
whatever each variant touched is not.
