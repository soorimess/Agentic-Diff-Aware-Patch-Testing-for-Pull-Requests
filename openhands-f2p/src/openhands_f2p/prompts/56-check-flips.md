---
needs: verify-tool
name: check-flips
job: Step two. Dropped with the diff, since `verify` needs the patch to have a second
  state to run against.
---
**2. `verify` — does it flip?** Failing before the change and passing after is the
property the test exists to have, and `verify` is the only thing here that answers it.

**Call `verify`, and keep calling it until it says fail-to-pass.** That is the loop, and
it is not optional: a test you have not run through `verify` is a guess, however right it
looks. Each answer tells you which way to move — passes on both sides means you asserted
something this pull request does not affect, so find what the change actually alters;
fails on both means the test itself is wrong rather than strict, so fix the test, not the
assertion's strength. Change the test, call `verify` again, and repeat. You are not done
with this step until it reports fail-to-pass.
