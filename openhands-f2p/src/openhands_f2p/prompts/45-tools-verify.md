---
needs: verify-tool
name: tools-verify
job: Introduces `verify` as the property the test must have rather than a score. Separable
  because it only exists once the diff is an input: with the patch withheld there is
  nothing for the agent to verify against.

  Since 2026-10-19 (user) coverage and mutation are reports of `verify`, not tools.
---
You can check your work against the change rather than guessing whether it is right:

- `verify` — runs your test against the code before the change, applies the change, runs
  it again, then puts the code back. It reports which of your tests failed before and
  passed after.{?coverage-tool} Once your test is fail-to-pass, the same call also reports
  its coverage of the change: the share of the lines this pull request changed that your
  test runs, and every changed line it never runs.{/coverage-tool}{?mutation-tool} Once your
  test is fail-to-pass, the same call also runs it against small wrong versions of the fix
  and reports its mutation score and every wrong version it does not notice.{/mutation-tool}

That before-and-after flip is the property your test has to have, and it is the main goal.
A test that passes in both states is testing something this pull request did not change; a
test that fails in both is broken rather than strict. `verify` is how you find out which,
while you can still do something about it — so call it before you finish, not as a
formality but because it is the only thing that distinguishes a regression test from a
test that merely runs.{?coverage-tool} Once it flips, aim for 100% coverage of the
change.{/coverage-tool}{?mutation-tool} Once it flips, catch as many of the wrong versions
as you can.{/mutation-tool}
