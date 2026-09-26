"""
Regression test for the bug where center kwarg is ignored when manually 
iterating over DataArrayRolling.

This test ensures that when using center=True in rolling operations,
manual iteration produces the same results as the direct method call.
"""

import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration with center=True produces center-justified windows."""
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Option 1: Direct method call with center=True
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: Manual iteration with center=True
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # The results should be equivalent
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Check that both approaches give the same result
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(np.array(result2), expected)


def test_rolling_center_vs_non_center_iteration():
    """Test that center and non-center iterations produce different, expected results."""
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Center-justified rolling mean
    center_result = my_data.rolling(x=3, center=True).mean().values
    
    # Non-center rolling mean
    non_center_result = my_data.rolling(x=3, center=False).mean().values
    
    # These should be different
    assert not np.array_equal(center_result, non_center_result)
    
    # Check specific expected values for center
    expected_center = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    np.testing.assert_array_equal(center_result, expected_center)
    
    # Check specific expected values for non-center
    expected_non_center = np.array([np.nan, np.nan, 2., 3., 4., 5., 6., 7., 8.])
    np.testing.assert_array_equal(non_center_result, expected_non_center)