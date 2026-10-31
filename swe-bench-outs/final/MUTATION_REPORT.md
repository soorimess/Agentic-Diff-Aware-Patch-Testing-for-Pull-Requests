# Mutation report: why the mutation tool does not help, and how to fix it

On top of the coverage tool, the mutation tool did not make the weak model's tests catch more bugs. The mutation score is a good measure of a test; as feedback to the agent it does not work.

## Why it is not useful

- **The agent cannot act on what it is shown.** The tool lists surviving mutants and wrong versions, often as a one-line description. To kill one, the model must work out an input that tells it apart from the fix and the value to assert. A weak model rarely does, so the same survivors come back call after call.
- **Tests kill mutants by crashing, not by checking.** Most mutants die because the test errors on them, not because an assertion fails. The tool counts both the same, so the agent is never pushed to check the values the change computes.
- **It competes with the coverage duty.** Both duties share one stop budget and one action budget. Time spent on survivors is taken from raising coverage, and coverage is what actually improved the tests.
- **Some survivors cannot be caught.** Mutants on lines the test never reaches, or that behave like the fix on any sensible input, are reported anyway and spend the agent's effort for nothing.

## Changes to the current tool

- **One duty at a time.** Ask about survivors only after the coverage duty is met, with its own small budget.
- **One survivor at a time.** Show the single most useful survivor, on a line the test already reaches.
- **Count only assertion kills.** A mutant the test kills by crashing is reported as still open.
- **Drop survivors no test can catch.** Leave out unreached lines and mutants that behave like the fix.

## A new design: LLM-based mutation

1. **Generate realistic bugs, not syntax edits.** A cheap model reads the change and writes a few plausible wrong versions of it: a missed case from the issue, a wrong default, an off-by-one on the new branch. These are the bugs a reviewer worries about, unlike mutmut's operator swaps.
2. **Ship each bug with a failing example.** For every wrong version the model also writes one input and the value the correct code returns. The harness runs that input on the fix and on the wrong version and keeps the bug only if the two really differ, so nothing hallucinated reaches the agent.
3. **Hand the agent the example, not the bug.** The agent is told: "with this input the change returns X; a likely bug returns Y; assert on it". Turning that into a test is copying, which a weak model can do.
4. **Keep a held-out set for scoring.** Generate the bugs once per PR and freeze them; show the agent one half and score every configuration on the other, as now.
