import numpy as np
import xarray as xr
import pytest


def test_where_attributes_lost_by_default():
    """Test that xr.where currently loses attributes (the bug)."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation - attributes should be lost (this is the bug)
    result = xr.where(data == 1, 5, 0)
    
    # Attributes should be lost in current implementation
    assert result.attrs == {}, "Attributes should be lost by default in current implementation"


def test_where_parameter_not_supported():
    """Test that keep_attrs parameter is not supported - this should fail with TypeError."""
    # Create a DataArray with attributes
    data = xr.DataArray([1, 2, 3])
    data.attrs["test_attr"] = "test_value"
    
    # This will fail with TypeError because keep_attrs parameter doesn't exist
    # The test passes when this specific error occurs (demonstrates the bug)
    with pytest.raises(TypeError, match="unexpected keyword argument.*keep_attrs"):
        xr.where(data > 1, 10, 0, keep_attrs=True)


def test_where_dtype_preservation():
    """Test that xr.where does not preserve dtype (mentioned in bug report)."""
    # Create a DataArray with specific dtype
    data = xr.DataArray(np.ones([5, 5], dtype=np.int8))
    data.attrs["test_attr"] = "test"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # The dtype should change from int8 to int64 (numpy behavior)
    # This is mentioned as a secondary issue in the bug report
    assert result.dtype == np.int64, "Result dtype should be int64 due to numpy behavior"