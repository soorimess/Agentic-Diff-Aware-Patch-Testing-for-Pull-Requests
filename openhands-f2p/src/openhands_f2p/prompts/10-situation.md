---
name: situation
job: Establishes where the model is and, critically, that the change is not in this code.
  "A bug" until 2026-10-11; feature and refactor PRs (ChaCo) are not bug fixes, and the
  model read "the new API must already exist" into it.
  Without this the model tends to assume the code is already correct and writes a test
  that passes, which is the opposite of what is wanted.
---
You are in a checkout of {repo} at the commit BEFORE a pull request was merged. Its change
is not in this code: whatever it fixes is still broken here, and whatever it adds -- a
function, an argument, a class, a module -- does not exist here yet.

There is no network here and no version control. You cannot look the answer up; you have
to find it by reading the code.
