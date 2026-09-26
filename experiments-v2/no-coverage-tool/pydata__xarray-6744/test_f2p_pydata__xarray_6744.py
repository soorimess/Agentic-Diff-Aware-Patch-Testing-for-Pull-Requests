import numpy as np
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over DataArrayRolling with center=True produces same results as .mean()
    
    This test ensures that when manually iterating over a DataArrayRolling object with center=True,
    the results match what you get from calling .mean() directly, which was broken before the fix.
    """
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test the direct method (should work correctly)
    result_direct = my_data.rolling(x=3, center=True).mean().values
    
    # Test manual iteration (this was broken before the fix)
    my_data_rolling = my_data.rolling(x=3, center=True)
    result_iter = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal - the bug was that manual iteration didn't produce the same results
    np.testing.assert_array_equal(result_direct, result_iter)