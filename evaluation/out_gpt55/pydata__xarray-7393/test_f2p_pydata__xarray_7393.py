from __future__ import annotations

import numpy as np

import xarray as xr


def test_stack_preserves_int32_coordinate_dtype() -> None:
    dtype = np.dtype("int32")
    ds = xr.Dataset(coords={"a": np.array([0], dtype=dtype)})

    stacked = ds.stack(b=("a",))

    assert stacked["a"].values.dtype == dtype
