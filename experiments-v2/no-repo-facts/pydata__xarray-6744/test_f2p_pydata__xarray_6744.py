"""
Regression test for the bug where the "center" kwarg is ignored 
when manually iterating over DataArrayRolling.

This test verifies that when using center=True in rolling windows,
manual iteration produces the same results as the .mean() method.
"""

import numpy as np
import xarray as xr


def test_center_kwarg_ignored_in_manual_iteration():
    """Test that center kwarg is respected in manual iteration over DataArrayRolling."""
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Option 1: take a center-justified rolling average using .mean()
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Expected result from bug report:
    # array([nan,  2.,  3.,  4.,  5.,  6.,  7.,  8., nan])
    
    # Option 2: try to manually iterate, but the result should be equivalent
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal when the bug is fixed
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # The bug manifests as result2 being:
    # [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # instead of the expected [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    
    print(f"Expected result: {expected}")
    print(f"Result from .mean(): {result1}")
    print(f"Result from manual iteration: {result2}")
    
    # Check that both methods produce the same result
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)


def test_center_false_works():
    """Test that center=False works correctly (should not be affected by the bug)."""
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test with center=False
    result1 = my_data.rolling(x=3, center=False).mean().values
    my_data_rolling = my_data.rolling(x=3, center=False)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal
    expected = np.array([np.nan, np.nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    
    print(f"Expected result (center=False): {expected}")
    print(f"Result from .mean() (center=False): {result1}")
    print(f"Result from manual iteration (center=False): {result2}")
    
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)


if __name__ == "__main__":
    test_center_kwarg_ignored_in_manual_iteration()
    test_center_false_works()
    print("All tests passed!")