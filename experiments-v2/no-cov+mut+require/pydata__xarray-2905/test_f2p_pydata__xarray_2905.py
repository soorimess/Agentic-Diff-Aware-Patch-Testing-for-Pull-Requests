import numpy as np
import pytest
import xarray as xr


def test_variable_setitem_coercing_types_with_values_property():
    """Test that objects with values property are not coerced to their values attribute."""
    # Create DataArrays with None values - this is the exact example from the bug report
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # Test the assignment that was broken
    good_indexed.loc[{'dim_0': 0}] = set()
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # The good case should store the set
    assert isinstance(good_indexed.values[0], set)
    
    # The bad case should store the HasValues instance, not its .values attribute (5)
    # Before the fix, this would incorrectly store array([5]) instead of the HasValues object
    # This is the core assertion that should pass after the fix
    assert isinstance(bad_indexed.values[0], HasValues)
    assert bad_indexed.values[0].values == 5


def test_variable_setitem_preserves_object_with_values_property():
    """Test that objects with values property are stored as-is in object arrays."""
    # Create DataArray with object dtype by creating it with object data
    # Use a more direct approach to create object array
    da = xr.DataArray([None], dims=['dim_0'])
    
    class CustomObject:
        values = "some_value"
        def __init__(self, value):
            self.value = value
    
    obj = CustomObject("test_value")
    
    # This assignment should store the object itself, not its .values attribute
    da.loc[{'dim_0': 0}] = obj
    
    # Should store the actual object, not the .values attribute
    stored_obj = da.values[0]
    assert isinstance(stored_obj, CustomObject)
    assert stored_obj.value == "test_value"
    assert stored_obj.values == "some_value"