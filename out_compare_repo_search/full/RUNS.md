# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: 2026-09-11 10:55 UTC.

- **24** instances across **12** repositories
- **24/24** fail-to-pass, of those that reached a verdict
- **24** measured for changed-line coverage; median 100%
- $1.41 and 14.8M tokens in total

Every row was produced with the same configuration: **`full`** &mdash; what the agent was given. `full` means nothing was withheld.

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

The two `mutants` columns are the same set of mutants asked of two tests. `mutmut` mutates the lines the patch changed -- negating a condition, moving a boundary, replacing a literal -- and each column is how many of those mutants that test fails on, which is how many wrong versions of the fix it would have caught. Nothing is filtered out, so the columns are comparable: a mutant the developer's test kills and the agent's does not is a gap, and one neither kills is probably behaviourally equivalent to the fix and says nothing about either test. The individual diffs are in each instance's `mutations/`.

| instance | version | verdict | coverage | mutants: agent test | mutants: dev test | actions | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | YES | 100% (1/1) | 5/5 | 4/5 | 29 | broader | complete | acceptable | 2026-09-11 10:35 UTC |
| [`django__django-13406`](./django__django-13406/) | 3.2 | YES | 100% (2/2) | no mutants | no mutants | 48 | narrower | partial | poor | 2026-09-11 10:38 UTC |
| [`django__django-15098`](./django__django-15098/) | 4.1 | YES | 100% (1/1) | 3/3 | 3/3 | 20 | narrower | partial | acceptable | 2026-09-11 10:37 UTC |
| [`django__django-16333`](./django__django-16333/) | 4.2 | YES | 100% (2/2) | 6/6 | 6/6 | 53 | same | complete | acceptable | 2026-09-11 10:45 UTC |
| [`django__django-17029`](./django__django-17029/) | 5.0 | YES | 100% (1/1) | no mutants | no mutants | 23 | narrower | complete | poor | 2026-09-11 10:33 UTC |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | YES | 100% (2/2) | 8/10 | 5/10 | 12 | broader | complete | acceptable | 2026-09-11 10:33 UTC |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | YES | 100% (2/2) | 3/3 | 3/3 | 38 | narrower | partial | acceptable | 2026-09-11 10:43 UTC |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | YES | 100% (2/2) | 1/4 | 1/4 | 14 | same | complete | good | 2026-09-11 10:31 UTC |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | YES | 100% (2/2) | 2/2 | 2/2 | 41 | same | complete | acceptable | 2026-09-11 10:41 UTC |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | YES | 100% (2/2) | 2/4 | 2/4 | 15 | narrower | partial | acceptable | 2026-09-11 10:34 UTC |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | YES | 100% (3/3) | no mutants | no mutants | 13 | same | complete | acceptable | 2026-09-11 10:32 UTC |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | YES | 100% (3/3) | 8/9 | 8/9 | 62 | narrower | partial | acceptable | 2026-09-11 10:49 UTC |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | YES | 67% (2/3) | 6/10 | 10/10 | 30 | narrower | partial | acceptable | 2026-09-11 10:42 UTC |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | YES | 80% (4/5) | 6/10 | 9/10 | 59 | different | misses_the_point | poor | 2026-09-11 10:50 UTC |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | YES | 100% (1/1) | 1/1 | 1/1 | 16 | same | complete | good | 2026-09-11 10:43 UTC |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | YES | 100% (1/1) | 6/6 | 6/6 | 14 | narrower | partial | good | 2026-09-11 10:45 UTC |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | YES | 100% (1/1) | no mutants | no mutants | 13 | broader | complete | acceptable | 2026-09-11 10:41 UTC |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | YES | 100% (1/1) | 1/1 | 1/1 | 23 | narrower | partial | acceptable | 2026-09-11 10:44 UTC |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | YES | 100% (1/1) | 2/5 | 2/5 | 17 | broader | complete | poor | 2026-09-11 10:47 UTC |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | YES | 100% (5/5) | no mutants | no mutants | 14 | narrower | partial | acceptable | 2026-09-11 10:46 UTC |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | YES | 100% (11/11) | 9/10 | 9/10 | 54 | narrower | partial | acceptable | 2026-09-11 10:55 UTC |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | YES | 33% (2/6) | 2/4 | 3/4 | 34 | narrower | partial | acceptable | 2026-09-11 10:52 UTC |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | YES | 100% (1/1) | no mutants | no mutants | 18 | same | complete | good | 2026-09-11 10:48 UTC |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | YES | 100% (2/2) | 4/7 | 4/7 | 22 | narrower | partial | acceptable | 2026-09-11 10:51 UTC |

