"""
Regression test for issue: Variable.__setitem__ coercing types on objects with a values property

Test that verifies when an object with a .values attribute is assigned to a DataArray,
the object itself should be stored (not the .values attribute). This was the bug where
all objects with .values were getting coerced, including non-pandas objects.

This test should:
1. Pass with the fix in place (correct behavior)
2. Fail with the bug present (incorrect behavior)
"""

import numpy as np
import xarray as xr


def test_object_with_values_property_preserved():
    """Objects with .values attributes should be stored as-is, not their .values."""
    # Create an array
    arr = xr.DataArray([None])
    
    # Define an object with a values attribute (this should NOT be coerced)
    class MyObject:
        values = "some_value"
    
    # Store the object 
    obj = MyObject()
    arr.loc[{'dim_0': 0}] = obj
    
    # In the buggy code, this would store "some_value" (obj.values) 
    # In the correct code, this should store the MyObject instance
    stored = arr.values[0]
    
    # This assertion shows the fix is in place:
    # It demonstrates that we properly store the object instead of coercing to its .values
    assert isinstance(stored, MyObject), f"Expected MyObject instance, got {type(stored)}"
    assert stored.values == "some_value"
    

def test_exact_bug_report_case():
    """Test using the exact case from the bug report."""
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This should correctly store a set
    good_indexed.loc[{'dim_0': 0}] = set()
    
    # This should store the HasValues object, not coerce to 5
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # Verify correct case
    assert isinstance(good_indexed.values[0], set)
    
    # Verify that bug case is fixed - the object should be stored, not coerced
    stored_obj = bad_indexed.values[0]
    
    # The OLD BUG: stored_obj would be 5 (the .values attribute)
    # The FIXED behavior: stored_obj should be a HasValues instance  
    assert isinstance(stored_obj, HasValues)  # This is what should happen
    # When the bug is present, this will fail


def test_functional_behavior():
    """Verify the concrete behavior described in the bug report."""
    # Exact reproduction from bug report
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    good_indexed.loc[{'dim_0': 0}] = set()
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # correct behavior
    assert isinstance(good_indexed.values[0], set)
    
    # BEFORE the fix, this would have been array([array(5)])
    # AFTER the fix, this should be array([< HasValues instance>])
    
    # Test that we preserve the object instead of its .values
    stored_bad = bad_indexed.values[0] 
    assert isinstance(stored_bad, HasValues)
    
    # The instance should have the values attribute accessible
    assert stored_bad.values == 5