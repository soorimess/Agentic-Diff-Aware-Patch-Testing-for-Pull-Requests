import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights.
    
    When boolean weights are passed to weighted mean, the sum_of_weights calculation
    was incorrectly treating boolean values as boolean instead of converting them to int.
    This caused incorrect results when some weights were False (0) and others were True (1).
    """
    # Create test data exactly as in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([True, True, False])  # This creates boolean array
    
    # The bug was that this returned 2.0 instead of 1.0
    # because xr.dot([True, True, True], [True, True, False]) -> True (instead of 2)
    result = dta.weighted(wgt).mean()
    
    # Should be 1.0, not 2.0
    expected = xr.DataArray(1.0)
    
    # Check that we get the correct result
    assert result.equals(expected)


def test_weighted_mean_all_true_boolean_weights():
    """Test weighted mean with all True boolean weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])
    
    result = dta.weighted(wgt).mean()
    expected = xr.DataArray(2.0)  # (1*1 + 2*1 + 3*1) / (1 + 1 + 1) = 2.0
    
    assert result.equals(expected)


def test_weighted_mean_mixed_boolean_weights():
    """Test weighted mean with mixed boolean weights."""
    dta = xr.DataArray([10., 20., 30., 40.])
    wgt = xr.DataArray([True, False, True, False])
    
    result = dta.weighted(wgt).mean()
    # Should be (10*1 + 20*0 + 30*1 + 40*0) / (1 + 0 + 1 + 0) = 40/2 = 20.0
    expected = xr.DataArray(20.0)
    
    assert result.equals(expected)