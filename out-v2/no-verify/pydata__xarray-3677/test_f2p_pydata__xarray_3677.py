"""
Regression test for issue where Dataset.merge() fails with DataArray inputs.

This test verifies that Dataset.merge() properly handles DataArray objects
by converting them to Dataset before merging, which was the fix applied
in the pull request.
"""

import xarray as xr
import pytest


def test_dataset_merge_dataarray():
    """Test that Dataset.merge() works with DataArray inputs."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work after the fix - using dataset method
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1


def test_dataset_merge_dataarray_with_coords():
    """Test that Dataset.merge() works with DataArray inputs that have coordinates."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray([1, 2, 3], dims='x', name='b')
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work after the fix - using dataset method
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert list(actual['b'].values) == [1, 2, 3]


def test_dataset_merge_dataarray_with_attrs():
    """Test that Dataset.merge() preserves attributes when merging with DataArray."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b', attrs={'units': 'm'})
    
    # This should work - using top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work after the fix - using dataset method
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1
    assert actual['b'].attrs['units'] == 'm'