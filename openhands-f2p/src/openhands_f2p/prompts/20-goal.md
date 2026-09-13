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
---
A pull request changes how this library behaves. Your job is to write the regression test
that pins that behaviour down: one test in `{test_file}` that would have caught this bug
before it was fixed, and that will catch it again if anyone reintroduces it.

{?patch}
Work out what the code does *now*, what it will do *after* the change, and assert the
difference. That difference is the whole subject of the test -- not the surrounding
function, and not some other property that happens to be broken at the same time.
{/patch}
{?issue}
The report itself is not the subject. It describes a symptom somebody noticed; what you
assert has to be the behaviour underneath it, not the wording of the complaint.
{/issue}
