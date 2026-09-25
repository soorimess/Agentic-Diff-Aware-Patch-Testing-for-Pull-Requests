# Run status, per pull request

Generated from `result.json` by `python -m openhands_f2p.runs`. Last run in this table: none.

- **26** instances across **12** repositories
- **0/0** fail-to-pass, of those that reached a verdict

- $0.00 and 0.0M tokens in total

Coverage is measured only for tests that are fail-to-pass; for anything else the question does not apply. A `—` in that column means not measured, not zero.

`concept`, `issue` and `readable` are three separate answers from one judgement call by a stronger model that wrote none of these tests: whether the test is about the same behaviour as the maintainer's, whether it reaches every behaviour the pull request settles, and whether it would pass review. None of them feeds the F2P verdict.

| instance | version | verdict | coverage | actions | concept | issue | readable | last run |
|---|---|---|---|---|---|---|---|---|
| [`django__django-11119`](./django__django-11119/) | 3.0 | — | — | — | — | — | — | — |
| [`django__django-13406`](./django__django-13406/) | 3.2 | — | — | — | — | — | — | — |
| [`django__django-15098`](./django__django-15098/) | 4.1 | — | — | — | — | — | — | — |
| [`django__django-16333`](./django__django-16333/) | 4.2 | — | — | — | — | — | — | — |
| [`django__django-17029`](./django__django-17029/) | 5.0 | — | — | — | — | — | — | — |
| [`psf__requests-1142`](./psf__requests-1142/) | 1.1 | — | — | — | — | — | — | — |
| [`psf__requests-6028`](./psf__requests-6028/) | 2.27 | — | — | — | — | — | — | — |
| [`pallets__flask-5014`](./pallets__flask-5014/) | 2.3 | — | — | — | — | — | — | — |
| [`pylint-dev__pylint-4970`](./pylint-dev__pylint-4970/) | 2.10 | — | — | — | — | — | — | — |
| [`pylint-dev__pylint-6903`](./pylint-dev__pylint-6903/) | 2.15 | — | — | — | — | — | — | — |
| [`pytest-dev__pytest-5262`](./pytest-dev__pytest-5262/) | 4.5 | — | — | — | — | — | — | — |
| [`pytest-dev__pytest-10081`](./pytest-dev__pytest-10081/) | 7.2 | — | — | — | — | — | — | — |
| [`sphinx-doc__sphinx-7454`](./sphinx-doc__sphinx-7454/) | 3.0 | — | — | — | — | — | — | — |
| [`sphinx-doc__sphinx-10614`](./sphinx-doc__sphinx-10614/) | 7.2 | — | — | — | — | — | — | — |
| [`pydata__xarray-3677`](./pydata__xarray-3677/) | 0.12 | — | — | — | — | — | — | — |
| [`pydata__xarray-7233`](./pydata__xarray-7233/) | 2022.09 | — | — | — | — | — | — | — |
| [`astropy__astropy-7336`](./astropy__astropy-7336/) | 1.3 | — | — | — | — | — | — | — |
| [`astropy__astropy-14995`](./astropy__astropy-14995/) | 5.2 | — | — | — | — | — | — | — |
| [`sympy__sympy-12096`](./sympy__sympy-12096/) | 1.0 | — | — | — | — | — | — | — |
| [`sympy__sympy-24562`](./sympy__sympy-24562/) | 1.12 | — | — | — | — | — | — | — |
| [`mwaskom__seaborn-3069`](./mwaskom__seaborn-3069/) | 0.12 | — | — | — | — | — | — | — |
| [`mwaskom__seaborn-3187`](./mwaskom__seaborn-3187/) | 0.12 | — | — | — | — | — | — | — |
| [`matplotlib__matplotlib-13989`](./matplotlib__matplotlib-13989/) | 3.0 | — | — | — | — | — | — | — |
| [`matplotlib__matplotlib-26208`](./matplotlib__matplotlib-26208/) | 3.7 | — | — | — | — | — | — | — |
| [`scikit-learn__scikit-learn-10908`](./scikit-learn__scikit-learn-10908/) | 0.20 | — | — | — | — | — | — | — |
| [`scikit-learn__scikit-learn-25747`](./scikit-learn__scikit-learn-25747/) | 1.3 | — | — | — | — | — | — | — |

## Without a verdict

- **django__django-11119** — never run
- **django__django-13406** — never run
- **django__django-15098** — never run
- **django__django-16333** — never run
- **django__django-17029** — never run
- **psf__requests-1142** — never run
- **psf__requests-6028** — never run
- **pallets__flask-5014** — never run
- **pylint-dev__pylint-4970** — never run
- **pylint-dev__pylint-6903** — never run
- **pytest-dev__pytest-5262** — never run
- **pytest-dev__pytest-10081** — never run
- **sphinx-doc__sphinx-7454** — never run
- **sphinx-doc__sphinx-10614** — never run
- **pydata__xarray-3677** — never run
- **pydata__xarray-7233** — never run
- **astropy__astropy-7336** — never run
- **astropy__astropy-14995** — never run
- **sympy__sympy-12096** — never run
- **sympy__sympy-24562** — never run
- **mwaskom__seaborn-3069** — never run
- **mwaskom__seaborn-3187** — never run
- **matplotlib__matplotlib-13989** — never run
- **matplotlib__matplotlib-26208** — never run
- **scikit-learn__scikit-learn-10908** — never run
- **scikit-learn__scikit-learn-25747** — never run

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

