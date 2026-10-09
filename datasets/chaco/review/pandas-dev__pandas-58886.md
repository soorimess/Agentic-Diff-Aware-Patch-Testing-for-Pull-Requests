# pandas-dev__pandas-58886

[back to the list](README.md) -- **BUG: Check `min_periods` before applying the function**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#58886](https://github.com/pandas-dev/pandas/pull/58886) (created 2024-06-01, merged 2024-06-03) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`f49b286615a3`](https://github.com/pandas-dev/pandas/commit/f49b286615a3a67d8bf41b007b18ce6e10f8d0de) (2024-06-03), first parent of the merge commit |
| merge commit | [`ed4b8676f46b`](https://github.com/pandas-dev/pandas/commit/ed4b8676f46bb259f8be2a6ba6466602002e0e4a) |
| issues closed | [#58868](https://github.com/pandas-dev/pandas/issues/58868) |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-58886:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-58886.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v3.0.0.rst`, `pandas/core/window/numba_.py` |
| test files (`test_patch`) | `pandas/tests/window/test_numba.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `pandas/tests/window/test_numba.py::TestEngine::test_numba_min_periods`

## PASS_TO_PASS (744)

<details><summary>show</summary>

- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-False-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-False-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-False-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-False-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-True-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-True-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-True-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-False-True-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-False-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-False-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-False-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-False-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-True-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-True-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-True-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-False-True-True-True-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-False-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-False-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-False-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-False-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-True-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-True-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-True-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-False-True-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-False-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-False-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-False-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-False-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-True-mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-True-mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-True-sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba[False-True-True-True-True-sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-False-True-False-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-False-True-False-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-False-True-True-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-False-True-True-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-True-True-False-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-True-True-False-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-True-True-True-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_cython_vs_numba_times[False-True-True-True-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine[mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine[mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine[sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine[sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine_kwargs[mean-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine_kwargs[mean-groupby]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine_kwargs[sum-None]`
- `pandas/tests/window/test_numba.py::TestEWM::test_invalid_engine_kwargs[sum-groupby]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-False-True-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_cache_apply[False-True-True-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-False-True-single-expanding-window_kwargs1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-False-True-single-rolling-window_kwargs0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-False-True-table-expanding-window_kwargs1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-False-True-table-rolling-window_kwargs0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-True-True-single-expanding-window_kwargs1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-True-True-single-rolling-window_kwargs0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-True-True-table-expanding-window_kwargs1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_args[False-True-True-table-rolling-window_kwargs0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_dont_cache_engine_kwargs`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-False-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-False-True-True-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-False-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-1-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-1-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-10-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-10-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-2-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-2-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-5-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-5-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-None-False]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_apply[False-True-True-True-None-True]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators0-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators0-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators3-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators3-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators4-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators4-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators6-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators6-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators7-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators7-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators8-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-False-True-arithmetic_numba_supported_operators8-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators0-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators0-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators3-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators3-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators4-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators4-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators6-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators6-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators7-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators7-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators8-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_expanding_methods[False-True-True-arithmetic_numba_supported_operators8-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5-data4]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None-data0]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None-data1]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None-data2]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None-data3]`
- `pandas/tests/window/test_numba.py::TestEngine::test_numba_vs_cython_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None-data4]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_apply[False-False-True]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_apply[False-True-True]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators3]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators4]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators6]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators7]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-False-True-arithmetic_numba_supported_operators8]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators0]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators3]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators4]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators6]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators7]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_expanding_methods[False-True-True-arithmetic_numba_supported_operators8]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-False-True-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-False-True-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-False-True-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-False-True-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-False-True-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-True-True-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-True-True-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-True-True-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-True-True-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_apply[False-True-True-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators0-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators1-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators2-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators3-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators4-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators5-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators6-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators7-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-False-True-arithmetic_numba_supported_operators8-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators0-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators1-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators2-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators3-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators4-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators5-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators6-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators7-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_methods[False-True-True-arithmetic_numba_supported_operators8-None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_weighted_mean[10]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_weighted_mean[1]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_weighted_mean[2]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_weighted_mean[5]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_rolling_weighted_mean[None]`
- `pandas/tests/window/test_numba.py::TestTableMethod::test_table_series_valueerror`
- `pandas/tests/window/test_numba.py::test_invalid_kwargs_nopython`
- `pandas/tests/window/test_numba.py::test_npfunc_no_warnings`
- `pandas/tests/window/test_numba.py::test_use_global_config`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #58868: BUG: Rolling .apply() with method='table' ignores min_periods

### Pandas version checks





### Reproducible Example

```python
import pandas as pd

df = pd.DataFrame([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]], columns=['A', 'B'])
print(df)

# prints this:
#    A   B
# 0  1   2
# 1  3   4
# 2  5   6
# 3  7   8
# 4  9  10

df.rolling(3, min_periods=3).apply(lambda x: bool(print(x, '\n')))

# prints this, so as expected, only batches of 3 are being evaluated
# 0    1.0
# 1    3.0
# 2    5.0
# dtype: float64 
# 
# 1    3.0
# 2    5.0
# 3    7.0
# dtype: float64 
# 
# 2    5.0
# 3    7.0
# 4    9.0
# dtype: float64 
# 
# 0    2.0
# 1    4.0
# 2    6.0
# dtype: float64 
# 
# 1    4.0
# 2    6.0
# 3    8.0
# dtype: float64 
# 
# 2     6.0
# 3     8.0
# 4    10.0
# dtype: float64 
# 
# Out[33]: 
#      A    B
# 0  NaN  NaN
# 1  NaN  NaN
# 2  0.0  0.0
# 3  0.0  0.0
# 4  0.0  0.0

df.rolling(3, method='table', min_periods=3).apply(lambda x: bool(print(x, '\n')), raw=True, engine='numba')

# prints this, where we see that the first two batches of sizes 1 and 2 are also being evaluated
# [[1. 2.]]   <-- batch of size 1, illegal
# 
# [[1. 2.]    <-- batch of size 2, illegal
#  [3. 4.]] 
# 
# [[1. 2.]
#  [3. 4.]
#  [5. 6.]] 
# 
# [[3. 4.]
#  [5. 6.]
#  [7. 8.]] 
# 
# [[ 5.  6.]
#  [ 7.  8.]
#  [ 9. 10.]] 
# Out[34]: 
#      A    B
# 0  NaN  NaN
# 1  NaN  NaN
# 2  0.0  0.0
# 3  0.0  0.0
# 4  0.0  0.0
```


### Issue Description

See example above, which violates the contract imposed by the `min_periods` parameter.

### Expected Behavior

The `min_periods` parameter should be respected.

### Installed Versions

<details>

INSTALLED VERSIONS
------------------
commit                : d9cdd2ee5a58015ef6f4d15c7226110c9aab8140
python                : 3.12.3.final.0
python-bits           : 64
OS                    : Windows
OS-release            : 11
Version               : 10.0.22631
machine               : AMD64
processor             : Intel64 Family 6 Model 165 Stepping 2, GenuineIntel
byteorder             : little
LC_ALL                : None
LANG                  : None
LOCALE                : German_Switzerland.utf8
pandas                : 2.2.2
numpy                 : 1.26.4
pytz                  : 2024.1
dateutil              : 2.9.0
setuptools            : 69.5.1
pip                   : 24.0
Cython                : None
pytest                : None
hypothesis            : None
sphinx                : None
blosc                 : None
feather               : None
xlsxwriter            : None
lxml.etree            : 5.2.2
html5lib              : 1.1
pymysql               : None
psycopg2              : None
jinja2                : 3.1.4
IPython               : 8.24.0
pandas_datareader     : None
adbc-driver-postgresql: None
adbc-driver-sqlite    : None
bs4                   : 4.12.3
bottleneck            : None
dataframe-api-compat  : None
fastparquet           : None
fsspec                : None
gcsfs                 : None
matplotlib            : 3.8.4
numba                 : 0.59.1
numexpr               : None
odfpy                 : None
openpyxl              : None
pandas_gbq            : None
pyarrow               : 16.0.0
pyreadstat            : None
python-calamine       : None
pyxlsb                : None
s3fs                  : None
scipy                 : 1.13.0
sqlalchemy            : None
tables                : None
tabulate              : None
xarray                : None
xlrd                  : None
zstandard             : None
tzdata                : 2024.1
qtpy                  : None
pyqt5                 : None
</details>

---

Pull request #58886: BUG: Check `min_periods` before applying the function
````

## Hints (issue comments before the PR; not shown to the agent)

```text
Thanks for the report - further investigations and PRs to fix are welcome!
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v3.0.0.rst b/doc/source/whatsnew/v3.0.0.rst
index 865996bdf889237a27b48fb8feba1e69ba4632a0..872c5b64892e107c268dda293b789ca00f4c9257 100644
--- a/doc/source/whatsnew/v3.0.0.rst
+++ b/doc/source/whatsnew/v3.0.0.rst
@@ -536,7 +536,7 @@ Groupby/resample/rolling
 - Bug in :meth:`DataFrameGroupBy.apply` that was returning a completely empty DataFrame when all return values of ``func`` were ``None`` instead of returning an empty DataFrame with the original columns and dtypes. (:issue:`57775`)
 - Bug in :meth:`DataFrameGroupBy.apply` with ``as_index=False`` that was returning :class:`MultiIndex` instead of returning :class:`Index`. (:issue:`58291`)
 - Bug in :meth:`DataFrameGroupby.transform` and :meth:`SeriesGroupby.transform` with a reducer and ``observed=False`` that coerces dtype to float when there are unobserved categories. (:issue:`55326`)
-
+- Bug in :meth:`Rolling.apply` where the applied function could be called on fewer than ``min_period`` periods if ``method="table"``. (:issue:`58868`)
 
 Reshaping
 ^^^^^^^^^
diff --git a/pandas/core/window/numba_.py b/pandas/core/window/numba_.py
index eb06479fc325ea4f3cb044a76545a62abaf1dd72..824cf936b81850a47cf486d39702e95a4f8404ad 100644
--- a/pandas/core/window/numba_.py
+++ b/pandas/core/window/numba_.py
@@ -227,10 +227,10 @@ def generate_numba_table_func(
             stop = end[i]
             window = values[start:stop]
             count_nan = np.sum(np.isnan(window), axis=0)
-            sub_result = numba_func(window, *args)
             nan_mask = len(window) - count_nan >= minimum_periods
+            if nan_mask.any():
+                result[i, :] = numba_func(window, *args)
             min_periods_mask[i, :] = nan_mask
-            result[i, :] = sub_result
         result = np.where(min_periods_mask, result, np.nan)
         return result
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/window/test_numba.py b/pandas/tests/window/test_numba.py
index 650eb911e410b7e952469bef94cadcdbeb34bc34..3695ab8bf6cd33fbbe93914100f0ca6f31475d2d 100644
--- a/pandas/tests/window/test_numba.py
+++ b/pandas/tests/window/test_numba.py
@@ -67,6 +67,21 @@ class TestEngine:
         )
         tm.assert_series_equal(result, expected)
 
+    def test_numba_min_periods(self):
+        # GH 58868
+        def last_row(x):
+            assert len(x) == 3
+            return x[-1]
+
+        df = DataFrame([[1, 2], [3, 4], [5, 6], [7, 8]])
+
+        result = df.rolling(3, method="table", min_periods=3).apply(
+            last_row, raw=True, engine="numba"
+        )
+
+        expected = DataFrame([[np.nan, np.nan], [np.nan, np.nan], [5, 6], [7, 8]])
+        tm.assert_frame_equal(result, expected)
+
     @pytest.mark.parametrize(
         "data",
         [
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/window/test_numba.py"
 ],
 "collected_before": 745,
 "collected_after": 745,
 "outcomes_before": {
  "PASSED": 744,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 745
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data2]\nPASSED pandas/tests/window/test_numba.py::test_npfunc_no_warnings\nFAILED pandas/tests/window/test_numba.py::TestEngine::test_numba_min_periods\n================== 1 failed, 744 passed in 249.12s (0:04:09) ===================",
 "tail_after": "e-True-arithmetic_numba_supported_operators8]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-mean-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-True-True-sum-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-mean-data2]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data0]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data1]\nPASSED pandas/tests/window/test_numba.py::TestTableMethod::test_table_method_ewm[False-False-True-sum-data2]\nPASSED pandas/tests/window/test_numba.py::test_npfunc_no_warnings\n======================= 745 passed in 256.14s (0:04:16) ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
