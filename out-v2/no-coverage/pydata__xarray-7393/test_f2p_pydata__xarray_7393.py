"""
Regression test for issue where stack casts int32 dtype coordinate to int64.

This test ensures that when creating a MultiIndex from coordinates with specific dtypes,
the dtype is preserved and not changed during the stack operation.
"""

import numpy as np
import pytest
import xarray as xr


def test_stack_preserves_coordinate_dtype():
    """Test that stack operation preserves the dtype of coordinates."""
    # Create a dataset with int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # The dtype should be preserved during stack operation
    original_dtype = ds['a'].values.dtype
    stacked_dtype = ds.stack(b=('a',))['a'].values.dtype
    
    # Before the fix, this would be False because dtype would change from 'i4' to 'i8'
    # After the fix, this should be True
    assert original_dtype == stacked_dtype, (
        f"Expected dtype {original_dtype} to be preserved, "
        f"but got {stacked_dtype}"
    )


def test_stack_preserves_various_dtypes():
    """Test that stack operation preserves various dtypes."""
    dtypes_to_test = ['i1', 'i2', 'i4', 'i8', 'u1', 'u2', 'u4', 'u8', 'f4', 'f8']
    
    for dtype in dtypes_to_test:
        # Create a dataset with coordinate of specific dtype
        ds = xr.Dataset(coords={'a': np.array([0, 1, 2], dtype=dtype)})
        
        # The dtype should be preserved during stack operation
        original_dtype = ds['a'].values.dtype
        stacked_dtype = ds.stack(b=('a',))['a'].values.dtype
        
        assert original_dtype == stacked_dtype, (
            f"Expected dtype {original_dtype} to be preserved for dtype {dtype}, "
            f"but got {stacked_dtype}"
        )