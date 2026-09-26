---
name: goal
job: The deliverable, stated as an engineering task rather than as our scoring function.

  This was rewritten after review. The earlier version read "write a test that FAILS on
  this code and PASSES once the change is applied, and that executes the lines the change
  touches" -- which is fail-to-pass and changed-line coverage, verbatim, the two numbers
  we score. Handing the agent the mark scheme means those numbers stop measuring test
  quality and start measuring compliance: an agent told to make a test flip can make it
  flip without understanding anything, and we would have no way to tell the two apart.

  So the instruction now names the job a developer would recognise -- capture the
  behaviour this pull request changes -- and lets F2P and coverage be consequences of
  doing that well. They remain how we score; they are no longer what we ask for.

  "One test" became "the tests, one per separable behaviour" after `astropy-13398`, which
  has 93 changed executable lines where every other instance on the evaluation set has one
  to eight. It adds a whole module of coordinate transforms, and both gpt-5-mini and
  gpt-5.5 wrote exactly one test function and left most of that module untested -- 32% and
  57% coverage. They were obeying the instruction. `57-check-reaches.md` already said the
  opposite, that a separate case "deserves a second test function", but it is gated on the
  coverage tool and it is not the sentence that states the deliverable.

  The clause "as many as the change has, and no more" is the half that keeps this from
  being an invitation to pad. An uncapped "write tests" is the failure this piece was
  rewritten to avoid the first time, arrived at from the other direction.
---
A pull request changes how this library behaves. Your job is to write the regression tests
that pin that behaviour down, in `{test_file}`{?!repo-facts} in the directory you chose{/!repo-facts}: enough to have caught this bug before it
was fixed, and to catch it again if anyone reintroduces it. One test per behaviour the
change settles separately -- as many as the change has, and no more. A test is whatever
this project's runner collects: a function in some projects, a method on a test class
in others. The briefing above says which, and a test the runner does not collect is
not a test.

{?patch}
Work out what the code does *now*, what it will do *after* the change, and assert the
difference. That difference is the whole subject of the test -- not the surrounding
function, and not some other property that happens to be broken at the same time.
{/patch}
{?issue}
The report itself is not the subject. It describes a symptom somebody noticed; what you
assert has to be the behaviour underneath it, not the wording of the complaint.
{/issue}
