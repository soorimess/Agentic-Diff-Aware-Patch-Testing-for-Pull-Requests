import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights."""
    # This is the exact example from the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # Before the fix, this would return 2.0 instead of 1.0
    result = dta.weighted(wgt).mean()
    
    # The expected result should be 1.0, not 2.0
    expected = xr.DataArray(1.0)
    
    # Check that we get the correct result
    assert result == expected


def test_weighted_sum_boolean_weights():
    """Test that weighted sum works correctly with boolean weights."""
    # Test sum operation with boolean weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # Before the fix, this would have incorrect behavior
    result = dta.weighted(wgt).sum()
    
    # The expected result should be 2.0 (1*1 + 1*1 + 1*0 = 2)
    expected = xr.DataArray(2.0)
    
    # Check that we get the correct result
    assert result == expected


def test_weighted_sum_of_weights_boolean_weights():
    """Test that sum_of_weights works correctly with boolean weights."""
    # Test sum_of_weights operation with boolean weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # This should return 2 (sum of weights where data is not null)
    result = dta.weighted(wgt).sum_of_weights()
    
    # The expected result should be 2.0 (True + True + False = 2)
    expected = xr.DataArray(2.0)
    
    # Check that we get the correct result
    assert result == expected


def test_weighted_mean_float_weights():
    """Test that weighted mean works correctly with float weights (control test)."""
    # Test with float weights to ensure non-boolean path works
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 1.0, 0.0])
    
    result = dta.weighted(wgt).mean()
    
    # The expected result should be 1.0
    expected = xr.DataArray(1.0)
    
    # Check that we get the correct result
    assert result == expected


def test_weighted_sum_float_weights():
    """Test that weighted sum works correctly with float weights (control test)."""
    # Test sum operation with float weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 1.0, 0.0])
    
    result = dta.weighted(wgt).sum()
    
    # The expected result should be 2.0 (1*1 + 1*1 + 1*0 = 2)
    expected = xr.DataArray(2.0)
    
    # Check that we get the correct result
    assert result == expected


def test_weighted_sum_of_weights_float_weights():
    """Test that sum_of_weights works correctly with float weights (control test)."""
    # Test sum_of_weights operation with float weights
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([1.0, 1.0, 0.0])
    
    result = dta.weighted(wgt).sum_of_weights()
    
    # The expected result should be 2.0 (1.0 + 1.0 + 0.0 = 2.0)
    expected = xr.DataArray(2.0)
    
    # Check that we get the correct result
    assert result == expected


if __name__ == "__main__":
    test_weighted_mean_boolean_weights()
    test_weighted_sum_boolean_weights()
    test_weighted_sum_of_weights_boolean_weights()
    test_weighted_mean_float_weights()
    test_weighted_sum_float_weights()
    test_weighted_sum_of_weights_float_weights()
    print("All tests passed!")