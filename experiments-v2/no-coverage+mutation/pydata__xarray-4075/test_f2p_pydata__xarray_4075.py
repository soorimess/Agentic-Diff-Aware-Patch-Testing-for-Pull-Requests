import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights.
    
    This is a regression test for GH#4075 where passing boolean weights
    to weighted mean returned wrong results due to improper handling of
    boolean dot products.
    """
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0, not 2.0
    result = dta.weighted(wgt).mean()
    
    # The bug caused this to return 2.0 instead of 1.0
    # because boolean dot product [True, True, True] · [True, True, False] = True
    # instead of the expected integer result 2
    assert result.values == 1.0


def test_weighted_sum_of_weights_boolean_weights():
    """Test that sum_of_weights works correctly with boolean weights."""
    # Create test data as described in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 2.0, not 1.0
    result = dta.weighted(wgt).sum_of_weights()
    
    # The bug caused this to return 1.0 instead of 2.0
    # because boolean dot product [True, True, True] · [True, True, False] = True
    # instead of the expected integer result 2
    assert result.values == 2.0


def test_weighted_mean_boolean_weights_different_values():
    """Test weighted mean with boolean weights and different data values."""
    # Test with different data values to ensure proper weighting
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray(np.array([1, 0, 1], dtype=bool))  # Only first and last values should be weighted
    
    result = dta.weighted(wgt).mean()
    
    # Should be (1*1 + 3*1) / (1 + 1) = 4/2 = 2.0
    # Not (1*1 + 2*0 + 3*1) / (1 + 0 + 1) = 4/2 = 2.0 in this case
    # But the key point is that boolean weights should be properly converted to int
    assert result.values == 2.0