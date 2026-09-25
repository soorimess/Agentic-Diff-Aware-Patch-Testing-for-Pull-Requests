"""
Regression test for DataArrayRolling center parameter ignoring bug.

This test ensures that when iterating over a DataArrayRolling object with 
center=True, the manual iteration produces identical results to the .mean() method.
This addresses the specific bug where the center parameter was ignored during manual iteration.

See: https://github.com/pydata/xarray/discussions/6738
"""

import numpy as np
import xarray as xr


def test_rolling_center_iteration_matches_mean_method():
    """Test that manual iteration over centered rolling windows matches .mean() method."""
    # Test case from the original bug report to reproduce the exact issue
    my_data = xr.DataArray(np.arange(1, 10), dims="x")
    
    # The .mean() method correctly applies centering
    mean_result = my_data.rolling(x=3, center=True).mean().values
    
    # Manual iteration should produce the same result but previously ignored center=True
    rolling_obj = my_data.rolling(x=3, center=True)
    iteration_result = [window.mean().values.item() for label, window in rolling_obj]
    
    # Both approaches should yield identical results when center=True
    np.testing.assert_array_equal(mean_result, iteration_result)