import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration_matches_direct_method():
    """Test that manually iterating over DataArrayRolling with center=True 
    produces same results as using .mean() directly.
    
    This test is to catch the bug where the center kwarg was ignored 
    when manually iterating over DataArrayRolling objects.
    """
    # Reproduce the exact example from the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")

    # Option 1: take a center-justified rolling average (expected behavior)
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: try to manually iterate (this was broken before the fix)
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal according to the bug report - both should be:
    # [nan, 2., 3., 4., 5., 6., 7., 8., nan]  
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Both methods should produce identical results
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)