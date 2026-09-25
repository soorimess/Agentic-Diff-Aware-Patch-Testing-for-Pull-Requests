import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights():
    """Test for bug when passing boolean weights to weighted mean.
    
    Before fix: boolean weights [True, True, False] are not properly converted
    to int for dot product calculation, causing sum_of_weights = 1 instead of 2.
    This leads to wrong weighted mean result.
    """
    
    # Create test data as in the bug report  
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0, not 2.0 due to bug in sum_of_weights
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(1.0)
    
    # The core bug: xr.dot([True, True, True], [True, True, False]) = True (1) 
    # instead of 2, so weighted sum = (1+1+0)/1 = 2 (wrong) instead of (1+1+0)/2 = 1 (correct)
    assert result == expected


def test_weighted_mean_boolean_weights_different_values():
    """Test with different data values to confirm correct weighted mean behavior."""
    
    # Data with different values
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))  # [True, True, False]
    
    # The weighted mean should be (2*1 + 4*1 + 6*0) / (1+1+0) = 6/2 = 3.0
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(3.0)
    
    # Exact computation: 
    # sum_of_weights = dot([True,True,True], [1,1,0]) should be 2, not 1
    # weighted_sum = 2*1 + 4*1 + 6*0 = 6
    # mean = 6/2 = 3.0
    assert result == expected


def test_sum_of_weights_boolean_case():
    """Test the specific sum_of_weights behavior that caused the bug."""
    
    # The root cause is in sum_of_weights method
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))  # [True, True, False]
    
    # This should give sum of weights = 2 (True + True + False = 2)
    result = dta.weighted(wgt).sum_of_weights()
    expected = xr.DataArray(2.0)
    
    # Before fix: xr.dot([True,True,True], [True,True,False]) = True = 1 (incorrect)
    # After fix: xr.dot([True,True,True], [1,1,0]) = 2 (correct) 
    assert result == expected


def test_sum_of_weights_non_boolean_weights():
    """Test that regular (non-boolean) weights still work correctly - regression test."""
    
    # Test with regular int weights to ensure non-regression 
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1, 2, 1])  # regular int weights
    
    # sum should be 1+2+1 = 4
    result = dta.weighted(wgt).sum_of_weights()
    expected = xr.DataArray(4.0)
    
    assert result == expected