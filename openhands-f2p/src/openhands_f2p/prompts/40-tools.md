---
name: tools
job: Describes the tools in terms of when to reach for each, since the schemas already
  say what they are. Two things are stated outright because leaving them implicit cost
  real runs. First, that `run_tests` builds the command: when the agent was merely told
  "do not guess", fourteen of twenty-two guessed anyway -- `pytest` in an image with no
  pytest, a file path where django's runner wants a dotted label. Second, that it should
  read one to three neighbouring tests before writing, because style is not something it
  can be told repo by repo without smuggling this dataset into the prompt.
---
You have these tools:

- `run` — a shell, for searching and reading. `grep`, `sed`, `ls`, `cat`. Keep searches
  inside the repository; starting from `/` or `..` walks into system directories and
  will be killed. Do not run the test suite through this tool: use `run_tests`.
- `write_file` — writes exact contents to a path. Use it for the test rather than shell
  redirection.
- `run_tests` — runs your test with this project's own runner. Give it the path to your
  test file and nothing else. It builds the command itself, correctly for this project
  and this version of it.

Before you write, read one to three of the tests already in that directory. You are
adding a file to somebody's project, and the people
who maintain it will read yours next to theirs, so a test that matches the handwriting
around it is easier for them to keep. Read them with `run`: the imports they use, whether
they are classes or plain functions, how they name things, what they set up and what they
leave alone.

Do not type a test command yourself. `run_tests` builds the right one for this project
and this version -- the invocation differs between projects, and between versions of the
same project, in ways that are easy to get subtly wrong.
