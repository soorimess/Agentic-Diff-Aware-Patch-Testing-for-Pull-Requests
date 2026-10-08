"""
Regression test for issue where Dataset.merge() fails with DataArray objects.

This test ensures that merging a Dataset and DataArray using the Dataset.merge()
method works correctly, matching the behavior of the top-level merge() function.
"""

import xarray as xr
import pytest


def test_dataset_merge_dataarray():
    """Test that Dataset.merge() works with DataArray objects."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work (Dataset.merge method) but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1


def test_dataset_merge_dataarray_with_attrs():
    """Test that Dataset.merge() works with DataArray objects that have attributes."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b', attrs={'units': 'm'})
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work (Dataset.merge method) but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 1
    assert actual['b'].attrs['units'] == 'm'


def test_dataset_merge_dataarray_multiple_vars():
    """Test that Dataset.merge() works with DataArray objects when dataset has multiple variables."""
    ds = xr.Dataset({'a': 0, 'c': [1, 2, 3]})
    da = xr.DataArray(10, name='b')
    
    # This should work (top-level merge function)
    expected = xr.merge([ds, da])
    
    # This should also work (Dataset.merge method) but currently fails
    actual = ds.merge(da)
    
    # Both should produce the same result
    assert actual.equals(expected)
    assert 'a' in actual
    assert 'b' in actual
    assert 'c' in actual
    assert actual['a'].values == 0
    assert actual['b'].values == 10
    assert list(actual['c'].values) == [1, 2, 3]