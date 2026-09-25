import numpy as np
import xarray as xr


def test_where_preserves_attributes_by_default():
    """Test that xr.where preserves attributes by default."""
    # Create DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # Before fix: result.attrs would be {} (attributes lost)
    # After fix: result.attrs should contain the attributes from data  
    assert result.attrs == data.attrs


def test_where_dtype_preservation():
    """Test that xr.where preserves dtype (from bug report)."""
    # Create DataArray with specific dtype 
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # Dtype should be preserved, not changed to int64
    assert result.dtype == np.int8