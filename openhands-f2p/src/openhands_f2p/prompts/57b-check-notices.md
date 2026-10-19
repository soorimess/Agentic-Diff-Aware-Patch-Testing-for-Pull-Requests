---
needs: mutation-tool
name: check-notices
job: The mutation step of the finishing sequence. Numbered between `coverage` and the
  stop condition because it is the last and strictest of the three questions, and it is
  only answerable once the test passes on the fixed code.

  Deliberately does not say "until none survive". Some survivors are not gaps, and an
  instruction to clear the board would turn the reasonable ones into padding.

  Since 2026-10-19 (user) coverage and mutation are reports of `verify`, not tools.
---
**{?coverage-tool}4{/coverage-tool}{?!coverage-tool}3{/!coverage-tool}. Mutation — would it notice a wrong fix?** Once your test flips, every
`verify` also breaks the fix in small ways and reports which broken versions your test
still passes on. Whatever survives is a version of this change that is wrong in a way your
test cannot tell apart from the right one.

**Read what comes back.** It is the only check that asks whether your assertions have any
force, and a test that flips{?coverage-tool} and covers every line{/coverage-tool} can still
pass against a fix that is subtly wrong.

**Work every survivor.** For each, decide whether the behaviour it breaks is part of what
this pull request fixes. If it is, add the assertion about that behaviour and call `verify`
again. If it is not, leave it.{?require-tools} This is a loop, and it is checked: while
survivors remain you will be sent back to work them and call `verify` again, until none
survives or an honest attempt catches no more -- what is left then breaks nothing a test
here can observe. A survivor you judged out of scope still brings that one attempt: change
the test to try to catch it and call `verify`; if it catches no more, the loop
ends.{/require-tools} What you must not do is close the list for its own sake: a run once
answered `0 killed` by adding a second test that failed on both sides, which turned a file
whose first test flipped correctly into no result at all. Keep `verify` saying
fail-to-pass while you work.

Ending with survivors you have considered and rejected is a good result. Ending with none
because you asserted on whatever each variant touched is not.
