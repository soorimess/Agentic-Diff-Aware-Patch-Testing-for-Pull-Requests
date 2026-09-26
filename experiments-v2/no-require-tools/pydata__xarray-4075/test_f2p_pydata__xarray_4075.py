import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights.
    
    This is a regression test for GH#4075 where passing boolean weights
    to weighted mean returned incorrect results due to improper handling
    of boolean dot products.
    """
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([True, True, False])
    
    # This should return 1.0, not 2.0 (the bug result)
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0 because:
    # - Weights are [True, True, False] which should be treated as [1, 1, 0]
    # - Valid data points are [1., 1., 1.] 
    # - Sum of weighted values = 1*1 + 1*1 + 0*1 = 2
    # - Sum of weights = 1 + 1 + 0 = 2
    # - Mean = 2/2 = 1.0
    expected = xr.DataArray(1.0)
    
    assert result == expected


def test_weighted_sum_of_weights_boolean_weights():
    """Test that sum_of_weights works correctly with boolean weights."""
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([True, True, False])
    
    # Test sum_of_weights specifically
    result = dta.weighted(wgt).sum_of_weights()
    
    # With boolean weights [True, True, False], sum should be 2 (not 1)
    expected = xr.DataArray(2.0)
    
    assert result == expected


def test_weighted_mean_boolean_weights_all_true():
    """Test weighted mean with all True boolean weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])
    
    # All weights are True, so should behave like normal mean
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(2.0)  # (1+2+3)/3 = 2.0
    
    assert result == expected


def test_weighted_mean_boolean_weights_all_false():
    """Test weighted mean with all False boolean weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([False, False, False])
    
    # All weights are False, should return NaN
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(np.nan)
    
    assert np.isnan(result.values)


def test_weighted_mean_non_boolean_weights():
    """Test that weighted mean works correctly with non-boolean weights.
    
    This ensures the else branch of the fix is also tested.
    """
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([1.0, 2.0, 0.0])  # Non-boolean weights
    
    # Should compute weighted mean correctly
    result = dta.weighted(wgt).mean()
    # Weighted sum = 1*1 + 2*2 + 3*0 = 5
    # Sum of weights = 1 + 2 + 0 = 3
    # Mean = 5/3
    expected = xr.DataArray(5.0/3.0)
    
    assert result == expected


def test_weighted_sum_of_weights_non_boolean_weights():
    """Test that sum_of_weights works correctly with non-boolean weights."""
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 2.0, 0.0])  # Non-boolean weights
    
    # Test sum_of_weights specifically
    result = dta.weighted(wgt).sum_of_weights()
    
    # With weights [1.0, 2.0, 0.0], sum should be 3.0
    expected = xr.DataArray(3.0)
    
    assert result == expected