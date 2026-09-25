"""
Regression test for issue where "center" kwarg is ignored when manually 
iterating over DataArrayRolling objects.

This test ensures that when center=True is used in rolling windows,
manual iteration produces the same results as direct application of methods.
"""
import numpy as np
import xarray as xr


def test_rolling_center_iter():
    """Test that center=True works consistently between direct methods and manual iteration."""
    # Create test data matching exactly the issue report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")

    # Option 1: take a center-justified rolling average directly
    result1 = my_data.rolling(x=3, center=True).mean().values
    # Expected from the issue report: [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    
    # Option 2: try to manually iterate  
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    result2 = np.array(result2)
    
    # These should be equal - the bug was that manual iteration didn't return
    # center-aligned windows like direct method does
    np.testing.assert_array_equal(result1, result2)


def test_rolling_center_iter_different_window_sizes():
    """Test that the fix works with different window sizes."""
    # Test window size 3 (as in original issue)
    my_data = xr.DataArray(np.arange(1, 10), dims="x")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    result1 = my_data.rolling(x=3, center=True).mean().values
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    result2 = np.array(result2)
    
    np.testing.assert_array_equal(result1, result2)
    
    # Test window size 5
    result1 = my_data.rolling(x=5, center=True).mean().values
    my_data_rolling = my_data.rolling(x=5, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    result2 = np.array(result2)
    
    np.testing.assert_array_equal(result1, result2)


def test_rolling_center_iter_false():
    """Test that non-centered behavior still works correctly."""
    my_data = xr.DataArray(np.arange(1, 10), dims="x")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    
    # Test with center=False - this should work the same way for both
    result1 = my_data.rolling(x=3, center=False).mean().values
    my_data_rolling = my_data.rolling(x=3, center=False)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    result2 = np.array(result2)
    
    np.testing.assert_array_equal(result1, result2)