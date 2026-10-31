# Three judgings of the same seventeen tests

The concept judge has changed twice: the model moved from `gpt-5.5` to `gpt-5.6-luna`,
and then the prompt was rewritten (`00f9210`). Both changes have now been measured on the
same seventeen generated tests from `take-two-retries-and-checks/no-require-tools`, one variable at
a time.

| pass | field in `result.json` | model | prompt |
|---|---|---|---|
| 1 | `concept` | `gpt-5.5` | before `00f9210` |
| 2 | `concept_luna` | `gpt-5.6-luna` | before `00f9210` |
| 3 | `concept_luna_v2` | `gpt-5.6-luna` | at `00f9210` |

Pass 1 → 2 is the **model** alone. Pass 2 → 3 is the **prompt** alone. Nothing else
differs: same tests, read off disk, no agent call and no container in any pass.

None of this touches a fail-to-pass verdict. The judge runs after the verdict is settled
and never feeds it, so no score in any run moves because of any of it.

## The headline: the new prompt cancels the model's leniency

Ranking each scale worst to best and counting which way every disagreement went:

| comparison | isolates | kinder | harsher | sign test |
|---|---|---:|---:|---:|
| `gpt-5.5` → luna, old prompt | the model | 9 | 1 | **p = 0.021** |
| luna old → luna new prompt | the prompt | 2 | 8 | p = 0.109 |
| `gpt-5.5` → luna, new prompt | both together | 5 | 3 | p = 0.727 |

Luna under the original prompt was measurably the softer judge. Luna under the revised
prompt is **indistinguishable from `gpt-5.5`**. The prompt did not make the judge stricter
in the abstract; it pushed back by about as much as the model change had given away, and
the two roughly cancel.

That is a better outcome than it first looks. When I read the ten original disagreements
by hand, `gpt-5.5` was the better judge on eight of them. The revised prompt moves luna
back toward the answers I agreed with, at luna's price.

The concept ranking treats `narrower` and `broader` as the same distance from `same`,
since neither is worse than the other — only `different` sits below them.

## Where each pass landed

`5.5` / `luna` / `luna+new prompt`, bold where they are not all three the same.

### concept

| instance | 5.5 | luna | luna + new |
|---|---|---|---|
| `astropy-14995` | **narrower** | **same** | **narrower** |
| `astropy-7336` | broader | broader | broader |
| `django-13406` | **different** | **narrower** | **different** |
| `matplotlib-13989` | broader | broader | broader |
| `matplotlib-26208` | narrower | narrower | narrower |
| `flask-5014` | broader | broader | broader |
| `requests-1142` | broader | broader | broader |
| `requests-6028` | narrower | narrower | narrower |
| `xarray-3677` | broader | broader | broader |
| `xarray-7233` | **narrower** | **same** | **same** |
| `pylint-4970` | different | different | different |
| `pytest-5262` | broader | broader | broader |
| `sklearn-10908` | broader | broader | broader |
| `sklearn-25747` | **same** | **same** | **narrower** |
| `sphinx-7454` | same | same | same |
| `sympy-12096` | **narrower** | **same** | **same** |
| `sympy-24562` | narrower | narrower | narrower |

### issue coverage

| instance | 5.5 | luna | luna + new |
|---|---|---|---|
| `astropy-14995` | partial | partial | partial |
| `astropy-7336` | **complete** | **complete** | **partial** |
| `django-13406` | **partial** | **partial** | **misses_the_point** |
| `matplotlib-13989` | complete | complete | complete |
| `matplotlib-26208` | partial | partial | partial |
| `flask-5014` | complete | complete | complete |
| `requests-1142` | complete | complete | complete |
| `requests-6028` | partial | partial | partial |
| `xarray-3677` | complete | complete | complete |
| `xarray-7233` | partial | partial | partial |
| `pylint-4970` | misses_the_point | misses_the_point | misses_the_point |
| `pytest-5262` | complete | complete | complete |
| `sklearn-10908` | partial | partial | partial |
| `sklearn-25747` | **partial** | **complete** | **partial** |
| `sphinx-7454` | complete | complete | complete |
| `sympy-12096` | **partial** | **complete** | **partial** |
| `sympy-24562` | partial | partial | partial |

### readability

