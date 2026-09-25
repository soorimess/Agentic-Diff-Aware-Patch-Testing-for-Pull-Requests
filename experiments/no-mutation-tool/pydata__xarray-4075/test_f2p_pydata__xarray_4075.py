import numpy as np
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test for boolean weights in weighted mean calculation.
    
    When boolean weights are passed to weighted.mean(), the sum_of_weights
    calculation was incorrect because dot product of boolean arrays returns
    a boolean instead of an integer, leading to wrong normalization.
    
    Specifically, xr.dot([True, True, True], [True, True, False]) returns True
    (representing the integer 2) instead of integer 2, causing incorrect division.
    """
    # Create test data as in the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # This should return 1.0 (mean of two valid data points, each with weight 1)
    # But before the fix it incorrectly returned 2.0 
    result = dta.weighted(wgt).mean()
    
    # The expected result is 1.0, not 2.0
    expected = 1.0
    
    # This assertion should pass after the fix and fail before the fix
    assert result == expected


def test_weighted_mean_all_true_boolean_weights():
    """Test with all True boolean weights to verify no regression."""
    # All weights are True -> should return the mean of all data points  
    dta = xr.DataArray([1., 2., 3.])
    wgt = xr.DataArray([True, True, True])
    
    result = dta.weighted(wgt).mean()
    # Should be (1*1 + 2*1 + 3*1) / (1+1+1) = 6/3 = 2.0
    expected = 2.0
    
    assert result == expected


if __name__ == "__main__":
    test_weighted_mean_boolean_weights()
    test_weighted_mean_all_true_boolean_weights()
    print("All tests completed!")