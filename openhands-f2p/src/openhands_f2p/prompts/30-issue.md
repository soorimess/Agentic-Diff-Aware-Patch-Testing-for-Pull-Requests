---
needs: issue
name: issue
job: What the pull request is about, verbatim from the dataset's problem_statement field
  (SWE-bench: the issue; ChaCo: the issues it closes and the PR's own description). This is the
  only instance data the model ever sees. The developer's fix and the developer's test
  are deliberately absent -- they are the answer.
---
What this pull request is about:

---
{problem}
---
