"""
Regression test for issue where merging a Dataset and DataArray
using the Dataset.merge() method fails.
"""
import xarray as xr


def test_merge_dataset_dataarray_method():
    """Test that Dataset.merge() works with DataArray objects."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    xr.testing.assert_identical(expected, actual)


def test_merge_dataset_dataarray_method_with_coords():
    """Test that Dataset.merge() works with DataArray objects that have coordinates."""
    # Create test data with coordinates
    ds = xr.Dataset({'a': [1, 2, 3]})
    da = xr.DataArray([4, 5, 6], dims=['x'], name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    xr.testing.assert_identical(expected, actual)