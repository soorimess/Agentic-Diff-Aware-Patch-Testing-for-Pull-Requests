---
needs: coverage-tool
name: tools-coverage
job: Says what `coverage` is *for* -- a better test -- which the previous version left
  implicit while describing only what it reports. Sixteen of twenty-two agents never
  called it, and a tool whose purpose is not stated is a tool with no reason to be
  reached for. Present only with `--add-coverage-tool`, which needs the diff.
---
- `coverage` — of the lines this pull request changed, which ones did your test actually
  execute. For each line it missed, you are shown that line's source and the conditions
  above it; those conditions are what your input has to satisfy for the line to run at
  all.

Aim for a test that runs every line the change touched, and reach each one through the
behaviour you are asserting. Use `coverage` to see which lines yours still misses, and
act on what it says — repeatedly. This is a working instrument, not a final
report: measure, add the case the missed lines point at, measure again. It applies the
change and reverts it itself, so calling it costs you nothing and leaves nothing behind.
Start using it once `verify` says your test is fail-to-pass: before that, which lines run
is not yet the question.

{?require-tools-with-score-report}
In this run it also reports your changed-line coverage as a percentage, and that number is
one of the two your test is scored on. Aim for 100%.

{/require-tools-with-score-report}
This exists to make the test better, and there is a specific way it does that. A test can
flip from failing to passing while running only part of what the change touched — it
reaches the new code by a path that skips a branch. That test still passes today, and it
will still pass tomorrow if that branch is broken again. The missed lines tell you which
input you did not think of.

Coverage only means something for a test that already flips: asking how much of the change
a test exercised presumes the test exercises the change. So the order is `verify` first,
then `coverage` — and that is also the only case we measure, so coverage of a test that
does not flip is not recorded at all.

What you must never do is add code whose only purpose is to execute a line. A call with no
assertion behind it makes a line run and tests nothing, and it hides the gap from
everyone who reads the test afterwards, including you. Reach a line because the behaviour you
are asserting takes you through it.
