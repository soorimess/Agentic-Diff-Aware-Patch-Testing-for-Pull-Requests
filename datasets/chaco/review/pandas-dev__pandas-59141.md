# pandas-dev__pandas-59141

[back to the list](README.md) -- **REF: Make concat not stateful.**

| field | value |
|---|---|
| pull request | [pandas-dev/pandas#59141](https://github.com/pandas-dev/pandas/pull/59141) (created 2024-06-28, merged 2024-07-05) |
| ChaCo lists | full, ablation, f2p30 |
| status | **runnable** -- 2 developer test(s) flip; oracle reproduces it |
| base commit | [`039edee0bc1a`](https://github.com/pandas-dev/pandas/commit/039edee0bc1a729ee9b67a6f9a337f7cd03118d1) (2024-07-05), first parent of the merge commit |
| merge commit | [`f3ad4d50aee3`](https://github.com/pandas-dev/pandas/commit/f3ad4d50aee360092c54b918b28c2cba90c90f20) |
| issues closed | none |
| version | 3.0 |
| image | `f2p-chaco/pandas-dev__pandas-59141:latest` -- [Dockerfile](../dockerfiles/pandas-dev__pandas-59141.Dockerfile) |
| source files (`patch`) | `pandas/core/generic.py`, `pandas/core/reshape/concat.py` |
| test files (`test_patch`) | `pandas/tests/generic/test_frame.py`, `pandas/tests/generic/test_series.py` |
| compiled files changed | none |
| binary files left out | none |

## FAIL_TO_PASS (2)

- `pandas/tests/generic/test_frame.py::TestDataFrame::test_metadata_propagation_indiv`
- `pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv`

## PASS_TO_PASS (29)

<details><summary>show</summary>

- `pandas/tests/generic/test_frame.py::TestDataFrame2::test_unexpected_keyword`
- `pandas/tests/generic/test_frame.py::TestDataFrame2::test_validate_bool_args[1]`
- `pandas/tests/generic/test_frame.py::TestDataFrame2::test_validate_bool_args[5.0]`
- `pandas/tests/generic/test_frame.py::TestDataFrame2::test_validate_bool_args[True]`
- `pandas/tests/generic/test_frame.py::TestDataFrame2::test_validate_bool_args[value2]`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_deepcopy_empty`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_metadata_propagation_indiv_groupby`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_metadata_propagation_indiv_resample`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_nonzero_single_element`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_set_attribute`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_set_axis_name[_set_axis_name]`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_set_axis_name[rename_axis]`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_set_axis_name_mi[_set_axis_name]`
- `pandas/tests/generic/test_frame.py::TestDataFrame::test_set_axis_name_mi[rename_axis]`
- `pandas/tests/generic/test_series.py::TestSeries::test_get_bool_data_preserve_dtype`
- `pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv_resample`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0.0]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[1]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[a]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data0]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data1]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[False]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[True]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[data1]`
- `pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[nan]`
- `pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_mi[_set_axis_name]`
- `pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_mi[rename_axis]`
- `pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_raises`

</details>

## Problem statement (what the agent may be shown)

```text
Pull request #59141: REF: Make concat not stateful.

All the logic used to be held in a `_Concatenator` class. The statefullness wasn't really needed since `concat` is a one-shot method so broke it out into its functions
```

## Hints (issue comments before the PR; not shown to the agent)

```text
(none)
```

## `patch` -- the change under test

```diff
diff --git a/pandas/core/generic.py b/pandas/core/generic.py
index 33190f905be13a199aab7a51d1271d84da1af82d..312f5d20d794f7ae5b9a5d559591546190949a17 100644
--- a/pandas/core/generic.py
+++ b/pandas/core/generic.py
@@ -6017,17 +6017,16 @@ class NDFrame(PandasObject, indexing.IndexingMixin):
                 object.__setattr__(self, name, getattr(other, name, None))
 
         if method == "concat":
+            objs = kwargs["objs"]
             # propagate attrs only if all concat arguments have the same attrs
-            if all(bool(obj.attrs) for obj in other.objs):
+            if all(bool(obj.attrs) for obj in objs):
                 # all concatenate arguments have non-empty attrs
