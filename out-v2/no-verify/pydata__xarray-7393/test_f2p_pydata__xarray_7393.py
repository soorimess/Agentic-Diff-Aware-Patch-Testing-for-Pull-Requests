import numpy as np
import pandas as pd
import xarray as xr


def test_stack_preserves_coordinate_dtype():
    """Test that stacking preserves the original dtype of coordinates.
    
    Regression test for issue where stack casts int32 dtype coordinate to int64.
    """
    # Create a dataset with int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # Check that original coordinate has int32 dtype
    original_dtype = ds['a'].values.dtype
    assert original_dtype == np.int32, f"Expected int32, got {original_dtype}"
    
    # Stack the coordinate - this should preserve the dtype
    stacked = ds.stack(b=('a',))
    stacked_dtype = stacked['a'].values.dtype
    
    # The bug was that this would be int64 instead of int32
    assert stacked_dtype == original_dtype, (
        f"Stacking changed dtype from {original_dtype} to {stacked_dtype}. "
        f"Expected {original_dtype} to be preserved."
    )