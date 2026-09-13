import xarray as xr

from . import assert_identical


def test_dataset_merge_method_accepts_dataarray():
    """Dataset.merge should accept a DataArray and behave like xr.merge.

    Regression test for GH#3677: ds.merge(da) used to raise AttributeError
    because the method did not coerce DataArray to Dataset before merging.
    """
    ds = xr.Dataset({"a": 0})
    da = xr.DataArray(1, name="b")

    expected = xr.merge([ds, da])
    actual = ds.merge(da)

    assert_identical(expected, actual)
