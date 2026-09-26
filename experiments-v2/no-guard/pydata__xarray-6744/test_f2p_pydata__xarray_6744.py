import numpy as np
import pytest
import xarray as xr


def test_rolling_center_iteration():
    """Test that center parameter is respected when manually iterating over rolling objects."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test center=True behavior - should produce center-justified windows
    result1 = my_data.rolling(x=3, center=True).mean().values
    
    # Manual iteration should produce the same result
    my_data_rolling = my_data.rolling(x=3, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal
    expected = np.array([np.nan, 2., 3., 4., 5., 6., 7., 8., np.nan])
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)


def test_rolling_non_center_iteration():
    """Test that non-center behavior works correctly."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test center=False behavior - should produce left-aligned windows
    result1 = my_data.rolling(x=3, center=False).mean().values
    
    # Manual iteration should produce the same result
    my_data_rolling = my_data.rolling(x=3, center=False)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal
    expected = np.array([np.nan, np.nan, 2., 3., 4., 5., 6., 7., 8.])
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)


def test_rolling_center_iteration_odd_window():
    """Test center iteration with odd window size."""
    # Create test data
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # Test center=True with odd window size
    result1 = my_data.rolling(x=5, center=True).mean().values
    
    # Manual iteration should produce the same result
    my_data_rolling = my_data.rolling(x=5, center=True)
    result2 = [window.mean().values.item() for label, window in my_data_rolling]
    
    # These should be equal
    expected = np.array([np.nan, np.nan, 3., 4., 5., 6., 7., np.nan, np.nan])
    np.testing.assert_array_equal(result1, expected)
    np.testing.assert_array_equal(result2, expected)