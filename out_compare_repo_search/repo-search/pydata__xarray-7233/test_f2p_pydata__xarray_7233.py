import numpy as np
import xarray as xr


def test_coarsen_construct_preserves_non_coarsened_coords():
    """
    Regression test for: Coarsen.construct demoting non-dimensional coordinates

    Ensure that coordinates that do not depend on the coarsened dimension
    are still coordinates after calling construct.
    """
    ds = xr.Dataset(
        {"T": ("time", np.arange(24))},
        coords={"time": np.arange(24), "meta": 42},
    )

    res = ds.coarsen(time=12).construct(time=("year", "month"))

    # 'meta' was a coordinate before construct and should remain a coordinate
    assert "meta" in res.coords
    # It should not be present as a data variable
    assert "meta" not in res.data_vars
