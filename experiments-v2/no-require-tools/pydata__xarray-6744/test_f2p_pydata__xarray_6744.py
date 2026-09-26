import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over DataArrayRolling respects center=True."""
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Option 1: take a center-justified rolling average (this should work correctly)
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Option 2: manually iterate over the rolling object
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equivalent - the bug was that they weren't
    np.testing.assert_array_equal(result1, result2)