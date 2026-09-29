---
name: concept
job: Subject one -- which behaviour the test pins, and how well. The questions separate
  what a single number hid: whether the assertion is on the contract at all (C1), how
  precise it is (C2), whether it would catch a plausible wrong fix (C3), whether it is the
  developer's behaviour (C4), and whether the developer's test knew something it did not
  (C5).
---
## Concept: which test pins the behaviour this fix establishes, and how well?

"The behaviour" is the observable contract the fix implements: what the changed code now
returns, raises or does, for the inputs the fix is about. Not the style, the names, the
route to the code, or the mechanism. Two tests that reach the same behaviour by different
routes pin the same concept. Work out that contract from the report and the fix first,
then answer, about the generated test:

- **C1** What does its main assertion check? Labels: `contract` · `symptom` · `neighbour` · `source-text` · `other`
  - `contract`: the behaviour the fix establishes; `symptom`: only the reported example of
    it; `neighbour`: another behaviour that changes in the same commit; `source-text`: it
    reads the project's source as text and asserts on it; `other`: something else.
- **C2** How exact is its expected outcome? Labels: `exact` · `partial` · `weak` · `none`
  - `exact`: a specific value, or the exception type (and message where it matters);
    `partial`: a property or subset of the outcome; `weak`: not None, truthy, a type, "no
    exception", "differs from the old output"; `none`: no assertion on the outcome.
- **C3** Would it fail on a plausible wrong fix -- one that handles only the reported
  input, only one of the branches, or the right case with the wrong value? Labels: `yes` · `partly` · `no` · `unclear`
- **C4** Is it the same behaviour the developer's test pins? Labels: `same` · `overlapping` · `different`
- **C5** Does the developer's test encode project knowledge -- security, compatibility, a
  known regression -- and does the generated test match it? Labels: `none` · `present-and-matched` · `present-and-missed`

Then the level:
- **1** The generated test asserts a different behaviour, a merely neighbouring one, the
  source text, or nothing meaningful -- while the developer's test pins the contract.
- **2** Both are about the contract, but the generated test pins it less well: a weaker
  assertion, a clearly smaller part of it, or it misses a case the developer checks
  deliberately (including one whose reason is developer experience).
- **3** Both pin the same contract with comparable precision. Differences are of route,
  naming or structure only, or each is stronger on a different minor point.
- **4** The generated test pins everything the developer's pins and pins it better on at
  least one real point: an exact value where the developer checks a weaker property, or
  an input the contract is genuinely about that the developer's test leaves unchecked.
- **5** The generated test pins the contract where the developer's test pins only a
  symptom, a single example of a general rule, or a weak proxy for it -- and loses
  nothing the developer's test checks for a reason.
