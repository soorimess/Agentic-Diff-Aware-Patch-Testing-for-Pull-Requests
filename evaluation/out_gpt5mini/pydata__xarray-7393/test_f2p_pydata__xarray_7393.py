from __future__ import annotations

import numpy as np

import xarray as xr


def test_stack_preserves_coordinate_dtype() -> None:
    """Regression test for pydata/xarray#7393

    Creating a MultiIndex via Dataset.stack should not change the dtype of
    the coordinates from which the MultiIndex is built. In particular, an
    int32 coordinate must remain int32 after stacking (was previously upcast
    to int64).
    """
    ds = xr.Dataset(coords={"a": np.array([0], dtype=np.int32)})

    original_dtype = ds["a"].values.dtype
    stacked = ds.stack(b=("a",))
    stacked_dtype = stacked["a"].values.dtype

    assert original_dtype == stacked_dtype
