"""
Regression test for bug where stack casts int32 dtype coordinate to int64.

This test ensures that when stacking coordinates, the dtype is preserved
and not automatically cast to a larger dtype like int64 from int32.
"""

import numpy as np
import xarray as xr


def test_stack_preserves_dtype():
    """Test that stack preserves the dtype of coordinates."""
    # Create a dataset with an int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # Stack the coordinate
    stacked = ds.stack(b=('a',))
    
    # The dtype should be preserved (int32), not cast to int64
    original_dtype = ds['a'].values.dtype
    stacked_dtype = stacked['a'].values.dtype
    
    # This should be True but was False before the fix
    assert original_dtype == stacked_dtype, f"Expected {original_dtype}, got {stacked_dtype}"


def test_stack_preserves_various_dtypes():
    """Test that stack preserves various dtypes."""
    # Test different integer dtypes
    for dtype in ['i1', 'i2', 'i4', 'i8']:
        ds = xr.Dataset(coords={'a': np.array([0], dtype=dtype)})
        stacked = ds.stack(b=('a',))
        original_dtype = ds['a'].values.dtype
        stacked_dtype = stacked['a'].values.dtype
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype}: expected {original_dtype}, got {stacked_dtype}"
    
    # Test float dtypes
    for dtype in ['f4', 'f8']:
        ds = xr.Dataset(coords={'a': np.array([0.0], dtype=dtype)})
        stacked = ds.stack(b=('a',))
        original_dtype = ds['a'].values.dtype
        stacked_dtype = stacked['a'].values.dtype
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype}: expected {original_dtype}, got {stacked_dtype}"