"""
Regression test for the bug where Variable.__setitem__ coerces types 
on objects with a values property

This test specifically ensures that objects with a 'values' property 
are preserved as-is during assignment, rather than having their
.values attribute extracted.
"""
import xarray as xr
import numpy as np

def test_variable_setitem_objects_with_values_property():
    """Test that objects with 'values' property are not coerced during assignment."""
    # Create test arrays as described in the bug report
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This should work correctly (no issue with regular set() type)
    good_indexed.loc[{'dim_0': 0}] = set()
    assert isinstance(good_indexed.values[0], set)
    
    # This is where the bug occurs - HasValues has a 'values' attribute
    # that gets incorrectly accessed in the buggy version
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # In the buggy version, this would show 5 (the values attribute) 
    # instead of the actual HasValues instance
    # The correct behavior should preserve the actual object
    assert isinstance(bad_indexed.values[0], HasValues)
    assert not isinstance(bad_indexed.values[0], np.ndarray)
    assert bad_indexed.values[0].values == 5  # Verify we have the right object