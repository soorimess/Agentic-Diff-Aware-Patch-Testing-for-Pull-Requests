import numpy as np
import xarray as xr


def test_stack_preserves_int32_coordinate_dtype():
    # Coordinate 'a' is int32. Stacking across 'a' should not cast it to int64.
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    before = ds['a'].values.dtype
    after = ds.stack(b=('a',))['a'].values.dtype
    assert before == after
