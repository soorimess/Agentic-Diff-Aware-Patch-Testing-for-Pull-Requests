"""
Regression test for bug where Variable.__setitem__ coerces types on objects 
with a values property.

This test should fail on the buggy version and pass on the fixed version.
"""
import numpy as np
import xarray as xr


def test_variable_setitem_preserves_objects_with_values_property():
    """Test that objects with values property are not coerced during assignment."""
    # Create test arrays
    bad_indexed = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This should store the HasValues object, not extract its .values attribute
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # Check that the HasValues object was stored, not its .values attribute
    stored_value = bad_indexed.values[0]
    
    # In the buggy version, stored_value will be 5 (the .values attribute)
    # In the fixed version, stored_value will be the HasValues object
    # The test passes if we have the HasValues object (the fix is working)
    # The test fails if we have the int 5 (the bug is present)
    
    # If it's an int with value 5, the bug is present
    if isinstance(stored_value, int) and stored_value == 5:
        # This test is designed to fail on buggy version, pass on fixed version
        # So we raise an assertion error to indicate the bug is present
        assert False, "Bug present: object's .values attribute was extracted instead of the object itself"
    
    # If we get here, it should be the HasValues object
    assert isinstance(stored_value, HasValues)
    assert stored_value.values == 5