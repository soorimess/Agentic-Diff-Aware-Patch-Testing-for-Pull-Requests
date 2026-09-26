"""
Regression test for issue where Variable.__setitem__ coerces types on objects 
with a values property.

This test ensures that objects with a 'values' attribute are stored as-is 
during setitem operations, rather than having their 'values' attribute 
extracted and stored instead.
"""
import numpy as np
import xarray as xr


def test_setitem_preserves_objects_with_values_property():
    """
    Test that objects with values property are not coerced to their values.
    
    Before the fix, this would store array([5], dtype=object) instead of 
    array([<HasValues instance>], dtype=object).
    """
    # Create test arrays as per the bug report example
    bad_indexed = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This assignment should store the HasValues object itself, not its .values attribute
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # The bug: values[0] was 5 (the .values attribute) instead of the HasValues object
    # After fix: values[0] should be the HasValues instance
    stored_object = bad_indexed.values[0]
    
    # Verify it's the actual object, not the .values attribute
    assert isinstance(stored_object, HasValues), f"Expected HasValues instance, got {type(stored_object)}"
    assert stored_object.values == 5  # The values property should still be accessible


def test_setitem_stores_exact_object_instance():
    """
    Test that the exact same object instance is stored.
    """
    arr = xr.DataArray([None])
    
    class HasValues(object):
        values = 5
    
    # Create and store an object
    obj = HasValues()
    arr.loc[{'dim_0': 0}] = obj
    
    # The stored object should be the exact same instance
    assert arr.values[0] is obj
    assert isinstance(arr.values[0], HasValues)
    assert arr.values[0].values == 5