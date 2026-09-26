import numpy as np
import xarray as xr


def test_where_attributes_dropped():
    """Test that xr.where drops attributes (the bug)."""
    # Create a DataArray with attributes as described in the bug report
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"

    result = xr.where(data == 1, 5, 0)
    
    # Bug: attributes should be preserved but are dropped
    # This test verifies the buggy behavior exists
    assert result.attrs == {}, f"Attributes should be dropped (bug) but got {result.attrs}"


def test_where_dtype_not_preserved():
    """Test that xr.where does not preserve dtype (the bug)."""
    # Create a DataArray with specific dtype
    data = xr.DataArray(np.ones([5, 5], dtype=np.int8))
    data.attrs["test_attr"] = "test_value"
    
    result = xr.where(data == 1, 5, 0)
    
    # Bug: dtype should be preserved but becomes int64
    assert result.dtype == np.int64, f"Dtype should be preserved but got {result.dtype}"


def test_where_keep_attrs_parameter_missing():
    """Test that the keep_attrs parameter is missing in current implementation."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([3, 3], dtype=np.int32))
    data.attrs["attr1"] = "value1"
    
    # This should fail with current implementation (no keep_attrs parameter)
    try:
        result = xr.where(data == 1, 5, 0, keep_attrs=True)
        # If we get here, the parameter exists (fix is applied)
        assert False, "keep_attrs parameter should not exist in current version"
    except TypeError:
        # This is expected with the buggy code - parameter doesn't exist
        # Test passes to show the bug exists
        pass