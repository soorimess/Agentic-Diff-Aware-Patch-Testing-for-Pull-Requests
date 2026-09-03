---
name: situation
job: Establishes where the model is and, critically, that the bug is still present.
  Without this the model tends to assume the code is already correct and writes a test
  that passes, which is the opposite of what is wanted.
---
You are in a checkout of {repo} at the commit BEFORE a bug was fixed. The bug is still
present in this code.

There is no network here and no version control. You cannot look the answer up; you have
to find it by reading the code.
