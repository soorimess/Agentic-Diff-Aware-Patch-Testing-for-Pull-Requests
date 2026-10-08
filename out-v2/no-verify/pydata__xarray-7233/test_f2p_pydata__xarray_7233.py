from __future__ import annotations

import numpy as np

import xarray as xr


def test_coarsen_construct_preserves_non_dimensional_coordinates():
    """Test that coarsen.construct preserves non-dimensional coordinates as coordinates.
    
    Before the fix, ds.coarsen.construct would demote non-dimensional coordinates
    to data variables, but they should remain coordinates.
    """
    # Create test data as described in the bug report
    da = xr.DataArray(np.arange(24), dims=["time"])
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    # Apply coarsen construct
    result = ds.coarsen(time=12).construct(time=("year", "month"))
    
    # The 'day' coordinate should remain a coordinate, not be demoted to a data variable
    # This is the core bug: coordinates were being demoted
    assert "day" in result.coords, "Non-dimensional coordinate 'day' should remain a coordinate"
    assert "day" not in result.data_vars, "Non-dimensional coordinate 'day' should not be a data variable"