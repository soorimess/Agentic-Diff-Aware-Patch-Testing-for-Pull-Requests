"""
Regression test for bug where "center" kwarg is ignored when manually iterating over DataArrayRolling.

This test checks that manual iteration over a DataArrayRolling object with center=True
produces the same results as the direct method call.
"""
import numpy as np
import pytest
import xarray as xr


def test_centered_rolling_manual_iteration():
    """Test that manual iteration over centered rolling windows produces same results as direct method."""
    # Create test data exactly matching the bug report example
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Direct approach (working correctly) - produces [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    result_direct = my_data.rolling(x=3, center=True).mean().values
    
    # Manual iteration (buggy in old code) - should also produce [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_manual = [window.mean().values.item() for label, window in my_data_rolling]
    
    print(f"Direct result:  {result_direct}")
    print(f"Manual result:  {result_manual}")
    
    # Key assertion: both should be identical
    # The bug was that manual iteration returned [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # instead of [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan]
    np.testing.assert_array_equal(result_direct, result_manual)


def test_non_centered_rolling_iteration():
    """Test that manual iteration without centering works correctly."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Method 1: Direct rolling.mean() with center=False (default)
    result1 = my_data.rolling(x=3, center=False).mean().values
    
    # Method 2: Manual iteration with center=False
    my_data_rolling = my_data.rolling(x=3, center=False)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # For center=False with window=3 on data [1,2,3,4,5,6,7,8,9],
    # the first window is [1,2,3], second is [2,3,4], etc.
    # Result should be: [nan, nan, 2., 3., 4., 5., 6., 7., 8.]
    assert np.isnan(result1[0]) and np.isnan(result2[0]), "First values should both be NaN"
    assert np.isnan(result1[1]) and np.isnan(result2[1]), "Second values should both be NaN"
    assert np.allclose(result1[2:], result2[2:], equal_nan=True), (
        "Non-centered rolling iteration should produce same results as direct method"
    )