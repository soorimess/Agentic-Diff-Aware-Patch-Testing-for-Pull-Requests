import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_coords():
    """Regression test for pydata/xarray#7233: Coarsen.construct should not
    demote coordinates to data variables.
    """
    da = xr.DataArray(np.arange(24), dims=["time"])
    # create a coordinate that depends on the original dimension
    da = da.assign_coords(day=365 * da)
    ds = da.to_dataset(name="T")

    result = ds.coarsen(time=12).construct(time=("year", "month"))

    # 'day' was a coordinate before coarsening and should remain a coordinate
    assert "day" in result.coords
    # it must not be present as a data variable
    assert "day" not in result.data_vars
