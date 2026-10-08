"""
Regression test for issue where merging a Dataset and DataArray
using the Dataset's merge method fails.
"""
import xarray as xr


def test_dataset_merge_dataarray():
    """Test that merging a Dataset and DataArray using ds.merge() works."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work but was failing before the fix
    actual = ds.merge(da)
    
    # The results should be equivalent
    xr.testing.assert_identical(expected, actual)


def test_dataset_merge_dataarray_with_existing_var():
    """Test merging when dataset already has variables."""
    ds = xr.Dataset({'a': 0, 'c': [1, 2, 3]})
    da = xr.DataArray(5, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work but was failing before the fix
    actual = ds.merge(da)
    
    # The results should be equivalent
    xr.testing.assert_identical(expected, actual)