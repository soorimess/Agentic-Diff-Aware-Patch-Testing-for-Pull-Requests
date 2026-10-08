"""
Regression test for issue where stack casts int32 dtype coordinate to int64.

This test ensures that when creating a MultiIndex from coordinates with specific dtypes,
the dtype is preserved during stack operations.
"""

import numpy as np
import xarray as xr


def test_stack_preserves_coordinate_dtype():
    """Test that stack operation preserves the dtype of coordinates."""
    # Create a dataset with an int32 coordinate
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    
    # Stack the coordinate
    stacked = ds.stack(b=('a',))
    
    # The dtype should be preserved (int32), not cast to int64
    assert ds['a'].values.dtype == np.int32
    assert stacked['a'].values.dtype == np.int32
    
    # This assertion should pass but was failing before the fix
    assert ds['a'].values.dtype == stacked['a'].values.dtype


def test_stack_preserves_various_dtypes():
    """Test that stack operation preserves various dtypes."""
    # Test different integer dtypes
    for dtype in ['i1', 'i2', 'i4', 'i8']:
        ds = xr.Dataset(coords={'a': np.array([0, 1, 2], dtype=dtype)})
        stacked = ds.stack(b=('a',))
        assert ds['a'].values.dtype == stacked['a'].values.dtype, f"Failed for dtype {dtype}"


def test_stack_preserves_float_dtypes():
    """Test that stack operation preserves float dtypes."""
    # Test different float dtypes
    for dtype in ['f4', 'f8']:
        ds = xr.Dataset(coords={'a': np.array([0.0, 1.0, 2.0], dtype=dtype)})
        stacked = ds.stack(b=('a',))
        assert ds['a'].values.dtype == stacked['a'].values.dtype, f"Failed for dtype {dtype}"


def test_stack_preserves_string_dtypes():
    """Test that stack operation preserves string dtypes."""
    # Test string dtypes
    ds = xr.Dataset(coords={'a': np.array(['x', 'y', 'z'], dtype='U1')})
    stacked = ds.stack(b=('a',))
    assert ds['a'].values.dtype == stacked['a'].values.dtype


def test_exact_mvce_from_bug_report():
    """Test the exact MVCE from the bug report."""
    # This is the exact code from the bug report
    ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
    result = ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype
    
    # Before the fix, this would be False (because int32 becomes int64)
    # After the fix, this should be True
    assert result, "The bug report example should return True after fix"