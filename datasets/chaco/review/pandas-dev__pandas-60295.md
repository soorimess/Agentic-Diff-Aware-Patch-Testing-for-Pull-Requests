# pandas-dev__pandas-60295

[back to the list](README.md) -- **TST (string dtype): resolve xfails for frame fillna and replace tests + fix bug in replace for string**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60295](https://github.com/pandas-dev/pandas/pull/60295) (created 2024-11-13, merged 2024-11-15) |
| ChaCo lists | full, ablation |
| status | **not-fail-to-pass** -- no developer test fails before the change and passes after (279 pass on both sides) |
| base commit | [`63d3971328f9`](https://github.com/pandas-dev/pandas/commit/63d3971328f96fb176305ff2886e5b67a9c39454) (2024-11-15), first parent of the merge commit |
| merge commit | [`fae3e8034faf`](https://github.com/pandas-dev/pandas/commit/fae3e8034faf66eb8ef00bcbed73d48e4ef791d3) |
| issues closed | none |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-60295:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60295.Dockerfile) |
| source files (`patch`) | `pandas/core/array_algos/replace.py`, `pandas/core/internals/blocks.py` |
| test files (`test_patch`) | `pandas/tests/frame/methods/test_fillna.py`, `pandas/tests/frame/methods/test_replace.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (0)

(none)

## PASS_TO_PASS (279)

<details><summary>show</summary>

- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_bfill`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_ffill`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fill_empty`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_categorical_nan`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_col_reordering`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_columns`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dataframe`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_datelike`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_datetime`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_datetime_columns`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_datetime_inplace`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dict_inplace_nonunique_columns`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dict_series`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dictlike_value_duplicate_colnames[columns0]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dictlike_value_duplicate_colnames[columns1]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_different_dtype`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dtype_conversion`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dtype_conversion_equiv_replace[1.0]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dtype_conversion_equiv_replace[1]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dtype_conversion_equiv_replace[]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_dtype_conversion_equiv_replace[nan]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_inplace`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_inplace_with_columns_limit_and_value`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_integer_limit[float]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_integer_limit[int]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_invalid_value`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_limit_and_value`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_mixed_float`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_mixed_type`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_no_downcast[DataFrame]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_no_downcast[Series]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_on_column_view`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_positive_limit[float]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_positive_limit[int]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_skip_certain_blocks`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_tzaware`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_tzaware_different_column`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_with_columns_and_limit`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_fillna_with_multi_index_frame`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_frame_fillna_limit`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_frame_pad_backfill_limit`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_inplace_dict_update_view[-1]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_inplace_dict_update_view[val1]`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_na_actions_categorical`
- `pandas/tests/frame/methods/test_fillna.py::TestFillNA::test_single_block_df_with_horizontal_axis`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data0-expected_data0-ffill-kwargs0]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data1-expected_data1-ffill-kwargs1]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data2-expected_data2-ffill-kwargs2]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data3-expected_data3-ffill-kwargs3]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data4-expected_data4-ffill-kwargs4]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data5-expected_data5-ffill-kwargs5]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data6-expected_data6-bfill-kwargs6]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data7-expected_data7-bfill-kwargs7]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data8-expected_data8-bfill-kwargs8]`
- `pandas/tests/frame/methods/test_fillna.py::test_ffill_bfill_limit_area[data9-expected_data9-bfill-kwargs9]`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_nonconsolidated_frame`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_nones_inplace`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_with_none_object[float-False]`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_with_none_object[float-True]`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_with_none_object[object-False]`
- `pandas/tests/frame/methods/test_fillna.py::test_fillna_with_none_object[object-True]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_categorical_replace_with_dict[replace_dict0-final_data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_categorical_replace_with_dict[replace_dict1-final_data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_joint_simple_replace_and_regex_replace[to_replace0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_joint_simple_replace_and_regex_replace[to_replace1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_nested_dict_overlapping_keys_replace_int`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_nested_dict_overlapping_keys_replace_str`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_mixed`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_gh4115`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_non_first_character[string=object]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_non_first_character[string=str[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_non_first_character[string=str[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_non_first_character[string=string[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_dict_nested_non_first_character[string=string[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_mixed`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_mixed_inplace`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-False-to_replace0-values0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-False-to_replace1-values1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-False-to_replace2-values2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-True-to_replace0-values0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-True-to_replace1-values1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[False-True-to_replace2-values2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-False-to_replace0-values0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-False-to_replace1-values1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-False-to_replace2-values2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-True-to_replace0-values0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-True-to_replace1-values1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_obj[True-True-to_replace2-values2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_list_to_scalar`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_numeric_to_object_conversion`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_regex_list_to_numeric`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_series_of_regexes`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_str_to_numeric`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=object-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=object-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=str[pyarrow]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=str[pyarrow]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=str[python]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=str[python]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=string[pyarrow]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=string[pyarrow]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=string[python]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[DataFrame-string=string[python]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=object-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=object-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=str[pyarrow]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=str[pyarrow]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=str[python]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=str[python]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=string[pyarrow]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=string[pyarrow]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=string[python]-data0-to_replace0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_regex_replace_string_types[Series-string=string[python]-data1-to_replace1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_NAT_with_None`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_NA_with_None`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_after_convert_dtypes`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_bool_with_bool`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_bool_with_string`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_bytes[DataFrame]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_bytes[Series]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_commutative[df0-to_replace0-exp0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_commutative[df1-to_replace1-exp1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_convert[string=object]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_convert[string=str[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_convert[string=str[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_convert[string=string[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_convert[string=string[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_datetimetz`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_category_type`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_no_regex[string=object]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_no_regex[string=str[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_no_regex[string=str[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_no_regex[string=string[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_no_regex[string=string[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_strings_vs_ints`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dict_tuple_list_ordering_remains_the_same`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_doesnt_replace_without_regex`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame0-1-0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame1-1-0-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame10-1.0-5.0-expected10]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame11-1-5.0-expected11]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame2-1-0-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame3-False-True-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame4-1j-0-expected4]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame5-to_replace5-value5-expected5]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame6-foo-bar-expected6]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame7-to_replace7-value7-expected7]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame8-1.0-5-expected8]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_dtypes[frame9-1-5-expected9]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_ea_ignore_float[DataFrame-value0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_ea_ignore_float[DataFrame-value1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_ea_ignore_float[Series-value0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_ea_ignore_float[Series-value1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_for_new_dtypes`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_inplace`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_input_formats_listlike`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_input_formats_scalar`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_intervals`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_invalid_to_replace`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_limit`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-array-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-array-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-array-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-array-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-list-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-list-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-list-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-list-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-tuple-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-tuple-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-tuple-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[DataFrame-tuple-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-array-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-array-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-array-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-array-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-list-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-list-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-list-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-list-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-tuple-data0-to_replace0-value0-expected0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-tuple-data1-to_replace1-value1-expected1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-tuple-data2-to_replace2-value2-expected2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_list_with_mixed_type[Series-tuple-data3-to_replace3-value3-expected3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_mixed`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_mixed2`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_mixed3`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_mixed_int_block_splitting`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_mixed_int_block_upcasting`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[nan-Int64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[nan-boolean]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[nan-float64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[nan-float]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[nan-int64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[value1-Int64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[value1-boolean]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[value1-float64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[value1-float]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_no_replacement_dtypes[value1-int64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_nullable_int_with_string_doesnt_cast`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_pure_bool_with_string_no_op`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_regex_metachar[()]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_regex_metachar[[]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_regex_metachar[\\d]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_regex_metachar[\\s]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_regex_metachar[\\w]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_replacer_dtype[1.0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_replacer_dtype[replacer0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_replacer_dtype[replacer1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_replacer_dtype[replacer2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_replacer_dtype[replacer3]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_dict`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_no_regex[string=object]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_no_regex[string=str[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_no_regex[string=str[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_no_regex[string=string[pyarrow]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_series_no_regex[string=string[python]]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_simple_nested_dict`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_simple_nested_dict_with_nonexistent_value`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_swapping_bug`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_truthy`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_unicode`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_value_category_type`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_value_is_none`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_value_none_dtype_numeric[2.0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_value_none_dtype_numeric[2]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_value_none_dtype_numeric[nan]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_None_keeps_categorical`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_compiled_regex`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_dict_with_bool_keys`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_duplicate_columns[5]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_duplicate_columns[nan]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_empty_dictlike`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_empty_list[DataFrame]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_empty_list[Series]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_nil_na`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_nullable_column[Float64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_nullable_column[Int64]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplace::test_replace_with_nullable_column[boolean]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-False-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-False-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-False-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-False-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-True-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-True-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-True-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-True-True-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-False-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-False-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-False-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-False-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-True-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-True-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-True-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-False-True-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-False-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-False-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-False-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-False-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-True-\\s*(\\.)\\s*-\\1\\1\\1-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-True-\\s*(\\.)\\s*-\\1\\1\\1-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-True-\\s*\\.\\s*-nan-data0]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[True-True-True-\\s*\\.\\s*-nan-data1]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_categorical_no_replacement`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_object_splitting`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[False]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[True]`
- `pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_with_value_also_being_replaced`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #60295: TST (string dtype): resolve xfails for frame fillna and replace tests + fix bug in replace for string

Follow-up on https://github.com/pandas-dev/pandas/pull/60285, fixing one additional bug in the string-fallback-to-object implementation, uncovered by enabling all other replace/fillna related tests.

xref https://github.com/pandas-dev/pandas/issues/54792
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/core/array_algos/replace.py b/pandas/core/array_algos/replace.py
index f946c5adcbb0b6fda573b5801f0f499b279a3de8..a9ad66b7cb2e5f17a42653c99d532d1bb7c0bcb9 100644
--- a/pandas/core/array_algos/replace.py
+++ b/pandas/core/array_algos/replace.py
@@ -151,4 +151,6 @@ def replace_regex(
     if mask is None:
         values[:] = f(values)
     else:
+        if values.ndim != mask.ndim:
+            mask = np.broadcast_to(mask, values.shape)
         values[mask] = f(values[mask])
diff --git a/pandas/core/internals/blocks.py b/pandas/core/internals/blocks.py
index 3c207e8c14b5b2df26f3b273db7bd87e43c603f9..54273ff89f1aff02edd8994b5e75c5175eac7dfb 100644
--- a/pandas/core/internals/blocks.py
+++ b/pandas/core/internals/blocks.py
@@ -1688,6 +1688,13 @@ class EABackedBlock(Block):
                 if isinstance(self.dtype, (IntervalDtype, StringDtype)):
                     # TestSetitemFloatIntervalWithIntIntervalValues
                     blk = self.coerce_to_target_dtype(orig_other, raise_on_upcast=False)
+                    if (
+                        self.ndim == 2
+                        and isinstance(orig_cond, np.ndarray)
+                        and orig_cond.ndim == 1
+                        and not is_1d_only_ea_dtype(blk.dtype)
+                    ):
+                        orig_cond = orig_cond[:, None]
                     return blk.where(orig_other, orig_cond)
 
                 elif isinstance(self, NDArrayBackedExtensionBlock):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/frame/methods/test_fillna.py b/pandas/tests/frame/methods/test_fillna.py
index ad1a37916e381d7f891e37b840a8bcb819328c43..67d1d45af1cb3a9b8ba9f8d078818a2bbd4f190f 100644
--- a/pandas/tests/frame/methods/test_fillna.py
+++ b/pandas/tests/frame/methods/test_fillna.py
@@ -1,8 +1,6 @@
 import numpy as np
 import pytest
 
-from pandas._config import using_string_dtype
-
 from pandas import (
     Categorical,
     DataFrame,
@@ -65,15 +63,20 @@ class TestFillNA:
         with pytest.raises(TypeError, match=msg):
             datetime_frame.fillna()
 
-    # TODO(infer_string) test as actual error instead of xfail
-    @pytest.mark.xfail(using_string_dtype(), reason="can't fill 0 in string")
-    def test_fillna_mixed_type(self, float_string_frame):
+    def test_fillna_mixed_type(self, float_string_frame, using_infer_string):
         mf = float_string_frame
         mf.loc[mf.index[5:20], "foo"] = np.nan
         mf.loc[mf.index[-10:], "A"] = np.nan
-        # TODO: make stronger assertion here, GH 25640
-        mf.fillna(value=0)
-        mf.ffill()
+
+        result = mf.ffill()
+        assert (
+            result.loc[result.index[-10:], "A"] == result.loc[result.index[-11], "A"]
+        ).all()
+        assert (result.loc[result.index[5:20], "foo"] == "bar").all()
+
+        result = mf.fillna(value=0)
+        assert (result.loc[result.index[-10:], "A"] == 0).all()
+        assert (result.loc[result.index[5:20], "foo"] == 0).all()
 
     def test_fillna_mixed_float(self, mixed_float_frame):
         # mixed numeric (but no float16)
@@ -84,28 +87,21 @@ class TestFillNA:
         result = mf.ffill()
         _check_mixed_float(result, dtype={"C": None})
 
-    @pytest.mark.xfail(using_string_dtype(), reason="TODO(infer_string)")
-    def test_fillna_different_dtype(self, using_infer_string):
+    def test_fillna_different_dtype(self):
         # with different dtype (GH#3386)
         df = DataFrame(
             [["a", "a", np.nan, "a"], ["b", "b", np.nan, "b"], ["c", "c", np.nan, "c"]]
         )
 
-        if using_infer_string:
-            with tm.assert_produces_warning(FutureWarning, match="Downcasting"):
-                result = df.fillna({2: "foo"})
-        else:
-            result = df.fillna({2: "foo"})
+        result = df.fillna({2: "foo"})
         expected = DataFrame(
             [["a", "a", "foo", "a"], ["b", "b", "foo", "b"], ["c", "c", "foo", "c"]]
         )
+        # column is originally float (all-NaN) -> filling with string gives object dtype
+        expected[2] = expected[2].astype("object")
         tm.assert_frame_equal(result, expected)
 
-        if using_infer_string:
-            with tm.assert_produces_warning(FutureWarning, match="Downcasting"):
-                return_value = df.fillna({2: "foo"}, inplace=True)
-        else:
-            return_value = df.fillna({2: "foo"}, inplace=True)
+        return_value = df.fillna({2: "foo"}, inplace=True)
         tm.assert_frame_equal(df, expected)
         assert return_value is None
 
@@ -276,8 +272,7 @@ class TestFillNA:
         expected["A"] = 0.0
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="TODO(infer_string)")
-    def test_fillna_dtype_conversion(self, using_infer_string):
+    def test_fillna_dtype_conversion(self):
         # make sure that fillna on an empty frame works
         df = DataFrame(index=["A", "B", "C"], columns=[1, 2, 3, 4, 5])
         result = df.dtypes
@@ -292,7 +287,7 @@ class TestFillNA:
         # empty block
         df = DataFrame(index=range(3), columns=["A", "B"], dtype="float64")
         result = df.fillna("nan")
-        expected = DataFrame("nan", index=range(3), columns=["A", "B"])
+        expected = DataFrame("nan", dtype="object", index=range(3), columns=["A", "B"])
         tm.assert_frame_equal(result, expected)
 
     @pytest.mark.parametrize("val", ["", 1, np.nan, 1.0])
@@ -540,18 +535,10 @@ class TestFillNA:
         filled = df.ffill()
         assert df.columns.tolist() == filled.columns.tolist()
 
-    # TODO(infer_string) test as actual error instead of xfail
-    @pytest.mark.xfail(using_string_dtype(), reason="can't fill 0 in string")
-    def test_fill_corner(self, float_frame, float_string_frame):
-        mf = float_string_frame
-        mf.loc[mf.index[5:20], "foo"] = np.nan
-        mf.loc[mf.index[-10:], "A"] = np.nan
-
-        filled = float_string_frame.fillna(value=0)
-        assert (filled.loc[filled.index[5:20], "foo"] == 0).all()
-        del float_string_frame["foo"]
-
-        float_frame.reindex(columns=[]).fillna(value=0)
+    def test_fill_empty(self, float_frame):
+        df = float_frame.reindex(columns=[])
+        result = df.fillna(value=0)
+        tm.assert_frame_equal(result, df)
 
     def test_fillna_with_columns_and_limit(self):
         # GH40989
diff --git a/pandas/tests/frame/methods/test_replace.py b/pandas/tests/frame/methods/test_replace.py
index 73f44bcc6657e72d660363890719becfaf0634a5..b2320798ea9a2aabdd7704a4d30e650d143603d9 100644
--- a/pandas/tests/frame/methods/test_replace.py
+++ b/pandas/tests/frame/methods/test_replace.py
@@ -6,8 +6,6 @@ import re
 import numpy as np
 import pytest
 
-from pandas._config import using_string_dtype
-
 import pandas as pd
 from pandas import (
     DataFrame,
@@ -30,7 +28,6 @@ def mix_abc() -> dict[str, list[float | str]]:
 
 
 class TestDataFrameReplace:
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_replace_inplace(self, datetime_frame, float_string_frame):
         datetime_frame.loc[datetime_frame.index[:5], "A"] = np.nan
         datetime_frame.loc[datetime_frame.index[-5:], "A"] = np.nan
@@ -46,7 +43,9 @@ class TestDataFrameReplace:
         mf.iloc[-10:, mf.columns.get_loc("A")] = np.nan
 
         result = float_string_frame.replace(np.nan, 0)
-        expected = float_string_frame.fillna(value=0)
+        expected = float_string_frame.copy()
+        expected["foo"] = expected["foo"].astype(object)
+        expected = expected.fillna(value=0)
         tm.assert_frame_equal(result, expected)
 
         tsframe = datetime_frame.copy()
@@ -291,22 +290,20 @@ class TestDataFrameReplace:
         expected = DataFrame({"first": [".bc", "bc.", "c.b"]}, dtype=dtype)
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_regex_replace_dict_nested_gh4115(self):
-        df = DataFrame({"Type": ["Q", "T", "Q", "Q", "T"], "tmp": 2})
-        expected = DataFrame(
-            {"Type": Series([0, 1, 0, 0, 1], dtype=df.Type.dtype), "tmp": 2}
+        df = DataFrame(
+            {"Type": Series(["Q", "T", "Q", "Q", "T"], dtype=object), "tmp": 2}
         )
+        expected = DataFrame({"Type": Series([0, 1, 0, 0, 1], dtype=object), "tmp": 2})
         result = df.replace({"Type": {"Q": 0, "T": 1}})
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_regex_replace_list_to_scalar(self, mix_abc):
         df = DataFrame(mix_abc)
         expec = DataFrame(
             {
                 "a": mix_abc["a"],
-                "b": np.array([np.nan] * 4, dtype=object),
+                "b": Series([np.nan] * 4, dtype="str"),
                 "c": [np.nan, np.nan, np.nan, "d"],
             }
         )
@@ -326,7 +323,6 @@ class TestDataFrameReplace:
         tm.assert_frame_equal(res2, expec)
         tm.assert_frame_equal(res3, expec)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_regex_replace_str_to_numeric(self, mix_abc):
         # what happens when you try to replace a numeric value with a regex?
         df = DataFrame(mix_abc)
@@ -338,11 +334,12 @@ class TestDataFrameReplace:
         return_value = res3.replace(regex=r"\s*\.\s*", value=0, inplace=True)
         assert return_value is None
         expec = DataFrame({"a": mix_abc["a"], "b": ["a", "b", 0, 0], "c": mix_abc["c"]})
+        # TODO(infer_string)
+        expec["c"] = expec["c"].astype(object)
         tm.assert_frame_equal(res, expec)
         tm.assert_frame_equal(res2, expec)
         tm.assert_frame_equal(res3, expec)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_regex_replace_regex_list_to_numeric(self, mix_abc):
         df = DataFrame(mix_abc)
         res = df.replace([r"\s*\.\s*", "b"], 0, regex=True)
@@ -535,31 +532,37 @@ class TestDataFrameReplace:
         result = df.replace(s, df.mean())
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
-    def test_replace_convert(self):
-        # gh 3907
-        df = DataFrame([["foo", "bar", "bah"], ["bar", "foo", "bah"]])
+    def test_replace_convert(self, any_string_dtype):
+        # gh 3907 (pandas >= 3.0 no longer converts dtypes)
+        df = DataFrame(
+            [["foo", "bar", "bah"], ["bar", "foo", "bah"]], dtype=any_string_dtype
+        )
         m = {"foo": 1, "bar": 2, "bah": 3}
         rep = df.replace(m)
-        expec = df.dtypes
-        res = rep.dtypes
-        tm.assert_series_equal(expec, res)
+        assert (rep.dtypes == object).all()
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     def test_replace_mixed(self, float_string_frame):
         mf = float_string_frame
         mf.iloc[5:20, mf.columns.get_loc("foo")] = np.nan
         mf.iloc[-10:, mf.columns.get_loc("A")] = np.nan
 
         result = float_string_frame.replace(np.nan, -18)
-        expected = float_string_frame.fillna(value=-18)
+        expected = float_string_frame.copy()
+        expected["foo"] = expected["foo"].astype(object)
+        expected = expected.fillna(value=-18)
         tm.assert_frame_equal(result, expected)
-        tm.assert_frame_equal(result.replace(-18, np.nan), float_string_frame)
+        expected2 = float_string_frame.copy()
+        expected2["foo"] = expected2["foo"].astype(object)
+        tm.assert_frame_equal(result.replace(-18, np.nan), expected2)
 
         result = float_string_frame.replace(np.nan, -1e8)
-        expected = float_string_frame.fillna(value=-1e8)
+        expected = float_string_frame.copy()
+        expected["foo"] = expected["foo"].astype(object)
+        expected = expected.fillna(value=-1e8)
         tm.assert_frame_equal(result, expected)
-        tm.assert_frame_equal(result.replace(-1e8, np.nan), float_string_frame)
+        expected2 = float_string_frame.copy()
+        expected2["foo"] = expected2["foo"].astype(object)
+        tm.assert_frame_equal(result.replace(-1e8, np.nan), expected2)
 
     def test_replace_mixed_int_block_upcasting(self):
         # int block upcasting
@@ -601,8 +604,7 @@ class TestDataFrameReplace:
         result = df.replace(0, 0.5)
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="TODO(infer_string)")
-    def test_replace_mixed2(self, using_infer_string):
+    def test_replace_mixed2(self):
         # to object block upcasting
         df = DataFrame(
             {
@@ -621,7 +623,7 @@ class TestDataFrameReplace:
 
         expected = DataFrame(
             {
-                "A": Series(["foo", "bar"]),
+                "A": Series(["foo", "bar"], dtype="object"),
                 "B": Series([0, "foo"], dtype="object"),
             }
         )
@@ -917,8 +919,7 @@ class TestDataFrameReplace:
         # TODO
         pass
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
-    def test_replace_dict_no_regex(self):
+    def test_replace_dict_no_regex(self, any_string_dtype):
         answer = Series(
             {
                 0: "Strongly Agree",
@@ -926,7 +927,8 @@ class TestDataFrameReplace:
                 2: "Neutral",
                 3: "Disagree",
                 4: "Strongly Disagree",
-            }
+            },
+            dtype=any_string_dtype,
         )
         weights = {
             "Agree": 4,
@@ -935,11 +937,11 @@ class TestDataFrameReplace:
             "Strongly Agree": 5,
             "Strongly Disagree": 1,
         }
-        expected = Series({0: 5, 1: 4, 2: 3, 3: 2, 4: 1}, dtype=answer.dtype)
+        expected = Series({0: 5, 1: 4, 2: 3, 3: 2, 4: 1}, dtype=object)
         result = answer.replace(weights)
         tm.assert_series_equal(result, expected)
 
-    def test_replace_series_no_regex(self):
+    def test_replace_series_no_regex(self, any_string_dtype):
         answer = Series(
             {
                 0: "Strongly Agree",
@@ -947,7 +949,8 @@ class TestDataFrameReplace:
                 2: "Neutral",
                 3: "Disagree",
                 4: "Strongly Disagree",
-            }
+            },
+            dtype=any_string_dtype,
         )
         weights = Series(
             {
@@ -1043,16 +1046,15 @@ class TestDataFrameReplace:
         expected = df.replace({"a": dict(zip(astr, bstr))})
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
-    def test_replace_swapping_bug(self, using_infer_string):
+    def test_replace_swapping_bug(self):
         df = DataFrame({"a": [True, False, True]})
         res = df.replace({"a": {True: "Y", False: "N"}})
-        expect = DataFrame({"a": ["Y", "N", "Y"]})
+        expect = DataFrame({"a": ["Y", "N", "Y"]}, dtype=object)
         tm.assert_frame_equal(res, expect)
 
         df = DataFrame({"a": [0, 1, 0]})
         res = df.replace({"a": {0: "Y", 1: "N"}})
-        expect = DataFrame({"a": ["Y", "N", "Y"]})
+        expect = DataFrame({"a": ["Y", "N", "Y"]}, dtype=object)
         tm.assert_frame_equal(res, expect)
 
     def test_replace_datetimetz(self):
@@ -1186,7 +1188,7 @@ class TestDataFrameReplace:
     )
     def test_replace_replacer_dtype(self, replacer):
         # GH26632
-        df = DataFrame(["a"])
+        df = DataFrame(["a"], dtype=object)
         result = df.replace({"a": replacer, "b": replacer})
         expected = DataFrame([replacer], dtype=object)
         tm.assert_frame_equal(result, expected)
@@ -1266,7 +1268,6 @@ class TestDataFrameReplace:
         assert return_value is None
         tm.assert_frame_equal(df, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="TODO(infer_string)")
     def test_replace_value_category_type(self):
         """
         Test for #23305: to ensure category dtypes are maintained
@@ -1322,7 +1323,7 @@ class TestDataFrameReplace:
             lambda x: x.astype("category").cat.rename_categories({"cat2": "catX"})
         )
 
-        result = result.astype({"col1": "int64", "col3": "float64", "col5": "object"})
+        result = result.astype({"col1": "int64", "col3": "float64", "col5": "str"})
         tm.assert_frame_equal(result, expected)
 
     def test_replace_dict_category_type(self):
@@ -1363,12 +1364,11 @@ class TestDataFrameReplace:
         expected = DataFrame(["z", "b", "c"])
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="TODO(infer_string)")
     def test_replace_intervals(self):
         # https://github.com/pandas-dev/pandas/issues/35931
         df = DataFrame({"a": [pd.Interval(0, 1), pd.Interval(0, 1)]})
         result = df.replace({"a": {pd.Interval(0, 1): "x"}})
-        expected = DataFrame({"a": ["x", "x"]})
+        expected = DataFrame({"a": ["x", "x"]}, dtype=object)
         tm.assert_frame_equal(result, expected)
 
     def test_replace_unicode(self):
@@ -1468,17 +1468,21 @@ class TestDataFrameReplaceRegex:
         expected.loc[expected["a"] == ".", "a"] = expected_replace_val
         tm.assert_frame_equal(result, expected)
 
-    @pytest.mark.xfail(using_string_dtype(), reason="can't set float into string")
     @pytest.mark.parametrize("regex", [False, True])
     def test_replace_regex_dtype_frame(self, regex):
         # GH-48644
         df1 = DataFrame({"A": ["0"], "B": ["0"]})
-        expected_df1 = DataFrame({"A": [1], "B": [1]}, dtype=df1.dtypes.iloc[0])
+        expected_df1 = DataFrame({"A": [1], "B": [1]}, dtype=object)
         result_df1 = df1.replace(to_replace="0", value=1, regex=regex)
         tm.assert_frame_equal(result_df1, expected_df1)
 
         df2 = DataFrame({"A": ["0"], "B": ["1"]})
-        expected_df2 = DataFrame({"A": [1], "B": ["1"]}, dtype=df2.dtypes.iloc[0])
+        if regex:
+            # TODO(infer_string): both string columns get cast to object,
+            # while only needed for column A
+            expected_df2 = DataFrame({"A": [1], "B": ["1"]}, dtype=object)
+        else:
+            expected_df2 = DataFrame({"A": Series([1], dtype=object), "B": ["1"]})
         result_df2 = df2.replace(to_replace="0", value=1, regex=regex)
         tm.assert_frame_equal(result_df2, expected_df2)
```

## Validation

```json
{
 "image_head": "63d3971328f96fb176305ff2886e5b67a9c39454",
 "patch_applies": true,
 "test_files": [
  "pandas/tests/frame/methods/test_fillna.py",
  "pandas/tests/frame/methods/test_replace.py"
 ],
 "collected_before": 279,
 "collected_after": 279,
 "outcomes_before": {
  "PASSED": 279
 },
 "outcomes_after": {
  "PASSED": 279
 },
 "exit_before": 0,
 "exit_after": 0,
 "tail_before": "FrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*\\\\.\\\\s*-nan-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*\\\\.\\\\s*-nan-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[False]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[True]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_with_value_also_being_replaced\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_categorical_no_replacement\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_object_splitting\n============================= 279 passed in 1.07s ==============================",
 "tail_after": "FrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-True-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*\\\\.\\\\s*-nan-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*\\\\.\\\\s*-nan-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data0]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_regex_replace_scalar[False-False-False-\\\\s*(\\\\.)\\\\s*-\\\\1\\\\1\\\\1-data1]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[False]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_regex_dtype_frame[True]\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_with_value_also_being_replaced\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_categorical_no_replacement\nPASSED pandas/tests/frame/methods/test_replace.py::TestDataFrameReplaceRegex::test_replace_object_splitting\n============================= 279 passed in 0.89s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
