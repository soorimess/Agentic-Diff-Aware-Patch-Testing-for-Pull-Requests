"""
Regression test for issue where ds.Coarsen.construct demotes 
non-dimensional coordinates to variables.

This test ensures that all coordinates that were coordinates before 
the coarsen.construct call remain as coordinates afterwards.
"""
import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_all_coordinates():
    """Test that coarsen.construct preserves all coordinates, not just window coordinates."""
    # Create test data as described in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Before the fix, this would incorrectly demote 'day' coordinate to a variable
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The 'day' coordinate should still be a coordinate, not a variable
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not become a data variable"
    
    # Check that the coordinate is properly shaped
    assert result.coords["day"].dims == ("year", "month"), "Coordinate 'day' should have correct dimensions"
    
    # The original data variable should also still be there
    assert "T" in result.data_vars, "Data variable 'T' should still be present"
    assert "T" not in result.coords, "Data variable 'T' should not be a coordinate"


def test_coarsen_construct_preserves_coordinates_from_original():
    """Test that coordinates from the original dataset are preserved."""
    # Create test data exactly as in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Apply coarsen construct - this is the exact example from the bug report
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The bug: 'day' coordinate gets demoted to a data variable
    # After fix: 'day' should remain a coordinate
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not become a data variable"
    
    # Verify it's still a coordinate with correct shape
    assert result.coords["day"].dims == ("year", "month")
    
    # Verify that the data variable is still there
    assert "T" in result.data_vars