---
name: user
job: The user turn: the four inputs, labelled with who wrote each test. Not numbered, so
  it is not joined into the system prompt; `compare.py` fills it with `str.format`.
---
Bug report
==========
{problem}

The fix that was merged
=======================
{patch}

The developer's test (the lines a maintainer of this project added, as part of the fix, to its existing test files)
===================================================================================================================
{developer_test}

The generated test (a whole new file, written afterwards from the report and the fix only)
==========================================================================================
{generated}
