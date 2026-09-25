"""
Regression test for issue where Variable.__setitem__ coerces types 
on objects with a values property.

This test ensures that objects with 'values' attributes are not 
coerced to their .values attribute when they are not pandas objects.
"""
import numpy as np
import xarray as xr


def test_objects_with_values_attribute_preserve_identity():
    """
    Test that objects with 'values' attribute are not automatically coerced.
    
    Before fix: HasValues() with values=5 would be stored as 5
    After fix: HasValues() with values=5 should be stored as HasValues instance
    
    This test confirms the behavior described in issue pydata/xarray#2905.
    """
    # Create test array  
    arr = xr.DataArray([None])
    
    class HasValues(object):
        values = 5
    
    # This should store the HasValues instance, not extract its values attribute
    arr.loc[{'dim_0': 0}] = HasValues()
    
    # If this assertion fails, it demonstrates the bug:
    # The HasValues object was incorrectly coerced to its .values attribute
    assert isinstance(arr.values[0], HasValues), (
        "Object with .values attribute was coerced to its .values instead of "
        f"preserving the object. Got {type(arr.values[0])}, expected HasValues instance"
    )
    assert arr.values[0].values == 5