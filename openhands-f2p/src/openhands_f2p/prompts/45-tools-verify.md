---
name: tools-verify
job: Introduces `verify` as the property the test must have rather than a score. Separable
  because it only exists once the diff is an input: with the patch withheld there is
  nothing for the agent to verify against.
---
Because the change is given to you, you can check your work against it rather than
guessing whether it is right:

- `verify` — runs your test against the code before the change, applies the change, runs
  it again, then puts the code back. It reports which of your tests failed before and
  passed after.

That before-and-after flip is the property your test has to have. A test that passes in
both states is testing something this pull request did not change; a test that fails in
both is broken rather than strict. `verify` is how you find out which, while you can
still do something about it — so call it before you finish, not as a formality but
because it is the only thing that distinguishes a regression test from a test that
merely runs.
