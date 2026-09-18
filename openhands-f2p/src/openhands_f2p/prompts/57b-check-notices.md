---
needs: mutation-tool
name: check-notices
job: The mutation step of the finishing sequence. Numbered between `coverage` and the
  stop condition because it is the last and strictest of the three questions, and it is
  only answerable once the test passes on the fixed code.

  Deliberately does not say "until none survive". Some survivors are not gaps, and an
  instruction to clear the board would turn the reasonable ones into padding.
---
**4. `mutation` — would it notice a wrong fix?** Break the fix in small ways and see
whether your test objects. Whatever survives is a version of this change that is wrong in
a way your test cannot tell apart from the right one.

Call it again after you change the test — a new assertion that closes one survivor often
closes others, and it can reveal ones the earlier version never reached.

Work through the survivors and decide about each, rather than trying to clear the list.
Where the broken behaviour is part of what the pull request fixes, add the assertion that
covers it; where it is not, say so to yourself and move on. Ending with survivors you have
considered and rejected is a good result. Ending with none because you asserted on
whatever each variant touched is not.
