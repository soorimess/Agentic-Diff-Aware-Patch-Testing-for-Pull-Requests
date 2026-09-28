---
name: rules
job: The constraints. The first one is load-bearing for the measurement rather than for
  the model -- an agent that edits the library can make any test pass, and then the
  "before the fix" run is not a fact about the pull request.

  Stating it is not enough and this file has the evidence. An earlier version opened with
  the permission to create fixture files and put the prohibition in its second paragraph;
  on the nano evaluation set the agent then rewrote `xarray/core/indexing.py` and
  `sklearn/impute/_iterative.py` with shell heredocs until its own test passed, and two
  instances that had been YES became BROKEN. The prohibition comes first again, and it is
  now also enforced between actions by `_undo_edits`, which reverts the file and says so.
  A rule a weak model can read past is not a rule.

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

  The third paragraph is there because eight "fail-to-pass" tests across every run read
  the patched function with `inspect.getsource` and asserted that the patch's lines were
  in it. That flips -- the agent was shown the patch -- and tests nothing. The harness
  also refuses such a stop (`V.source_gap`); the rule says it before the work starts.
---
**Do not modify or delete any file that is already here.** Not the library source, not
an existing test, not an existing fixture. The test is supposed to fail on this code —
that is the entire point — and editing what it tests destroys the measurement rather than
passing it.{?guard} This is checked after every action and any such edit is reverted, so it costs
you the action and gains you nothing.{/guard}

Creating files is allowed. Your test goes in `{test_file}`{?!repo-facts}, in the directory you chose{/!repo-facts}, and if it genuinely needs more
— a fixture directory, a sample package to import, data to read — create those too, under
names of your own rather than an existing fixture's. A file that did not exist before is
present when the test runs against the old code and against the fixed code alike, so it
cannot make a test appear to flip. A file you edited can, which is the whole difference.

**Test what the code does, not what it says.** Do not read the project's source as text —
no `inspect.getsource`, no opening a `.py` file — and assert on its contents. Such a test
passes on this fix's exact wording and fails on an equivalent fix written differently{?require-tools}; it
is refused when you try to finish{/require-tools}. Call the changed code and assert on what it returns,
raises or does.

Read the source before you write -- enough to know what to assert, not enough to be
certain of everything. Then get a test running, and let what it does correct the rest of
your reading: a draft you have executed tells you more than another file you have skimmed,
and it is cheap to change. Reading has no natural stopping point and running does.
{?issue}
The report describes a symptom; the cause may be several layers below it and may never be
named in the report.
{/issue}