## Behaviours the judge says are not covered

Read alongside the coverage column: these come from reading the issue and the fix, not from line execution, so the two disagree in useful ways.

- **django__django-13406** (partial)
  - It does not cover a real pickled values().annotate() queryset returning the expected dict.
  - It does not cover any real values_list() queryset.
  - It does not cover the flat=True or named=True values_list() variants.
- **django__django-15098** (partial)
  - The broadened matching also applies to other valid configured two-subtag forms, such as language-region-variant and three-letter-language script/region tags.
  - Longer hyphenated URL path components that are not valid language prefixes are not consumed as language prefixes.
- **psf__requests-6028** (partial)
  - For URLs with an existing scheme and `user:pass` auth, `prepend_scheme_if_needed` preserves the credentials instead of stripping them.
  - For username-only auth such as `user@host`, `prepend_scheme_if_needed` preserves the auth component as well.
- **pylint-dev__pylint-6903** (partial)
  - a quota-based cgroup calculation that truncates to 0 is also normalized to 1
  - Pylint invoked with `--jobs=0` should not pass 0 processes to multiprocessing and crash
- **pytest-dev__pytest-10081** (partial)
  - The same class-level skipped-TestCase behaviour is pinned for @pytest.mark.skip on the class.
- **sphinx-doc__sphinx-7454** (partial)
  - Other annotation names continue to be represented as py:class references.
- **sphinx-doc__sphinx-10614** (misses_the_point)
  - SVG inheritance-diagram links generated from internal refuri values are emitted without an extra ../ prefix so nested-document links do not point to the wrong directory.
  - SVG inheritance-diagram links generated from refid values are emitted as current_filename#refid without an extra ../ prefix.
  - External intersphinx references are keyed by the target name derived from the refuri fragment so graph nodes receive the correct external URL.
- **pydata__xarray-7233** (partial)
  - DataArray `coarsen.construct` preserves non-dimensional coordinates through the temporary-Dataset construction path.
  - The construct result retains the full set of original coordinate names.
- **astropy__astropy-14995** (partial)
  - masked NDDataRef multiplied by a scalar/no-mask operand with handle_mask=np.bitwise_or copies the existing bitmask instead of raising TypeError
  - unmasked operands with handle_mask=np.bitwise_or still produce no mask
  - operands that both have masks still use the mask handler, including bitwise_or of distinct bitmasks
- **sympy__sympy-24562** (partial)
  - For a non-integer numerator and a fractional string or float denominator, Rational(p, q) computes the same quotient as parsing p/q.
  - For an integer numerator and a non-integer string or float denominator, the denominator's Rational numerator and denominator are combined correctly.
  - For a non-integer numerator and an integer denominator, the numerator's denominator is still combined correctly with the integer denominator.
- **mwaskom__seaborn-3069** (partial)
  - Explicit user limits on nominal x axes are preserved.
  - Explicit user limits on nominal y axes are preserved.
- **mwaskom__seaborn-3187** (partial)
  - seaborn.objects continuous legends disable ScalarFormatter offset/scientific notation so large numeric labels show their actual magnitude
- **scikit-learn__scikit-learn-10908** (partial)
  - It does not assert fixed_vocabulary_ or the vocabulary_ term-to-index mapping after the call.
  - It does not cover validation/error behaviour for invalid supplied vocabularies.

## What is in each directory

| file | what it holds |
|---|---|
| `result.json` | the verdict, the coverage, token usage, the audit |
| `flow.log` | every step in order: container, commands, both test runs, verdict |
| `flow.jsonl` | the same, one JSON object per step |
| `trajectory.json` | the agent's events, for the OpenHands visualizer |
| `tool_log.json` | one entry per tool call, as it reached the container |
| `test_f2p_*.py` | the test the agent wrote |
| `before_fix.log`, `after_fix.log` | the two runs the verdict is read from |
| `fix.diff` | the pull request's change, which the agent is shown |
| `developer_test.diff` | the maintainer's test, which it is **not** |
| `pr.json` | the full SWE-bench row |
| `child.log` | the child process's stdout, under `--parallel` |

`completions/` (raw prompt and response bytes per model call) is not committed: 43 MB across these instances. Set `LLM_LOG_COMPLETIONS=1` and rerun to regenerate it locally.

