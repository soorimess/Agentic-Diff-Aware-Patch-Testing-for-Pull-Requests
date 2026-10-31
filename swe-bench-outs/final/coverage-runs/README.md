# Coverage runs: 18 PRs, without and with the coverage tool

Each PR has one run without the coverage tool and one with it. Every folder is a full copy of the run: `trajectory.json` (the agent's steps), `flow.log` (readable step log), `tool_log.json` (tool calls and answers), the handed-in test `test_f2p_*.py` and `result.json` (verdict and coverage).

| PR | without | with | gain | without: run | with: run |
|---|---:|---:|---:|---|---|
| xarray 6971 | 1.3% | 87.0% | +85.7 | [without-coverage-tool/pydata__xarray-6971](without-coverage-tool/pydata__xarray-6971/trajectory.json) | [with-coverage-tool/pydata__xarray-6971](with-coverage-tool/pydata__xarray-6971/trajectory.json) |
| pylint 4551 | 16.1% | 82.3% | +66.2 | [without-coverage-tool/pylint-dev__pylint-4551](without-coverage-tool/pylint-dev__pylint-4551/trajectory.json) | [with-coverage-tool/pylint-dev__pylint-4551](with-coverage-tool/pylint-dev__pylint-4551/trajectory.json) |
| sympy 14085 | 41.4% | 89.7% | +48.3 | [without-coverage-tool/sympy__sympy-14085](without-coverage-tool/sympy__sympy-14085/trajectory.json) | [with-coverage-tool/sympy__sympy-14085](with-coverage-tool/sympy__sympy-14085/trajectory.json) |
| matplotlib 20693 | 13.0% | 57.4% | +44.4 | [without-coverage-tool/matplotlib__matplotlib-20693](without-coverage-tool/matplotlib__matplotlib-20693/trajectory.json) | [with-coverage-tool/matplotlib__matplotlib-20693](with-coverage-tool/matplotlib__matplotlib-20693/trajectory.json) |
| pytest 5787 | 59.2% | 100.0% | +40.8 | [without-coverage-tool/pytest-dev__pytest-5787](without-coverage-tool/pytest-dev__pytest-5787/trajectory.json) | [with-coverage-tool/pytest-dev__pytest-5787](with-coverage-tool/pytest-dev__pytest-5787/trajectory.json) |
| sphinx 7380 | 38.8% | 79.1% | +40.3 | [without-coverage-tool/sphinx-doc__sphinx-7380](without-coverage-tool/sphinx-doc__sphinx-7380/trajectory.json) | [with-coverage-tool/sphinx-doc__sphinx-7380](with-coverage-tool/sphinx-doc__sphinx-7380/trajectory.json) |
| scikit-learn 14012 | 64.6% | 98.5% | +33.9 | [without-coverage-tool/scikit-learn__scikit-learn-14012](without-coverage-tool/scikit-learn__scikit-learn-14012/trajectory.json) | [with-coverage-tool/scikit-learn__scikit-learn-14012](with-coverage-tool/scikit-learn__scikit-learn-14012/trajectory.json) |
| sympy 17512 | 24.7% | 56.5% | +31.8 | [without-coverage-tool/sympy__sympy-17512](without-coverage-tool/sympy__sympy-17512/trajectory.json) | [with-coverage-tool/sympy__sympy-17512](with-coverage-tool/sympy__sympy-17512/trajectory.json) |
| sphinx 7234 | 6.6% | 35.0% | +28.4 | [without-coverage-tool/sphinx-doc__sphinx-7234](without-coverage-tool/sphinx-doc__sphinx-7234/trajectory.json) | [with-coverage-tool/sphinx-doc__sphinx-7234](with-coverage-tool/sphinx-doc__sphinx-7234/trajectory.json) |
| matplotlib 25515 | 7.5% | 30.6% | +23.1 | [without-coverage-tool/matplotlib__matplotlib-25515](without-coverage-tool/matplotlib__matplotlib-25515/trajectory.json) | [with-coverage-tool/matplotlib__matplotlib-25515](with-coverage-tool/matplotlib__matplotlib-25515/trajectory.json) |
| sphinx 7590 | 42.6% | 63.0% | +20.4 | [without-coverage-tool/sphinx-doc__sphinx-7590](without-coverage-tool/sphinx-doc__sphinx-7590/trajectory.json) | [with-coverage-tool/sphinx-doc__sphinx-7590](with-coverage-tool/sphinx-doc__sphinx-7590/trajectory.json) |
| xarray 7444 | 80.4% | 98.0% | +17.6 | [without-coverage-tool/pydata__xarray-7444](without-coverage-tool/pydata__xarray-7444/trajectory.json) | [with-coverage-tool/pydata__xarray-7444](with-coverage-tool/pydata__xarray-7444/trajectory.json) |
| sympy 13236 | 6.8% | 20.5% | +13.7 | [without-coverage-tool/sympy__sympy-13236](without-coverage-tool/sympy__sympy-13236/trajectory.json) | [with-coverage-tool/sympy__sympy-13236](with-coverage-tool/sympy__sympy-13236/trajectory.json) |
| django 11991 | 35.8% | 47.2% | +11.4 | [without-coverage-tool/django__django-11991](without-coverage-tool/django__django-11991/trajectory.json) | [with-coverage-tool/django__django-11991](with-coverage-tool/django__django-11991/trajectory.json) |
| astropy 7008 | 81.5% | 81.5% | +0.0 | [without-coverage-tool/astropy__astropy-7008](without-coverage-tool/astropy__astropy-7008/trajectory.json) | [with-coverage-tool/astropy__astropy-7008](with-coverage-tool/astropy__astropy-7008/trajectory.json) |
| django 16092 | 13.1% | 13.1% | +0.0 | [without-coverage-tool/django__django-16092](without-coverage-tool/django__django-16092/trajectory.json) | [with-coverage-tool/django__django-16092](with-coverage-tool/django__django-16092/trajectory.json) |
| matplotlib 19743 | 43.3% | 43.3% | +0.0 | [without-coverage-tool/matplotlib__matplotlib-19743](without-coverage-tool/matplotlib__matplotlib-19743/trajectory.json) | [with-coverage-tool/matplotlib__matplotlib-19743](with-coverage-tool/matplotlib__matplotlib-19743/trajectory.json) |
| astropy 14295 | 54.0% | 46.0% | -8.0 | [without-coverage-tool/astropy__astropy-14295](without-coverage-tool/astropy__astropy-14295/trajectory.json) | [with-coverage-tool/astropy__astropy-14295](with-coverage-tool/astropy__astropy-14295/trajectory.json) |

Source arm of each copy:

- xarray 6971: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- pylint 4551: without = arm A (no coverage tool), with = arm B (coverage tool)
- sympy 14085: without = arm A (no coverage tool), with = arm B (coverage tool)
- matplotlib 20693: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- pytest 5787: without = arm A (no coverage tool), with = arm B (coverage tool)
- sphinx 7380: without = arm A (no coverage tool), with = arm B (coverage tool)
- scikit-learn 14012: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- sympy 17512: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- sphinx 7234: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- matplotlib 25515: without = arm A (no coverage tool), with = arm B (coverage tool)
- sphinx 7590: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- xarray 7444: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- sympy 13236: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- django 11991: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- astropy 7008: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- django 16092: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- matplotlib 19743: without = arm A (no coverage tool), with = arm C (coverage + mutation tool)
- astropy 14295: without = arm A (no coverage tool), with = arm B (coverage tool)
