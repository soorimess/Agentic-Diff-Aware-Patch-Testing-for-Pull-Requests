# pandas-dev__pandas-60196

[back to the list](README.md) -- **BUG: fix inspect usage when pyarrow or jinja2 is not installed**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60196](https://github.com/pandas-dev/pandas/pull/60196) (created 2024-11-05, merged 2024-11-05) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (208 pass on both sides) |
| base commit | [`e449b4971620`](https://github.com/pandas-dev/pandas/commit/e449b49716203bbf04d20bc867fda7ea6d562ef5) (2024-11-05), first parent of the merge commit |
| merge commit | [`169b00e1eaf0`](https://github.com/pandas-dev/pandas/commit/169b00e1eaf06924aee585d8e5469dc284992382) |
| issues closed | none |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-60196:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60196.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v2.3.0.rst`, `pandas/core/arrays/arrow/accessors.py`, `pandas/core/frame.py` |
| test files (`test_patch`) | `pandas/tests/frame/test_api.py`, `pandas/tests/series/test_api.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (208)

<details><summary>show</summary>

- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_attrs`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_attrs_deepcopy`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_axis_aliases`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_class_axis`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_column_contains_raises`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_constructor_expanddim`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_deepcopy`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_display_max_dir_items`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty_like[df0]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty_like[df1]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty_like[df2]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty_like[df3]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_empty_nonzero`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_get_agg_axis`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_get_axis`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_getitem_pop_assign_name`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_inplace_return_self`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_inspect_getmembers`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_len`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_new_empty_index`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_not_hashable`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_series_put_names`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[DataFrame-False]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[DataFrame-None]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[DataFrame-True]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[Series-False]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[Series-None]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_set_flags[Series-True]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_tab_complete_warning[DataFrame]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_tab_complete_warning[Series]`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_tab_completion`
- `pandas/tests/frame/test_api.py::TestDataFrameMisc::test_with_datetimelikes`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_attrs`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_axis_alias`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_class_axis`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_contains`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_datetime_series_no_datelike_attrs[day]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_datetime_series_no_datelike_attrs[second]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_datetime_series_no_datelike_attrs[weekday]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_datetime_series_no_datelike_attrs[year]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_empty_method`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_empty_method_full_series[int64]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_empty_method_full_series[object]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index0]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index10]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index11]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index12]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index1]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index2]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index3]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index4]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index5]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index6]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index7]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index8]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_index_tab_completion[index9]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_inspect_getmembers`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_integer_series_size[Int64]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_integer_series_size[None]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_ndarray_compat`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_ndarray_compat_like_func`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_not_hashable[ser0]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_not_hashable[ser1]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-all-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-any-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-bfill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-corr-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-count-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-cov-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-cummax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-cummin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-cumprod-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-cumsum-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-diff-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-ffill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-fillna-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-head-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-idxmax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-idxmin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-max-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-mean-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-median-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-min-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-nunique-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-pct_change-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-prod-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-quantile-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-rank-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-sample-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-sem-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-shift-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-skew-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-std-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-sum-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-tail-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-take-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[bool-var-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-all-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-any-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-bfill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-corr-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-count-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-cov-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-cummax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-cummin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-cumprod-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-cumsum-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-diff-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-ffill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-fillna-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-head-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-idxmax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-idxmin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-max-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-mean-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-median-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-min-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-nunique-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-pct_change-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-prod-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-quantile-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-rank-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-sample-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-sem-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-shift-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-skew-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-std-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-sum-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-tail-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-take-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[float-var-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-all-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-any-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-bfill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-corr-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-count-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-cov-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-cummax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-cummin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-cumprod-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-cumsum-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-diff-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-ffill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-fillna-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-head-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-idxmax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-idxmin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-max-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-mean-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-median-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-min-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-nunique-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-pct_change-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-prod-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-quantile-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-rank-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-sample-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-sem-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-shift-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-skew-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-std-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-sum-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-tail-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-take-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[int-var-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-all-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-any-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-bfill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-corr-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-count-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cov-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cummax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cummin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumprod-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumsum-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-diff-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-ffill-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-fillna-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-head-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-idxmax-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-idxmin-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-max-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-mean-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-median-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-min-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-nunique-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-pct_change-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-prod-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-quantile-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-rank-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-sample-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-sem-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-shift-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-skew-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-std-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-sum-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-tail-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-take-False]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-var-True]`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_series_datetimelike_attribute_access`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_series_datetimelike_attribute_access_invalid`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_tab_completion`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_tab_completion_cat`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_tab_completion_cat_str`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_tab_completion_dt`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_tab_completion_with_categorical`
- `pandas/tests/series/test_api.py::TestSeriesMisc::test_unknown_attribute`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #60196: BUG: fix inspect usage when pyarrow or jinja2 is not installed

This started with trying to fix the xfail when using the string dtype without pyarrow installed, but in practice this was not related to the string dtype, but just to pyarrow not being available (and apparently we only test that case in the build with the future string dtype enabled?).

We need to ensure to return an AttributeError instead of ImportError when accessing attributes on Series/DataFrame, and then `inspect.getmembers` will ignore that error.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v2.3.0.rst b/doc/source/whatsnew/v2.3.0.rst
index 90f9f4ed464c692a41978988459d07677424a9c4..922cc0ead7fb090277f35727e024d4161c74f26d 100644
--- a/doc/source/whatsnew/v2.3.0.rst
+++ b/doc/source/whatsnew/v2.3.0.rst
@@ -173,7 +173,8 @@ Styler
 
 Other
 ^^^^^
--
+- Fixed usage of ``inspect`` when the optional dependencies ``pyarrow`` or ``jinja2``
+  are not installed (:issue:`60196`)
 -
 
 .. ---------------------------------------------------------------------------
diff --git a/pandas/core/arrays/arrow/accessors.py b/pandas/core/arrays/arrow/accessors.py
index d9a80b699b0bb8b7b298c2618fb0b34df0d14ca4..230522846d3773b0832a8f59855949a29c7e7df5 100644
--- a/pandas/core/arrays/arrow/accessors.py
+++ b/pandas/core/arrays/arrow/accessors.py
@@ -46,7 +46,7 @@ class ArrowAccessor(metaclass=ABCMeta):
 
     def _validate(self, data) -> None:
         dtype = data.dtype
-        if not isinstance(dtype, ArrowDtype):
+        if pa_version_under10p1 or not isinstance(dtype, ArrowDtype):
             # Raise AttributeError so that inspect can handle non-struct Series.
             raise AttributeError(self._validation_msg.format(dtype=dtype))
 
diff --git a/pandas/core/frame.py b/pandas/core/frame.py
index a3a459796f7653412f919bc2ae0c78252e4cfc8a..b35e2c8497fb7c8ad7317ef4da8fe039e291c736 100644
--- a/pandas/core/frame.py
+++ b/pandas/core/frame.py
@@ -1397,6 +1397,11 @@ class DataFrame(NDFrame, OpsMixin):
         Please see
         `Table Visualization <../../user_guide/style.ipynb>`_ for more examples.
         """
+        # Raise AttributeError so that inspect works even if jinja2 is not installed.
+        has_jinja2 = import_optional_dependency("jinja2", errors="ignore")
+        if not has_jinja2:
+            raise AttributeError("The '.style' accessor requires jinja2")
+
         from pandas.io.formats.style import Styler
 
         return Styler(self)
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/frame/test_api.py b/pandas/tests/frame/test_api.py
index 3fb994f2e0aff5f5f1d1d632f104df47444feb77..2b0bf1b0576f9765056a6ee303f4e1b2fe0d325f 100644
--- a/pandas/tests/frame/test_api.py
+++ b/pandas/tests/frame/test_api.py
@@ -376,6 +376,5 @@ class TestDataFrameMisc:
 
     def test_inspect_getmembers(self):
         # GH38740
-        pytest.importorskip("jinja2")
         df = DataFrame()
         inspect.getmembers(df)
diff --git a/pandas/tests/series/test_api.py b/pandas/tests/series/test_api.py
index 79a55eb357f87922b9dd3d15288a02af74c26b81..4b369bb0bc86935ac94113a858cfb5d99082e34f 100644
--- a/pandas/tests/series/test_api.py
+++ b/pandas/tests/series/test_api.py
@@ -4,10 +4,6 @@ import pydoc
 import numpy as np
 import pytest
 
-from pandas._config import using_string_dtype
-
-from pandas.compat import HAS_PYARROW
-
 import pandas as pd
 from pandas import (
     DataFrame,
@@ -164,12 +160,8 @@ class TestSeriesMisc:
         result = s + 1
         assert result.attrs == {"version": 1}
 
-    @pytest.mark.xfail(
-        using_string_dtype() and not HAS_PYARROW, reason="TODO(infer_string)"
-    )
     def test_inspect_getmembers(self):
         # GH38782
-        pytest.importorskip("jinja2")
         ser = Series(dtype=object)
         inspect.getmembers(ser)
```

## Validation

```json
{
 "image_head": "e449b49716203bbf04d20bc867fda7ea6d562ef5",
 "patch_applies": true,
 "test_files": [
  "pandas/tests/frame/test_api.py",
  "pandas/tests/series/test_api.py"
 ],
 "collected_before": 209,
 "collected_after": 209,
 "outcomes_before": {
  "PASSED": 208,
  "XFAIL": 1
 },
 "outcomes_after": {
  "PASSED": 208,
  "XFAIL": 1
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "eries/test_api.py::TestSeriesMisc::test_numeric_only[object-shift-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-diff-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumsum-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cummin-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumprod-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-fillna-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-ffill-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-bfill-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-sample-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-tail-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-take-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-head-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cov-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-corr-False]\nXFAIL pandas/tests/frame/test_api.py::TestDataFrameMisc::test_column_name_contains_unicode_surrogate - surrogates not allowed\n======================== 208 passed, 1 xfailed in 3.73s ========================",
 "tail_after": "eries/test_api.py::TestSeriesMisc::test_numeric_only[object-shift-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-diff-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumsum-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cummin-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cumprod-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-fillna-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-ffill-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-bfill-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-sample-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-tail-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-take-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-head-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-cov-False]\nPASSED pandas/tests/series/test_api.py::TestSeriesMisc::test_numeric_only[object-corr-False]\nXFAIL pandas/tests/frame/test_api.py::TestDataFrameMisc::test_column_name_contains_unicode_surrogate - surrogates not allowed\n======================== 208 passed, 1 xfailed in 1.95s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
