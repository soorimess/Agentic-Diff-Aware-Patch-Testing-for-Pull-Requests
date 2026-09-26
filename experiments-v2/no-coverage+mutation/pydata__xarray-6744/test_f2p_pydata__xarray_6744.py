"""
Regression test for the bug where the "center" kwarg is ignored 
when manually iterating over DataArrayRolling objects.
"""
import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration_consistency():
    """Test that manual iteration over rolling windows produces same results as .mean() for center=True."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=True
    # Using .mean() method
    mean_result = my_data.rolling(x=3, center=True).mean().values
    
    # Using manual iteration
    manual_result = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=True)]
    
    # They should be equal
    np.testing.assert_array_equal(mean_result, manual_result)


def test_rolling_center_iteration_consistency_with_nan():
    """Test that manual iteration properly handles NaN values for center=True."""
    # Create test data with some NaN values
    data = np.array([1., 2., np.nan, 4., 5., 6., 7., 8., 9.])
    my_data = xr.DataArray(data, dims="x")
    
    # Test with center=True
    mean_result = my_data.rolling(x=3, center=True).mean().values
    
    # Using manual iteration
    manual_result = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=True)]
    
    # They should be equal
    np.testing.assert_array_equal(mean_result, manual_result)


def test_rolling_non_center_iteration_consistency():
    """Test that manual iteration over rolling windows works correctly for center=False."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=False
    mean_result = my_data.rolling(x=3, center=False).mean().values
    
    # Using manual iteration
    manual_result = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=False)]
    
    # They should be equal (this was already working)
    np.testing.assert_array_equal(mean_result, manual_result)