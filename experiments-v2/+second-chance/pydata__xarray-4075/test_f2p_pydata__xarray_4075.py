import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights.
    
    When passing boolean weights to weighted mean, the sum_of_weights calculation
    was incorrect because xr.dot([True, True], [True, True]) returns True instead
    of 2, causing incorrect normalization.
    """
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([True, True, False])  # Using Python bool directly
    
    # This should return 1.0 (the mean of the valid data points)
    # but before the fix it incorrectly returned 2.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0, not 2.0
    assert result.values == 1.0


def test_weighted_mean_numeric_weights():
    """Test that weighted mean still works correctly with numeric weights.
    
    This ensures the else branch (non-boolean weights) is also tested.
    """
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([1., 2., 3.])  # Numeric weights
    
    result = dta.weighted(wgt).mean()
    
    # Should return weighted mean: (1*1 + 2*2 + 3*3) / (1+2+3) = 14/6 = 2.333...
    expected = (1*1 + 2*2 + 3*3) / (1+2+3)
    assert np.isclose(result.values, expected)


def test_weighted_mean_boolean_weights_all_true():
    """Test weighted mean with all True boolean weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])
    
    result = dta.weighted(wgt).mean()
    
    # Should return the mean of all values: (1+2+3)/3 = 2.0
    assert result.values == 2.0


def test_weighted_mean_boolean_weights_all_false():
    """Test weighted mean with all False boolean weights."""
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([False, False, False])
    
    result = dta.weighted(wgt).mean()
    
    # Should return NaN since no weights are valid
    assert np.isnan(result.values)


def test_weighted_mean_boolean_weights_mixed():
    """Test weighted mean with mixed boolean weights."""
    dta = xr.DataArray([10., 20., 30., 40.])
    wgt = xr.DataArray([True, False, True, False])
    
    result = dta.weighted(wgt).mean()
    
    # Should return mean of values where weight is True: (10+30)/2 = 20.0
    assert result.values == 20.0