---
name: check-runs
job: Step one of the finishing sequence, and the only step that exists in every configuration --
  `run_tests` is registered whether or not the diff was given. Split from the other checks so a configuration without `verify` does not read instructions about tools it was never handed, which is what happened when all three steps lived in one file. The multi-check framing is gated too: with one check left, "work through these in order" describes nothing.
---
## Before you finish
{?verify-tool}

Work through these checks in order. Each one answers a question the previous leaves open,
and each catches a mistake the others do not.

They are not all the same kind of thing. The first two are gates: the file runs, and the
test flips. The ones after them are instruments you work with — call one, change the test
in the light of what it says, call it again, as many times as it takes. Nothing here is a
one-shot formality, and none of these tools costs anything but time; each puts the tree
back exactly as it found it, so you can call any of them whenever you want. When you are
done changing the test, run `verify` once more: an assertion added for any other reason
can quietly stop the test failing on the old code, and then it is no longer the test you
set out to write.
{/verify-tool}

**1. `run_tests` — does the file run at all?** A test that errors on an import, a typo or
a missing fixture tells you nothing about the library; it never reached the code. What you
want to see here is the library behaving the old way: an assertion that does not hold, or
the wrong exception coming back.
