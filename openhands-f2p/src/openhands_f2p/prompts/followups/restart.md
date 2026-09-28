---
name: restart
job: The second chance (2026-09-28): opens a fresh conversation after a run ended without a
  test this run accepts, when actions remain. Sent after the unchanged task, so the agent
  reads the job first and its first attempt second. It carries why the attempt was not
  accepted -- the harness's verdict and what each test did before and after the fix --
  the test it left whatever the verdict, the record of the attempt (its tool calls and
  what they returned, shortened), and the budget that remains. Telling the agent why is a
  deliberate choice (user, 2026-09-28): it is the one place the head run reaches the agent
  directly, and the agent could have learned the same with `verify`.
---
## Second attempt

You have worked on this task once already. That attempt is over: it used {used} of the
{cap} actions this run has, and it ended without a test this run accepts.

Why it was not accepted:

{why}

{test_block}

What you did in the first attempt, in order -- each tool call and what it returned,
shortened:

{history}

This is a fresh start on the same checkout: every file you wrote is still on disk, and the
task above has not changed. You have {budget} actions. Use what the first attempt showed
you -- above all the reason it was not accepted -- rather than repeating it: if an
approach did not work there, it will not work now for being tried again.
