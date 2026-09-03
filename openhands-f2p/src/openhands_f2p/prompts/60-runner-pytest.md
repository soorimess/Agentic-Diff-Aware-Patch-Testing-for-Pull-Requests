---
name: runner-pytest
job: Per-repo advice for the pytest projects. The `pytest` warning is here because it is
  where the guessing actually happened: agents typed `pytest -q <file>` in eight of these
  repositories, and the bare command is missing in some images while others carry a pytest
  old enough to reject flags that have been standard for years.
---
This is a pytest project. Plain `def test_...()` functions are fine.

Do not invoke `pytest` yourself. These checkouts span many years and their pytest
versions differ: in some images the bare `pytest` command is not on the path, and in
others it is old enough to reject options that are standard now, which comes back as a
usage error rather than a test result. `run_tests` knows which form this image accepts.
