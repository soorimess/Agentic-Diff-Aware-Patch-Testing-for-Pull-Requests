"""
Regression test for bug where the "center" kwarg is ignored 
when manually iterating over DataArrayRolling.

The issue is that when using center=True with rolling windows,
manual iteration produces different results than the direct .mean() method.
"""
import numpy as np
import xarray as xr


def test_rolling_center_iteration_equivalence():
    """Test that manual iteration produces same results as direct method when center=True.
    
    This test catches the regression where center=True was ignored during manual iteration,
    ensuring that both approaches produce identical results.
    """
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Option 1: take a center-justified rolling average (direct method)
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: manually iterate over rolling object (was buggy)
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # Before fix: result1 = [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    #              result2 = [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # After fix: both should be [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    
    # The core behavior we're pinning down is that manual iteration
    # should produce exactly the same results as the direct method
    np.testing.assert_array_equal(result1, result2)