import numpy as np
import xarray as xr


def test_stack_preserves_coordinate_dtype():
    """Test that stack operation preserves the dtype of coordinates.
    
    This reproduces the exact issue from the bug report:
    stack casts int32 dtype coordinate to int64
    """
    # Exact reproduction from bug report
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    result = ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype
    
    # This should be True but was False before the fix
    assert result, "Stack operation should preserve dtype"