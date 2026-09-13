---
needs: verify-tool
name: check-flips
job: Step two. Dropped with the diff, since `verify` needs the patch to have a second
  state to run against.
---
**2. `verify` — does it flip?** Failing before the change and passing after is the
property the test exists to have. If it passes on both sides, you asserted something this
pull request does not affect. If it fails on both, the test itself is wrong rather than
strict. This is the one check that distinguishes a regression test from a test that merely
runs, so do not skip it on the grounds that the test looks right.
