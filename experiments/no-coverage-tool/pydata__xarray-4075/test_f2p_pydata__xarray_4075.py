import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights():
    """Test weighted mean with boolean weights returns correct result.
    
    When boolean weights are used in weighted.mean(), the sum_of_weights
    calculation incorrectly treats boolean arrays in dot product as single 
    boolean values instead of integer counts, leading to wrong normalization.
    
    Bug: xr.dot([True, True], [True, True]) -> True (should be 2)
    Fix: Convert boolean weights to int before dot product 
    """
    # Create test data as described in the bug report  
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Expected result: 
    # - Only first two elements are weighted (weights 1, 1) with values 1, 1
    # - Weighted sum = 1*1 + 1*1 = 2
    # - Sum of weights = 1 + 1 = 2  
    # - Mean = 2/2 = 1.0
    expected = 1.0
    
    result = dta.weighted(wgt).mean()
    
    # Before the fix, this incorrectly returned 2.0
    # because sum_of_weights was computed as True (1) instead of 2
    assert result.values == expected


def test_weighted_mean_boolean_weights_different_values():
    """Test weighted mean with boolean weights and different data values."""
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray(np.array([1, 0, 1], dtype=bool))
    
    # Expected result: 
    # - Only elements 0 and 2 are weighted (values 2, 6) with weights 1, 1
    # - Weighted sum = 2*1 + 6*1 = 8
    # - Sum of weights = 1 + 1 = 2
    # - Mean = 8/2 = 4.0
    expected = 4.0
    
    result = dta.weighted(wgt).mean()
    
    assert result.values == expected


def test_sum_of_weights_boolean():
    """Test sum_of_weights with boolean weights correctly counts weights."""
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return the sum of weights = 2.0 (both first two are True)
    expected = 2.0
    
    result = dta.weighted(wgt).sum_of_weights()
    assert result.values == expected

if __name__ == "__main__":
    test_weighted_mean_boolean_weights()
    test_weighted_mean_boolean_weights_different_values()
    test_sum_of_weights_boolean()
    print("All tests passed!")