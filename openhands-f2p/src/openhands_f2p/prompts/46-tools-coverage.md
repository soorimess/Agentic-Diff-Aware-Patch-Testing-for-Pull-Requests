---
needs: coverage-tool
name: tools-coverage
job: Says what `coverage` is *for* -- a better test -- which the previous version left
  implicit while describing only what it reports. Sixteen of twenty-two agents never
  called it, and a tool whose purpose is not stated is a tool with no reason to be
  reached for. Present only with `--add-coverage-tool`, which needs the diff.

  Since 2026-10-19 (user) coverage and mutation are reports of `verify`, not tools.
---
**Coverage, reported by `verify`.** Once your test is fail-to-pass, every `verify` reports
its changed-line coverage — the share of the lines this pull request changed that your
test runs — and that number is one of those your test is scored on. The target is 100%.

It lists every changed line your test never runs, as line numbers grouped by the function
that holds them. The numbers are in the files *with* the change applied — the `+` side of
the diff — so read each line in the diff, with the conditions above it: those conditions
are what your input has to satisfy for the line to run at all.

Use it as a working instrument, not a final report: read the missed lines, add the case
they point at, call `verify` again — repeatedly. A test can flip from failing to passing
while running only part of what the change touched: it reaches the new code by a path that
skips a branch. That test still passes today, and it will still pass tomorrow if that
branch is broken again. The missed lines tell you which input you did not think of.

What you must never do is add code whose only purpose is to execute a line. A call with no
assertion behind it makes a line run and tests nothing, and it hides the gap from
everyone who reads the test afterwards, including you. Reach a line because the behaviour you
are asserting takes you through it.
