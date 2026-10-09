# pandas-dev__pandas-60505

[back to the list](README.md) -- **BUG: Fix bug in GroupBy that ignores group_keys arg for empty datafra…**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60505](https://github.com/pandas-dev/pandas/pull/60505) (created 2024-12-06, merged 2024-12-06) |
| ChaCo lists | full, ablation |
| status | **runnable** -- 2 developer test(s) flip; oracle reproduces it |
| base commit | [`497208f03ce2`](https://github.com/pandas-dev/pandas/commit/497208f03ce226d5e006e7a713ceab5f303fe1e2) (2024-12-06), first parent of the merge commit |
| merge commit | [`8a286fa16f31`](https://github.com/pandas-dev/pandas/commit/8a286fa16f3160e939b192cbe8e218992a84e6fc) |
| issues closed | [#60471](https://github.com/pandas-dev/pandas/issues/60471) |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-60505:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60505.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v3.0.0.rst`, `pandas/core/groupby/generic.py` |
| test files (`test_patch`) | `pandas/tests/groupby/aggregate/test_aggregate.py`, `pandas/tests/groupby/test_all_methods.py`, `pandas/tests/groupby/test_grouping.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (2)

- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_apply_corner`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_apply_empty_with_group_keys_false`

## PASS_TO_PASS (659)

<details><summary>show</summary>

- `pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_agg_multiple_lambda`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_agg_with_one_lambda`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_basic`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_mangle_series_groupby`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_agg_namedtuple`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_agg_relabel`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_agg_relabel_non_identifier`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_agg_relabel_other_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_agg_relabel_with_level`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_duplicate_no_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_mangled`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationDataFrame::test_missing_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_mangled`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_named_agg_nametuple[inp0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_named_agg_nametuple[inp1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_named_agg_nametuple[inp2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_no_args_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_series_named_agg`
- `pandas/tests/groupby/aggregate/test_aggregate.py::TestNamedAggregationSeries::test_series_named_agg_duplicates_no_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_grouping_is_list_tuple`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_groupings_selection`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_index_has_complex_internals[index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_index_has_complex_internals[index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_index_has_complex_internals[index2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_index_has_complex_internals[index3]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_multiple_functions_maintain_order`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_multiple_functions_same_name`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_multiple_functions_same_name_with_ohlc_present`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_multiple_with_as_index_false_subset_to_a_single_column`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_must_agg`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_of_mode_list[test0-constant0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_of_mode_list[test1-constant1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_of_mode_list[test2-constant2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_python_multiindex`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_regression1`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_relabel_multiindex_column[agg_col10-agg_col20-agg_col30-agg_result10-agg_result20-agg_result30]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_relabel_multiindex_column[agg_col11-agg_col21-agg_col31-agg_result11-agg_result21-agg_result31]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_relabel_multiindex_column[agg_col12-agg_col22-agg_col32-agg_result12-agg_result22-agg_result32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_relabel_multiindex_duplicates`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_relabel_multiindex_raises_not_exist`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_ser_multi_key`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_split_block`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_split_object_part_datetime`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[all]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[any]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[corrwith]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[count]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[first]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[idxmax]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[idxmin]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[last]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[max]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[mean]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[median]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[min]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[nunique]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[prod]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[quantile]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[sem]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[size]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[skew]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[std]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[sum]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_str_with_kwarg_axis_1_raises[var]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_with_as_index_false_with_list`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_with_missing_values`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_datetime_objects`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_item_by_item`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_mixed_types`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_str_func[<lambda>]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_str_func[groupbyfunc1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>3]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>4]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_bool_agg_dtype[<lambda>5]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-bool-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-float64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[aggregate-int64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-bool-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-float64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[apply-int64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-bool-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-float64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int32-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-bool-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-bool-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-float32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-float32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-float64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-float64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-int32-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-int32-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-int64-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_frame[transform-int64-int64-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-bool-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-float-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[aggregate-int-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-bool-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-float-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[apply-int-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-bool-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-float-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-1-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-1-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-1.0-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-1.0-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-True-keys0-agg_index0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_callable_result_dtype_series[transform-int-True-keys1-agg_index1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_dataframe_groupy_agg_list_like_func_with_args`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_func_duplicates_raises`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_grouby_agg_loses_results_with_as_index_false_relabel`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_grouby_agg_loses_results_with_as_index_false_relabel_multiindex`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_group_mean_datetime64_nat[input_data0-expected_output0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_group_mean_datetime64_nat[input_data1-expected_output1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_group_mean_timedelta_nat`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_coercing_bools`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_dict_dup_columns`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_dict_with_getitem`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_extension_timedelta_cumsum_with_named_aggregation`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_no_extra_calls`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Float32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Float64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Int16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Int32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[Int8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[UInt16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[UInt32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[UInt64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[UInt8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[float32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[float64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[float]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[int16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[int32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[int8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[int]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[uint16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[uint32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_agg_precision[uint8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[all]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[any]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[corrwith]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[count]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[first]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[idxmax]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[idxmin]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[last]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[max]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[mean]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[median]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[min]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[nunique]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[prod]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[quantile]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[sem]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[size]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[skew]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[std]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[sum]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_directory[var]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_empty_key[kwargs0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_empty_key[kwargs1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_empty_key_empty_return`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregate_empty_with_multiindex_frame`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_duplicate_columns_multiple_dict_values`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_duplicate_columns_single_dict_value`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_duplicate_columns_some_empty_result`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_empty_group`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_func_list_multi_index_duplicate_columns`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_mixed_dtype`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_aggregation_multi_index_duplicate_columns`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_as_index_agg`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_combined_aggs_cat_cols[grp_col_dict0-exp_data0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_combined_aggs_cat_cols[grp_col_dict1-exp_data1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_combined_aggs_cat_cols[grp_col_dict2-exp_data2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_complex[mean-output0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_complex[sum-output1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_complex_raises[max]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_complex_raises[min]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_complex_raises[var]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_get_by_index`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_index_object_dtype`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_single_agg_cat_cols[grp_col_dict0-exp_data0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_single_agg_cat_cols[grp_col_dict1-exp_data1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_groupby_single_agg_cat_cols[grp_col_dict2-exp_data2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_lambda_named_agg[<lambda>]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_lambda_named_agg[myfunc]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_more_flexible_frame_multi_function`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_multi_function_flexible_mix`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_multiindex_custom_func[<lambda>0]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_multiindex_custom_func[<lambda>1]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_multiindex_custom_func[<lambda>2]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_multiple_functions_tuples_and_non_tuples`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_nonagg_agg`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Float32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Float64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Int16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Int32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[Int8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[UInt16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[UInt32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[UInt64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_ohlc_ea_dtypes[UInt8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_order_aggregate_multiple_funcs`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_pass_args_kwargs_duplicate_columns[False]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_pass_args_kwargs_duplicate_columns[True]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_series_groupy_agg_list_like_func_with_args`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_series_index_name`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Float32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Float64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Int16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Int32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[Int8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[UInt16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[UInt32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[UInt64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_std_masked_dtype[UInt8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_timeseries_groupby_agg`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[first-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[first-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[last-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[last-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[max-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[max-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[mean-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[mean-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[median-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[median-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[min-int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_uint64_type_handling[min-uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[float32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[float64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[float]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[int16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[int32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[int64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[int8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[int]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[uint16]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[uint32]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[uint64]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_with_na_groups[uint8]`
- `pandas/tests/groupby/aggregate/test_aggregate.py::test_wrap_agg_out`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[all-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[all-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[any-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[any-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[bfill-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[bfill-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[corrwith-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[corrwith-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[count-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[count-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cummax-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cummax-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cummin-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cummin-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cumprod-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cumprod-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cumsum-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[cumsum-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[diff-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[diff-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[ffill-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[ffill-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[first-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[first-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[idxmax-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[idxmax-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[idxmin-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[idxmin-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[last-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[last-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[max-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[max-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[mean-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[mean-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[median-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[median-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[min-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[min-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[nunique-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[nunique-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[pct_change-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[pct_change-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[prod-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[prod-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[quantile-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[quantile-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[rank-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[rank-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[sem-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[sem-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[shift-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[shift-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[skew-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[skew-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[std-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[std-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[sum-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[sum-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[var-idx0]`
- `pandas/tests/groupby/test_all_methods.py::test_dup_labels_output_shape[var-idx1]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[all-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[all-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[any-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[any-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[bfill-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[bfill-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[count-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[count-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumcount-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumcount-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cummax-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cummax-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cummin-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cummin-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumprod-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumprod-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumsum-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[cumsum-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[diff-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[diff-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[ffill-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[ffill-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[first-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[first-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[idxmax-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[idxmax-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[idxmin-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[idxmin-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[last-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[last-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[max-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[max-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[mean-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[mean-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[median-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[median-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[min-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[min-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[ngroup-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[ngroup-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[nunique-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[nunique-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[pct_change-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[pct_change-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[prod-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[prod-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[quantile-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[quantile-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[rank-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[rank-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[sem-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[sem-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[shift-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[shift-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[size-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[size-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[skew-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[skew-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[std-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[std-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[sum-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[sum-True]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[var-False]`
- `pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[var-True]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[all]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[any]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[bfill]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[corrwith]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[count]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[cumcount]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[cummax]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[cummin]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[cumprod]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[cumsum]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[diff]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[ffill]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[first]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[idxmax]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[idxmin]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[last]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[max]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[mean]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[median]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[min]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[ngroup]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[nunique]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[pct_change]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[prod]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[quantile]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[rank]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[sem]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[shift]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[size]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[skew]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[std]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[sum]`
- `pandas/tests/groupby/test_all_methods.py::test_multiindex_group_all_columns_when_empty[var]`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_gb_key_len_equal_axis_len`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_get_group`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_get_group_empty_bins[False]`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_get_group_empty_bins[True]`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_get_group_grouped_by_tuple`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_get_group_grouped_by_tuple_with_lambda`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_groupby_with_empty`
- `pandas/tests/groupby/test_grouping.py::TestGetGroup::test_groupby_with_single_column`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_agg_with_dict_raises`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_empty_groups`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_evaluate_with_empty_groups[agg-expected1]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_evaluate_with_empty_groups[apply-expected2]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_evaluate_with_empty_groups[transform-expected0]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_args`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_categorical_index_and_columns[False]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_categorical_index_and_columns[True]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_dict_mapping`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_empty`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_grouper`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_grouper_f_sanity_checked`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level[False]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level[True]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level_index_names`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level_index_value_all_na`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level_with_nas[False]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_level_with_nas[True]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_levels_and_columns`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_multiindex_level_empty`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_multiindex_partial_indexing_equivalence`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_multiindex_tuple`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[DataFrame-index0]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[DataFrame-index1]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[DataFrame-index2]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[Series-index0]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[Series-index1]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_series_named_with_tuple[Series-index2]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_tuple_keys_handle_multiindex`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_with_datetime_key`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_column_and_index`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug2`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug3[ms]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug3[ns]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug3[s]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_creation_bug3[us]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_getting_correct_binner`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_index_types[index0]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_index_types[index1]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_index_types[index2]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_index_types[index3]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_index_types[index4]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_iter`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_multilevel_freq`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_returning_tuples[False]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouper_returning_tuples[True]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouping_error_on_multidim_input`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_grouping_labels`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_level_preserve_order[False-labels1]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_level_preserve_order[True-labels0]`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_list_grouper_with_nat`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_multiindex_columns_empty_level`
- `pandas/tests/groupby/test_grouping.py::TestGrouping::test_multiindex_negative_level`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_dictify`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_groupby_with_small_elem`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_grouping_is_iterable`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_grouping_string_repr`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_groups`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_multi_iter`
- `pandas/tests/groupby/test_grouping.py::TestIteration::test_multi_iter_frame`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_column_select_via_attr`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_from_grouper[<lambda>0]`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_from_grouper[<lambda>1]`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_list_of_columns`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_numeric_column_names`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_single_column`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_getitem_single_tuple_of_columns_raises`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_groupby_duplicated_column_errormsg`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_indices_grouped_by_tuple_with_lambda`
- `pandas/tests/groupby/test_grouping.py::TestSelection::test_select_bad_cols`
- `pandas/tests/groupby/test_grouping.py::test_groupby_any_with_timedelta`
- `pandas/tests/groupby/test_grouping.py::test_grouping_by_key_is_in_axis`

</details>

## Problem statement (what the agent may be shown)

````text
Issue #60471: BUG: DataFrameGroupBy.apply ignores group_keys setting when empty

### Pandas version checks





### Reproducible Example

```python
df = pd.DataFrame({'A': 'a a b'.split(), 'B': [1, 2, 3], 'C': [4, 6, 5]})
g1 = df.groupby('A', group_keys=False)

df = pd.DataFrame({'A': [], 'B': [], 'C': []})
g2 = df.groupby('A', group_keys=False)
g3 = df.groupby('A', group_keys=True)

r1 = g1.apply(lambda x: x / x.sum())
r2 = g2.apply(lambda x: x / x.sum())
r3 = g3.apply(lambda x: x / x.sum())

print(r1.index) # Index([0, 1, 2], dtype='int64')
print(r2.index) # Index([], dtype='float64', name='A')
print(r3.index) # Index([], dtype='float64', name='A')
```


### Issue Description

The group_keys parameter has no effect when the source dataframe is empty

### Expected Behavior

group_keys=False should not include the group keys into the index regardless of whether the source dataframe is empty
I would expect results such as:
```python
print(r2.index) # Index([], dtype='float64')
print(r2.index) # RangeIndex(start=0, stop=0, step=1)
```

### Installed Versions

<details>

INSTALLED VERSIONS
------------------
commit                : 0691c5cf90477d3503834d983f69350f250a6ff7
python                : 3.10.11
python-bits           : 64
OS                    : Windows
OS-release            : 10
Version               : 10.0.22631
machine               : AMD64
processor             : Intel64 Family 6 Model 141 Stepping 1, GenuineIntel
byteorder             : little
LC_ALL                : None
LANG                  : None
LOCALE                : es_ES.cp1252

pandas                : 2.2.3
numpy                 : 1.26.4
pytz                  : 2024.2
dateutil              : 2.9.0.post0
pip                   : 23.0.1
Cython                : None
sphinx                : None
IPython               : 8.30.0
adbc-driver-postgresql: None
...
zstandard             : None
tzdata                : 2024.2
qtpy                  : None
pyqt5                 : None

</details>

---

Pull request #60505: BUG: Fix bug in GroupBy that ignores group_keys arg for empty datafra…

…mes/series


When using `groupby.apply` on an empty dataframe or series with `group_keys=False`, the output index is incorrectly set to the grouping keys, while it is expected to be a `RangeIndex(0, 0, 1)`.
From the original issue:
```
>>> df = pd.DataFrame({'A': [], 'B': [], 'C': []})
>>> g2 = df.groupby('A', group_keys=False)
>>> r2 = g2.apply(lambda x: x / x.sum())
>>> print(r2.index)
Index([], dtype='float64', name='A')
```
Expected:
```
>>> print(r2.index)
RangeIndex(start=0, stop=0, step=1)
```
````

## Hints (issue comments before the PR; not shown to the agent)

```text
Thanks for the report! PRs to fix are welcome.
take
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v3.0.0.rst b/doc/source/whatsnew/v3.0.0.rst
index bb9f48d17b2e1858ab840201547d15c2246eb141..ab5746eca1b185403d4f2360e32b251057d54862 100644
--- a/doc/source/whatsnew/v3.0.0.rst
+++ b/doc/source/whatsnew/v3.0.0.rst
@@ -733,6 +733,7 @@ Groupby/resample/rolling
 - Bug in :meth:`.Resampler.interpolate` on a :class:`DataFrame` with non-uniform sampling and/or indices not aligning with the resulting resampled index would result in wrong interpolation (:issue:`21351`)
 - Bug in :meth:`DataFrame.ewm` and :meth:`Series.ewm` when passed ``times`` and aggregation functions other than mean (:issue:`51695`)
 - Bug in :meth:`DataFrameGroupBy.agg` that raises ``AttributeError`` when there is dictionary input and duplicated columns, instead of returning a DataFrame with the aggregation of all duplicate columns. (:issue:`55041`)
+- Bug in :meth:`DataFrameGroupBy.apply` and :meth:`SeriesGroupBy.apply` for empty data frame with ``group_keys=False`` still creating output index using group keys. (:issue:`60471`)
 - Bug in :meth:`DataFrameGroupBy.apply` that was returning a completely empty DataFrame when all return values of ``func`` were ``None`` instead of returning an empty DataFrame with the original columns and dtypes. (:issue:`57775`)
 - Bug in :meth:`DataFrameGroupBy.apply` with ``as_index=False`` that was returning :class:`MultiIndex` instead of returning :class:`Index`. (:issue:`58291`)
 - Bug in :meth:`DataFrameGroupBy.cumsum` and :meth:`DataFrameGroupBy.cumprod` where ``numeric_only`` parameter was passed indirectly through kwargs instead of passing directly. (:issue:`58811`)
diff --git a/pandas/core/groupby/generic.py b/pandas/core/groupby/generic.py
index 3fa34007a739b56ee945eacd908e7dc9ab431784..f4e3f3e8b10012ee711fcec37ac5827be2b40c9b 100644
--- a/pandas/core/groupby/generic.py
+++ b/pandas/core/groupby/generic.py
@@ -583,6 +583,8 @@ class SeriesGroupBy(GroupBy[Series]):
             if is_transform:
                 # GH#47787 see test_group_on_empty_multiindex
                 res_index = data.index
+            elif not self.group_keys:
+                res_index = None
             else:
                 res_index = self._grouper.result_index
 
@@ -1967,6 +1969,8 @@ class DataFrameGroupBy(GroupBy[DataFrame]):
             if is_transform:
                 # GH#47787 see test_group_on_empty_multiindex
                 res_index = data.index
+            elif not self.group_keys:
+                res_index = None
             else:
                 res_index = self._grouper.result_index
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/groupby/aggregate/test_aggregate.py b/pandas/tests/groupby/aggregate/test_aggregate.py
index 64220f1d3d5b4de8000573127ab0d40b5eb15b3b..b7e6e55739c17d1e0608e9abefae1fed6ef14c46 100644
--- a/pandas/tests/groupby/aggregate/test_aggregate.py
+++ b/pandas/tests/groupby/aggregate/test_aggregate.py
@@ -159,6 +159,7 @@ def test_agg_apply_corner(ts, tsframe):
     tm.assert_frame_equal(grouped.agg("sum"), exp_df)
 
     res = grouped.apply(np.sum, axis=0)
+    exp_df = exp_df.reset_index(drop=True)
     tm.assert_frame_equal(res, exp_df)
 
 
diff --git a/pandas/tests/groupby/test_all_methods.py b/pandas/tests/groupby/test_all_methods.py
index 945c3e421a1321ae19782fda1d4a21c5289fad1e..4625c5c27a803c74fb9b7fbcfc83702228c0f3fa 100644
--- a/pandas/tests/groupby/test_all_methods.py
+++ b/pandas/tests/groupby/test_all_methods.py
@@ -22,7 +22,7 @@ from pandas.tests.groupby import get_groupby_method_args
 def test_multiindex_group_all_columns_when_empty(groupby_func):
     # GH 32464
     df = DataFrame({"a": [], "b": [], "c": []}).set_index(["a", "b", "c"])
-    gb = df.groupby(["a", "b", "c"], group_keys=False)
+    gb = df.groupby(["a", "b", "c"], group_keys=True)
     method = getattr(gb, groupby_func)
     args = get_groupby_method_args(groupby_func, df)
     if groupby_func == "corrwith":
diff --git a/pandas/tests/groupby/test_grouping.py b/pandas/tests/groupby/test_grouping.py
index 366eb59ee226a0de45caabd74775f9fa4ab0221d..4e7c0acb127ed90bd428b1782824d36ff8bd3ec8 100644
--- a/pandas/tests/groupby/test_grouping.py
+++ b/pandas/tests/groupby/test_grouping.py
@@ -777,10 +777,21 @@ class TestGrouping:
         # (not testing other agg fns, because they return
         # different index objects.
         df = DataFrame({1: [], 2: []})
-        g = df.groupby(1, group_keys=False)
+        g = df.groupby(1, group_keys=True)
         result = getattr(g[2], func)(lambda x: x)
         tm.assert_series_equal(result, expected)
 
+    def test_groupby_apply_empty_with_group_keys_false(self):
+        # 60471
+        # test apply'ing empty groups with group_keys False
+        # (not testing other agg fns, because they return
+        # different index objects.
+        df = DataFrame({"A": [], "B": [], "C": []})
+        g = df.groupby("A", group_keys=False)
+        result = g.apply(lambda x: x / x.sum(), include_groups=False)
+        expected = DataFrame({"B": [], "C": []}, index=None)
+        tm.assert_frame_equal(result, expected)
+
     def test_groupby_empty(self):
         # https://github.com/pandas-dev/pandas/issues/27190
         s = Series([], name="name", dtype="float64")
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/groupby/aggregate/test_aggregate.py",
  "pandas/tests/groupby/test_all_methods.py",
  "pandas/tests/groupby/test_grouping.py"
 ],
 "collected_before": 672,
 "collected_after": 672,
 "outcomes_before": {
  "PASSED": 659,
  "FAILED": 2,
  "XFAIL": 5,
  "SKIPPED": 6
 },
 "outcomes_after": {
  "PASSED": 661,
  "XFAIL": 5,
  "SKIPPED": 6
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "st_dictify\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_groupby_with_small_elem\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_grouping_string_repr\nPASSED pandas/tests/groupby/test_grouping.py::test_grouping_by_key_is_in_axis\nPASSED pandas/tests/groupby/test_grouping.py::test_groupby_any_with_timedelta\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for size\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for cumcount\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for ngroup\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_udf_na_extension_type - Not implemented;see GH 31256\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_with_kwargs - GH-26611. kwargs for multi-agg.\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_of_mode_list[test3-constant3]\nXFAIL pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[corrwith-True] - GH#50845 - corrwith fails when there are duplicate columns\nXFAIL pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[corrwith-False] - GH#50845 - corrwith fails when there are duplicate columns\nFAILED pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_apply_corner\nFAILED pandas/tests/groupby/test_grouping.py::TestGrouping::test_groupby_apply_empty_with_group_keys_false\n============= 2 failed, 659 passed, 6 skipped, 5 xfailed in 3.33s ==============",
 "tail_after": "ping.py::TestIteration::test_multi_iter\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_multi_iter_frame\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_dictify\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_groupby_with_small_elem\nPASSED pandas/tests/groupby/test_grouping.py::TestIteration::test_grouping_string_repr\nPASSED pandas/tests/groupby/test_grouping.py::test_grouping_by_key_is_in_axis\nPASSED pandas/tests/groupby/test_grouping.py::test_groupby_any_with_timedelta\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for size\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for cumcount\nSKIPPED [2] pandas/tests/groupby/test_all_methods.py:68: Not applicable for ngroup\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::test_aggregate_udf_na_extension_type - Not implemented;see GH 31256\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::TestLambdaMangling::test_with_kwargs - GH-26611. kwargs for multi-agg.\nXFAIL pandas/tests/groupby/aggregate/test_aggregate.py::test_agg_of_mode_list[test3-constant3]\nXFAIL pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[corrwith-True] - GH#50845 - corrwith fails when there are duplicate columns\nXFAIL pandas/tests/groupby/test_all_methods.py::test_duplicate_columns[corrwith-False] - GH#50845 - corrwith fails when there are duplicate columns\n================== 661 passed, 6 skipped, 5 xfailed in 3.10s ===================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
