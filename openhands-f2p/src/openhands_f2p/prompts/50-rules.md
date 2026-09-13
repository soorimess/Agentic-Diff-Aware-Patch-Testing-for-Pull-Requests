---
name: rules
job: The constraints. The first one is load-bearing for the measurement rather than for
  the model -- an agent that edits the library can make any test pass, and then the
  "before the fix" run is not a fact about the pull request. It is enforced afterwards
  by hashing the tree, but stating it avoids wasting a run.
---
Create only `{test_file}`. Do not modify, create or delete any other file.

In particular, do not change the library source to make your test pass. The test is
supposed to fail here — that is the entire point — and editing the code under test
destroys the measurement.

Read the source before you write.
{?issue}
The report describes a symptom; the cause may be several layers below it and may never be
named in the report.
{/issue}
