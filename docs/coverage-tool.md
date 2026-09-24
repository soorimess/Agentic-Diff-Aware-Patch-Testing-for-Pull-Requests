# What the coverage tool is worth

Arm 6 withheld the `coverage` tool from the agent and returned 43 fail-to-pass against the
base's 42, with a per-test mean of 86% against 88%. Read off the top of the two tables that
says the tool does nothing. It says no such thing, and the reason is worth writing down,
because the same trap is waiting in every other instrument arm.

## Fail-to-pass was never the question

A test flips if it fails before the fix and passes after. It can do that while executing
one changed line in three. Raising it from 40% to 100% does not change the verdict, so an
instrument that improves coverage cannot show up in the fail-to-pass count. Measuring it
there measures the wrong outcome.

## The per-test mean is over different tests in each arm

The two arms do not pass the same instances, so their means are not comparable. Splitting
the instances three ways shows where the difference goes:

| | n | with the tool | without |
|---|---|---|---|
| passed in **both** arms | 34 | **90.0%** | **85.1%** |
| passed only with the tool | 8 | 77.8% | — |
| passed only without it | 9 | — | 88.2% |
| *headline mean* | | *87.7%* | *85.8%* |

The base's mean is dragged down by eight weak tests it kept. The withheld arm's is propped
up by nine fresh ones, five of them at 100%. Between them they hide three of the five
points.

The corpus figure misleads in the same way and for the same reason: 34% without the tool
against 30% with it, because 43 passing tests cover more total lines than 42 do, however
much worse each one is.

## Paired, the tool is worth about five points

Same 34 instances, same 187 changed lines:

| | with the tool | without |
|---|---|---|
| mean coverage | 90.0% | 85.1% |
| tests at 100% | 27/34 | 24/34 |
| pooled lines | 131/187 (70%) | 121/187 (65%) |
| instances where coverage **fell** without it | | **6** |
| instances where coverage **rose** without it | | **0** |

Six down and none up is a sign test at p = 0.03.

## The mechanism, visible instance by instance

In the base run, 129 coverage calls were made across 70 instances. Twenty-five of them read
below 100% on the first call. Seven went back and closed the gap:

```
astropy-7606      66.7% -> 100%      requests-2931   33.3% -> 100%
matplotlib-20676  75.0% -> 100%      sphinx-7462     66.7% -> 100%
sympy-19637       50.0% -> 100%      sympy-12489     50.0% ->  80%
matplotlib-24870  64.7% ->  82.4%
```

Two of those same instances are in the withheld arm's losses. `sphinx-7462` reached 100%
with the tool and sits at 40% without it; `sympy-19637` reached 100% with it and 50%
without. That is the whole chain in one instance: the tool reports a gap, the agent closes
it, and removing the tool leaves the gap open.

## What it does not fix

Of the 25 runs that saw a gap, 7 closed it. Eleven called coverage again and the number did
not move, six never looked again — four of those from **0%**, a test that flips without
executing a single line the patch changed — and one got worse. `require-tools` makes the
agent call the instrument; nothing makes it act on the answer.

## It does not replicate

Arm 8 withheld both instruments, which makes two further comparisons possible. One of them
is an independent test of the same question: arm 7 already lacks the mutation tool, and arm
8 lacks mutation *and* coverage, so the pair differs by the coverage tool alone, exactly as
base and arm 6 do.

| comparison | n | coverage fell | rose | p |
|---|---|---|---|---|
| base → arm 6 | 34 | 6 | 0 | **0.031** |
| **arm 7 → arm 8** *(independent)* | 30 | **3** | **3** | **1.000** |
| base → arm 8 | 30 | 3 | 0 | 0.250 |
| combined, the two independent pairs | | 9 | 3 | **0.146** |

The replication fails. Six down and none up on 34 instances looked like a finding; the
same question asked again on 30 other instance-pairs gives three down and three up. Pooled,
nine against three is p = 0.15.

So the five points above are one arm's result, not an established effect. The direction has
never reversed -- base → arm 8 is still 3 and 0 -- and the instance-level chain, where
`sphinx-7462` climbs 67% → 100% with the tool and sits at 40% without it, is still a real
thing that happened. But a single sign test on six discordant instances is exactly the
evidence this corpus has been punishing all series, and it should not have been reported as
settled on one arm.

What would settle it is the arm nobody has run: the base repeated. Three of the nine
comparisons in this series now hinge on whether a handful of instances moving is signal,
and there is still no measurement of how many move when nothing changes at all.

## The trade

What is certain is the cost: \$3.46 against \$2.97, about a seventh of the agent's spend,
across 129 calls. What is not certain is the benefit. One arm says five points of
changed-line coverage, its replication says nothing, and the pooled evidence says nine
instances down against three up at p = 0.15 -- suggestive of a real but smaller effect than
the first arm implied, and short of demonstrated.

It buys nothing in fail-to-pass and never could; that part was never in doubt. The open
question is only whether it buys coverage, and on current evidence the answer is *probably
a little, and not five points*.
