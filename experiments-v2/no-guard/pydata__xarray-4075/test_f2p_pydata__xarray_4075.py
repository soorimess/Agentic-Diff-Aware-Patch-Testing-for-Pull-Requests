import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test for bug with boolean weights in weighted mean operations.
    
    When passing boolean weights to weighted mean, the result was incorrect
    because boolean weights were not properly normalized in sum_of_weights calculation.
    """
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0, not 2.0 (the bug)
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0 because:
    # - weights [True, True, False] should be treated as [1, 1, 0] 
    # - sum of valid data values: 1 + 1 = 2
    # - sum of weights: 1 + 1 = 2
    # - mean: 2 / 2 = 1.0
    expected = xr.DataArray(1.0)
    
    assert result == expected


def test_weighted_sum_of_weights_boolean_weights():
    """Test that sum_of_weights correctly handles boolean weights."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Test sum_of_weights specifically
    result = dta.weighted(wgt).sum_of_weights()
    
    # With boolean weights [True, True, False], the sum should be 2 (not 1)
    # because True + True + False = 2 (when converted to int)
    expected = xr.DataArray(2.0)
    
    assert result == expected


def test_weighted_mean_boolean_weights_different_values():
    """Test weighted mean with boolean weights and different data values."""
    # Test with different data values
    dta = xr.DataArray([2., 4., 6.])  # Values: 2, 4, 6
    wgt = xr.DataArray(np.array([1, 0, 1], dtype=bool))  # Weights: True, False, True
    
    # Expected: (2*1 + 6*1) / (1 + 1) = 8/2 = 4.0
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(4.0)
    
    assert result == expected


def test_weighted_mean_non_boolean_weights():
    """Test that non-boolean weights still work correctly (ensures else branch is covered)."""
    # Test with regular float weights
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray([1.0, 0.0, 2.0])  # Weights: 1.0, 0.0, 2.0
    
    # Expected: (2*1 + 6*2) / (1 + 2) = 14/3 = 4.666...
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(14.0/3.0)
    
    assert result == expected


def test_weighted_sum_of_weights_non_boolean_weights():
    """Test that sum_of_weights works correctly with non-boolean weights."""
    # Test with regular float weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 0.0, 2.0])  # Weights: 1.0, 0.0, 2.0
    
    # Expected: 1.0 + 0.0 + 2.0 = 3.0
    result = dta.weighted(wgt).sum_of_weights()
    expected = xr.DataArray(3.0)
    
    assert result == expected