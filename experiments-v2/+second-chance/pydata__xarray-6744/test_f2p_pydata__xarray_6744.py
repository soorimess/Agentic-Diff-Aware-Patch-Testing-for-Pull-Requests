import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over DataArrayRolling with center=True produces 
    center-justified windows, matching the behavior of the .mean() method.
    
    This is a regression test for the bug where the "center" kwarg was ignored
    when manually iterating over DataArrayRolling objects.
    """
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=True
    rolling_obj = my_data.rolling(x=3, center=True)
    
    # Method 1: Using .mean() method (expected behavior)
    result_mean = rolling_obj.mean().values
    
    # Method 2: Manual iteration (this was broken before the fix)
    result_iter = [window.mean().values.item() for label, window in rolling_obj]
    
    # The results should be identical
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Check that both methods produce the same result
    np.testing.assert_array_equal(result_mean, expected)
    np.testing.assert_array_equal(result_iter, expected)


def test_rolling_center_iteration_edge_cases():
    """Test edge cases for rolling window iteration with center=True"""
    # Test with different window sizes
    data = xr.DataArray(np.arange(1, 11), dims="x")
    
    # Odd window size
    rolling_odd = data.rolling(x=3, center=True)
    result_odd = [window.mean().values.item() for label, window in rolling_odd]
    expected_odd = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., 9., np.nan])
    np.testing.assert_array_equal(result_odd, expected_odd)
    
    # Even window size
    rolling_even = data.rolling(x=4, center=True)
    result_even = [window.mean().values.item() for label, window in rolling_even]
    expected_even = np.array([np.nan, np.nan, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, np.nan])
    np.testing.assert_array_equal(result_even, expected_even)


def test_rolling_non_center_iteration():
    """Test that non-centered rolling still works correctly"""
    data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=False (default)
    rolling_obj = data.rolling(x=3, center=False)
    result_mean = rolling_obj.mean().values
    result_iter = [window.mean().values.item() for label, window in rolling_obj]
    
    # These should be different from centered results
    expected = np.array([np.nan, np.nan, 2., 3., 4., 5., 6., 7., 8.])
    
    np.testing.assert_array_equal(result_mean, expected)
    np.testing.assert_array_equal(result_iter, expected)