import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coordinates():
    """
    Regression test for https://github.com/pydata/xarray/issues/7233

    Coarsen.construct should preserve variables that were coordinates
    in the original Dataset (i.e., they should remain coordinates,
    not be demoted to data variables).
    """
    da = xr.DataArray(np.arange(24), dims=["time"])
    # create a coordinate that depends on the "time" dimension
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    assert "day" in ds.coords

    # coarsen and construct, splitting time into (year, month)
    out = ds.coarsen(time=12).construct(time=("year", "month"))

    # The 'day' coordinate should still be a coordinate after construct
    assert "day" in out.coords

    # and it should have the new coarsened dimensions
    assert out.coords["day"].dims == ("year", "month")
