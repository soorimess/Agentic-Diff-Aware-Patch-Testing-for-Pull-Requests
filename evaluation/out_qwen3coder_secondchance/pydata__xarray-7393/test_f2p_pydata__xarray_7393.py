"""
Regression test for stack casting int32 dtype coordinate to int64.

This test ensures that stacking coordinates maintains their original dtype.
"""
import numpy as np
import xarray as xr


def test_stack_preserves_dtype_int32():
    """Test that stack operation preserves int32 dtype of coordinates."""
    # Create dataset with int32 coordinate (the exact case from the bug report)
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # Stack the coordinate 
    result = ds.stack(b=('a',))
    
    # The dtype should be preserved (i4) not cast to i8 (int64)
    original_dtype = ds['a'].values.dtype
    stacked_dtype = result['a'].values.dtype
    
    # This should be True, but was False before the fix 
    assert original_dtype == stacked_dtype, f"Expected {original_dtype}, got {stacked_dtype}"


def test_stack_preserves_dtype_multiple_coordinates():
    """Test that multiple stacked coordinates preserve their dtypes."""
    # Create dataset with int32 coordinates
    ds = xr.Dataset(coords={
        'a': np.array([0, 1], dtype='i4'),
        'b': np.array([2, 3], dtype='i4')
    })
    
    # Stack both coordinates
    result = ds.stack(c=('a', 'b'))
    
    # Both dtypes should be preserved
    assert ds['a'].values.dtype == result['a'].values.dtype
    assert ds['b'].values.dtype == result['b'].values.dtype


def test_stack_preserves_various_dtypes():
    """Test that stack preserves various dtypes (not just int32)."""
    dtypes_to_test = ['i1', 'i2', 'i4', 'i8', 'u1', 'u2', 'u4', 'u8', 'f4', 'f8']
    
    for dtype in dtypes_to_test:
        ds = xr.Dataset(coords={'a': np.array([0], dtype=dtype)})
        result = ds.stack(b=('a',))
        
        original_dtype = ds['a'].values.dtype
        stacked_dtype = result['a'].values.dtype
        
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype}: expected {original_dtype}, got {stacked_dtype}"