import numpy as np
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that weighted mean works correctly with boolean weights (GH#4075)."""
    # Test case from the bug report - boolean weights should be cast to int
    # to avoid boolean arithmetic in sum_of_weights computation
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Before fix: xr.dot(dta.notnull(), wgt) would return True (1)  
    # After fix: xr.dot(dta.notnull(), wgt.astype(int)) correctly returns 2 (int)
    # Expected result: (1*1 + 1*1 + 1*0) / (1 + 1 + 0) = 2 / 2 = 1.0
    result = dta.weighted(wgt).mean()
    expected = 1.0
    
    assert result.values == expected, f"Expected {expected}, got {result.values}"


def test_weighted_mean_non_boolean_weights_still_work():
    """Test that non-boolean weights continue to work correctly."""
    # Test with regular numeric weights to ensure we don't break existing behavior
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([1.0, 2.0, 0.0])
    
    # Should return (1*1 + 2*2 + 3*0) / (1 + 2 + 0) = 5 / 3
    result = dta.weighted(wgt).mean()
    expected = 5.0 / 3.0
    
    assert result.values == expected, f"Expected {expected}, got {result.values}"