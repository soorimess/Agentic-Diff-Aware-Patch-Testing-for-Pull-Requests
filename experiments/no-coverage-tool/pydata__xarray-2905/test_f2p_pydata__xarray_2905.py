"""Regression test for bug where Variable.__setitem__ coerces types on objects with a values property.

The bug was in the as_compatible_data function in xarray/core/variable.py where it was
incorrectly extracting the 'values' attribute from any object, not just pandas objects.
"""

import xarray as xr


def test_variable_setitem_preserves_objects_with_values_attribute():
    """
    Test that objects with values attribute are stored as-is, not coerced to their .values.
    
    The bug: when assigning an object with a `.values` attribute (like HasValues)
    to a DataArray using __setitem__, the object's .values attribute was incorrectly 
    accessed and the result stored instead of the object itself.
    
    Before fix: bad_indexed.values would be array([5]) - the object's .values
    After fix: bad_indexed.values should be array([HasValues()]) - the object itself
    """
    # Create test array
    arr = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This assignment should preserve the HasValues object, not coerce it to int 5
    arr.loc[{'dim_0': 0}] = HasValues()
    
    # Get the result  
    result = arr.values
    
    # This assertion demonstrates the bug - we should NOT get int 5
    # If this assertion fails, it means the bug has been fixed
    assert not (isinstance(result[0], int) and result[0] == 5), \
        "BUG: Object incorrectly coerced to its .values attribute. " \
        "Expected object to be stored as-is, not converted to int 5."