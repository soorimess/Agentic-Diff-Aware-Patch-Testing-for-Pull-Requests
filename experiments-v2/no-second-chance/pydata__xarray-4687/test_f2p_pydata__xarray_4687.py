import numpy as np
import xarray as xr


def test_where_preserves_attributes():
    """Test that xr.where preserves attributes from the second argument."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"

    # Apply where operation - attributes should be preserved
    result = xr.where(data == 1, 5, 0)
    
    # This test demonstrates the bug: attributes are currently lost
    assert result.attrs == data.attrs


def test_where_preserves_dtype():
    """Test that xr.where preserves dtype."""
    # Create a DataArray with specific dtype
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"

    # Apply where operation - dtype should be preserved
    result = xr.where(data == 1, 5, 0)
    
    # This test demonstrates the bug: dtype is currently changed
    assert result.dtype == data.dtype