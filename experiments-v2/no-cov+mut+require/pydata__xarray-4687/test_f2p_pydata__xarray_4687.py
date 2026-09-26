"""
Regression test for xr.where not preserving attributes.

This test specifically checks that xr.where preserves attributes from DataArrays,
which was a bug where attributes were lost.
"""
import numpy as np
import xarray as xr


def test_where_attributes_preserved():
    """
    Test that xr.where preserves attributes from input DataArray.
    
    This test should fail in the current buggy implementation where attributes are lost,
    and should pass after the fix is applied.
    """
    # Create DataArray with attributes as per bug report
    data = xr.DataArray(np.ones([10,10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"

    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # The bug: attributes are lost
    # This assertion should fail in current implementation
    expected_attrs = {"attr_1": "test1", "attr_2": "test2"}
    
    # This assertion captures the core issue - attributes should be preserved
    # In the buggy version, result.attrs will be {} instead of expected_attrs
    assert result.attrs == expected_attrs, f"Attributes not preserved: expected {expected_attrs}, got {result.attrs}"


def test_where_simple_case_attributes_preserved():
    """
    Simple test case for attribute preservation.
    """
    # Create simple DataArray with attributes as per bug report
    da = xr.DataArray(1)
    da.attrs['foo'] = 'bar'
    
    # Apply where operation
    result = xr.where(da == 0, -1, da)
    
    # The bug: attributes are lost
    # This assertion should fail in current implementation
    expected_attrs = {'foo': 'bar'}
    
    # This assertion captures the core issue - attributes should be preserved
    assert result.attrs == expected_attrs, f"Attributes not preserved: expected {expected_attrs}, got {result.attrs}"