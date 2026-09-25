import xarray as xr


def test_dataset_merge_accepts_dataarray_method():
    """Dataset.merge should accept a DataArray like xr.merge does.

    This pins down pydata/xarray#3677: Dataset.merge previously failed when
    passed a DataArray because it didn't coerce it to a Dataset first.
    """
    ds = xr.Dataset({"a": 0})
    da = xr.DataArray(1, name="b")

    expected = xr.merge([ds, da])
    assert isinstance(expected, xr.Dataset)

    actual = ds.merge(da)
    assert actual.identical(expected)
