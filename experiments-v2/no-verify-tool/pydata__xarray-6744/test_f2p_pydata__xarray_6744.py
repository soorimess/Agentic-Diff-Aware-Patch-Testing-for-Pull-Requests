import numpy as np
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over DataArrayRolling with center=True produces 
    same results as using the rolling.mean() method."""
    
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Option 1: Use the rolling.mean() method (expected behavior)
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: Manual iteration (this was broken before the fix)
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal but were not before the fix
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Before the fix, result2 would be [nan, nan, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    # After the fix, result2 should match result1
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)