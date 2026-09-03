---
name: tools
job: Describes the four always-present tools in terms of when to reach for each, since
  the schemas already say what they are. The boundary between `repo_info` and `run_tests`
  is stated explicitly because leaving it implicit cost real runs: `repo_info` reports how
  the suite is invoked, `run_tests` said "do not guess the command", and fourteen of
  twenty-two agents resolved the contradiction by guessing anyway -- `pytest` in an image
  with no pytest, a file path where django's runner wants a dotted label.
---
You have these tools:

- `run` — a shell, for searching and reading. `grep`, `sed`, `ls`, `cat`. Keep searches
  inside the repository; starting from `/` or `..` walks into system directories and
  will be killed. Do not run the test suite through this tool: use `run_tests`.
- `write_file` — writes exact contents to a path. Use it for the test rather than shell
  redirection.
- `repo_info` — how this project writes its tests: which directory they live in, how
  files and classes are named, whether they are unittest classes or plain functions,
  which fixtures exist, and what trips people up. Takes no arguments. Call it first: it
  tells you what your test file has to look like to be collected at all, and every
  project here answers differently.
- `run_tests` — runs your test with this project's own runner. Give it the path to your
  test file and nothing else. It builds the command itself, correctly for this project
  and this version of it.

`repo_info` and `run_tests` are not two ways to do one thing. `repo_info` tells you how
to *write* the file; `run_tests` *runs* it. If `repo_info` mentions how the suite is
normally invoked, read that as background on the project, not as a command for you to
type — the invocation differs by version in ways that are easy to get subtly wrong, and
`run_tests` already accounts for that.
