import xarray as xr
import numpy as np

def test_variable_setitem_coercing_types_with_values_property():
    """Test that Variable.__setitem__ does not coerce types on objects with values property.
    
    This is a regression test for the bug where objects with a 'values' attribute 
    would have their 'values' extracted instead of being stored as-is.
    """
    # Create test arrays
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This should work correctly - good_indexed should store the set() object
    good_indexed.loc[{'dim_0': 0}] = set()
    
    # This is the problematic case - bad_indexed should store the HasValues object,
    # but due to the bug it stores HasValues.values (which is 5) instead
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # The bug causes bad_indexed.values[0] to be the integer 5 instead of a HasValues instance
    # Check that we have the actual HasValues object, not its .values attribute
    assert isinstance(bad_indexed.values[0], HasValues), f"Expected HasValues instance, got {type(bad_indexed.values[0])}"
    
    # The incorrect behavior would make bad_indexed.values[0] == 5 instead of a HasValues object
    # This assertion should fail if the problem exists, and pass after it's fixed
    assert bad_indexed.values[0].values == 5, "The HasValues object should have values=5 attribute"
    
    # Test what happens with a simple case that should obviously work
    # The good case that works fine
    good_indexed.loc[{'dim_0': 0}] = set()
    assert isinstance(good_indexed.values[0], set), "set should be stored as-is"