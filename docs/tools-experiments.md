# Tool and feature experiments

What each arm removes, why it is worth a run, and what to read out of it. One row per
run, run in the order given.

The system is PR-aware by design: every arm keeps both the bug report and the diff.
`--no-issue` and `--no-patch` are real questions but a different one -- whether the
system works without the pull request at all -- and they are deliberately out of this
series.

## The base

`full` configuration plus `--second-chance`: every input, every tool, guard on, tool
duty on. All seventy pull requests, `qwen3-coder-30b-a3b-instruct`, `--mutants 10`,
`--parallel 50`.

| | |
|---|---|
| fail-to-pass | **38 / 70** |
| NO | 26 |
| BROKEN | 6 (4 of them a Docker daemon error, retryable) |
| actions | 2359 |
| pre-existing files altered | **0** |

Every call was served by one provider, pinned in the registry and checked against the
completions afterwards rather than assumed: 2478 of 2478 from SiliconFlow. The provider
is held constant for the whole series, so no arm differs from another by where the model
was served.

The five matplotlib instances were run a second time, after the target-directory fix
below, so that every instance in this row comes from the same harness.

Every other arm is one step away from this row, on the same seventy instances.

## The arms

`--second-chance` is on everywhere except arm 2.

| # | added flags | features off | isolates | primary readout |
|---|---|---|---|---|
| **1** | `--second-chance` | — | **base** *(done)* | reference row for all others |
| **2** | *(none)* | — | second chance itself | fail-to-pass against arm 1; refusals, reasons, conversions |
| **3** | `--no-guard` | guard | source-edit rate | **BROKEN-VOID count** and the `tree_altered` file list |
| **4** | `--no-require-tools` | require-tools | tool duty | verify calls per run, runs that never verify |
| **5** | `--no-repo-facts` | repo-facts | the testing briefing | fail-to-pass, and how often the test lands somewhere uncollected |
| **6** | `--no-coverage-tool` | coverage-tool | the coverage instrument | fail-to-pass, actions |
| **7** | `--no-mutation-tool` | mutation-tool | the mutation instrument | fail-to-pass, actions |
| **8** | `--no-coverage-tool --no-mutation-tool` | coverage, mutation | both instruments at once | fail-to-pass; also the control for a later `--no-patch` |
| **9** | `--no-verify-tool` | verify, coverage, mutation, **require-tools** | nothing on its own | read only against arm 10 |
| **10** | `--no-coverage-tool --no-mutation-tool --no-require-tools` | coverage, mutation, require-tools | **verify, cleanly** (9 against 10) | fail-to-pass difference 9 to 10 |

## Two things the table cannot show

**Arm 9 is not a one-variable arm.** `verify-tool` is a dependency of three other
features, so `--no-verify-tool` withholds four things at once -- and the fourth,
`require-tools`, is easy to miss because nothing on the command line names it. Arm 10
exists only so that arm 9 has a partner differing from it by the verify tool alone.
Arm 9 reported against the base is a four-way change and says nothing about verify.

**Arm 3 cannot produce a judge result.** A run that edits a file which was already there
has its verdict replaced by BROKEN, and the judge, coverage and mutation all run only on
a fail-to-pass YES. So withholding the guard yields *fewer* judge rows, never worse ones.
What it yields instead is the thing the guard otherwise hides: with the guard on, an edit
to library source is reverted between actions and the tree is clean by the time anything
looks at it -- the base run's zero altered files is that repair, not an absence of
attempts. Arm 3 is the only configuration in which the attempts survive to be counted.

## What to record for every arm

Scores matter most on the tool arms, but no arm is finished at a single number.

fail-to-pass · BROKEN · **BROKEN-VOID** · files written outside the test ·
changed-line coverage on YES · mutation score on YES · judge triple ·
verify calls · actions · cost

## Reading the arms against each other

Every arm runs the same seventy instances, so each one pairs with the base
instance by instance. Read the per-instance movement -- which ones went YES to NO and
which went NO to YES -- rather than the two totals, which throw that away. A difference
of a few instances on seventy is small enough that the direction matters more than the
size.

## Gates

**Arm 5 was blocked on a bug, now fixed.** The target-directory heuristic preferred
`requirements/testing` over `lib/matplotlib/tests` -- the decoy matches on name and holds
no test at all -- so the briefing arm 5 withholds was itself wrong on the five matplotlib
instances. Fixed, and those five were re-run so the base row is uniform. One of them,
`matplotlib-24870`, went YES to NO on the re-run: a test in the real test directory picks
up that directory's conftest, and the earlier YES may have been an artefact of running
outside it. One instance cannot separate that from run-to-run variation.

**Arm 9 runs only with arm 10.** On its own it produces a row nobody can interpret.

## Known caveat in one readout

`files_written_outside_test` is currently inflated. It compares the path the agent passed
to `write_file` against the recorded test path as plain strings, so a test written to
`/testbed/sympy/core/tests/test_f2p_sympy__sympy_16766.py` is counted as a write
elsewhere when the recorded path is relative. Most of the base run's twenty-six are that.
The genuine ones are scratch files -- `debug.py`, `test_reproduce_bug.py` -- which are new
files rather than edits and so cannot void a measurement. `tree_altered`, which comes
from the tree itself rather than the log, is not affected and is the number arm 3 turns on.
