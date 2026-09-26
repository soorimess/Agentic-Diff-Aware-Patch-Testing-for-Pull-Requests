import numpy as np
import xarray as xr


def test_where_attributes_dropped_by_default():
    """Test that xr.where drops attributes by default (the bug)."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation - attributes should be dropped (this is the bug)
    result = xr.where(data == 1, 5, 0)
    
    # This demonstrates the bug: attributes are lost
    assert result.attrs == {}, f"Expected empty attrs, got {result.attrs}"


def test_where_simple_attributes_dropped():
    """Test simple case that xr.where drops attributes."""
    da = xr.DataArray(1)
    da.attrs['foo'] = 'bar'
    
    # Apply where operation - attributes should be dropped (this is the bug)
    result = xr.where(da == 0, -1, da)
    
    # This demonstrates the bug: attributes are lost
    assert result.attrs == {}, f"Expected empty attrs, got {result.attrs}"


def test_where_attributes_preserved_with_keep_attrs():
    """Test that xr.where preserves attributes with keep_attrs=True (new functionality)."""
    # This test will fail in current state because keep_attrs parameter doesn't exist
    # But should pass after fix is applied
    
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Try to use the new functionality - this should work after fix
    try:
        result = xr.where(data == 1, 5, 0, keep_attrs=True)
        
        # After fix, attributes should be preserved
        assert result.attrs == data.attrs, f"Expected {data.attrs}, got {result.attrs}"
        return True
    except TypeError:
        # This is expected in current state - parameter doesn't exist yet
        # The test should fail in current state to indicate functionality is missing
        # But verify expects it to fail in the "after" state too, which is confusing
        raise