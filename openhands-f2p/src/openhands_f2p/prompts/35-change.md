---
needs: patch
name: change
job: The pull request's diff, framed as evidence to interpret rather than a target to
  satisfy. The closing instruction used to be "the test has to run the lines above",
  which restates our coverage metric; it now asks the agent to work out the behavioural
  difference, which is the thing the metric is a proxy for.

  Why the diff is shown at all: our reference paper (Haratian et al., PR-Aware Automated
  Unit Test Generation) says "We provide the model with the PR's code difference (the
  diff), the whole source file, and any existing tests", so a comparison against that
  work needs the same input. What stays hidden is `test_patch`, the developer's test --
  the assignment is explicit about that one and only that one.

  The closing paragraph on choosing inputs was added after `seaborn-3187`. Its test
  executed every changed line and still could not tell the patch from its absence: the
  change disables an additive offset, and the values it used were nowhere near the range
  where matplotlib would have applied one. Coverage said 100%, a mutant flipping that very
  flag survived, and the judge independently reported the behaviour uncovered. Reaching a
  line and discriminating on it are different properties, and nothing in the prompt had
  asked for the second.

  It names no metric, which is the test for whether it belongs here: an input that cannot
  distinguish the two versions is a bad test whether or not anyone is scoring it.

  Dropped by `--no-patch`, which is the harder task and the one comparable to TDD-Bench baselines.
---
## What this pull request changes

```diff
{patch}
```

Read it as evidence, not as a specification to copy. Ask what a caller can observe that
differs before and after: a different return value, an exception that is or is not
raised, a side effect that now happens. Then write the test around that observable
difference.

A change is not always one behaviour. Read every hunk, and every branch it adds or
removes, and work out what each one does for a caller: a condition that now holds, a path
that is now taken, a case that is now handled differently. Understanding the change means
being able to say what it does everywhere it acts, not only where you first recognised
it.

Then choose inputs the difference is visible in. Many changes are silent for most values:
a mode turned off does nothing until the input is one the mode would have acted on, a
widened bound matters only just outside the old one, an extra case matters only in that
case. Feed such a change ordinary data and both versions agree, and the test is
indistinguishable from one that asserts nothing about it. So for each difference you
found, say what the old code would have produced for the input you picked -- if the
answer is "the same thing", that input does not test this change and you need a
different one.
