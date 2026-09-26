import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration():
    """Test that manual iteration over rolling windows respects center=True parameter."""
    # Create test data as described in the bug report
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test the expected behavior with center=True
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Expected result from the bug report
    expected_centered = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    
    # Manual iteration should produce the same result
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # Convert to numpy array for comparison
    result2_array = np.array(result2)
    
    # These should be equal - the bug was that they weren't
    np.testing.assert_array_equal(result1, result2_array)
    
    # Also test that non-centered iteration behaves differently
    result3 = my_data.rolling(x=3, center=False).mean().values
    result4 = [window.mean().values.item() for label, window in my_data.rolling(x=3, center=False)]
    result4_array = np.array(result4)
    
    # Non-centered should be different from centered
    assert not np.array_equal(result3, result2_array)
    
    # Non-centered manual iteration should match non-centered mean
    np.testing.assert_array_equal(result3, result4_array)