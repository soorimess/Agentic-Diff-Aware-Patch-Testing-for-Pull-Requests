import numpy as np
import pytest

import xarray as xr
from xarray import DataArray


def test_weighted_mean_boolean_weights():
    """Test that boolean weights are properly handled in weighted mean calculation.
    
    When boolean weights are passed to weighted.mean(), they should be converted
    to integers before computing the sum of weights to avoid incorrect results.
    """
    # Test case from the bug report
    dta = DataArray([1., 1., 1.])
    wgt = DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Without fix, this would return 2.0 instead of 1.0
    result = dta.weighted(wgt).mean()
    expected = DataArray(1.0)
    
    # The result should be 1.0, not 2.0 as would happen with the bug
    assert result.equals(expected)


def test_weighted_sum_of_weights_boolean_weights():
    """Test that sum_of_weights correctly handles boolean weights."""
    dta = DataArray([1., 1., 1.])
    wgt = DataArray(np.array([1, 1, 0], dtype=bool))
    
    # The sum of weights should be 2 (count of True values in weights)
    result = dta.weighted(wgt).sum_of_weights()
    expected = DataArray(2.0)
    
    assert result.equals(expected)


def test_weighted_mean_boolean_weights_varied():
    """Test weighted mean with different boolean weight patterns."""
    # Test case where not all weights are True
    dta = DataArray([10., 20., 30.])
    wgt = DataArray(np.array([1, 0, 1], dtype=bool))  # Only first and last weights are True
    
    result = dta.weighted(wgt).mean()
    # Expected: (10*1 + 30*1) / (1+1) = 40/2 = 20.0
    expected = DataArray(20.0)
    
    assert result.equals(expected)


def test_weighted_mean_regular_weights_still_work():
    """Test that regular (non-boolean) weights still work correctly."""
    # Test with regular float weights to ensure we don't break existing behavior
    dta = DataArray([10., 20., 30.])
    wgt = DataArray([1.0, 2.0, 0.0])  # Regular weights
    
    result = dta.weighted(wgt).mean()
    # Expected: (10*1 + 20*2 + 30*0) / (1+2+0) = 50/3 = 16.666...
    expected = DataArray(50.0/3.0)
    
    assert np.allclose(result.values, expected.values, rtol=1e-10)


def test_weighted_sum_of_weights_regular_weights():
    """Test that sum_of_weights works correctly with regular weights."""
    dta = DataArray([1., 1., 1.])
    wgt = DataArray([1.0, 2.0, 0.0])  # Regular float weights
    
    result = dta.weighted(wgt).sum_of_weights()
    # Expected: 1.0 + 2.0 + 0.0 = 3.0
    expected = DataArray(3.0)
    
    assert result.equals(expected)