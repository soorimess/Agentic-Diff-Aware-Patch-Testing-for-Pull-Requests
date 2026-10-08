import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinate_status():
    """Test that coarsen.construct preserves coordinate status of non-dimensional coordinates."""
    # Create the test case from the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")
    
    # Apply coarsen.construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # Before the fix, 'day' coordinate would be demoted to a variable
    # After the fix, 'day' should remain a coordinate
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not be a data variable after coarsen.construct"
    
    # Verify the coordinate is properly shaped
    assert result.coords["day"].dims == ("year", "month"), "Coordinate 'day' should have correct dimensions"
    
    # Verify the data variable is properly shaped
    assert result.data_vars["T"].dims == ("year", "month"), "Data variable 'T' should have correct dimensions"