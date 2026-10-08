import numpy as np
import pytest

import xarray as xr


def test_merge_dataarray_into_dataset():
    """Test that merging a DataArray into a Dataset works correctly."""
    # Create test data
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # This should work - using the top-level merge function
    expected = xr.merge([ds, da])
    
    # This should also work but currently fails in the buggy version
    actual = ds.merge(da)
    
    # The results should be identical
    xr.testing.assert_identical(expected, actual)


def test_merge_dataarray_into_dataset_with_compat():
    """Test that merging a DataArray into a Dataset with compat parameter works."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # Test with different compat options
    expected = xr.merge([ds, da], compat='no_conflicts')
    actual = ds.merge(da, compat='no_conflicts')
    
    xr.testing.assert_identical(expected, actual)


def test_merge_dataarray_into_dataset_with_join():
    """Test that merging a DataArray into a Dataset with join parameter works."""
    ds = xr.Dataset({'a': 0})
    da = xr.DataArray(1, name='b')
    
    # Test with different join options
    expected = xr.merge([ds, da], join='outer')
    actual = ds.merge(da, join='outer')
    
    xr.testing.assert_identical(expected, actual)