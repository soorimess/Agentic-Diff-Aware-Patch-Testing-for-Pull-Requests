"""
Test for regression of boolean weights issue in weighted mean.

This test verifies the fix for the bug where passing boolean weights 
to weighted mean returns wrong results.
"""

import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights."""
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # This should return 1.0, not 2.0
    result = dta.weighted(wgt).mean()
    
    # Before fix: result would be 2.0 (incorrect)
    # After fix: result should be 1.0 (correct)
    expected = 1.0
    
    assert result.values == expected


def test_weighted_mean_boolean_weights_different_values():
    """Test weighted mean with different data values and boolean weights."""
    # Test with different data values
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray(np.array([1, 0, 1], dtype=np.bool))  # Only first and third values count
    
    result = dta.weighted(wgt).mean()
    # Should be (2*1 + 6*1) / (1 + 1) = 8/2 = 4.0
    expected = 4.0
    
    assert result.values == expected


def test_weighted_mean_boolean_weights_all_false():
    """Test weighted mean with all false weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([False, False, False])  # All false weights
    
    # Should return NaN since no valid weights
    result = dta.weighted(wgt).mean()
    
    # This should be NaN because no valid data points
    assert np.isnan(result.values)


def test_weighted_mean_boolean_weights_all_true():
    """Test weighted mean with all true weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])  # All true weights
    
    result = dta.weighted(wgt).mean()
    # Should be (1 + 2 + 3) / 3 = 2.0
    expected = 2.0
    
    assert result.values == expected


if __name__ == "__main__":
    # Run the tests when directly executed
    test_weighted_mean_boolean_weights()
    test_weighted_mean_boolean_weights_different_values()
    test_weighted_mean_boolean_weights_all_false()
    test_weighted_mean_boolean_weights_all_true()
    print("All tests passed!")