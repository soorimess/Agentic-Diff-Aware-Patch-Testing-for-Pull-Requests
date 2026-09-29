---
name: context
job: What each author could know, and how the two tests reach the judge. The first
  paragraph is the user's decision of 2026-09-28 (the judge knows which test is the
  developer's and looks for the experience behind its choices). The second is taken from
  the annotation study's judge (Task/llm_judge.py): the developer's test arrives as the
  lines a patch added to existing test files, the generated one as a whole file, and a
  judge that does not know that credits the one for being short and faults the other for
  building its own setup.
---
**What each author could know.** A choice in the developer's test that looks odd, narrow
or even like bad practice may come from experience the generated test's author did not
have: a security consequence (an escaping or permission path a django fix must not
reopen), backwards compatibility, an earlier regression in the same place, a platform or
database quirk, a convention this project enforces. Before you rank the generated test
higher on a point where it differs from the developer's choice, ask whether that choice
has such a reason -- visible in the report, in the fix (a comment, a guard, the shape of
the change), or in what a maintainer of this project would plausibly know. If it
plausibly does and the generated test lacks it, the generated test is not better on that
point; name the reason in `developer_reasons`. If you can find no such reason, do not
invent one, and do not penalise the generated test for not copying an arbitrary choice.

**How the two tests reach you.** The developer's test is the lines their patch *added* to
the project's existing test files. It can rely on fixtures, helpers, imports and base
classes already there that you are not shown, and it is often a few rows added to an
existing test. The generated test is a whole new file that builds its own setup. Compare
what the tests check, not how much code each needed: do not count the developer's
brevity for it, nor the generated test's own scaffolding against it.

**You cannot run either test.** Reason from the code; do not assume a result you cannot
derive from it. A long test may reach you elided: judge what you were given, and do not
report truncation, an unterminated string at the end of an excerpt, or a missing closing
bracket as a fault in either test.
