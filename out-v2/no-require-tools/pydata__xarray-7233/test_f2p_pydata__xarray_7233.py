"""
Regression test for bug where ds.Coarsen.construct demotes 
non-dimensional coordinates to variables.

This test ensures that all coordinates that were coordinates 
before the coarsen.construct call remain as coordinates afterwards.
"""

import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinates():
    """Test that coarsen.construct preserves coordinate status of variables."""
    # Create test data as described in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Before the fix, this would demote 'day' from coordinate to variable
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The 'day' coordinate should still be a coordinate in the result
    # This should pass after the fix, but fails with the buggy code
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate"
    assert "day" not in result.data_vars, "Coordinate 'day' should not be a data variable"
    
    # Verify the coordinate is properly shaped
    assert result.coords["day"].dims == ("year", "month"), "Coordinate 'day' should have correct dimensions"
    
    # Verify the data is correct
    expected_day_values = np.array([[0, 365, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650, 4015],
                                   [4380, 4745, 5110, 5475, 5840, 6205, 6570, 6935, 7300, 7665, 8030, 8395]])
    np.testing.assert_array_equal(result.coords["day"].values, expected_day_values)


def test_coarsen_construct_with_dataarray():
    """Test that coarsen.construct preserves coordinates for DataArray as well."""
    # Create test data as DataArray
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    
    # Apply coarsen construct
    result = da.coarsen(time=12).construct(time=("year", "month"))
    
    # The 'day' coordinate should still be a coordinate in the result
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate"
    # For DataArray, we check that it's not a data variable by checking it's in coords
    # DataArray doesn't have data_vars attribute, so we just check it's in coords