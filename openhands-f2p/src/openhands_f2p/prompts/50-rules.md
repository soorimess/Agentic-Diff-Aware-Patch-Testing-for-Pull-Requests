---
name: rules
job: The constraints. The first one is load-bearing for the measurement rather than for
  the model -- an agent that edits the library can make any test pass, and then the
  "before the fix" run is not a fact about the pull request. It is enforced afterwards
  by hashing the tree, but stating it avoids wasting a run.

  "Read the source before you write" used to be the whole of the last rule, and on a large
  repository that has no stopping point. `sphinx-10614` followed it to the end of its
  budget: 98 of 100 actions were `sed`, `grep` and `ls`, one was a write, one was a test
  run, and the run was cut off holding a test that did not flip. Across four runs of that
  same instance the outcome ranks exactly by how many times it revised -- w=4 v=2 c=2 gave
  full coverage and 9 of 10 mutants, w=1 v=1 c=0 gave nothing -- and not at all by how much
  it read, which ran 50, 66, 91, 98 with no relation to the result.

  So the rule now says what the reading is *for* and hands the stopping point to the test.
  It names no metric: preferring a draft you have run to a file you have skimmed is how the
  work is done whether or not anyone is scoring it.
---
Your test goes in `{test_file}`. If it genuinely needs more than that — a fixture
directory, a sample package to import, data to read — create those files too. Give them
names of your own rather than reusing an existing fixture's.

**Do not modify or delete a file that is already here.** Not the library: the test is
supposed to fail on this code, that is the entire point, and editing what it tests
destroys the measurement rather than passing it. And not an existing test or fixture
either — the maintainer's own test for this bug is applied to this tree later, and a file
you changed underneath it may no longer accept it.

New files are safe in a way edits are not: a file that did not exist before is there when
the test runs against the old code and against the fixed code alike, so it cannot make a
test appear to flip. A file you edited can.

Read the source before you write -- enough to know what to assert, not enough to be
certain of everything. Then get a test running, and let what it does correct the rest of
your reading: a draft you have executed tells you more than another file you have skimmed,
and it is cheap to change. Reading has no natural stopping point and running does.
{?issue}
The report describes a symptom; the cause may be several layers below it and may never be
named in the report.
{/issue}
