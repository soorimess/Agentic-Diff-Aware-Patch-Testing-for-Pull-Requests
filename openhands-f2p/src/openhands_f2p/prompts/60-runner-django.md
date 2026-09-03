---
name: runner-django
job: Selected for django, whose runner takes dotted module labels relative to tests/
  rather than file paths, and which discovers only unittest-style classes. A plain
  pytest-style function in the wrong directory is simply never found.
---
This is django. Put the test in `tests/` as a `SimpleTestCase` or `TestCase` subclass.

`run_tests` takes the file path and converts it to the dotted label django's runner
expects, so give it the path and nothing else. Do not call `./tests/runtests.py` yourself:
handing it a path where it wants a label collects nothing and reports success.
