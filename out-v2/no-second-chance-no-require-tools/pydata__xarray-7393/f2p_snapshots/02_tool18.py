import numpy as np
import xarray as xr


def test_stack_preserves_dtype():
    """Test that stack preserves the dtype of coordinates."""
    # Create a dataset with int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # Stack the coordinate
    stacked = ds.stack(b=('a',))
    
    # The dtype should be preserved
    original_dtype = ds['a'].values.dtype
    stacked_dtype = stacked['a'].values.dtype
    
    # This should be True, but was False before the fix
    assert original_dtype == stacked_dtype, f"Expected {original_dtype}, got {stacked_dtype}"


def test_stack_preserves_various_dtypes():
    """Test that stack preserves various dtypes."""
    dtypes_to_test = ['i1', 'i2', 'i4', 'i8', 'u1', 'u2', 'u4', 'u8', 'f4', 'f8']
    
    for dtype in dtypes_to_test:
        # Create a dataset with coordinate of specific dtype
        ds = xr.Dataset(coords={'a': np.array([0, 1, 2], dtype=dtype)})
        
        # Stack the coordinate
        stacked = ds.stack(b=('a',))
        
        # The dtype should be preserved
        original_dtype = ds['a'].values.dtype
        stacked_dtype = stacked['a'].values.dtype
        
        assert original_dtype == stacked_dtype, f"Failed for dtype {dtype}: expected {original_dtype}, got {stacked_dtype}"