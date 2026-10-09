# pandas-dev__pandas-59488

[back to the list](README.md) -- **String dtype: honor mode.string_storage option (and change default to None)**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#59488](https://github.com/pandas-dev/pandas/pull/59488) (created 2024-08-12, merged 2024-08-12) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 1 developer test(s) flip; oracle reproduces it |
| base commit | [`96d732e3ccaf`](https://github.com/pandas-dev/pandas/commit/96d732e3ccaf5b10373747664392fa231afd3c3a) (2024-08-12), first parent of the merge commit |
| merge commit | [`8ab673cdaed9`](https://github.com/pandas-dev/pandas/commit/8ab673cdaed9a2620a1d7070199e539dcecb111d) |
| issues closed | none |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-59488:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-59488.Dockerfile) |
| source files (`patch`) | `pandas/core/arrays/string_.py`, `pandas/core/config_init.py` |
| test files (`test_patch`) | `pandas/tests/arrays/string_/test_string_arrow.py`, `pandas/tests/dtypes/test_common.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (1)

- `pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[python]`

## PASS_TO_PASS (505)

<details><summary>show</summary>

- `pandas/tests/arrays/string_/test_string_arrow.py::test_config[pyarrow]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_config[python]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_config_bad_storage_raises`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_from_list`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_not_string_type_raises[numpy-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_not_string_type_raises[pyarrow-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_not_string_type_raises[pyarrow-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_not_string_type_value_dictionary_raises[False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_not_string_type_value_dictionary_raises[True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_valid_string_type_value_dictionary[False-large_string]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_valid_string_type_value_dictionary[False-string]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_valid_string_type_value_dictionary[True-large_string]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_constructor_valid_string_type_value_dictionary[True-string]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_eq_all_na`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_from_sequence_wrong_dtype_raises`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_pickle_roundtrip[string[pyarrow]]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_pickle_roundtrip[string[pyarrow_numpy]]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[-1-XX-expected0-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[-1-XX-expected0-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-None-expected2-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-None-expected2-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-XX-expected1-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-XX-expected1-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-value3-expected3-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[1-value3-expected3-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key10-XX-expected10-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key10-XX-expected10-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key11-value11-expected11-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key11-value11-expected11-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key12-value12-expected12-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key12-value12-expected12-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key13-XX-expected13-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key13-XX-expected13-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key14-value14-expected14-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key14-value14-expected14-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key4-XX-expected4-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key4-XX-expected4-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key5-value5-expected5-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key5-value5-expected5-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key6-value6-expected6-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key6-value6-expected6-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key7-value7-expected7-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key7-value7-expected7-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key8-value8-expected8-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key8-value8-expected8-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key9-value9-expected9-False]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem[key9-value9-expected9-True]`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_setitem_invalid_indexer_raises`
- `pandas/tests/arrays/string_/test_string_arrow.py::test_string_dtype_error_message`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_categorical_dtype`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[M8[ns,`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[M8[ns, Asia/Tokyo]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[M8[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[M8[ns, UTC]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[datetime64[ns, Asia/Tokyo]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_datetimetz_dtype[datetime64[ns, UTC]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_invalid_dtype_error[Timestamp]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_invalid_dtype_error[list]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_invalid_dtype_error[pd.Timestamp]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_dtype[M8[ns]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_dtype[float64]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_dtype[int64]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_dtype[m8[ns]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_dtype[object]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_numpy_string_dtype`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[O]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[dtype3]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[dtype7]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[float64_0]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[float64_1]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[float]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[object]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[object_0]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_pandas_dtype_valid[object_1]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[Period[3M]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[Period[D]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[Period[us]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[period[3M]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[period[D]]`
- `pandas/tests/dtypes/test_common.py::TestNumpyEADtype::test_period_dtype[period[us]]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[1-NoneType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[1.2-NoneType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[<M8[ns]-datetime64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[None-NoneType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[category-CategoricalDtypeType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[datetime64[ns, Europe/London]-Timestamp]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[float-float64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[float64-float64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param11-CategoricalDtypeType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param12-CategoricalDtypeType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param13-CategoricalDtypeType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param14-CategoricalDtypeType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param15-datetime64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param16-datetime64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param18-Timestamp]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param19-Timestamp]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param21-Period]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param23-Interval]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param27-NoneType]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param4-float64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param6-int16]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param7-object_]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param8-int64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[input_param9-object_]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[int-int64]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[int32-int32]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[period[D]-Period]`
- `pandas/tests/dtypes/test_common.py::test__is_dtype_type[str-str_]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int16]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int32]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int64]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int8]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint16]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint32]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint64]`
- `pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint8]`
- `pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[datetime64]`
- `pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[timedelta64]`
- `pandas/tests/dtypes/test_common.py::test_custom_ea_kind_M_not_datetime64tz`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[category-category-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime-datetime64[ns]-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[datetime_tz-datetime64[ns, US/Eastern]-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[float-float64-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[integer-int64-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[object-object-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[period-period[D]-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[string-string-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-category-category]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-float-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-object-object]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-string-string]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal[timedelta-timedelta64[ns]-timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[None-None]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[dtype14-dtype24]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[dtype15-dtype25]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[float32-float64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[int16-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[int32-int64]`
- `pandas/tests/dtypes/test_common.py::test_dtype_equal_strict[int8-int64]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[<M8[ns]-result18]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[category-category]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[datetime64[ns, Europe/London]-result19]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[float-result2]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[float64-result3]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param11-result11]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param12-result12]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param13-result13]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param14-result14]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param15-result15]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param16-result16]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param17-result17]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param20-result20]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param22-result22]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param4-result4]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param6-result6]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param7-result7]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param8-result8]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[input_param9-result9]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[int-result0]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[int32-result1]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[period[D]-result21]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype[str-result5]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_1d_only_ea_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_any_real_numeric_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_bool_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_categorical_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_complex_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_datetime64_any_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_datetime64_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_datetime64_ns_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_datetime64tz_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_ea_or_datetimelike_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_extension_array_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_float_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_int64_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_integer_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_interval_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_numeric_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_object_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_period_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_signed_integer_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_string_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_timedelta64_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_timedelta64_ns_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_error_catch[is_unsigned_integer_dtype]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[1-data`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[1-data type not understood]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[1.2-data`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[1.2-data type not understood]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[None-Cannot`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[None-Cannot deduce dtype from null object]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[input_param4-data`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[input_param4-data type not understood]`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[random`
- `pandas/tests/dtypes/test_common.py::test_get_dtype_fails[random string-data type ["']random string["'] not understood]`
- `pandas/tests/dtypes/test_common.py::test_is_any_real_numeric_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_bool_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_bool_dtype_numpy_error`
- `pandas/tests/dtypes/test_common.py::test_is_categorical_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_complex_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_datetime64_any_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_datetime64_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_datetime64_ns_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_datetime64tz_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_extension_array_dtype[False]`
- `pandas/tests/dtypes/test_common.py::test_is_extension_array_dtype[True]`
- `pandas/tests/dtypes/test_common.py::test_is_float_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_int64_dtype[Int64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_int64_dtype[Int64]`
- `pandas/tests/dtypes/test_common.py::test_is_int64_dtype[dtype1]`
- `pandas/tests/dtypes/test_common.py::test_is_int64_dtype[int64]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int16]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int32]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int64]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[Int8]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt16]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt32]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt64]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[UInt8]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[dtype0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int8_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[int]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_integer_dtype[uint8_1]`
- `pandas/tests/dtypes/test_common.py::test_is_interval_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[Int8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[Int8]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[dtype4]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[dtype5]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[dtype6]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[float]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[int32]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[int8]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[str]`
- `pandas/tests/dtypes/test_common.py::test_is_not_int64_dtype[uint64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[datetime64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[dtype4]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[dtype5]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[dtype6]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[float]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[str]`
- `pandas/tests/dtypes/test_common.py::test_is_not_integer_dtype[timedelta64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt16]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt32]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[UInt8]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[datetime64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[dtype4]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[dtype5]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[dtype6]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[float]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[str]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[timedelta64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_signed_integer_dtype[uint8_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int16]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int32]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[Int8]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[datetime64]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[dtype4]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[dtype5]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[dtype6]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[float]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int8_1]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[int]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[str]`
- `pandas/tests/dtypes/test_common.py::test_is_not_unsigned_integer_dtype[timedelta64]`
- `pandas/tests/dtypes/test_common.py::test_is_numeric_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_numeric_v_string_like`
- `pandas/tests/dtypes/test_common.py::test_is_object`
- `pandas/tests/dtypes/test_common.py::test_is_period_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_scipy_sparse`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int16]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int32]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int64]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[Int8]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[dtype0]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int8_1]`
- `pandas/tests/dtypes/test_common.py::test_is_signed_integer_dtype[int]`
- `pandas/tests/dtypes/test_common.py::test_is_sparse[False]`
- `pandas/tests/dtypes/test_common.py::test_is_sparse[True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[dtype1-False]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[dtype4-True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[dtype5-True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[dtype6-True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[int-False]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[object-True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype[str-True]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype_arraylike_with_object_elements_not_strings[data0]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype_arraylike_with_object_elements_not_strings[data1]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype_arraylike_with_object_elements_not_strings[data2]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype_nullable[string[pyarrow]]`
- `pandas/tests/dtypes/test_common.py::test_is_string_dtype_nullable[string[python]]`
- `pandas/tests/dtypes/test_common.py::test_is_timedelta64_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_timedelta64_ns_dtype`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt16Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt16]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt32Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt32]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt64Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt64]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt8Dtype]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[UInt8]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[dtype0]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint16_0]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint16_1]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint32_0]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint32_1]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint64_0]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint64_1]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint8_0]`
- `pandas/tests/dtypes/test_common.py::test_is_unsigned_integer_dtype[uint8_1]`
- `pandas/tests/dtypes/test_common.py::test_needs_i8_conversion`
- `pandas/tests/dtypes/test_common.py::test_pandas_dtype_ea_not_instance`
- `pandas/tests/dtypes/test_common.py::test_pandas_dtype_numpy_warning`
- `pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[pyarrow]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[category-category]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[datetime-datetime64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[datetime_tz-datetime64[ns,`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[datetime_tz-datetime64[ns, US/Eastern]]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[float-float64]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[integer-int64]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[object-object]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[period-period[D]]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[string-string]`
- `pandas/tests/dtypes/test_common.py::test_pyarrow_string_import_error[timedelta-timedelta64[ns]]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Float32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Float64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[Int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[UInt16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[UInt32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[UInt64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_numeric_ea_dtype[UInt8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[float32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[float64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[float]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[int]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[uint16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[uint32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[uint64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_real_numpy_dtype[uint8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int16-int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int16-int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int16-int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int16-int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int16-int]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int32-int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int32-int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int32-int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int32-int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int32-int]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int64-int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int64-int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int64-int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int64-int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int64-int]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int8-int16]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int8-int32]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int8-int64]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int8-int8]`
- `pandas/tests/dtypes/test_common.py::test_type_comparison_with_signed_int_ea_dtype_and_signed_int_numpy_dtype[Int8-int]`
- `pandas/tests/dtypes/test_common.py::test_validate_allhashable`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #59488: String dtype: honor mode.string_storage option (and change default to None)

At the moment, the `pd.options.mode.string_storage` option defaults to `"python"`, and the `StringDtype()` constructor just ignores it when constructing the future default NaN-variant (i.e. the option is only used for creating the NA-variant), but uses the logic of "use `"pyarrow"` if installed otherwise `"python"`".

Given this option exists, I think it makes sense to let it always be honored, so that a user can actually control this through the option (and also for testing this makes things a bit easier to check the behaviour in case pyarrow is not installed without uninstalling/installing it constantly). 

In order to honor the option, I changed the default to `None` to mean this "use `"pyarrow"` if installed otherwise `"python"`" logic as default if constructing the NaN-variant. 
When constructing the NA-variant, for now `None` still gets translated to `"python"`. I think we should also change the default for this dtype to use pyarrow if installed, but that's a change only for 3.0, I think (not to backport for 2.3), so therefore didn't include that in this PR.

xref https://github.com/pandas-dev/pandas/issues/54792
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/core/arrays/string_.py b/pandas/core/arrays/string_.py
index 2ba7c9fccbfce7b2b6663c320b35b2e8a668987a..45dc0ef374b136ebd5cfb6d9c0fe61976b518286 100644
--- a/pandas/core/arrays/string_.py
+++ b/pandas/core/arrays/string_.py
@@ -140,12 +140,16 @@ class StringDtype(StorageExtensionDtype):
         # infer defaults
         if storage is None:
             if na_value is not libmissing.NA:
-                if HAS_PYARROW:
-                    storage = "pyarrow"
-                else:
-                    storage = "python"
+                storage = get_option("mode.string_storage")
+                if storage == "auto":
+                    if HAS_PYARROW:
+                        storage = "pyarrow"
+                    else:
+                        storage = "python"
             else:
                 storage = get_option("mode.string_storage")
+                if storage == "auto":
+                    storage = "python"
 
         if storage == "pyarrow_numpy":
             # TODO raise a deprecation warning
diff --git a/pandas/core/config_init.py b/pandas/core/config_init.py
index e62cda0dfe8d02574cfe3c1fe535ac156b859b89..e4eefb570fd95974103c666f03cb70ca93824cbf 100644
--- a/pandas/core/config_init.py
+++ b/pandas/core/config_init.py
@@ -452,13 +452,12 @@ with cf.config_prefix("mode"):
 
 string_storage_doc = """
 : string
-    The default storage for StringDtype. This option is ignored if
-    ``future.infer_string`` is set to True.
+    The default storage for StringDtype.
 """
 
 
 def is_valid_string_storage(value: Any) -> None:
-    legal_values = ["python", "pyarrow"]
+    legal_values = ["auto", "python", "pyarrow"]
     if value not in legal_values:
         msg = "Value must be one of python|pyarrow"
         if value == "pyarrow_numpy":
@@ -473,7 +472,7 @@ def is_valid_string_storage(value: Any) -> None:
 with cf.config_prefix("mode"):
     cf.register_option(
         "string_storage",
-        "python",
+        "auto",
         string_storage_doc,
         # validator=is_one_of_factory(["python", "pyarrow"]),
         validator=is_valid_string_storage,
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/arrays/string_/test_string_arrow.py b/pandas/tests/arrays/string_/test_string_arrow.py
index c01966c72f8119090494cc1ac1930de658f4ea1b..cfba32c62f2069f97c2841a4ff4d55023a156dc9 100644
--- a/pandas/tests/arrays/string_/test_string_arrow.py
+++ b/pandas/tests/arrays/string_/test_string_arrow.py
@@ -4,7 +4,6 @@ import re
 import numpy as np
 import pytest
 
-from pandas.compat import HAS_PYARROW
 import pandas.util._test_decorators as td
 
 import pandas as pd
@@ -27,11 +26,10 @@ def test_eq_all_na():
     tm.assert_extension_array_equal(result, expected)
 
 
-def test_config(string_storage, request, using_infer_string):
-    if using_infer_string and string_storage == "python" and HAS_PYARROW:
-        # string storage with na_value=NaN always uses pyarrow if available
-        # -> does not yet honor the option
-        request.applymarker(pytest.mark.xfail(reason="TODO(infer_string)"))
+def test_config(string_storage, using_infer_string):
+    # with the default string_storage setting
+    # always "python" at the moment
+    assert StringDtype().storage == "python"
 
     with pd.option_context("string_storage", string_storage):
         assert StringDtype().storage == string_storage
diff --git a/pandas/tests/dtypes/test_common.py b/pandas/tests/dtypes/test_common.py
index 4bf97b1fd84945bf14d9b6007b8c509969b6cac0..2c2dff7a957fedafc24ff57225e8cebe0c5540df 100644
--- a/pandas/tests/dtypes/test_common.py
+++ b/pandas/tests/dtypes/test_common.py
@@ -3,6 +3,7 @@ from __future__ import annotations
 import numpy as np
 import pytest
 
+from pandas.compat import HAS_PYARROW
 import pandas.util._test_decorators as td
 
 from pandas.core.dtypes.astype import astype_array
@@ -802,13 +803,17 @@ def test_pandas_dtype_ea_not_instance():
 
 
 def test_pandas_dtype_string_dtypes(string_storage):
-    # TODO(infer_string) remove skip if "python" is supported
-    pytest.importorskip("pyarrow")
+    with pd.option_context("future.infer_string", True):
+        # with the default string_storage setting
+        result = pandas_dtype("str")
+    assert result == pd.StringDtype(
+        "pyarrow" if HAS_PYARROW else "python", na_value=np.nan
+    )
+
     with pd.option_context("future.infer_string", True):
         with pd.option_context("string_storage", string_storage):
             result = pandas_dtype("str")
-    # TODO(infer_string) hardcoded to pyarrow until python is supported
-    assert result == pd.StringDtype("pyarrow", na_value=np.nan)
+    assert result == pd.StringDtype(string_storage, na_value=np.nan)
 
     with pd.option_context("future.infer_string", False):
         with pd.option_context("string_storage", string_storage):
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/arrays/string_/test_string_arrow.py",
  "pandas/tests/dtypes/test_common.py"
 ],
 "collected_before": 508,
 "collected_after": 508,
 "outcomes_before": {
  "PASSED": 505,
  "SKIPPED": 2,
  "FAILED": 1
 },
 "outcomes_after": {
  "PASSED": 506,
  "SKIPPED": 2
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "ts/dtypes/test_common.py::test_astype_nansafe_copy_false[uint16]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint32]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int8]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int16]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int32]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[datetime64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[timedelta64]\nPASSED pandas/tests/dtypes/test_common.py::test_validate_allhashable\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_numpy_warning\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_ea_not_instance\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[pyarrow]\nSKIPPED [1] pandas/tests/arrays/string_/test_string_arrow.py:62: chunked not applicable to numpy array\nSKIPPED [1] pandas/tests/arrays/string_/test_string_arrow.py:166: Skipping because pyarrow is installed.\nFAILED pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[python]\n=================== 1 failed, 486 passed, 2 skipped in 1.69s ===================",
 "tail_after": "ts/dtypes/test_common.py::test_astype_nansafe_copy_false[uint16]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint32]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[uint64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int8]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int16]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int32]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_nansafe_copy_false[int64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[datetime64]\nPASSED pandas/tests/dtypes/test_common.py::test_astype_object_preserves_datetime_na[timedelta64]\nPASSED pandas/tests/dtypes/test_common.py::test_validate_allhashable\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_numpy_warning\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_ea_not_instance\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[python]\nPASSED pandas/tests/dtypes/test_common.py::test_pandas_dtype_string_dtypes[pyarrow]\nSKIPPED [1] pandas/tests/arrays/string_/test_string_arrow.py:62: chunked not applicable to numpy array\nSKIPPED [1] pandas/tests/arrays/string_/test_string_arrow.py:166: Skipping because pyarrow is installed.\n======================== 487 passed, 2 skipped in 1.03s ========================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
