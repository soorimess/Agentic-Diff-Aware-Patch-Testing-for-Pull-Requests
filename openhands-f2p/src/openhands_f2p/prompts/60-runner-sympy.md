---
name: runner-sympy
job: Selected for sympy, whose bin/test runner collects module-level test functions and
  ignores unittest classes. It also has no `pytest` on PATH, which models discover the
  hard way -- exit 127 -- unless told.
---
This is sympy. Write plain `def test_...()` functions with asserts. Do not use unittest
classes; sympy's runner will not collect them.

There is no `pytest` command in this image. Use `run_tests`.
