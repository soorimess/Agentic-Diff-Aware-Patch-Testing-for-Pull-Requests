import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that boolean weights are properly handled in weighted mean calculation.
    
    When boolean weights are passed to weighted.mean(), they should be converted
    to integers to avoid incorrect dot product behavior.
    """
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0 (the mean of the first two elements)
    # but without the fix it incorrectly returns 2.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0, not 2.0
    expected = xr.DataArray(1.0)
    
    assert result == expected


def test_weighted_sum_of_weights_boolean_weights():
    """Test that boolean weights are properly handled in sum_of_weights calculation."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 2.0 (sum of weights for first two elements)
    # but without the fix it incorrectly returns 1.0 (boolean True)
    result = dta.weighted(wgt).sum_of_weights()
    
    # The correct result should be 2.0, not 1.0
    expected = xr.DataArray(2.0)
    
    assert result == expected


def test_weighted_mean_boolean_weights_all_true():
    """Test weighted mean with all True boolean weights."""
    # Create test data
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray(np.array([1, 1, 1], dtype=bool))
    
    # This should return 2.0 (the mean of all elements)
    result = dta.weighted(wgt).mean()
    
    expected = xr.DataArray(2.0)
    
    assert result == expected


def test_weighted_mean_boolean_weights_all_false():
    """Test weighted mean with all False boolean weights."""
    # Create test data
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray(np.array([0, 0, 0], dtype=bool))
    
    # This should return NaN (no valid weights)
    result = dta.weighted(wgt).mean()
    
    # Should be NaN since all weights are 0
    assert np.isnan(result.values)


def test_weighted_sum_of_weights_float_weights():
    """Test that float weights work correctly (ensuring else branch is tested)."""
    # Create test data with float weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 1.0, 0.0])  # float weights
    
    # This should return 2.0 (sum of weights for first two elements)
    result = dta.weighted(wgt).sum_of_weights()
    
    # The result should be 2.0
    expected = xr.DataArray(2.0)
    
    assert result == expected


def test_weighted_mean_float_weights():
    """Test that float weights work correctly in weighted mean."""
    # Create test data with float weights
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([1.0, 1.0, 0.0])  # float weights
    
    # This should return 1.5 (weighted mean of first two elements)
    result = dta.weighted(wgt).mean()
    
    expected = xr.DataArray(1.5)
    
    assert result == expected