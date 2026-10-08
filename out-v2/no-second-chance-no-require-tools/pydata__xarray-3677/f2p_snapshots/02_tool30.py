"""
Regression test for issue where merging a Dataset and DataArray using 
Dataset.merge() method fails.

This test ensures that the fix for the bug where Dataset.merge() fails 
when passed a DataArray object is properly implemented.
"""

import xarray as xr


def test_merge_dataset_with_named_dataarray():
    """Test that merging a dataset with a named dataarray using the dataset method works."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work (dataset merge method) but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert expected.equals(actual)
    
    # Verify the result has the expected structure
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1