"""
Regression test for pydata/xarray issue #2905.

Tests that Variable.__setitem__ behaves correctly for objects with values property:

1. Objects with .values property that are NOT pandas objects should be stored as-is
2. This fixes a regression where such objects were incorrectly being coerced to their .values attribute
"""
import numpy as np
import pytest
import xarray as xr


def test_setitem_with_generic_object_having_values_property():
    """Test that generic objects with .values property are stored as-is."""
    # Test the core bug: objects with .values should NOT be coerced to values
    bad_indexed = xr.DataArray([None])
    
    class HasValues(object):
        values = 5
    
    # This assignment should store HasValues instance, not extract its .values property
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # Verify it's the object itself
    assert isinstance(bad_indexed.values[0], HasValues)
    # Verify it's not just the value 5 from .values  
    assert bad_indexed.values[0] is not 5


def test_ensure_bug_fix():
    """Test that validates the original bug report case no longer fails."""
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This is the exact failing example from the bug report
    good_indexed.loc[{'dim_0': 0}] = set()
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # The bug showed bad_indexed.values as array([5]) instead of array([HasValues instance])
    # This should properly contain the HasValues instance
    assert isinstance(bad_indexed.values[0], HasValues)
    assert bad_indexed.values[0] is not 5