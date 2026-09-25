"""
Regression tests for bug where "center" kwarg is ignored when manually iterating over DataArrayRolling
Issue: https://github.com/pydata/xarray/discussions/6738
"""
import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration_consistency():
    """Test that manual iteration produces same results as direct rolling operations when center=True."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=True
    result_direct = my_data.rolling(x=3, center=True).mean()
    result_manual = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=True)]
    
    # Convert manual result to array for comparison  
    result_manual_array = np.array(result_manual)
    
    # The direct method should produce centered windows
    # Expected: [nan, 2., 3., 4., 5., 6., 7., 8., nan]  (centered windows)
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Before fix: manual iteration would give [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # After fix: both should give [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    np.testing.assert_allclose(result_direct.values, expected, equal_nan=True)
    np.testing.assert_allclose(result_manual_array, expected, equal_nan=True)


def test_rolling_center_iteration_edge_cases():
    """Test edge cases for center=True iteration."""
    # Small dataset
    data_small = xr.DataArray([1, 2, 3], dims="x")
    result_direct = data_small.rolling(x=3, center=True).mean()
    result_manual = [window.mean().values.item() for label, window in data_small.rolling(x=3, center=True)]
    result_manual_array = np.array(result_manual)
    
    # With small window size, should return [nan, 2., nan] 
    expected_small = np.array([np.nan, 2., np.nan])
    
    np.testing.assert_allclose(result_direct.values, expected_small, equal_nan=True)
    np.testing.assert_allclose(result_manual_array, expected_small, equal_nan=True)


def test_rolling_center_false_iteration():
    """Test that center=False works correctly (should not be affected by bug)."""
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=False
    result_direct = my_data.rolling(x=3, center=False).mean()
    result_manual = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=False)]
    result_manual_array = np.array(result_manual)
    
    # With center=False: windows start from left 
    # [1, 2, 3] -> 2.0, [2, 3, 4] -> 3.0, [3, 4, 5] -> 4.0, ...
    expected = np.array([np.nan, np.nan, 2., 3., 4., 5., 6., 7., 8.])
    
    np.testing.assert_allclose(result_direct.values, expected, equal_nan=True)
    np.testing.assert_allclose(result_manual_array, expected, equal_nan=True)