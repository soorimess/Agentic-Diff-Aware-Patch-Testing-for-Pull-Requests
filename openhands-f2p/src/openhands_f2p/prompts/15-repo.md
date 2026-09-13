---
name: repo
needs: repo-facts
job: How testing works in this checkout -- runner, target path, neighbouring tests, and
  the project's own pytest configuration verbatim. Read off the tree by `repo_facts`, with
  no model involved.

  This replaces a `repo_info` sub-agent that answered the same question with an LLM call.
  It was doing two jobs badly: repeating `find` commands the harness already ran, and
  paraphrasing a config file into something less precise than the file. `xfail_strict =
  true` is clearer than any sentence about it. What a summary genuinely could not give --
  how tests are written here -- the agent now gets by reading one, which is a better
  source than a description of one.

  Early in the order on purpose: the agent needs it before its first action, and this way
  it does not spend a turn asking.
---
{repo_facts}
