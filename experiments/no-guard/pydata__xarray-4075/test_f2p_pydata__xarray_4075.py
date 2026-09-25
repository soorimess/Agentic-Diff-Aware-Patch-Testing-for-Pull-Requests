"""
Regression test for issue with boolean weights in weighted mean.

This test ensures that when boolean weights are used in weighted operations,
they are properly converted to integers to avoid incorrect accumulation
of boolean values.
"""

import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights_bug():
    """
    Test case that demonstrates the boolean weights bug.
    
    When using boolean weights [True, True, False], the weighted mean
    should return 1.0 but incorrectly returns 2.0 due to boolean arithmetic issues.
    """
    # Exact reproduction from the bug report  
    # Using the explicit bool type as in the original report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))

    # This should return 1.0, not 2.0 (the bug result)  
    result = dta.weighted(wgt).mean()
    
    # With the fix applied, this should be correct
    assert result.values == 1.0, f"Expected 1.0, got {result.values}"


def test_sum_of_weights_boolean_conversion():
    """
    Test the specific issue in sum_of_weights calculation with boolean arrays.
    
    This tests that boolean weights are converted to int before computation
    to avoid boolean arithmetic errors.
    """
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This tests that boolean weights get properly converted to int in sum_of_weights calculation
    sum_of_weights = dta.weighted(wgt).sum_of_weights()
    
    # With the fix, this should be 2.0 (the sum of non-zero weights: 1 + 1 + 0 = 2)
    expected_sum = 2.0
    assert sum_of_weights.values == expected_sum, f"Expected sum of weights {expected_sum}, got {sum_of_weights.values}"


def test_weighted_mean_regular_float_weights():
    """
    Test that regular (non-boolean) weights still work correctly.
    This ensures the else branch of the fix is also tested.
    """
    # Test with regular float weights to make sure we didn't break anything
    dta = xr.DataArray([10., 20., 30.])
    wgt = xr.DataArray([1.0, 2.0, 1.0])  # Regular float weights
    
    result = dta.weighted(wgt).mean()
    
    # Should be: (10*1 + 20*2 + 30*1) / (1 + 2 + 1) = 80/4 = 20.0
    expected = 20.0
    assert result.values == expected, f"Expected {expected}, got {result.values}"