-                attrs = other.objs[0].attrs
-                have_same_attrs = all(obj.attrs == attrs for obj in other.objs[1:])
+                attrs = objs[0].attrs
+                have_same_attrs = all(obj.attrs == attrs for obj in objs[1:])
                 if have_same_attrs:
                     self.attrs = deepcopy(attrs)
 
-            allows_duplicate_labels = all(
-                x.flags.allows_duplicate_labels for x in other.objs
-            )
+            allows_duplicate_labels = all(x.flags.allows_duplicate_labels for x in objs)
             self.flags.allows_duplicate_labels = allows_duplicate_labels
 
         return self
diff --git a/pandas/core/reshape/concat.py b/pandas/core/reshape/concat.py
index 2d2787e56f40293844d8b98ee40940993dce4f25..6381869c3e559a34b7422a8a8c6c4dcbc5a6d1cd 100644
--- a/pandas/core/reshape/concat.py
+++ b/pandas/core/reshape/concat.py
@@ -16,10 +16,12 @@ import warnings
 import numpy as np
 
 from pandas._libs import lib
-from pandas.util._decorators import cache_readonly
 from pandas.util._exceptions import find_stack_level
 
-from pandas.core.dtypes.common import is_bool
+from pandas.core.dtypes.common import (
+    is_bool,
+    is_scalar,
+)
 from pandas.core.dtypes.concat import concat_compat
 from pandas.core.dtypes.generic import (
     ABCDataFrame,
@@ -385,291 +387,328 @@ def concat(
             DeprecationWarning,
             stacklevel=find_stack_level(),
         )
+    if join == "outer":
+        intersect = False
+    elif join == "inner":
+        intersect = True
+    else:  # pragma: no cover
+        raise ValueError(
+            "Only can inner (intersect) or outer (union) join the other axis"
+        )
 
-    op = _Concatenator(
-        objs,
-        axis=axis,
-        ignore_index=ignore_index,
-        join=join,
-        keys=keys,
-        levels=levels,
-        names=names,
-        verify_integrity=verify_integrity,
-        sort=sort,
-    )
-
-    return op.get_result()
+    if not is_bool(sort):
+        raise ValueError(
+            f"The 'sort' keyword only accepts boolean values; {sort} was passed."
+        )
+    sort = bool(sort)
 
+    objs, keys, ndims = _clean_keys_and_objs(objs, keys)
 
-class _Concatenator:
-    """
-    Orchestrates a concatenation operation for BlockManagers
-    """
+    # select an object to be our result reference
+    sample, objs = _get_sample_object(objs, ndims, keys, names, levels, intersect)
 
-    sort: bool
-
-    def __init__(
-        self,
-        objs: Iterable[Series | DataFrame] | Mapping[HashableT, Series | DataFrame],
-        axis: Axis = 0,
-        join: str = "outer",
-        keys: Iterable[Hashable] | None = None,
-        levels=None,
-        names: list[HashableT] | None = None,
-        ignore_index: bool = False,
-        verify_integrity: bool = False,
-        sort: bool = False,
-    ) -> None:
-        if isinstance(objs, (ABCSeries, ABCDataFrame, str)):
-            raise TypeError(
-                "first argument must be an iterable of pandas "
-                f'objects, you passed an object of type "{type(objs).__name__}"'
-            )
+    # Standardize axis parameter to int
+    if sample.ndim == 1:
+        from pandas import DataFrame
 
-        if join == "outer":
-            self.intersect = False
-        elif join == "inner":
-            self.intersect = True
-        else:  # pragma: no cover
-            raise ValueError(
-                "Only can inner (intersect) or outer (union) join the other axis"
-            )
+        bm_axis = DataFrame._get_axis_number(axis)
+        is_frame = False
+        is_series = True
+    else:
+        bm_axis = sample._get_axis_number(axis)
+        is_frame = True
+        is_series = False
 
-        if not is_bool(sort):
-            raise ValueError(
-                f"The 'sort' keyword only accepts boolean values; {sort} was passed."
-            )
-        # Incompatible types in assignment (expression has type "Union[bool, bool_]",
-        # variable has type "bool")
-        self.sort = sort  # type: ignore[assignment]
+        # Need to flip BlockManager axis in the DataFrame special case
+        bm_axis = sample._get_block_manager_axis(bm_axis)
 
-        self.ignore_index = ignore_index
-        self.verify_integrity = verify_integrity
+    # if we have mixed ndims, then convert to highest ndim
+    # creating column numbers as needed
+    if len(ndims) > 1:
+        objs = _sanitize_mixed_ndim(objs, sample, ignore_index, bm_axis)
 
-        objs, keys, ndims = _clean_keys_and_objs(objs, keys)
+    axis = 1 - bm_axis if is_frame else 0
+    names = names or getattr(keys, "names", None)
+    return _get_result(
+        objs,
+        is_series,
+        bm_axis,
+        ignore_index,
+        intersect,
+        sort,
+        keys,
+        levels,
+        verify_integrity,
+        names,
+        axis,
+    )
 
-        # select an object to be our result reference
-        sample, objs = _get_sample_object(
-            objs, ndims, keys, names, levels, self.intersect
-        )
 
-        # Standardize axis parameter to int
-        if sample.ndim == 1:
-            from pandas import DataFrame
+def _sanitize_mixed_ndim(
+    objs: list[Series | DataFrame],
+    sample: Series | DataFrame,
+    ignore_index: bool,
+    axis: AxisInt,
+) -> list[Series | DataFrame]:
+    # if we have mixed ndims, then convert to highest ndim
+    # creating column numbers as needed
+
+    new_objs = []
+
+    current_column = 0
+    max_ndim = sample.ndim
+    for obj in objs:
+        ndim = obj.ndim
+        if ndim == max_ndim:
+            pass
+
+        elif ndim != max_ndim - 1:
+            raise ValueError(
+                "cannot concatenate unaligned mixed dimensional NDFrame objects"
+            )
 
-            axis = DataFrame._get_axis_number(axis)
-            self._is_frame = False
-            self._is_series = True
         else:
-            axis = sample._get_axis_number(axis)
-            self._is_frame = True
-            self._is_series = False
-
-            # Need to flip BlockManager axis in the DataFrame special case
-            axis = sample._get_block_manager_axis(axis)
-
-        # if we have mixed ndims, then convert to highest ndim
-        # creating column numbers as needed
-        if len(ndims) > 1:
-            objs = self._sanitize_mixed_ndim(objs, sample, ignore_index, axis)
-
-        self.objs = objs
-
-        # note: this is the BlockManager axis (since DataFrame is transposed)
-        self.bm_axis = axis
-        self.axis = 1 - self.bm_axis if self._is_frame else 0
-        self.keys = keys
-        self.names = names or getattr(keys, "names", None)
-        self.levels = levels
-
-    def _sanitize_mixed_ndim(
-        self,
-        objs: list[Series | DataFrame],
-        sample: Series | DataFrame,
-        ignore_index: bool,
-        axis: AxisInt,
-    ) -> list[Series | DataFrame]:
-        # if we have mixed ndims, then convert to highest ndim
-        # creating column numbers as needed
-
-        new_objs = []
-
-        current_column = 0
-        max_ndim = sample.ndim
-        for obj in objs:
-            ndim = obj.ndim
-            if ndim == max_ndim:
-                pass
-
-            elif ndim != max_ndim - 1:
-                raise ValueError(
-                    "cannot concatenate unaligned mixed dimensional NDFrame objects"
-                )
-
-            else:
-                name = getattr(obj, "name", None)
-                if ignore_index or name is None:
-                    if axis == 1:
-                        # doing a row-wise concatenation so need everything
-                        # to line up
-                        name = 0
-                    else:
-                        # doing a column-wise concatenation so need series
-                        # to have unique names
-                        name = current_column
-                        current_column += 1
-                    obj = sample._constructor(obj, copy=False)
-                    if isinstance(obj, ABCDataFrame):
-                        obj.columns = range(name, name + 1, 1)
+            name = getattr(obj, "name", None)
+            if ignore_index or name is None:
+                if axis == 1:
+                    # doing a row-wise concatenation so need everything
+                    # to line up
+                    name = 0
                 else:
-                    obj = sample._constructor({name: obj}, copy=False)
-
-            new_objs.append(obj)
-
-        return new_objs
+                    # doing a column-wise concatenation so need series
+                    # to have unique names
+                    name = current_column
+                    current_column += 1
+                obj = sample._constructor(obj, copy=False)
+                if isinstance(obj, ABCDataFrame):
+                    obj.columns = range(name, name + 1, 1)
+            else:
+                obj = sample._constructor({name: obj}, copy=False)
 
-    def get_result(self):
-        cons: Callable[..., DataFrame | Series]
-        sample: DataFrame | Series
+        new_objs.append(obj)
 
-        # series only
-        if self._is_series:
-            sample = cast("Series", self.objs[0])
+    return new_objs
 
-            # stack blocks
-            if self.bm_axis == 0:
-                name = com.consensus_name_attr(self.objs)
-                cons = sample._constructor
 
-                arrs = [ser._values for ser in self.objs]
+def _get_result(
+    objs: list[Series | DataFrame],
+    is_series: bool,
+    bm_axis: AxisInt,
+    ignore_index: bool,
+    intersect: bool,
+    sort: bool,
+    keys: Iterable[Hashable] | None,
+    levels,
+    verify_integrity: bool,
+    names: list[HashableT] | None,
+    axis: AxisInt,
+):
+    cons: Callable[..., DataFrame | Series]
+    sample: DataFrame | Series
 
-                res = concat_compat(arrs, axis=0)
+    # series only
+    if is_series:
+        sample = cast("Series", objs[0])
 
-                new_index: Index
-                if self.ignore_index:
-                    # We can avoid surprisingly-expensive _get_concat_axis
-                    new_index = default_index(len(res))
-                else:
-                    new_index = self.new_axes[0]
+        # stack blocks
+        if bm_axis == 0:
+            name = com.consensus_name_attr(objs)
+            cons = sample._constructor
 
-                mgr = type(sample._mgr).from_array(res, index=new_index)
+            arrs = [ser._values for ser in objs]
 
-                result = sample._constructor_from_mgr(mgr, axes=mgr.axes)
-                result._name = name
-                return result.__finalize__(self, method="concat")
+            res = concat_compat(arrs, axis=0)
 
-            # combine as columns in a frame
+            if ignore_index:
+                new_index: Index = default_index(len(res))
             else:
-                data = dict(enumerate(self.objs))
+                new_index = _get_concat_axis_series(
+                    objs,
+                    ignore_index,
+                    bm_axis,
+                    keys,
+                    levels,
+                    verify_integrity,
+                    names,
+                )
 
-                # GH28330 Preserves subclassed objects through concat
-                cons = sample._constructor_expanddim
+            mgr = type(sample._mgr).from_array(res, index=new_index)
 
-                index, columns = self.new_axes
-                df = cons(data, index=index, copy=False)
-                df.columns = columns
-                return df.__finalize__(self, method="concat")
+            result = sample._constructor_from_mgr(mgr, axes=mgr.axes)
+            result._name = name
+            return result.__finalize__(object(), method="concat", objs=objs)
 
-        # combine block managers
+        # combine as columns in a frame
         else:
-            sample = cast("DataFrame", self.objs[0])
-
-            mgrs_indexers = []
-            for obj in self.objs:
-                indexers = {}
-                for ax, new_labels in enumerate(self.new_axes):
-                    # ::-1 to convert BlockManager ax to DataFrame ax
-                    if ax == self.bm_axis:
-                        # Suppress reindexing on concat axis
-                        continue
-
-                    # 1-ax to convert BlockManager axis to DataFrame axis
-                    obj_labels = obj.axes[1 - ax]
-                    if not new_labels.equals(obj_labels):
-                        indexers[ax] = obj_labels.get_indexer(new_labels)
-
-                mgrs_indexers.append((obj._mgr, indexers))
-
-            new_data = concatenate_managers(
-                mgrs_indexers, self.new_axes, concat_axis=self.bm_axis, copy=False
-            )
+            data = dict(enumerate(objs))
 
-            out = sample._constructor_from_mgr(new_data, axes=new_data.axes)
-            return out.__finalize__(self, method="concat")
+            # GH28330 Preserves subclassed objects through concat
+            cons = sample._constructor_expanddim
 
-    @cache_readonly
-    def new_axes(self) -> list[Index]:
-        if self._is_series and self.bm_axis == 1:
-            ndim = 2
-        else:
-            ndim = self.objs[0].ndim
-        return [
-            self._get_concat_axis
-            if i == self.bm_axis
-            else get_objs_combined_axis(
-                self.objs,
-                axis=self.objs[0]._get_block_manager_axis(i),
-                intersect=self.intersect,
-                sort=self.sort,
+            index = get_objs_combined_axis(
+                objs,
+                axis=objs[0]._get_block_manager_axis(0),
+                intersect=intersect,
+                sort=sort,
             )
-            for i in range(ndim)
-        ]
-
-    @cache_readonly
-    def _get_concat_axis(self) -> Index:
-        """
-        Return index to be used along concatenation axis.
-        """
-        if self._is_series:
-            if self.bm_axis == 0:
-                indexes = [x.index for x in self.objs]
-            elif self.ignore_index:
-                idx = default_index(len(self.objs))
-                return idx
-            elif self.keys is None:
-                names: list[Hashable] = [None] * len(self.objs)
-                num = 0
-                has_names = False
-                for i, x in enumerate(self.objs):
-                    if x.ndim != 1:
-                        raise TypeError(
-                            f"Cannot concatenate type 'Series' with "
-                            f"object of type '{type(x).__name__}'"
-                        )
-                    if x.name is not None:
-                        names[i] = x.name
-                        has_names = True
-                    else:
-                        names[i] = num
-                        num += 1
-                if has_names:
-                    return Index(names)
-                else:
-                    return default_index(len(self.objs))
-            else:
-                return ensure_index(self.keys).set_names(self.names)
-        else:
-            indexes = [x.axes[self.axis] for x in self.objs]
+            columns = _get_concat_axis_series(
+                objs, ignore_index, bm_axis, keys, levels, verify_integrity, names
+            )
+            df = cons(data, index=index, copy=False)
+            df.columns = columns
+            return df.__finalize__(object(), method="concat", objs=objs)
+
+    # combine block managers
+    else:
+        sample = cast("DataFrame", objs[0])
+
+        mgrs_indexers = []
+        result_axes = new_axes(
+            objs,
+            bm_axis,
+            intersect,
+            sort,
+            keys,
+            names,
+            axis,
+            levels,
+            verify_integrity,
+            ignore_index,
+        )
+        for obj in objs:
+            indexers = {}
+            for ax, new_labels in enumerate(result_axes):
+                # ::-1 to convert BlockManager ax to DataFrame ax
+                if ax == bm_axis:
+                    # Suppress reindexing on concat axis
+                    continue
+
+                # 1-ax to convert BlockManager axis to DataFrame axis
+                obj_labels = obj.axes[1 - ax]
+                if not new_labels.equals(obj_labels):
+                    indexers[ax] = obj_labels.get_indexer(new_labels)
+
+            mgrs_indexers.append((obj._mgr, indexers))
+
+        new_data = concatenate_managers(
+            mgrs_indexers, result_axes, concat_axis=bm_axis, copy=False
+        )
+
+        out = sample._constructor_from_mgr(new_data, axes=new_data.axes)
+        return out.__finalize__(object(), method="concat", objs=objs)
 
-        if self.ignore_index:
-            idx = default_index(sum(len(i) for i in indexes))
-            return idx
 
-        if self.keys is None:
-            if self.levels is not None:
+def new_axes(
+    objs: list[Series | DataFrame],
+    bm_axis: AxisInt,
+    intersect: bool,
+    sort: bool,
+    keys: Iterable[Hashable] | None,
+    names: list[HashableT] | None,
+    axis: AxisInt,
+    levels,
+    verify_integrity: bool,
+    ignore_index: bool,
+) -> list[Index]:
+    """Return the new [index, column] result for concat."""
+    return [
+        _get_concat_axis_dataframe(
+            objs,
+            axis,
+            ignore_index,
+            keys,
+            names,
+            levels,
+            verify_integrity,
+        )
+        if i == bm_axis
+        else get_objs_combined_axis(
+            objs,
+            axis=objs[0]._get_block_manager_axis(i),
+            intersect=intersect,
+            sort=sort,
+        )
+        for i in range(2)
+    ]
+
+
+def _get_concat_axis_series(
+    objs: list[Series | DataFrame],
+    ignore_index: bool,
+    bm_axis: AxisInt,
+    keys: Iterable[Hashable] | None,
+    levels,
+    verify_integrity: bool,
+    names: list[HashableT] | None,
+) -> Index:
+    """Return result concat axis when concatenating Series objects."""
+    if ignore_index:
+        return default_index(len(objs))
+    elif bm_axis == 0:
+        indexes = [x.index for x in objs]
+        if keys is None:
+            if levels is not None:
                 raise ValueError("levels supported only when keys is not None")
             concat_axis = _concat_indexes(indexes)
         else:
-            concat_axis = _make_concat_multiindex(
-                indexes, self.keys, self.levels, self.names
-            )
+            concat_axis = _make_concat_multiindex(indexes, keys, levels, names)
+        if verify_integrity and not concat_axis.is_unique:
+            overlap = concat_axis[concat_axis.duplicated()].unique()
+            raise ValueError(f"Indexes have overlapping values: {overlap}")
+        return concat_axis
+    elif keys is None:
+        result_names: list[Hashable] = [None] * len(objs)
+        num = 0
+        has_names = False
+        for i, x in enumerate(objs):
+            if x.ndim != 1:
+                raise TypeError(
+                    f"Cannot concatenate type 'Series' with "
+                    f"object of type '{type(x).__name__}'"
+                )
+            if x.name is not None:
+                result_names[i] = x.name
+                has_names = True
+            else:
+                result_names[i] = num
+                num += 1
+        if has_names:
+            return Index(result_names)
+        else:
+            return default_index(len(objs))
+    else:
+        return ensure_index(keys).set_names(names)  # type: ignore[arg-type]
 
-        if self.verify_integrity:
-            if not concat_axis.is_unique:
-                overlap = concat_axis[concat_axis.duplicated()].unique()
-                raise ValueError(f"Indexes have overlapping values: {overlap}")
 
-        return concat_axis
+def _get_concat_axis_dataframe(
+    objs: list[Series | DataFrame],
+    axis: AxisInt,
+    ignore_index: bool,
+    keys: Iterable[Hashable] | None,
+    names: list[HashableT] | None,
+    levels,
+    verify_integrity: bool,
+) -> Index:
+    """Return result concat axis when concatenating DataFrame objects."""
+    indexes_gen = (x.axes[axis] for x in objs)
+
+    if ignore_index:
+        return default_index(sum(len(i) for i in indexes_gen))
+    else:
+        indexes = list(indexes_gen)
+
+    if keys is None:
+        if levels is not None:
+            raise ValueError("levels supported only when keys is not None")
+        concat_axis = _concat_indexes(indexes)
+    else:
+        concat_axis = _make_concat_multiindex(indexes, keys, levels, names)
+
+    if verify_integrity and not concat_axis.is_unique:
+        overlap = concat_axis[concat_axis.duplicated()].unique()
+        raise ValueError(f"Indexes have overlapping values: {overlap}")
+
+    return concat_axis
 
 
 def _clean_keys_and_objs(
@@ -680,7 +719,7 @@ def _clean_keys_and_objs(
     Returns
     -------
     clean_objs : list[Series | DataFrame]
-        LIst of DataFrame and Series with Nones removed.
+        List of DataFrame and Series with Nones removed.
     keys : Index | None
         None if keys was None
         Index if objs was a Mapping or keys was not None. Filtered where objs was None.
@@ -690,28 +729,33 @@ def _clean_keys_and_objs(
     if isinstance(objs, abc.Mapping):
         if keys is None:
             keys = objs.keys()
-        objs_list = [objs[k] for k in keys]
-    else:
-        objs_list = list(objs)
+        objs = [objs[k] for k in keys]
+    elif isinstance(objs, (ABCSeries, ABCDataFrame)) or is_scalar(objs):
+        raise TypeError(
+            "first argument must be an iterable of pandas "
+            f'objects, you passed an object of type "{type(objs).__name__}"'
+        )
+    elif not isinstance(objs, abc.Sized):
+        objs = list(objs)
 
-    if len(objs_list) == 0:
+    if len(objs) == 0:
         raise ValueError("No objects to concatenate")
 
     if keys is not None:
         if not isinstance(keys, Index):
             keys = Index(keys)
-        if len(keys) != len(objs_list):
+        if len(keys) != len(objs):
             # GH#43485
             raise ValueError(
                 f"The length of the keys ({len(keys)}) must match "
-                f"the length of the objects to concatenate ({len(objs_list)})"
+                f"the length of the objects to concatenate ({len(objs)})"
             )
 
     # GH#1649
     key_indices = []
     clean_objs = []
     ndims = set()
-    for i, obj in enumerate(objs_list):
+    for i, obj in enumerate(objs):
         if obj is None:
             continue
         elif isinstance(obj, (ABCSeries, ABCDataFrame)):
```

## `test_patch` -- the developer's tests (held out)

```diff
diff --git a/pandas/tests/generic/test_frame.py b/pandas/tests/generic/test_frame.py
index 1d0f491529b56db96b4fa4fc435cc83b8c9bbc9b..d06bfad930d7cf88303a6b82deaa3a2418172295 100644
--- a/pandas/tests/generic/test_frame.py
+++ b/pandas/tests/generic/test_frame.py
@@ -84,8 +84,9 @@ class TestDataFrame:
                     value = getattr(left, name, "") + "|" + getattr(right, name, "")
                     object.__setattr__(self, name, value)
                 elif method == "concat":
+                    objs = kwargs["objs"]
                     value = "+".join(
-                        [getattr(o, name) for o in other.objs if getattr(o, name, None)]
+                        [getattr(o, name) for o in objs if getattr(o, name, None)]
                     )
                     object.__setattr__(self, name, value)
                 else:
diff --git a/pandas/tests/generic/test_series.py b/pandas/tests/generic/test_series.py
index 7dcdcd96cce5168d7be6c13cc287a5ede4d3841c..9e2dae8d132eb5f817638c2467e9555778613daa 100644
--- a/pandas/tests/generic/test_series.py
+++ b/pandas/tests/generic/test_series.py
@@ -94,12 +94,9 @@ class TestSeries:
         def finalize(self, other, method=None, **kwargs):
             for name in self._metadata:
                 if method == "concat" and name == "filename":
+                    objs = kwargs["objs"]
                     value = "+".join(
-                        [
-                            getattr(obj, name)
-                            for obj in other.objs
-                            if getattr(obj, name, None)
-                        ]
+                        [getattr(obj, name) for obj in objs if getattr(obj, name, None)]
                     )
                     object.__setattr__(self, name, value)
                 else:
```

## Validation

```json
{
 "image_head": "039edee0bc1a729ee9b67a6f9a337f7cd03118d1",
 "patch_applies": true,
 "test_files": [
  "pandas/tests/generic/test_frame.py",
  "pandas/tests/generic/test_series.py"
 ],
 "collected_before": 31,
 "collected_after": 31,
 "outcomes_before": {
  "PASSED": 29,
  "FAILED": 2
 },
 "outcomes_after": {
  "PASSED": 31
 },
 "exit_before": 1,
 "exit_after": 0,
 "tail_before": "s_name]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_raises\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_get_bool_data_preserve_dtype\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[nan]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[data1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[True]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[False]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[a]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0.0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv_resample\nFAILED pandas/tests/generic/test_frame.py::TestDataFrame::test_metadata_propagation_indiv\nFAILED pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv\n========================= 2 failed, 29 passed in 0.77s =========================",
 "tail_after": "is]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_mi[_set_axis_name]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_set_axis_name_raises\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_get_bool_data_preserve_dtype\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[nan]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[data1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[True]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_single_element_raise_1[False]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonzero_multiple_element_raise[data1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[1]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[a]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_nonbool_single_element_raise[0.0]\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv_resample\nPASSED pandas/tests/generic/test_series.py::TestSeries::test_metadata_propagation_indiv\n============================== 31 passed in 0.10s ==============================",
 "runner": "python -m pytest -v -rA -p no:cacheprovider --tb=short --color=no"
}
```
