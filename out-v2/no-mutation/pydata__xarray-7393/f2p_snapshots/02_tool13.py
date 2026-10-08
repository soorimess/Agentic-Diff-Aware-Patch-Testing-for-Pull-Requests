import numpy as np
import pytest
import xarray as xr


def test_stack_coordinate_dtype_preservation():
    """Test that stack preserves the dtype of coordinates.
    
    Regression test for issue where stack casts int32 dtype coordinate to int64.
    """
    # Create a dataset with int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # The original coordinate should be int32
    original_dtype = ds['a'].values.dtype
    assert original_dtype == np.int32
    
    # After stacking, the dtype should be preserved
    stacked = ds.stack(b=('a',))
    stacked_dtype = stacked['a'].values.dtype
    
    # This should be True, but was False before the fix
    assert original_dtype == stacked_dtype


def test_stack_multiple_coordinate_dtypes():
    """Test that stack preserves dtypes for multiple coordinates."""
    # Test with different integer dtypes
    for dtype_str in ['i1', 'i2', 'i4', 'i8']:
        ds = xr.Dataset(coords={'a': np.array([0, 1], dtype=dtype_str)})
        original_dtype = ds['a'].values.dtype
        
        # Stack the coordinate
        stacked = ds.stack(b=('a',))
        stacked_dtype = stacked['a'].values.dtype
        
        # Dtype should be preserved
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype_str}"


def test_stack_float_coordinate_dtypes():
    """Test that stack preserves float coordinate dtypes."""
    # Test with different float dtypes
    for dtype_str in ['f4', 'f8']:
        ds = xr.Dataset(coords={'a': np.array([0.0, 1.0], dtype=dtype_str)})
        original_dtype = ds['a'].values.dtype
        
        # Stack the coordinate
        stacked = ds.stack(b=('a',))
        stacked_dtype = stacked['a'].values.dtype
        
        # Dtype should be preserved
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype_str}"