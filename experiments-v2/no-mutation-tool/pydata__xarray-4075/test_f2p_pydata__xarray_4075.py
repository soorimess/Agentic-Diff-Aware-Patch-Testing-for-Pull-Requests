import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that boolean weights are properly handled in weighted mean operations.
    
    When boolean weights are passed to weighted mean, they should be converted
    to integers to ensure proper calculation of sum of weights.
    """
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    # Use bool instead of np.bool for modern compatibility
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0 (the mean of valid data points)
    # But due to the bug, it returns 2.0 because boolean dot product
    # of [True, True, True] and [True, True, False] gives True
    # instead of 2 (the count of True values)
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0, not 2.0
    expected = xr.DataArray(1.0)
    xr.testing.assert_allclose(result, expected)


def test_weighted_sum_of_weights_boolean_weights():
    """Test that boolean weights are properly handled in sum_of_weights operations."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    # Use bool instead of np.bool for modern compatibility
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 2.0 (sum of valid weights)
    # But due to the bug, it returns 1.0 because boolean dot product
    # of [True, True, True] and [True, True, False] gives True
    # instead of 2 (the count of True values)
    result = dta.weighted(wgt).sum_of_weights()
    
    # The correct result should be 2.0, not 1.0
    expected = xr.DataArray(2.0)
    xr.testing.assert_allclose(result, expected)


def test_weighted_sum_boolean_weights():
    """Test that boolean weights are properly handled in weighted sum operations."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    # Use bool instead of np.bool for modern compatibility
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 2.0 (sum of valid data points weighted by weights)
    # But due to the bug, it would return a wrong value
    result = dta.weighted(wgt).sum()
    
    # The correct result should be 2.0 (1*1 + 1*1 + 1*0 = 2)
    expected = xr.DataArray(2.0)
    xr.testing.assert_allclose(result, expected)