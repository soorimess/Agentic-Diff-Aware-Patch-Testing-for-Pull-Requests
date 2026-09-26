import numpy as np
import xarray as xr
import pytest


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # This should return 1.0, not 2.0 (before fix it returned 2.0 due to boolean dot product)
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0 because:
    # - Weights are [True, True, False] which should sum to 2 (count of True values)
    # - Data values are [1., 1., 1.] 
    # - Weighted sum = 1*1 + 1*1 + 1*0 = 2
    # - Sum of weights = 2
    # - Weighted mean = 2/2 = 1.0
    expected = 1.0
    assert result.values == expected


def test_weighted_mean_boolean_weights_different_values():
    """Test weighted mean with boolean weights and different data values."""
    # Create test data with different values
    dta = xr.DataArray([2., 4., 6.])
    wgt = xr.DataArray(np.array([1, 0, 1], dtype=np.bool))
    
    # This should return 4.0, not 3.0 (before fix it would return wrong value)
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 4.0 because:
    # - Weights are [True, False, True] which should sum to 2
    # - Data values are [2., 4., 6.]
    # - Weighted sum = 2*1 + 4*0 + 6*1 = 8
    # - Sum of weights = 2
    # - Weighted mean = 8/2 = 4.0
    expected = 4.0
    assert result.values == expected


def test_weighted_mean_boolean_weights_all_false():
    """Test weighted mean with all False weights."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([0, 0, 0], dtype=np.bool))
    
    # This should return NaN since all weights are zero
    result = dta.weighted(wgt).mean()
    
    # All weights are False, so sum of weights = 0, which should return NaN
    assert np.isnan(result.values)


def test_sum_of_weights_boolean_weights():
    """Test that sum_of_weights works correctly with boolean weights."""
    # Create test data
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # Test the sum_of_weights method directly
    result = dta.weighted(wgt).sum_of_weights()
    
    # The sum of weights should be 2 (count of True values in [True, True, False])
    expected = 2.0
    assert result.values == expected


def test_weighted_mean_with_nan_values_and_boolean_weights():
    """Test weighted mean with NaN values in data and boolean weights."""
    # Create test data with NaN values
    dta = xr.DataArray([1., np.nan, 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=np.bool))
    
    # This should return 1.0, not 2.0
    result = dta.weighted(wgt).mean()
    
    # The correct result should be 1.0 because:
    # - Weights are [True, True, False] 
    # - Data values are [1., NaN, 1.] (NaN is masked out)
    # - Effective data values are [1., 1.] with weights [True, True]
    # - Weighted sum = 1*1 + 1*1 = 2
    # - Sum of weights = 2
    # - Weighted mean = 2/2 = 1.0
    expected = 1.0
    assert result.values == expected