"""
Regression test for issue where Variable.__setitem__ coerces types 
on objects with a values property.

This test verifies that objects with a 'values' property are not 
coerced to their 'values' attribute when assigned to a DataArray.
"""

import numpy as np
import xarray as xr


def test_variable_setitem_with_values_property():
    """Test that objects with values property are not coerced to their values."""
    # Reproduce the exact bug scenario from the issue
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # Test the assignment - this should work the same way for both
    good_indexed[0] = set()
    bad_indexed[0] = HasValues()

    # The good case should store the set object
    assert isinstance(good_indexed.values[0], set)
    
    # The bad case should store the HasValues instance, not its .values attribute
    # Before the fix, this incorrectly returned 5 (the .values attribute)
    # After the fix, this should return the HasValues instance
    assert isinstance(bad_indexed.values[0], HasValues)
    assert bad_indexed.values[0].values == 5