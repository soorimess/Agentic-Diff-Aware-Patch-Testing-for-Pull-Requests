import numpy as np
import pytest
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that boolean weights are correctly handled in weighted mean calculations.
    
    Bug: When boolean weights like [True, True, False] are passed, 
    the sum_of_weights incorrectly returns boolean True instead of integer 2,
    which leads to an incorrect weighted mean result of 2.0 instead of 1.0.
    
    This test ensures that the fix in the weighted.py prevents this bug from returning.
    """
    # Exact reproduction of bug report case  
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray([True, True, False], dims='dim_0')
    
    # The bug: instead of computing (1*1 + 1*1 + 1*0) / (1 + 1 + 0) = 2/2 = 1.0
    # It computes (1*1 + 1*1 + 1*0) / (1) = 2/1 = 2.0
    # Because xr.dot([True, True, True], [True, True, False]) = True instead of 2
    result = dta.weighted(wgt).mean()
    
    # This should be 1.0, not 2.0
    assert result.values == 1.0, \
        f"Weighted mean with boolean weights should return 1.0, but got {result.values}"


def test_weighted_sum_of_weights_boolean_logic():
    """Test the core logic that causes the bug in sum_of_weights."""
    # Test that demonstrates what exactly goes wrong
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, False])  # Should weight first two elements
    
    # Get an instance of the weighted object to test internal logic
    weighted_obj = dta.weighted(wgt)
    
    # What sum_of_weights should logically compute:
    # sum of weights = 1 + 1 + 0 = 2 (integer)
    # But with the bug, it computes:
    # sum_of_weights = dot([True, True, True], [True, True, False]) = True (boolean) 
    # Which when converted to float is 1.0, not 2.0
    
    result = weighted_obj.sum_of_weights()
    
    # The test will only pass if the fix is implemented
    # Before fix: result.values would be 1.0 (because dot of bools returns True)
    # After fix: result.values should be 2.0 (because weights converted to int first)
    assert result.values == 2.0, \
        f"sum_of_weights should be 2.0 with boolean weights [True, True, False], got {result.values}"