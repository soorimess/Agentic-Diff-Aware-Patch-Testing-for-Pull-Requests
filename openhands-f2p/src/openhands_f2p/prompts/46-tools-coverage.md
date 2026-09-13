---
needs: coverage-tool
name: tools-coverage
job: Says what `coverage` is *for* -- a better test -- which the previous version left
  implicit while describing only what it reports. Sixteen of twenty-two agents never
  called it, and a tool whose purpose is not stated is a tool with no reason to be
  reached for. Dropped by `--no-coverage-tool`, and with the diff, since the tool needs it.
---
- `coverage` — of the lines this pull request changed, which ones did your test actually
  execute. For each line it missed, you are shown that line's source and the conditions
  above it; those conditions are what your input has to satisfy for the line to run at
  all.

This exists to make the test better, and there is a specific way it does that. A test can
flip from failing to passing while running only part of what the change touched — it
reaches the new code by a path that skips a branch. That test still passes today, and it
will still pass tomorrow if that branch is broken again. The missed lines tell you which
input you did not think of.

Coverage only means something for a test that already flips: asking how much of the change
a test exercised presumes the test exercises the change. So the order is `verify` first,
then `coverage` — and that is also the only case we measure, so a coverage figure for a
test that does not flip is not recorded at all.
