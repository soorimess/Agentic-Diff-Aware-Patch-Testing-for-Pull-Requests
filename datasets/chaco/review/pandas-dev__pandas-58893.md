# pandas-dev__pandas-58893

[back to the list](README.md) -- **ENH: Add **kwargs to pivot_table to allow the specification of aggfunc keyword arguments #57884**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#58893](https://github.com/pandas-dev/pandas/pull/58893) (created 2024-06-02, merged 2024-06-06) |
| ChaCo lists | full, ablation, f2p30 |
| status | **runnable** -- 7 developer test(s) flip; oracle reproduces it |
| base commit | [`d6b7d5c9a25e`](https://github.com/pandas-dev/pandas/commit/d6b7d5c9a25e3dd02c8ea249a92f2f0f329b0e42) (2024-06-06), first parent of the merge commit |
| merge commit | [`8b705675bcb8`](https://github.com/pandas-dev/pandas/commit/8b705675bcb8ae86fb03e388e9969a1772236bf0) |
| issues closed | [#57884](https://github.com/pandas-dev/pandas/issues/57884) |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-58893:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-58893.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v3.0.0.rst`, `pandas/core/frame.py`, `pandas/core/reshape/pivot.py` |
| test files (`test_patch`) | `pandas/tests/reshape/test_pivot.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (7)

- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs3]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs4]`

## PASS_TO_PASS (168)

<details><summary>show</summary>

- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_columns_is_none`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_columns_not_given`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_duplicates`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_empty`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_is_none`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_list_values_none_immutable_args`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_none`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_integer_bug[object]`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_integer_bug[string]`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_not_changing_index_name`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_empty_dataframe_correct_index`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_handles_explicit_datetime_types`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_with_margins_and_numeric_column_names`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_values_is_none`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[10]`
- `pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_aggfunc[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_aggfunc[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_margins[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_margins[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_margins_category[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_margins_category[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_pivot_index_ordering[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_categorical_pivot_index_ordering[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_daily`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margin_with_only_columns_defined[A-mean-values0-expected_columns0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margin_with_only_columns_defined[columns1-sum-values1-expected_columns1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_casted_to_float`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_dtype`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_dtype_len`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_no_values_no_cols`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_no_values_one_row_one_col`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_no_values_two_row_two_cols`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_margins_no_values_two_rows`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_monthly`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_no_col`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pass_array`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pass_function`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_columns_lexsorted`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_columns_none_raise_error`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_complex_aggfunc`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_datetime_tz`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_dtaccessor`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_dtypes`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_ea_dtype_dropna[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_ea_dtype_dropna[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_index_with_nan[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_index_with_nan[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_index_with_nan_dates[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_index_with_nan_dates[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_integer_columns`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_margins_name_unicode`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_multi_functions`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_multi_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_no_level_overlap`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_no_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_number_of_levels_larger_than_int32[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_number_of_levels_larger_than_int32[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_periods[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_periods[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_periods_with_margins`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_preserve_dtypes[bool1-values0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_preserve_dtypes[bool1-values1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_preserve_dtypes[bool2-values2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_as_func`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[f3-f_numpy3]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[f4-f_numpy4]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[f5-f_numpy5]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[mean-mean]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[min-min]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_string_func_vs_func[sum-sum]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_aggfunc_dropna[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_aggfunc_dropna[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_aggfunc_nunique_with_different_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_aggfunc_scalar_dropna[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_aggfunc_scalar_dropna[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_categorical`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_categorical_observed_equal[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_categorical_observed_equal[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_datetime_warning`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_dropna`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_dropna_categoricals[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_dropna_categoricals[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_empty_aggfunc[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_empty_aggfunc[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_margins_name_with_aggfunc_list`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiindex_columns_doctest_case`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiindex_only[cols0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiindex_only[cols1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiindex_only[cols2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiindex_only[cols3]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_multiple`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_no_column_raises`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_nocols`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_not_series`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_nullable_margins`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_retains_tz`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_sort_false`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_sort_false_with_multiple_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_iterator_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_and_numeric_columns`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_set_margin_name[666]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_set_margin_name[None]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_set_margin_name[foo]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_set_margin_name[margin_name4]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_margins_set_margin_name[one]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_with_mixed_nested_tuples`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_timegrouper`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_timegrouper_double`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_tz_in_values`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[False-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[False-None]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[False-True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[True-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[True-None]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_categorical[True-True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-both-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-both-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-left-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-left-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-neither-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-neither-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-right-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[False-right-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-both-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-both-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-left-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-left-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-neither-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-neither-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-right-left_right0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index[True-right-left_right1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_interval_index_margins`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[False-Index]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[False-Series]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[False-array]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[False-list]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[True-Index]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[True-Series]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[True-array]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values[True-list]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[False-values0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[False-values1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[False-values2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[False-values3]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[True-values0]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[True-values1]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[True-values2]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_list_like_values_nans[True-values3]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_non_observable_dropna[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_non_observable_dropna[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_non_observable_dropna_multi_cat[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_non_observable_dropna_multi_cat[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tuple_of_values[False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tuple_of_values[True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[ms-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[ms-True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[ns-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[ns-True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[s-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[s-True]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[us-False]`
- `pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_tz[us-True]`

</details>

## Problem statement (what the agent may be shown)

```text
Issue #57884: ENH: Allow args to be specified for the pivot_table aggfunc

### Feature Type





### Problem Description

Currently the `pivot_table` has an `aggfunc` parameter which is used to do a groupby aggregation [here](https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py#L170). However, no additional arguments can be passed into that `agg` call. I'm specifically referring to the `*args` which can be specified in (df/series) [groupby.agg](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.agg.html) function. It would be very useful if `pivot_table` could accept additional arguments for the `aggfunc`.

### Feature Description

I'm not 100% sure, but I think it would be something like this:
1. Add a `**aggfunc_args` or `aggfunc_args: dict` parameter to the `pivot_table` function.
2. Do the same for the `__internal_pivot_table` function
3. Change the line [here](https://github.com/pandas-dev/pandas/blob/main/pandas/core/reshape/pivot.py#L170), from `agged = grouped.agg(aggfunc)` to `agged = grouped.agg(aggfunc, **aggfunc_args)`.
4. Update the docs

### Alternative Solutions

The same functionality can currently be achieved by specifying a custom function as `aggfunc`, but using that is much slower. My use case is pretty much the same as [this](https://stackoverflow.com/questions/56890105/how-to-keep-nan-in-pivot-table).
Instead of using `pd.pivot_table(... , aggfunc=lambda x: x.sum(min_count=1))`, I would like to be able to do `pd.pivot_table(... , aggfunc=sum, min_count=1)` or similiar.

### Additional Context

_No response_

---

Pull request #58893: ENH: Add **kwargs to pivot_table to allow the specification of aggfunc keyword arguments #57884

Add the option of passing keyword arguments to DataFrame.pivot_table and pivot_table's aggfunc through **kwargs.
```

## Hints (issue comments before the PR; not shown to the agent)

```text
Thanks for the request - it makes sense to me to support passing through kwargs here. The only question is how:

    def pivot_table(self, ..., **kwargs)
    def pivot_table(self, ..., kwargs)
    def pivot_table(self, ..., args, kwargs)

I do not think we should do

    def pivot_table(self, *args, ..., **kwargs)

If we want to agree with the current direction of apply/agg/transform, it would be the first of the above three options. Ref: https://github.com/pandas-dev/pandas/issues/40112
take
Hi, regarding that first option, would passing positional arguments to the aggfunc not be supported?
I must say I agree on the signature you proposed on the referenced issue ( `func, args, kwargs, other_arg`, sort of like the third option here) being the best overall, however, it seems like this is not the current standard for pandas.
take
> Hi, regarding that first option, would passing positional arguments to the aggfunc not be supported? I must say I agree on the signature you proposed on the referenced issue ( `func, args, kwargs, other_arg`, sort of like the third option here) being the best overall, however, it seems like this is not the current standard for pandas.

@rhshadrach Sorry to bother you, but could you share your thoughts on this matter?
@PF2100 - thanks for the ping! 

> I must say I agree on the signature you proposed on the referenced issue ( `func, args, kwargs, other_arg`, sort of like the third option here) being the best overall, however, it seems like this is not the current standard for pandas.

Same here, but for consistency, it seems best to go with (1) for now. Changing from `**kwargs` to `kwargs` is likely to be quite noisy or users and I don't feel confident it will get enough support.

> regarding that first option, would passing positional arguments to the aggfunc not be supported?

Correct.
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v3.0.0.rst b/doc/source/whatsnew/v3.0.0.rst
index 802a9fd7e2099e9ea6f79461fd87695b906b0117..abf18968076d06567b849e053b519ba04c22d151 100644
--- a/doc/source/whatsnew/v3.0.0.rst
+++ b/doc/source/whatsnew/v3.0.0.rst
@@ -42,6 +42,7 @@ Other enhancements
 - :meth:`DataFrame.corrwith` now accepts ``min_periods`` as optional arguments, as in :meth:`DataFrame.corr` and :meth:`Series.corr` (:issue:`9490`)
 - :meth:`DataFrame.cummin`, :meth:`DataFrame.cummax`, :meth:`DataFrame.cumprod` and :meth:`DataFrame.cumsum` methods now have a ``numeric_only`` parameter (:issue:`53072`)
 - :meth:`DataFrame.fillna` and :meth:`Series.fillna` can now accept ``value=None``; for non-object dtype the corresponding NA value will be used (:issue:`57723`)
+- :meth:`DataFrame.pivot_table` and :func:`pivot_table` now allow the passing of keyword arguments to ``aggfunc`` through ``**kwargs`` (:issue:`57884`)
 - :meth:`Series.cummin` and :meth:`Series.cummax` now supports :class:`CategoricalDtype` (:issue:`52335`)
 - :meth:`Series.plot` now correctly handle the ``ylabel`` parameter for pie charts, allowing for explicit control over the y-axis label (:issue:`58239`)
 - Restore support for reading Stata 104-format and enable reading 103-format dta files (:issue:`58554`)
diff --git a/pandas/core/frame.py b/pandas/core/frame.py
index c37dfa225de5ac636b716ba1d0ad32b61e1f93ba..a6c0e1e3725302868c77a6ecd3bbebe6d486d8cf 100644
--- a/pandas/core/frame.py
+++ b/pandas/core/frame.py
@@ -9275,6 +9275,11 @@ class DataFrame(NDFrame, OpsMixin):
 
             .. versionadded:: 1.3.0
 
+        **kwargs : dict
+            Optional keyword arguments to pass to ``aggfunc``.
+
+            .. versionadded:: 3.0.0
+
         Returns
         -------
         DataFrame
@@ -9382,6 +9387,7 @@ class DataFrame(NDFrame, OpsMixin):
         margins_name: Level = "All",
         observed: bool = True,
         sort: bool = True,
+        **kwargs,
     ) -> DataFrame:
         from pandas.core.reshape.pivot import pivot_table
 
@@ -9397,6 +9403,7 @@ class DataFrame(NDFrame, OpsMixin):
             margins_name=margins_name,
             observed=observed,
             sort=sort,
+            **kwargs,
         )
 
     def stack(
diff --git a/pandas/core/reshape/pivot.py b/pandas/core/reshape/pivot.py
index ff993c039bf9a5e101bc3e24c94a58a25f2c054b..8c2c2053b0554f1b05953639fa6dfe8acd3c8207 100644
--- a/pandas/core/reshape/pivot.py
+++ b/pandas/core/reshape/pivot.py
@@ -61,6 +61,7 @@ def pivot_table(
     margins_name: Hashable = "All",
     observed: bool = True,
     sort: bool = True,
+    **kwargs,
 ) -> DataFrame:
     """
     Create a spreadsheet-style pivot table as a DataFrame.
@@ -119,6 +120,11 @@ def pivot_table(
 
         .. versionadded:: 1.3.0
 
+    **kwargs : dict
+        Optional keyword arguments to pass to ``aggfunc``.
+
+        .. versionadded:: 3.0.0
+
     Returns
     -------
     DataFrame
@@ -246,6 +252,7 @@ def pivot_table(
                 margins_name=margins_name,
                 observed=observed,
                 sort=sort,
+                kwargs=kwargs,
             )
             pieces.append(_table)
             keys.append(getattr(func, "__name__", func))
@@ -265,6 +272,7 @@ def pivot_table(
         margins_name,
         observed,
         sort,
+        kwargs,
     )
     return table.__finalize__(data, method="pivot_table")
 
@@ -281,6 +289,7 @@ def __internal_pivot_table(
     margins_name: Hashable,
     observed: bool,
     sort: bool,
+    kwargs,
 ) -> DataFrame:
     """
     Helper of :func:`pandas.pivot_table` for any non-list ``aggfunc``.
@@ -323,7 +332,7 @@ def __internal_pivot_table(
         values = list(values)
 
     grouped = data.groupby(keys, observed=observed, sort=sort, dropna=dropna)
-    agged = grouped.agg(aggfunc)
+    agged = grouped.agg(aggfunc, **kwargs)
 
     if dropna and isinstance(agged, ABCDataFrame) and len(agged.columns):
         agged = agged.dropna(how="all")
@@ -378,6 +387,7 @@ def __internal_pivot_table(
             rows=index,
             cols=columns,
             aggfunc=aggfunc,
+            kwargs=kwargs,
             observed=dropna,
             margins_name=margins_name,
             fill_value=fill_value,
@@ -403,6 +413,7 @@ def _add_margins(
     rows,
     cols,
     aggfunc,
+    kwargs,
     observed: bool,
     margins_name: Hashable = "All",
     fill_value=None,
@@ -415,7 +426,7 @@ def _add_margins(
         if margins_name in table.index.get_level_values(level):
             raise ValueError(msg)
 
-    grand_margin = _compute_grand_margin(data, values, aggfunc, margins_name)
+    grand_margin = _compute_grand_margin(data, values, aggfunc, kwargs, margins_name)
 
     if table.ndim == 2:
         # i.e. DataFrame
@@ -436,7 +447,15 @@ def _add_margins(
 
     elif values:
         marginal_result_set = _generate_marginal_results(
-            table, data, values, rows, cols, aggfunc, observed, margins_name
+            table,
+            data,
+            values,
+            rows,
+            cols,
+            aggfunc,
+            kwargs,
+            observed,
+            margins_name,
         )
         if not isinstance(marginal_result_set, tuple):
             return marginal_result_set
@@ -445,7 +464,7 @@ def _add_margins(
         # no values, and table is a DataFrame
         assert isinstance(table, ABCDataFrame)
         marginal_result_set = _generate_marginal_results_without_values(
-            table, data, rows, cols, aggfunc, observed, margins_name
+            table, data, rows, cols, aggfunc, kwargs, observed, margins_name
         )
         if not isinstance(marginal_result_set, tuple):
             return marginal_result_set
@@ -482,26 +501,26 @@ def _add_margins(
 
 
 def _compute_grand_margin(
-    data: DataFrame, values, aggfunc, margins_name: Hashable = "All"
+    data: DataFrame, values, aggfunc, kwargs, margins_name: Hashable = "All"
 ):
     if values:
         grand_margin = {}
         for k, v in data[values].items():
             try:
                 if isinstance(aggfunc, str):
-                    grand_margin[k] = getattr(v, aggfunc)()
+                    grand_margin[k] = getattr(v, aggfunc)(**kwargs)
                 elif isinstance(aggfunc, dict):
                     if isinstance(aggfunc[k], str):
-                        grand_margin[k] = getattr(v, aggfunc[k])()
+                        grand_margin[k] = getattr(v, aggfunc[k])(**kwargs)
                     else:
-                        grand_margin[k] = aggfunc[k](v)
+                        grand_margin[k] = aggfunc[k](v, **kwargs)
                 else:
-                    grand_margin[k] = aggfunc(v)
+                    grand_margin[k] = aggfunc(v, **kwargs)
             except TypeError:
                 pass
         return grand_margin
     else:
-        return {margins_name: aggfunc(data.index)}
+        return {margins_name: aggfunc(data.index, **kwargs)}
 
 
 def _generate_marginal_results(
@@ -511,6 +530,7 @@ def _generate_marginal_results(
     rows,
     cols,
     aggfunc,
+    kwargs,
     observed: bool,
     margins_name: Hashable = "All",
 ):
@@ -524,7 +544,11 @@ def _generate_marginal_results(
             return (key, margins_name) + ("",) * (len(cols) - 1)
 
         if len(rows) > 0:
-            margin = data[rows + values].groupby(rows, observed=observed).agg(aggfunc)
+            margin = (
+                data[rows + values]
+                .groupby(rows, observed=observed)
+                .agg(aggfunc, **kwargs)
+            )
             cat_axis = 1
 
             for key, piece in table.T.groupby(level=0, observed=observed):
@@ -549,7 +573,7 @@ def _generate_marginal_results(
                 table_pieces.append(piece)
                 # GH31016 this is to calculate margin for each group, and assign
                 # corresponded key as index
-                transformed_piece = DataFrame(piece.apply(aggfunc)).T
+                transformed_piece = DataFrame(piece.apply(aggfunc, **kwargs)).T
                 if isinstance(piece.index, MultiIndex):
                     # We are adding an empty level
                     transformed_piece.index = MultiIndex.from_tuples(
@@ -579,7 +603,9 @@ def _generate_marginal_results(
         margin_keys = table.columns
 
     if len(cols) > 0:
-        row_margin = data[cols + values].groupby(cols, observed=observed).agg(aggfunc)
+        row_margin = (
+            data[cols + values].groupby(cols, observed=observed).agg(aggfunc, **kwargs)
+        )
         row_margin = row_margin.stack()
 
         # GH#26568. Use names instead of indices in case of numeric names
@@ -598,6 +624,7 @@ def _generate_marginal_results_without_values(
     rows,
     cols,
     aggfunc,
+    kwargs,
     observed: bool,
     margins_name: Hashable = "All",
 ):
@@ -612,14 +639,16 @@ def _generate_marginal_results_without_values(
             return (margins_name,) + ("",) * (len(cols) - 1)
 
         if len(rows) > 0:
-            margin = data.groupby(rows, observed=observed)[rows].apply(aggfunc)
+            margin = data.groupby(rows, observed=observed)[rows].apply(
+                aggfunc, **kwargs
+            )
             all_key = _all_key()
             table[all_key] = margin
             result = table
             margin_keys.append(all_key)
 
         else:
-            margin = data.groupby(level=0, observed=observed).apply(aggfunc)
+            margin = data.groupby(level=0, observed=observed).apply(aggfunc, **kwargs)
             all_key = _all_key()
             table[all_key] = margin
             result = table
@@ -630,7 +659,9 @@ def _generate_marginal_results_without_values(
         margin_keys = table.columns
 
     if len(cols):
-        row_margin = data.groupby(cols, observed=observed)[cols].apply(aggfunc)
+        row_margin = data.groupby(cols, observed=observed)[cols].apply(
+            aggfunc, **kwargs
+        )
     else:
         row_margin = Series(np.nan, index=result.columns)
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/reshape/test_pivot.py b/pandas/tests/reshape/test_pivot.py
index 4a13c1f5e1167966dd07bb57503127d637ff7bda..728becc76b71f521fa00e56c5a1f5affc36b6ab3 100644
--- a/pandas/tests/reshape/test_pivot.py
+++ b/pandas/tests/reshape/test_pivot.py
@@ -2058,6 +2058,60 @@ class TestPivotTable:
         ).rename_axis("A")
         tm.assert_frame_equal(result, expected)
 
+    @pytest.mark.parametrize("kwargs", [{"a": 2}, {"a": 2, "b": 3}, {"b": 3, "a": 2}])
+    def test_pivot_table_kwargs(self, kwargs):
+        # GH#57884
+        def f(x, a, b=3):
+            return x.sum() * a + b
+
+        def g(x):
+            return f(x, **kwargs)
+
+        df = DataFrame(
+            {
+                "A": ["good", "bad", "good", "bad", "good"],
+                "B": ["one", "two", "one", "three", "two"],
+                "X": [2, 5, 4, 20, 10],
+            }
+        )
+        result = pivot_table(
+            df, index="A", columns="B", values="X", aggfunc=f, **kwargs
+        )
+        expected = pivot_table(df, index="A", columns="B", values="X", aggfunc=g)
+        tm.assert_frame_equal(result, expected)
+
+    @pytest.mark.parametrize(
+        "kwargs", [{}, {"b": 10}, {"a": 3}, {"a": 3, "b": 10}, {"b": 10, "a": 3}]
+    )
+    def test_pivot_table_kwargs_margin(self, data, kwargs):
+        # GH#57884
+        def f(x, a=5, b=7):
+            return (x.sum() + b) * a
+
+        def g(x):
+            return f(x, **kwargs)
+
+        result = data.pivot_table(
+            values="D",
+            index=["A", "B"],
+            columns="C",
+            aggfunc=f,
+            margins=True,
+            fill_value=0,
+            **kwargs,
+        )
+
+        expected = data.pivot_table(
+            values="D",
+            index=["A", "B"],
+            columns="C",
+            aggfunc=g,
+            margins=True,
+            fill_value=0,
+        )
+
+        tm.assert_frame_equal(result, expected)
+
     @pytest.mark.parametrize(
         "f, f_numpy",
         [
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/reshape/test_pivot.py"
 ],
 "collected_before": 177,
 "collected_after": 177,
 "outcomes_before": {
  "PASSED": 168,
  "XFAIL": 2,
  "FAILED": 7
 },
 "outcomes_after": {
  "PASSED": 175,
  "XFAIL": 2
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "t.py::TestPivot::test_pivot_table_empty_dataframe_correct_index\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_handles_explicit_datetime_types\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_with_margins_and_numeric_column_names\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[1]\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[10]\nXFAIL pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_multiindex[True] - MultiIndexed unstack with tuple names fails with KeyError GH#19966\nXFAIL pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_multiindex[False] - MultiIndexed unstack with tuple names fails with KeyError GH#19966\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs0]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs1]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs[kwargs2]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs1]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs2]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs3]\nFAILED pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_table_kwargs_margin[kwargs4]\n=================== 7 failed, 168 passed, 2 xfailed in 8.97s ===================",
 "tail_after": "::TestPivot::test_pivot_integer_bug[string]\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_none\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_list_values_none_immutable_args\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_columns_not_given\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_columns_is_none\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_index_is_none\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_values_is_none\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_not_changing_index_name\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_empty_dataframe_correct_index\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_handles_explicit_datetime_types\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_pivot_table_with_margins_and_numeric_column_names\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[1]\nPASSED pandas/tests/reshape/test_pivot.py::TestPivot::test_unstack_copy[10]\nXFAIL pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_multiindex[True] - MultiIndexed unstack with tuple names fails with KeyError GH#19966\nXFAIL pandas/tests/reshape/test_pivot.py::TestPivotTable::test_pivot_with_multiindex[False] - MultiIndexed unstack with tuple names fails with KeyError GH#19966\n======================== 175 passed, 2 xfailed in 8.62s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
