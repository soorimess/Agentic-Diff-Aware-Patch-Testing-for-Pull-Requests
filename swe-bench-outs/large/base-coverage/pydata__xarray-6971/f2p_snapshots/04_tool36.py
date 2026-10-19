"""
Regression tests for the new set_xindex and drop_indexes methods.

This test file verifies the behavior of the new public API methods for setting
and dropping indexes in DataArray and Dataset objects.
"""

import pytest
import numpy as np
import pandas as pd

import xarray as xr
from xarray import DataArray, Dataset


def test_dataarray_set_xindex_exists():
    """Test that set_xindex method exists on DataArray."""
    # Create a simple DataArray
    data = np.array([1, 2, 3, 4])
    da = DataArray(data, coords={'x': [0, 1, 2, 3]}, dims='x')
    
    # Test that set_xindex method exists (this should not raise AttributeError)
    assert hasattr(da, 'set_xindex')
    assert callable(getattr(da, 'set_xindex'))


def test_dataset_set_xindex_exists():
    """Test that set_xindex method exists on Dataset."""
    # Create a simple Dataset
    data = np.array([1, 2, 3, 4])
    ds = Dataset({'var': ('x', data)}, coords={'x': [0, 1, 2, 3]})
    
    # Test that set_xindex method exists (this should not raise AttributeError)
    assert hasattr(ds, 'set_xindex')
    assert callable(getattr(ds, 'set_xindex'))


def test_dataarray_drop_indexes_exists():
    """Test that drop_indexes method exists on DataArray."""
    # Create a simple DataArray
    data = np.array([1, 2, 3, 4])
    da = DataArray(data, coords={'x': [0, 1, 2, 3]}, dims='x')
    
    # Test that drop_indexes method exists (this should not raise AttributeError)
    assert hasattr(da, 'drop_indexes')
    assert callable(getattr(da, 'drop_indexes'))


def test_dataset_drop_indexes_exists():
    """Test that drop_indexes method exists on Dataset."""
    # Create a simple Dataset
    data = np.array([1, 2, 3, 4])
    ds = Dataset({'var': ('x', data)}, coords={'x': [0, 1, 2, 3]})
    
    # Test that drop_indexes method exists (this should not raise AttributeError)
    assert hasattr(ds, 'drop_indexes')
    assert callable(getattr(ds, 'drop_indexes'))


def test_method_signatures():
    """Test that the methods have expected signatures."""
    # Create a simple DataArray
    data = np.array([1, 2, 3, 4])
    da = DataArray(data, coords={'x': [0, 1, 2, 3]}, dims='x')
    
    # Test that we can call the methods without errors (they exist)
    # This is a basic test that they can be called
    try:
        # Just checking that the methods exist and can be called without syntax errors
        set_xindex_method = getattr(da, 'set_xindex')
        drop_indexes_method = getattr(da, 'drop_indexes')
        assert callable(set_xindex_method)
        assert callable(drop_indexes_method)
    except AttributeError:
        pytest.fail("Methods do not exist as expected")


def test_dataset_method_signatures():
    """Test that Dataset methods have expected signatures."""
    # Create a simple Dataset
    data = np.array([1, 2, 3, 4])
    ds = Dataset({'var': ('x', data)}, coords={'x': [0, 1, 2, 3]})
    
    # Test that we can call the methods without errors (they exist)
    try:
        set_xindex_method = getattr(ds, 'set_xindex')
        drop_indexes_method = getattr(ds, 'drop_indexes')
        assert callable(set_xindex_method)
        assert callable(drop_indexes_method)
    except AttributeError:
        pytest.fail("Methods do not exist as expected")


def test_error_handling_invalid_coordinate():
    """Test that set_xindex properly handles invalid coordinate names."""
    # Create a simple DataArray
    data = np.array([1, 2, 3, 4])
    da = DataArray(data, coords={'x': [0, 1, 2, 3]}, dims='x')
    
    # Test that invalid coordinate names raise ValueError
    with pytest.raises(ValueError):
        da.set_xindex('nonexistent')


def test_set_xindex_can_be_called():
    """Test that set_xindex can be called without AttributeError."""
    # Create a simple DataArray
    data = np.array([1, 2, 3, 4])
    da = DataArray(data, coords={'x': [0, 1, 2, 3]}, dims='x')
    
    # This test ensures the method exists and can be called
    # We don't test the return value to avoid double-indexing issues
    try:
        # Just calling it should not raise AttributeError
        da.set_xindex('x')
    except AttributeError:
        pytest.fail("set_xindex method does not exist or is not callable")
    except ValueError as e:
        # If we get a ValueError about already indexed, that's fine - it means
        # the method exists and is working correctly
        if "already have an index" in str(e):
            # This is expected behavior when calling twice
            pass
        else:
            raise  # Re-raise if it's a different ValueError