| instance | 5.5 | luna | luna + new |
|---|---|---|---|
| `astropy-14995` | poor | poor | poor |
| `astropy-7336` | poor | poor | poor |
| `django-13406` | poor | poor | poor |
| `matplotlib-13989` | acceptable | acceptable | acceptable |
| `matplotlib-26208` | poor | poor | poor |
| `flask-5014` | **acceptable** | **good** | **good** |
| `requests-1142` | **poor** | **poor** | **acceptable** |
| `requests-6028` | acceptable | acceptable | acceptable |
| `xarray-3677` | acceptable | acceptable | acceptable |
| `xarray-7233` | acceptable | acceptable | acceptable |
| `pylint-4970` | poor | poor | poor |
| `pytest-5262` | acceptable | acceptable | acceptable |
| `sklearn-10908` | **poor** | **acceptable** | **poor** |
| `sklearn-25747` | **poor** | **acceptable** | **acceptable** |
| `sphinx-7454` | **acceptable** | **poor** | **acceptable** |
| `sympy-12096` | poor | poor | poor |
| `sympy-24562` | acceptable | acceptable | acceptable |

## Agreement between each pair

| scale | 5.5 vs luna | 5.5 vs luna+new | luna vs luna+new |
|---|---:|---:|---:|
| concept | 13/17 (76%) | **14/17 (82%)** | 14/17 (82%) |
| issue coverage | 15/17 (88%) | 15/17 (88%) | **13/17 (76%)** |
| readability | 13/17 (76%) | **14/17 (82%)** | 14/17 (82%) |

The prompt moved **issue coverage** hardest — four splits against luna's earlier reading,
and all four the same direction: `complete` back to `partial`, or `partial` down to
`misses_the_point`. That is the scale the rewrite targeted, since it is the one whose
question was "how many distinct behaviours does the pull request settle, and which does
the test reach", and the one where the judge had been answering it loosely.

## What the rewrite actually changed in the output

| | old prompt | new prompt |
|---|---:|---:|
| covered behaviours carrying the exact assertion that checks them | 0/17 | **14/17** |
| runs raising no readability problem at all | — | 1/17 |
| of those, `nothing_to_raise` filled in rather than left blank | — | 1/1 |

The evidence requirement is the substantive change. Before it, the judge asserted that a
behaviour was covered; now it has to quote the line that covers it. Three of seventeen
still do not, which is worth watching but is not a failure of the format.

`nothing_to_raise` exists so that "no problems" is a stated finding rather than an empty
list that could equally mean the judge did not look. It fired once, correctly.

## What follows from it

**Which arm carries which judge.** The switch happened mid-series, between arm 5 and
arm 6:

| arms | judge |
|---|---|
| 2, 3 | `gpt-5.5`, original prompt |
| 1, 4, 5 | luna, original prompt |
| 6, 7, 8, 9, 10 | luna, revised prompt |

Confirmed two ways: the `model` field in every `result.json`, and the fact that only the
revised prompt emits a quoted `assertion` per covered behaviour — 0 of 43 in arm 5, 39 of
43 in arm 6. The commit lands at 17:06 UTC on 2026-09-24; arm 5 finished at 16:49 and arm
6 started at 17:13.

**Fail-to-pass is unaffected everywhere.** The judge runs after the verdict and never
feeds it. Every score in `experiments/comparison/` stands.

**Judge columns still are not comparable across the series**, and now for two reasons
rather than one. Arms 6–10 should be expected to read slightly *harsher* on issue
coverage than arms 1–5, for prompt reasons alone. This is why those columns are absent
from the ten-arm comparison.

**The quantity to distrust is a small movement in judge columns across either switch.**
Two or three verdicts is the size of both effects on seventeen instances.

**Everything here is seventeen instances and at most ten disagreements.** The model effect
reaches p = 0.021 and the prompt effect does not reach significance at all — 8 of 10 in
one direction is suggestive, not settled. What is solid is that the two changes push
opposite ways and that the combined result is a wash against `gpt-5.5`.

## Cost

| pass | cost | tokens |
|---|---:|---:|
| `gpt-5.5` | not logged | not logged |
| luna, original prompt | \$0.104 | 115,411 |
| luna, revised prompt | \$0.124 | 139,779 |

The revised prompt costs 21% more tokens — larger excerpts in, quoted evidence out — and
two cents more across all seventeen. The same seventeen judgements under `gpt-5.5` would
have been roughly \$2.60, at \$5.00 and \$30.00 per million against \$0.20 and \$1.20.
Judge calls were not logged at all until the model switch, which is why the first row is
empty.
