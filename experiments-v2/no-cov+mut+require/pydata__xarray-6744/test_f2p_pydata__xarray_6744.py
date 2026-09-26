"""
Regression test for the bug where the "center" kwarg is ignored 
when manually iterating over DataArrayRolling.

This test verifies that manual iteration over a rolling object
with center=True produces the same results as using the .mean() method directly.
"""

import numpy as np
import xarray as xr


def test_rolling_center_iteration():
    """Test that center-justified rolling windows work correctly in manual iteration."""
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test 1: Using .mean() method directly - this should work correctly
    result_mean = my_data.rolling(x=3, center=True).mean()
    expected_values = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Verify the expected result from the bug report
    np.testing.assert_array_equal(result_mean.values, expected_values)
    
    # Test 2: Manual iteration - this was broken before the fix
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    
    # The manual iteration should produce the same results as .mean()
    # Before the fix, this would fail because manual iteration didn't respect center=True
    # After the fix, both should give [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    np.testing.assert_array_equal(result_mean.values, result_iter)


def test_rolling_center_iteration_with_nan():
    """Test rolling with center=True and NaN values."""
    # Create test data with NaN values
    data = np.array([1., 2., np.nan, 4., 5., 6., 7., 8., 9.])
    my_data = xr.DataArray(data, dims="x")
    
    # Test with center=True
    result_mean = my_data.rolling(x=3, center=True).mean()
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    
    # Both should give the same results
    np.testing.assert_array_equal(result_mean.values, result_iter)


def test_rolling_center_vs_non_center():
    """Test that center=True and center=False produce different results."""
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Center-justified
    result_center = my_data.rolling(x=3, center=True).mean()
    
    # Non-centered
    result_non_center = my_data.rolling(x=3, center=False).mean()
    
    # These should be different
    assert not np.array_equal(result_center.values, result_non_center.values)
    
    # Manual iteration should match the mean() for center=True
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    
    np.testing.assert_array_equal(result_center.values, result_iter)