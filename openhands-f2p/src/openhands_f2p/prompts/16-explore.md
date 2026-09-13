---
name: explore
needs: !repo-facts
job: What to establish about the checkout, for runs where the harness hands none of it
  over. The counterpart to `15-repo.md`, which is dropped in the same configuration --
  same subject, worked out by the agent instead of read off the tree by `repo_facts`.

  It names the questions and none of the answers. An answer -- that tests live in a
  directory called `tests`, that a project ships its own runner -- is the
  per-repository advice that was deleted from here once already: right for the twelve
  repositories someone had looked at and silently wrong for the thirteenth. The
  questions hold in any checkout, which is the only reason they can be stated here.

  The destination is the load-bearing one, and worth being honest about. `run_tests`
  picks this project's runner in every configuration, and the agent could always have
  read a configuration file for itself. Where a new file has to sit for the runner to
  collect it is the fact the harness supplied outright and now does not -- so this is
  the piece that decides whether the flag measures anything.

  Every line is what a developer joining the project would do on their first day, which
  is the test for whether an instruction belongs in a prompt at all.
---
## Work out how testing works here

You have not been told anything about this project's test setup, and you are not expected
to work from what is in front of you. The whole checkout is yours to look at: search it
wherever you think the answer is, read whatever file you need to read, and follow
whatever leads you find. `run` gives you a shell -- `ls`, `cat`, `grep`, `find` -- and
there is no part of the tree that is off limits to read.

Establish these before you write anything:

* **Where a new test file has to live to be collected.** Test discovery is
  configuration, not convention, and a file in a directory the runner never looks at is
  not a failing test, it is an invisible one. Find where the existing tests sit and what
  the configuration says about discovery, and put yours where the same run would pick it
  up.
* **What the test configuration enforces.** Strict markers, warnings promoted to errors,
  required plugins or fixtures. These change what a valid test looks like here, and the
  configuration file states them more exactly than a summary of it would.
* **How tests in that area are written.** Read one or two of them. Imports, fixtures,
  naming, how they assert -- yours should look like it belongs beside them.

Then write your test to a file named `{test_file}`, in whichever directory you concluded
is right -- that choice is yours, and nobody has pre-decided it for you. `run_tests` runs
this project's own runner; give it the path you chose and confirm the test is actually
collected, because a path the runner cannot reach reports nothing at all rather than
failing.

Reading is unrestricted; creating is not. That one file is the only thing you may add,
and the library source stays exactly as you found it.
