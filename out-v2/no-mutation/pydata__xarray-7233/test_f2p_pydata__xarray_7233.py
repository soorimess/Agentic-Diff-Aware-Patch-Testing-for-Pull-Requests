import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinates():
    """Test that coarsen.construct preserves non-dimensional coordinates as coordinates."""
    # Create test data as described in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Before the fix, this would demote 'day' coordinate to a variable
    # After the fix, 'day' should remain a coordinate
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # Check that 'day' is still a coordinate (not a variable)
    # The bug is that 'day' gets demoted to a data variable
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not become a data variable"
    
    # Verify the coordinate has the expected shape
    assert result.coords["day"].dims == ("year", "month"), "Coordinate 'day' should have correct dimensions"
    
    # Verify the data is correct
    expected_day_values = np.array([[0, 365, 730, 1095, 1460, 1825, 2190, 2555, 2920, 3285, 3650, 4015],
                                   [4380, 4745, 5110, 5475, 5840, 6205, 6570, 6935, 7300, 7665, 8030, 8395]])
    np.testing.assert_array_equal(result.coords["day"].values, expected_day_values)


def test_coarsen_construct_preserves_all_coordinates():
    """Test that coarsen.construct preserves all coordinates, not just those related to window dims."""
    # Create test data with a coordinate that is NOT part of the window dimension
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)  # This coordinate is NOT part of the window dimension
    ds = da.to_dataset(name="T")

    # This should preserve 'day' as a coordinate even though it's not related to the window dimension
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The key assertion: 'day' should remain a coordinate, not be demoted to a variable
    # Before fix: 'day' would be in data_vars, after fix: 'day' should be in coords
    assert "day" in result.coords, "Coordinate 'day' should remain a coordinate after coarsen.construct"
    assert "day" not in result.data_vars, "Coordinate 'day' should not become a data variable"