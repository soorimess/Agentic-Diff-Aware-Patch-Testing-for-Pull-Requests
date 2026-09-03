---
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

  Drop this piece for the blind arm, which is the harder task and the one comparable to
  TDD-Bench baselines.
---
## What this pull request changes

```diff
{patch}
```

Read it as evidence, not as a specification to copy. Ask what a caller can observe that
differs before and after: a different return value, an exception that is or is not
raised, a side effect that now happens. Then write the test around that observable
difference.

If you cannot state the behavioural difference in one sentence, you do not understand the
change yet -- keep reading the surrounding code until you can.
