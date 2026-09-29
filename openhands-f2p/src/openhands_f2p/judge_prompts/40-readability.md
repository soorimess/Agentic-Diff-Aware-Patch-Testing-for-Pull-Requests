---
name: readability
job: Subject three -- which test a reviewer of this project would find easier to read and
  maintain. Each test gets an absolute review outcome first; the questions then name the
  parts of readability that decide it (intent, names, setup, assertion style,
  convention). Length and comments are named as not readability, because generated tests
  are longer and more commented and a judge rewards that unless told not to.
---
## Readability: which test would a reviewer of this project find easier to read, understand and maintain?

Read both as a reviewer would, in this project's conventions -- the developer's test and
the code around the fix are your evidence of them. Length, docstrings and comments are not
readability in themselves: a comment helps only when it says *why* something non-obvious
is done, a docstring that restates the test name adds nothing, and a longer test is not
more readable for being longer. Do not prefer either test because of who wrote it. Ignore
formatting and line length.

Give each test an absolute review outcome first -- `accept`, `nits` (accept with small
comments), `changes` (changes requested before merging) or `reject` -- with its concrete
problems. Then answer, about the generated test:

- **R1** Can a reader tell from the test alone which behaviour it pins, and why? Labels: `clear` · `partly` · `unclear`
- **R2** Do the names of tests and values say what they are? Labels: `descriptive` · `mixed` · `poor`
  - `result`, `data`, `x`, `test1` are not names.
- **R3** How much setup does it carry? Labels: `minimal` · `some-noise` · `heavy`
  - `heavy`: dead code, unused fixtures, debug prints, production logic re-implemented
    inside the test.
- **R4** How are its assertions written? Labels: `direct` · `indirect` · `vacuous`
  - `direct`: the expected value is stated plainly, so a failure explains itself;
    `indirect`: scanning, searching or computing the expectation; `vacuous`: an assertion
    that cannot fail or says nothing about the behaviour.
- **R5** Does it follow the project's conventions -- test class or function as the
  project does, its own helpers (such as `assert_node`), its fixtures? Labels: `follows` · `partly` · `ignores`

Then the level:
- **1** The generated test is clearly less readable: it would need substantial rework
  where the developer's would not, or it is misleading or vacuous.
- **2** The generated test is somewhat less readable: it would draw more or weightier review
  comments than the developer's.
- **3** On a par: comparable review outcome and comparable problems, even if different ones.
- **4** The generated test is somewhat more readable: clearer names, plainer assertions or
  tighter setup, and it would draw fewer review comments.
- **5** The generated test is clearly more readable: it would be accepted as it stands
  while the developer's test has real readability problems (misleading names, an
  assertion that does not say what it checks, unexplained magic values or setup).
