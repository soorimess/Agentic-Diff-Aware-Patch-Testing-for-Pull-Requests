import xarray as xr


def test_dataset_merge_accepts_dataarray():
    """Regression test for merging a Dataset with a DataArray using
    Dataset.merge. Previously, passing a DataArray to Dataset.merge
    raised AttributeError because DataArray lacks an `items` method.

    This test ensures ds.merge(da) returns the same result as
    xr.merge([ds, da]).
    """
    ds = xr.Dataset({"a": 0})
    da = xr.DataArray(1, name="b")

    expected = xr.merge([ds, da])
    actual = ds.merge(da)

    assert actual.identical(expected)
