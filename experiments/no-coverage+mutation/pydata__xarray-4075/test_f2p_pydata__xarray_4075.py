"""
Regression test for bug where boolean weights in weighted mean produce wrong result.

This tests the specific issue described in the bug report where passing
boolean weights to weighted.mean() returns an incorrect result because
the sum_of_weights calculation doesn't properly handle boolean arrays.
"""

import numpy as np
import xarray as xr


def test_weighted_mean_boolean_weights():
    """Test that boolean weights produce correct results in weighted mean."""
    # This is the exact test case from the bug report
    dta = xr.DataArray([1., 1., 1.])
    wgt = xr.DataArray(np.array([1, 1, 0], dtype=bool))
    
    # Before the fix, this would return 2.0 instead of 1.0
    result = dta.weighted(wgt).mean()
    
    # The expected result should be 1.0 
    # With weights [True, True, False], only first two values should be considered
    # Average of [1., 1.] = 1.0
    expected = 1.0
    
    assert result.values == expected