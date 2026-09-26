"""
Regression test for bug where Variable.__setitem__ coerces types 
on objects with a values property.

This test ensures that objects with a 'values' attribute are not 
incorrectly coerced to their .values property during assignment.
"""

import numpy as np
import xarray as xr


def test_objects_with_values_property_preserved():
    """Test that objects with values property are stored as-is, not coerced to .values"""
    
    # Create a DataArray
    da = xr.DataArray([None])
    
    # Define a class with a values property (this SHOULD be preserved as-is)
    class HasValues(object):
        values = 5
    
    # This assignment should store the HasValues object itself
    # In the buggy version, it gets coerced to the .values property (5)
    da.loc[{'dim_0': 0}] = HasValues()
    
    # The bug: we get int(5) instead of HasValues object
    # This test should pass in the fixed version and fail in the buggy version
    assert isinstance(da.values[0], HasValues), "Object with .values property should be preserved as-is"
    assert da.values[0].values == 5, "The .values property should still be accessible"