"""Test for the new set_xindex and drop_indexes methods."""

import xarray as xr
from xarray import DataArray, Dataset


def test_set_xindex_method_exists():
    """Test that set_xindex method exists and can be accessed without AttributeError."""
    # Create simple test objects
    data = [1, 2, 3, 4]
    coords = {"time": [0, 1, 2, 3]}
    da = DataArray(data, coords=coords, dims="time")
    
    # This should not raise AttributeError after the change
    # The test is that we can access the method without AttributeError
    method = da.set_xindex
    assert callable(method)


def test_drop_indexes_method_exists():
    """Test that drop_indexes method exists and can be accessed without AttributeError."""
    # Create simple test objects
    data = [1, 2, 3, 4]
    coords = {"time": [0, 1, 2, 3]}
    da = DataArray(data, coords=coords, dims="time")
    
    # This should not raise AttributeError after the change
    # The test is that we can access the method without AttributeError
    method = da.drop_indexes
    assert callable(method)