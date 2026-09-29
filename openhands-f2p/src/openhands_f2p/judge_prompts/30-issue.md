---
name: issue
job: Subject two -- how much of what the pull request settles each test covers. The
  behaviour list comes from the report and the fix, never from either test, and a
  behaviour counts as covered only with a quotable assertion. The questions add what the
  list alone did not say: whether the main behaviour is there (I2), the error and boundary
  paths (I3), every site the fix touched (I4), and which way the difference runs (I5).
---
## Issue coverage: which test covers more of what the fix settles?

First list the distinct behaviours this pull request settles, from the report *and the
fix* -- never from either test. Separate cases, separate branches, an error path as well as
a success path, the same fix applied in two symmetric places, and a behaviour the fix
implements that the report never mentioned (developers often fix a neighbouring hazard
they know about -- if the fix implements it, it counts). Keep the list to behaviours of
this change; general properties of the function that the fix does not touch do not count.

Then, for each behaviour and for each test, quote the single line that asserts it, or
write "none". **A behaviour is covered by a test only if you can quote the assertion that
checks its outcome.** Reaching the code path without asserting what it should now produce,
or asserting something weaker (not None, no exception, not equal to the old buggy value
when the new value is specific), is not coverage.

Then answer, about the generated test:

- **I1** What share of the listed behaviours does it cover? Labels: `all` · `most` · `main-only` · `minor-only` · `none`
- **I2** Is the main behaviour -- the one the report is about -- covered? Labels: `yes` · `weakly` · `no`
- **I3** Are the error, boundary and edge paths the fix adds covered? Labels: `all` · `some` · `none` · `n/a`
  - `n/a` when the fix adds none.
- **I4** Where the fix changes several places (symmetric sites, several functions or
  branches), how many does it cover? Labels: `all` · `some` · `one` · `n/a`
  - `n/a` when the fix changes one place.
- **I5** How does its coverage compare with the developer's test? Labels: `generated-covers-more` · `same` · `developer-covers-more` · `each-covers-something-else`

Then the level, from the two columns you filled in:
- **1** The developer's test covers two or more listed behaviours that the generated test
  does not, or covers the main behaviour while the generated test covers none.
- **2** The developer's test covers one listed behaviour the generated test does not, and
  the generated test covers nothing the developer's misses of equal weight.
- **3** Both cover the same behaviours, or each covers one the other misses and those are
  of similar weight.
- **4** The generated test covers one listed behaviour the developer's does not, and misses
  nothing the developer's test covers.
- **5** The generated test covers two or more listed behaviours the developer's does not,
  and misses nothing the developer's test covers.
