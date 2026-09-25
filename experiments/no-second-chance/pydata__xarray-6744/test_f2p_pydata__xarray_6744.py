"""
Regression test for manual iteration of DataArrayRolling with center=True.

This test specifically validates that when manually iterating over a 
DataArrayRolling object with center=True, the behavior matches that of 
calling methods directly (like .mean()).

Before the bug fix, manual iteration would not respect the center parameter,
leading to misaligned sliding windows.
"""

import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration_respects_center_parameter():
    """
    Test that manual iteration over rolling object with center=True matches
    direct method calls.
    
    The bug was that manual iteration with center=True produced incorrect
    results compared to direct method application.
    """
    # Reproduce exact test case from bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Direct method application (this worked correctly)
    direct_result = my_data.rolling(x=3, center=True).mean().values
    
    # Manual iteration (this was broken before fix) 
    manual_result = [window.mean().values.item() 
                     for label, window in my_data.rolling(x=3, center=True)]
    
    # Direct approach should produce: [nan, 2., 3., 4., 5., 6., 7., 8., nan]
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # The bug: manual iteration had first valid value at index 2 instead of index 1
    # In the buggy version: manual_result = [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # In the fixed version:  manual_result = [nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, nan]
    
    # Check that direct and manual results are equivalent  
    np.testing.assert_allclose(direct_result, manual_result, equal_nan=True)
    
    # Specific assertion about the key bug: when center=True, first valid element 
    # should be 2.0 (not NaN), because [1,2,3] centered at position 1 should give mean=2
    assert not np.isnan(manual_result[1]), (
        "With center=True and window=3, manual iteration should produce 2.0 at index 1, "
        "not NaN. The center parameter was being ignored in manual iteration."
    )
    
    assert manual_result[1] == 2.0, (
        "Expected center-justified window to produce mean of 2.0 at index 1, "
        "but got {}".format(manual_result[1])
    )

    
def test_rolling_center_iteration_window_alignment():
    """
    Additional test to verify window alignment is correct with center=True.
    
    With center=True, window size=3 on data [1,2,3,4,5,6,7,8,9]:
    - At position 1: window [1,2,3] should yield mean 2.0 (centered correctly)
    - At position 2: window [1,2,3] should yield mean 2.0 (centered correctly) 
    - etc.
    """
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Get both results 
    direct_result = my_data.rolling(x=3, center=True).mean().values
    manual_result = [window.mean().values.item() 
                     for label, window in my_data.rolling(x=3, center=True)]
    
    # Validate they match exactly - if they don't, the center parameter wasn't respected
    for i, (direct, manual) in enumerate(zip(direct_result, manual_result)):
        if np.isnan(direct):
            assert np.isnan(manual), f"Position {i}: Direct is NaN but manual is {manual}"
        else:
            assert abs(direct - manual) < 1e-10, f"Position {i}: direct={direct}, manual={manual}"