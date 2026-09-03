---
name: check-runs
job: Step one of the finishing sequence, and the only step that exists in every arm --
  `run_tests` is registered whether or not the diff was given. Split from the other checks
  so the blind arm does not read instructions about tools it was never handed, which is
  what happened when all three steps lived in one file.
---
## Before you finish

Work through these checks in order. Each one answers a question the previous leaves open,
and each catches a mistake the others do not.

**1. `run_tests` — does the file run at all?** A test that errors on an import, a typo or
a missing fixture tells you nothing about the library; it never reached the code. What you
want to see here is the library behaving the old way: an assertion that does not hold, or
the wrong exception coming back.
