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
test flips.{?coverage-tool} The ones after them are what `verify` reports once the test
flips, and they are instruments you work with — read the report, change the test in the
light of it, call `verify` again, as many times as it takes.{/coverage-tool}{?!coverage-tool}{?mutation-tool} The one after them is what `verify` reports once the test
flips, and it is an instrument you work with — read the report, change the test in the
light of it, call `verify` again, as many times as it takes.{/mutation-tool}{/!coverage-tool} Nothing here is a
one-shot formality, and none of it costs anything but time; `verify` puts the tree back
exactly as it found it, so you can call it whenever you want. When you are
done changing the test, run `verify` once more: an assertion added for any other reason
can quietly stop the test failing on the old code, and then it is no longer the test you
set out to write.
{/verify-tool}

{?verify-tool}**1. `run_tests` — does the file run at all?**{/verify-tool}{?!verify-tool}**`run_tests` — does the file run at all?**{/!verify-tool} A test that errors on a typo, a missing
fixture or a name this project never had tells you nothing about the library; it never
reached the code. A name the change *adds* is different: here it does not exist yet, so an
`ImportError`, `AttributeError` or `TypeError` about it is exactly the old behaviour, and a
test that uses it the way the change intends fails here for the right reason. Do not catch
or skip that error to make the test pass on this code. What you want to see here is the
library behaving the old way: an assertion that does not hold, the wrong exception coming
back, or a name the change adds not being there yet.
