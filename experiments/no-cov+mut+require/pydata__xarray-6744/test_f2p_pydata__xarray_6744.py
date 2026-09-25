"""
Regression test for center kwarg issue in DataArrayRolling iteration.

The bug: When manually iterating over a DataArrayRolling object with center=True,
the iteration ignores the center parameter and produces left-aligned windows
instead of center-aligned windows.

This test ensures that after the fix, manual iteration produces the same
results as the direct .mean() method when center=True.
"""
import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration_matches_direct_method():
    """
    Test that manual iteration over DataArrayRolling with center=True 
    produces the same results as the direct .mean() method.
    
    This test verifies that the fix for the center parameter being ignored
    during manual iteration is working correctly.
    """
    # Reproduce the exact example from the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Direct method with center=True - should be center-justified
    result_direct = my_data.rolling(x=3, center=True).mean()
    expected_centered = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Manual iteration - should now produce same result after fix
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    result_iter_array = np.array(result_iter)
    
    # Both methods should produce identical results when center=True
    # This assertion passes after fix, fails before fix
    np.testing.assert_array_equal(result_direct.values, expected_centered)
    np.testing.assert_array_equal(result_iter_array, expected_centered)
    
    # Double check that the values are correct for the example
    # Direct result should be: [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    # Manual iteration should match exactly after fix
    assert np.isnan(result_direct.values[0])
    assert result_direct.values[1] == 2.0
    assert result_direct.values[2] == 3.0
    assert result_direct.values[3] == 4.0
    assert result_direct.values[4] == 5.0
    assert result_direct.values[5] == 6.0
    assert result_direct.values[6] == 7.0
    assert result_direct.values[7] == 8.0
    assert np.isnan(result_direct.values[8])