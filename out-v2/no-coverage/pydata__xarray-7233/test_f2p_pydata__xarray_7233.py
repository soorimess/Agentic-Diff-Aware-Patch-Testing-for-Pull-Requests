"""
Regression test for the bug where ds.Coarsen.construct demotes 
non-dimensional coordinates to variables.
"""
import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinates():
    """Test that coarsen.construct preserves all coordinates, not just those in window dimensions."""
    # Create test data as described in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")
    
    # Apply coarsen.construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # Before the fix, 'day' coordinate would be demoted to a variable
    # After the fix, 'day' should remain a coordinate
    # The key assertion: day should be in coords, not data_vars
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not be a data variable after coarsen.construct"


def test_coarsen_construct_preserves_all_coordinates():
    """Test that coarsen.construct preserves all coordinates, even those not in window dimensions."""
    # Create test data with a coordinate that is not a dimension coordinate
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(some_coord=100 * da)  # This coordinate is not a dimension coordinate
    ds = da.to_dataset(name="T")
    
    # Apply coarsen.construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The coordinate should still be preserved as a coordinate
    assert "some_coord" in result.coords, "Coordinate 'some_coord' should remain a coordinate"
    assert "some_coord" not in result.data_vars, "Coordinate 'some_coord' should not be a data variable"