"""
Regression test for xr.where not preserving attributes.
"""
import numpy as np
import xarray as xr


def test_where_preserves_attributes():
    """Test that xr.where preserves attributes from the input DataArray."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # This should pass after fix, fails before fix
    assert result.attrs == data.attrs


def test_where_dtype_preservation():
    """Test that xr.where preserves dtype of input DataArray."""
    # Create a DataArray with specific dtype
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # This should pass after fix, fails before fix
    assert result.dtype == data.dtype