import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights_issue():
    """Test that weighted mean with boolean weights returns correct result.
    
    The bug is that when boolean weights are used, the sum of weights calculation
    incorrectly treats boolean True as 1 but the dot product of boolean arrays
    gives a boolean result rather than a count.
    """
    # Test data from the issue report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Current buggy behavior returns 2.0 instead of 1.0
    # Because sum_of_weights returns True (which evaluates to 1) instead of 2
    result = dta.weighted(wgt).mean()
    
    # This is what we expect after fix (2.0 score from 2 valid weights)
    expected = 1.0
    assert result == expected


def test_sum_of_weights_boolean_weights():
    """Test that sum_of_weights correctly handles boolean weights."""
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # sum_of_weights should return 2.0 (count of True values in weights)
    # bug causes it to return 1.0 instead because of boolean dot product
    result = dta.weighted(wgt).sum_of_weights()
    
    # Should equal 2.0 (two True values in weights)
    expected = 2.0
    assert result == expected


def test_weighted_mean_with_different_boolean_patterns():
    """Test various boolean weight patterns."""
    # Test case where all weights are True
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])
    
    result = dta.weighted(wgt).mean()
    # Should be (1*1 + 2*1 + 3*1) / (1 + 1 + 1) = 6/3 = 2.0
    expected = 2.0
    assert result == expected
    
    # Test case where no weights are True  
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([False, False, False])
    
    # Should return NaN (division by zero)
    result = dta.weighted(wgt).mean()
    # This should be NaN since sum of weights is 0
    assert np.isnan(result.values)


def test_regular_weighted_mean_still_works():
    """Ensure non-boolean weights still work correctly."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([1., 2., 3.])
    
    result = dta.weighted(wgt).mean()
    # Should be (1*1 + 2*2 + 3*3) / (1 + 2 + 3) = 14/6 = 2.333...
    expected = 14.0 / 6.0
    assert np.isclose(result, expected)