import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that boolean weights are properly handled in weighted mean calculations.
    
    When boolean arrays are passed as weights, the sum_of_weights calculation
    was incorrectly treating boolean values as boolean instead of converting them
    to integers, leading to wrong results.
    """
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0 (the mean of all valid data points)
    # but without the fix it incorrectly returns 2.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0, not 2.0
    assert result.values == 1.0


def test_weighted_mean_boolean_weights_different_values():
    """Test boolean weights with different data values."""
    # Test with different data values
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray(np.array([True, True, False], dtype=bool))
    
    # Should compute weighted mean of [2, 4] with weights [1, 1] = 3.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 3.0
    assert result.values == 3.0


def test_weighted_mean_boolean_weights_all_true():
    """Test boolean weights where all values are True."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray(np.array([True, True, True], dtype=bool))
    
    # Should compute weighted mean of [1, 2, 3] with weights [1, 1, 1] = 2.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 2.0
    assert result.values == 2.0


def test_weighted_mean_boolean_weights_all_false():
    """Test boolean weights where all values are False."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray(np.array([False, False, False], dtype=bool))
    
    # Should return NaN since no valid weights
    result = dta.weighted(wgt).mean()
    
    # The result should be NaN
    assert np.isnan(result.values)