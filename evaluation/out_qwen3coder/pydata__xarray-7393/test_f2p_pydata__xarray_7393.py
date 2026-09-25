import numpy as np
import xarray as xr


def test_stack_int32_coordinate_dtype_preserved():
    """Test that reproduces the exact bug from the issue report.
    
    The bug: stack casts int32 dtype coordinate to int64
    Expected: result should be True, not False
    """
    # Exact code from bug report
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    result = ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype
    
    # This should be True but was False before the fix
    assert result, "int32 dtype should be preserved when stacking"


def test_stack_preserves_various_dtypes():
    """Test that stacking preserves all integer dtypes."""
    # Test various integer dtypes that were affected
    dtypes_to_test = ['i1', 'i2', 'i4', 'i8']
    
    for dtype in dtypes_to_test:
        ds = xr.Dataset(coords={'a': np.array([0, 1, 2], dtype=dtype)})
        stacked = ds.stack(b=('a',))
        
        original_dtype = ds['a'].values.dtype
        stacked_dtype = stacked['a'].values.dtype
        
        assert original_dtype == stacked_dtype, f"dtype {dtype} not preserved"


def test_stack_multiple_coordinates_preserves_dtypes():
    """Test that stacking multiple coordinates preserves their dtypes."""
    ds = xr.Dataset(
        coords={
            'a': np.array([0, 1], dtype='i4'),
            'b': np.array([10, 20], dtype='i2')
        }
    )
    
    stacked = ds.stack(c=('a', 'b'))
    
    # Both coordinates should maintain their original dtypes
    assert ds['a'].values.dtype == stacked['a'].values.dtype
    assert ds['b'].values.dtype == stacked['b'].values.dtype