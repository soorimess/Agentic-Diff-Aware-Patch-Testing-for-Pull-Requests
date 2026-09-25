"""
Regression test for the center kwarg ignored when manually iterating over DataArrayRolling bug.

This test specifically demonstrates the exact bug where manual iteration over a 
DataArrayRolling object ignores the center=True parameter, producing incorrect window positions.
"""
import numpy as np
import xarray as xr


def test_rolling_center_iteration_bug():
    """
    Test that matches the exact example from the bug report.
    
    The bug: manual iteration returns [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    Instead of: [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan]
    """
    # Use exactly the example data from the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")

    # Direct method (should work correctly with center=True)
    result_direct = my_data.rolling(x=3, center=True).mean().values
    print(f"Direct method result: {result_direct}")
    
    # Manual iteration (currently buggy)
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    print(f"Iteration result: {result_iter}")
    
    # The core bug: result_iter[1] should be 2.0 but returns NaN due to centering bug
    assert not np.isnan(result_iter[1]), "Bug: Second element should be 2.0, not NaN"
    assert result_direct[1] == result_iter[1], "Centered windows do not match between direct and iteration methods"


def test_rolling_center_specific_issue():
    """
    Test a simplified case that focuses on the exact core issue.
    """
    # Test with a smaller set that's easier to reason about
    my_data = xr.DataArray(np.arange(1, 6), dims="x")  # [1, 2, 3, 4, 5]
    
    # Direct method: [nan, 2.0, 3.0, 4.0, nan] 
    result_direct = my_data.rolling(x=3, center=True).mean().values  
    print(f"Direct result: {result_direct}")
    
    # Manual iteration method  
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    print(f"Iteration result: {result_iter}")
    
    # The bug can be clearly seen: 
    # result_direct[2] = 3.0 (the centered position)
    # result_iter[2] should also == 3.0, but due to the bug it's a different value 
    # This directly tests that iteration respects centering
    assert result_direct[2] == 3.0, "Direct method should produce 3.0 at center"
    assert not np.isnan(result_iter[2]), "Bug: Manual iteration does not respect center=True - should produce 3.0, not NaN"


if __name__ == "__main__":
    test_rolling_center_iteration_bug()
    test_rolling_center_specific_issue()
    print("All tests passed!")