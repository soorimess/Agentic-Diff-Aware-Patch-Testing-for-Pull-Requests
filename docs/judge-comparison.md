# Two judges on the same seventeen tests

The concept judge moved from `gpt-5.5` to `gpt-5.6-luna`. Both were asked the same
question about the same seventeen generated tests, with nothing else changed, so the
difference below is the judge and only the judge.

None of this touches a fail-to-pass verdict. The judge runs after the verdict is settled
and never feeds it, so no score in any run moves because of the change.

| instance | concept | issue coverage | readability |
|---|---|---|---|
| `astropy-14995` | **narrower → same** | partial | poor |
| `astropy-7336` | broader | complete | poor |
| `django-13406` | **different → narrower** | partial | poor |
| `matplotlib-13989` | broader | complete | acceptable |
| `matplotlib-26208` | narrower | partial | poor |
| `flask-5014` | broader | complete | **acceptable → good** |
| `requests-1142` | broader | complete | poor |
| `requests-6028` | narrower | partial | acceptable |
| `xarray-3677` | broader | complete | acceptable |
| `xarray-7233` | **narrower → same** | partial | acceptable |
| `pylint-4970` | different | misses_the_point | poor |
| `pytest-5262` | broader | complete | acceptable |
| `scikit-learn-10908` | broader | partial | **poor → acceptable** |
| `scikit-learn-25747` | same | **partial → complete** | **poor → acceptable** |
| `sphinx-7454` | same | complete | **acceptable → poor** |
| `sympy-12096` | **narrower → same** | **partial → complete** | poor |
| `sympy-24562` | narrower | partial | acceptable |

Bold marks a disagreement, `gpt-5.5` first.

## They agree on most of it

| scale | agree |
|---|---|
| concept | 13/17 (76%) |
| issue coverage | 15/17 (88%) |
| readability | 13/17 (76%) |

## But the disagreements lean one way

Ranking each scale worst to best and asking which judge was kinder on every disagreement:
**nine times luna, once `gpt-5.5`**. A sign test on ten disagreements gives p = 0.02, so
this is a lean rather than noise.

It is strongest where it matters most. All four concept disagreements go luna's way, and
three of them are the same move -- `narrower` becoming `same`. Luna is readier to call a
test equivalent to the maintainer's where `gpt-5.5` called it a smaller test. Both issue
coverage disagreements are `partial` becoming `complete`, the same direction again.

Readability is the only scale with a disagreement in the other direction: `sphinx-7454`
went `acceptable` to `poor`.

## What follows from it

**Scores are unaffected, columns are not.** Runs judged by `gpt-5.5` and runs judged by
luna can be compared on fail-to-pass without any adjustment. Their `concept`, `issue` and
`readable` columns cannot be compared quite so freely: a run judged by luna should be
expected to show slightly more `same` and slightly more `complete` than the same tests
would have scored under `gpt-5.5`, by roughly one instance in four on concept.

**The quantity to distrust is a small improvement in judge columns across the switch.**
A run after the change showing two or three more `same` verdicts than one before it has
shown nothing; that is the size of the lean on seventeen instances.

**Cost.** The seventeen judgements cost \$0.10 under luna. The same work under `gpt-5.5`
would have been around \$2.60, at \$5.00 and \$30.00 per million tokens against \$0.20
and \$1.20. The earlier figure was never recorded, because judge calls were not logged
until the switch.
