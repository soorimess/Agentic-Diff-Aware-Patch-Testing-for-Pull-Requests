# pandas-dev__pandas-60739

[back to the list](README.md) -- **ENH: `pandas.api.interchange.from_dataframe` now uses the Arrow PyCapsule Interface if available, only falling back to the Dataframe Interchange Protocol if that fails**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#60739](https://github.com/pandas-dev/pandas/pull/60739) (created 2025-01-20, merged 2025-01-21) |
| ChaCo lists | full, f2p30 |
| status | **runnable** -- 2 developer test(s) flip; oracle reproduces it |
| base commit | [`27baf4887a1b`](https://github.com/pandas-dev/pandas/commit/27baf4887a1b7d4f4a378c2f951cdc95fb1ab2b8) (2025-01-21), first parent of the merge commit |
| merge commit | [`bbd6526461b6`](https://github.com/pandas-dev/pandas/commit/bbd6526461b6e9fc7783bd51298db5cb2ae0c679) |
| issues closed | none |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-60739:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-60739.Dockerfile) |
| source files (`patch`) | `doc/source/whatsnew/v3.0.0.rst`, `pandas/core/interchange/from_dataframe.py` |
| test files (`test_patch`) | `pandas/tests/interchange/test_impl.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (2)

- `pandas/tests/interchange/test_impl.py::test_from_dataframe_list_dtype`
- `pandas/tests/interchange/test_impl.py::test_multi_chunk_pyarrow`

## PASS_TO_PASS (83)

<details><summary>show</summary>

- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[0-1-expected_values4]`
- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[0-2-expected_values3]`
- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[0-None-expected_values0]`
- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[1-1-expected_values5]`
- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[1-None-expected_values1]`
- `pandas/tests/interchange/test_impl.py::test_bitmasks_pyarrow[2-None-expected_values2]`
- `pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data0-expected_dtype0-expected_buffer_dtype0]`
- `pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data1-expected_dtype1-expected_buffer_dtype1]`
- `pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data2-expected_dtype2-expected_buffer_dtype2]`
- `pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data3-expected_dtype3-expected_buffer_dtype3]`
- `pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data4-expected_dtype4-expected_buffer_dtype4]`
- `pandas/tests/interchange/test_impl.py::test_categorical_dtype[data0]`
- `pandas/tests/interchange/test_impl.py::test_categorical_dtype[data1]`
- `pandas/tests/interchange/test_impl.py::test_categorical_pyarrow`
- `pandas/tests/interchange/test_impl.py::test_categorical_to_numpy_dlpack`
- `pandas/tests/interchange/test_impl.py::test_dataframe[<lambda>0]`
- `pandas/tests/interchange/test_impl.py::test_dataframe[<lambda>1]`
- `pandas/tests/interchange/test_impl.py::test_dataframe[<lambda>2]`
- `pandas/tests/interchange/test_impl.py::test_dataframe[<lambda>3]`
- `pandas/tests/interchange/test_impl.py::test_dataframe[<lambda>4]`
- `pandas/tests/interchange/test_impl.py::test_datetime`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[ms-US/Pacific]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[ms-UTC]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[ns-US/Pacific]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[ns-UTC]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[s-US/Pacific]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[s-UTC]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[us-US/Pacific]`
- `pandas/tests/interchange/test_impl.py::test_datetimetzdtype[us-UTC]`
- `pandas/tests/interchange/test_impl.py::test_empty_categorical_pyarrow`
- `pandas/tests/interchange/test_impl.py::test_empty_dataframe`
- `pandas/tests/interchange/test_impl.py::test_empty_pyarrow[data0]`
- `pandas/tests/interchange/test_impl.py::test_empty_pyarrow[data1]`
- `pandas/tests/interchange/test_impl.py::test_empty_string_column`
- `pandas/tests/interchange/test_impl.py::test_interchange_from_corrected_buffer_dtypes`
- `pandas/tests/interchange/test_impl.py::test_interchange_from_non_pandas_tz_aware`
- `pandas/tests/interchange/test_impl.py::test_large_string`
- `pandas/tests/interchange/test_impl.py::test_large_string_pyarrow`
- `pandas/tests/interchange/test_impl.py::test_missing_from_masked`
- `pandas/tests/interchange/test_impl.py::test_mixed_data[data0]`
- `pandas/tests/interchange/test_impl.py::test_mixed_data[data1]`
- `pandas/tests/interchange/test_impl.py::test_mixed_data[data2]`
- `pandas/tests/interchange/test_impl.py::test_mixed_missing`
- `pandas/tests/interchange/test_impl.py::test_multi_chunk_column`
- `pandas/tests/interchange/test_impl.py::test_non_str_names`
- `pandas/tests/interchange/test_impl.py::test_non_str_names_w_duplicates`
- `pandas/tests/interchange/test_impl.py::test_nonstring_object`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data0-Int64-int64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data1-Int64[pyarrow]-int64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data10-dtype10-large_string]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data11-string[pyarrow]-large_string]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data12-timestamp[ns][pyarrow]-timestamp[ns]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data13-timestamp[us][pyarrow]-timestamp[us]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data14-timestamp[us,`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data14-timestamp[us, Asia/Kathmandu][pyarrow]-timestamp[us, tz=Asia/Kathmandu]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data2-Int8-int8]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data3-Int8[pyarrow]-int8]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data4-UInt64-uint64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data5-UInt64[pyarrow]-uint64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data6-Float32-float32]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data7-Float32[pyarrow]-float32]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data8-boolean-bool]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_with_missing_values[data9-boolean[pyarrow]-bool]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data0-Int64-int64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data1-Int64[pyarrow]-int64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data10-dtype10-large_string]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data11-string[pyarrow]-large_string]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data12-timestamp[ns][pyarrow]-timestamp[ns]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data13-timestamp[us][pyarrow]-timestamp[us]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data14-timestamp[us,`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data14-timestamp[us, Asia/Kathmandu][pyarrow]-timestamp[us, tz=Asia/Kathmandu]]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data2-Int8-int8]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data3-Int8[pyarrow]-int8]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data4-UInt64-uint64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data5-UInt64[pyarrow]-uint64]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data6-Float32-float32]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data7-Float32[pyarrow]-float32]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data8-boolean-bool]`
- `pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data9-boolean[pyarrow]-bool]`
- `pandas/tests/interchange/test_impl.py::test_string`
- `pandas/tests/interchange/test_impl.py::test_string_validity_buffer`
- `pandas/tests/interchange/test_impl.py::test_string_validity_buffer_no_missing`
- `pandas/tests/interchange/test_impl.py::test_timestamp_ns_pyarrow`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #60739: ENH: `pandas.api.interchange.from_dataframe` now uses the Arrow PyCapsule Interface if available, only falling back to the Dataframe Interchange Protocol if that fails

There's some related discussion to the interchange protocol in #56732 

Regardless of whether it gets deprecated, what we can already do is prefer the PyCapsule Interface if it's available. I'd discussed this informally with @WillAyd 

`pandas.api.interchange.from_dataframe` is still used in some places (Seaborn, Plotly<6.0, Altair<5.4) where people may want to upgrade pandas whilst keeping some other deps pinned, so this should make the transition to the PyCapsule Interface seamless for them
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/doc/source/whatsnew/v3.0.0.rst b/doc/source/whatsnew/v3.0.0.rst
index 102628257d6f2621b6f746fe2111a4905a93c6d9..8471630511e32e92485059c40707d3cface9d936 100644
--- a/doc/source/whatsnew/v3.0.0.rst
+++ b/doc/source/whatsnew/v3.0.0.rst
@@ -30,6 +30,7 @@ Other enhancements
 ^^^^^^^^^^^^^^^^^^
 - :class:`pandas.api.typing.FrozenList` is available for typing the outputs of :attr:`MultiIndex.names`, :attr:`MultiIndex.codes` and :attr:`MultiIndex.levels` (:issue:`58237`)
 - :class:`pandas.api.typing.SASReader` is available for typing the output of :func:`read_sas` (:issue:`55689`)
+- :meth:`pandas.api.interchange.from_dataframe` now uses the `PyCapsule Interface <https://arrow.apache.org/docs/format/CDataInterface/PyCapsuleInterface.html>`_ if available, only falling back to the Dataframe Interchange Protocol if that fails (:issue:`60739`)
 - :class:`pandas.api.typing.NoDefault` is available for typing ``no_default``
 - :func:`DataFrame.to_excel` now raises an ``UserWarning`` when the character count in a cell exceeds Excel's limitation of 32767 characters (:issue:`56954`)
 - :func:`pandas.merge` now validates the ``how`` parameter input (merge type) (:issue:`59435`)
diff --git a/pandas/core/interchange/from_dataframe.py b/pandas/core/interchange/from_dataframe.py
index 5c9b8ac8ea08569ca7e12712b847ee1d25630f4d..b990eca39b3dd0910ef0a58825db4ee4dc8e5ca4 100644
--- a/pandas/core/interchange/from_dataframe.py
+++ b/pandas/core/interchange/from_dataframe.py
@@ -41,7 +41,9 @@ def from_dataframe(df, allow_copy: bool = True) -> pd.DataFrame:
     .. note::
 
        For new development, we highly recommend using the Arrow C Data Interface
-       alongside the Arrow PyCapsule Interface instead of the interchange protocol
+       alongside the Arrow PyCapsule Interface instead of the interchange protocol.
+       From pandas 3.0 onwards, `from_dataframe` uses the PyCapsule Interface,
+       only falling back to the interchange protocol if that fails.
 
     .. warning::
 
@@ -90,6 +92,18 @@ def from_dataframe(df, allow_copy: bool = True) -> pd.DataFrame:
     if isinstance(df, pd.DataFrame):
         return df
 
+    if hasattr(df, "__arrow_c_stream__"):
+        try:
+            pa = import_optional_dependency("pyarrow", min_version="14.0.0")
+        except ImportError:
+            # fallback to _from_dataframe
+            pass
+        else:
+            try:
+                return pa.table(df).to_pandas(zero_copy_only=not allow_copy)
+            except pa.ArrowInvalid as e:
+                raise RuntimeError(e) from e
+
     if not hasattr(df, "__dataframe__"):
         raise ValueError("`df` does not support __dataframe__")
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/interchange/test_impl.py b/pandas/tests/interchange/test_impl.py
index b80b4b923c24782c8505c948b77ba6da4d6a017d..a41d7dec8b496c05bf5cd783ba31289a86f20dc4 100644
--- a/pandas/tests/interchange/test_impl.py
+++ b/pandas/tests/interchange/test_impl.py
@@ -278,7 +278,7 @@ def test_empty_pyarrow(data):
     expected = pd.DataFrame(data)
     arrow_df = pa_from_dataframe(expected)
     result = from_dataframe(arrow_df)
-    tm.assert_frame_equal(result, expected)
+    tm.assert_frame_equal(result, expected, check_column_type=False)
 
 
 def test_multi_chunk_pyarrow() -> None:
@@ -288,8 +288,7 @@ def test_multi_chunk_pyarrow() -> None:
     table = pa.table([n_legs], names=names)
     with pytest.raises(
         RuntimeError,
-        match="To join chunks a copy is required which is "
-        "forbidden by allow_copy=False",
+        match="Cannot do zero copy conversion into multi-column DataFrame block",
     ):
         pd.api.interchange.from_dataframe(table, allow_copy=False)
 
@@ -641,3 +640,12 @@ def test_buffer_dtype_categorical(
     col = dfi.get_column_by_name("data")
     assert col.dtype == expected_dtype
     assert col.get_buffers()["data"][1] == expected_buffer_dtype
+
+
+def test_from_dataframe_list_dtype():
+    pa = pytest.importorskip("pyarrow", "14.0.0")
+    data = {"a": [[1, 2], [4, 5, 6]]}
+    tbl = pa.table(data)
+    result = from_dataframe(tbl)
+    expected = pd.DataFrame(data)
+    tm.assert_frame_equal(result, expected)
```

## Validation

```json
{
 "test_files": [
  "pandas/tests/interchange/test_impl.py"
 ],
 "collected_before": 85,
 "collected_after": 85,
 "outcomes_before": {
  "PASSED": 83,
  "FAILED": 2
 },
 "outcomes_after": {
  "PASSED": 85
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data12-timestamp[ns][pyarrow]-timestamp[ns]]\nPASSED pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data13-timestamp[us][pyarrow]-timestamp[us]]\nPASSED pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data14-timestamp[us, Asia/Kathmandu][pyarrow]-timestamp[us, tz=Asia/Kathmandu]]\nPASSED pandas/tests/interchange/test_impl.py::test_string_validity_buffer\nPASSED pandas/tests/interchange/test_impl.py::test_string_validity_buffer_no_missing\nPASSED pandas/tests/interchange/test_impl.py::test_empty_dataframe\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data0-expected_dtype0-expected_buffer_dtype0]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data1-expected_dtype1-expected_buffer_dtype1]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data2-expected_dtype2-expected_buffer_dtype2]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data3-expected_dtype3-expected_buffer_dtype3]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data4-expected_dtype4-expected_buffer_dtype4]\nFAILED pandas/tests/interchange/test_impl.py::test_multi_chunk_pyarrow - Asse...\nFAILED pandas/tests/interchange/test_impl.py::test_from_dataframe_list_dtype\n========================= 2 failed, 81 passed in 0.48s =========================",
 "tail_after": "llable_without_missing_values[data11-string[pyarrow]-large_string]\nPASSED pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data12-timestamp[ns][pyarrow]-timestamp[ns]]\nPASSED pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data13-timestamp[us][pyarrow]-timestamp[us]]\nPASSED pandas/tests/interchange/test_impl.py::test_pandas_nullable_without_missing_values[data14-timestamp[us, Asia/Kathmandu][pyarrow]-timestamp[us, tz=Asia/Kathmandu]]\nPASSED pandas/tests/interchange/test_impl.py::test_string_validity_buffer\nPASSED pandas/tests/interchange/test_impl.py::test_string_validity_buffer_no_missing\nPASSED pandas/tests/interchange/test_impl.py::test_empty_dataframe\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data0-expected_dtype0-expected_buffer_dtype0]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data1-expected_dtype1-expected_buffer_dtype1]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data2-expected_dtype2-expected_buffer_dtype2]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data3-expected_dtype3-expected_buffer_dtype3]\nPASSED pandas/tests/interchange/test_impl.py::test_buffer_dtype_categorical[data4-expected_dtype4-expected_buffer_dtype4]\nPASSED pandas/tests/interchange/test_impl.py::test_from_dataframe_list_dtype\n============================== 83 passed in 0.33s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
