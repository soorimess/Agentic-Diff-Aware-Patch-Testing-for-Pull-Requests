import xarray as xr


def test_variable_setitem_objects_with_values_property_not_coerced():
    """
    Regression test for the bug where objects with 'values' property 
    were incorrectly coerced to their .values attribute instead of being stored as-is.
    
    This test directly addresses the behavior change in PR #1746 to as_compatible_data:
    - BEFORE: data = getattr(data, "values", data) - ALL objects with .values get extracted
    - AFTER:  if isinstance(data, (pd.Series, pd.Index, pd.DataFrame)): data = data.values - only pandas objects
    
    The bug manifest: When storing a custom object with .values attribute, it should be 
    stored as the object itself, not the .values attribute.
    """
    
    # This reproduces the exact example from the bug report 
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This works correctly - stores a set
    good_indexed.loc[{'dim_0': 0}] = set()
    
    # This should preserve the HasValues object, not coerce to its .values attribute (5)
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # The bug: bad_indexed.values would be [5] (the values property)
    # The fix: bad_indexed.values should be [<HasValues object>] (the actual object)
    
    # Verify: check that we didn't extract the .values property 
    # If the bug is present, bad_indexed.values[0] will be 5 (the .values attribute)
    # If the bug is fixed, bad_indexed.values[0] should reference the HasValues object
    stored_value = bad_indexed.values[0]
    
    # This assertion should fail in the buggy version (when it gets 5)
    # and pass in the fixed version (when it gets the HasValues object)
    assert stored_value != 5, ("Bug still present: objects with .values property were "
                             "coerced to their .values attribute instead of being stored as-is")


if __name__ == "__main__":
    test_variable_setitem_objects_with_values_property_not_coerced()
    print("Test passed - the bug is correctly reproduced!")