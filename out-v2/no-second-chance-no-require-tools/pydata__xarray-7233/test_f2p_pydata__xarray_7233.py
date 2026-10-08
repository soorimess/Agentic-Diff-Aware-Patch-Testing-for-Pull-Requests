"""
Regression test for the bug where ds.Coarsen.construct demotes 
non-dimensional coordinates to variables.

The issue is that after calling ds.coarsen().construct(), non-dimensional 
coordinates are incorrectly converted to data variables instead of remaining 
as coordinates.
"""

import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinates():
    """Test that coarsen.construct preserves coordinate status of variables."""
    # Reproduce the exact example from the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")
    
    # Before the fix, this would demote 'day' from coordinate to variable
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The 'day' coordinate should still be a coordinate in the result
    # This assertion should pass after the fix, fail before the fix
    assert "day" in result.coords, "day coordinate should remain a coordinate"
    
    # Verify it's actually a coordinate with correct dimensions
    assert result.coords["day"].dims == ("year", "month"), "day coordinate should have correct dimensions"
    
    # Verify it's NOT a data variable
    assert "day" not in result.data_vars, "day should not be a data variable"


def test_coarsen_construct_preserves_multiple_coordinates():
    """Test that multiple coordinates are preserved correctly."""
    # Create test data with multiple coordinates
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    da = da.assign_coords(time_coord=da * 2)  # This should also be preserved
    ds = da.to_dataset(name="T")
    
    # Apply coarsen construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # Both coordinates should remain as coordinates
    assert "day" in result.coords, "day coordinate should remain a coordinate"
    assert "time_coord" in result.coords, "time_coord should remain a coordinate"
    
    # Neither should be data variables
    assert "day" not in result.data_vars, "day should not be a data variable"
    assert "time_coord" not in result.data_vars, "time_coord should not be a data variable"


def test_coarsen_construct_preserves_all_original_coords():
    """Test that all original coordinates are preserved."""
    # Create test data matching the bug report exactly
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")
    
    # Apply coarsen construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The original dataset had 'day' as coordinate
    assert "day" in ds.coords, "day should be coordinate in original dataset"
    
    # After coarsen.construct, 'day' should still be a coordinate
    assert "day" in result.coords, "day should still be coordinate after coarsen.construct"
    
    # The result should have the same coordinates as the original
    # (the coordinate should be preserved even though dimensions changed)
    assert result.coords["day"].dims == ("year", "month")