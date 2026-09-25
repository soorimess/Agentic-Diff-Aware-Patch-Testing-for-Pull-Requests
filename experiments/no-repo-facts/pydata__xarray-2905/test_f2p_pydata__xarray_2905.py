"""
Test for regression of bug where Variable.__setitem__ coercing types 
on objects with a values property
"""
import numpy as np
import xarray as xr


def test_variable_setitem_preserves_objects_with_values_property():
    """Test that objects with .values property are stored as-is in DataArray."""
    # Create DataArrays to test with - exactly replicating the bug report
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])
    
    # Create a class with a values property as in the bug report
    class HasValues(object):
        values = 5
    
    # Test assignment of a set (should work correctly)
    good_indexed.loc[{'dim_0': 0}] = set()
    expected_good = np.array([set()], dtype=object)
    # This was working correctly in both old and new versions
    assert np.array_equal(good_indexed.values, expected_good)
    
    # Test assignment of object with values property (this is the bug case)
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # The bug causes this to incorrectly extract the .values attribute 
    # and store array(5) instead of the actual object
    # In old version: bad_indexed.values => array([array(5)], dtype=object) 
    # In fixed version: bad_indexed.values => array([<HasValues instance>], dtype=object)
    assert isinstance(bad_indexed.values[0], HasValues), f"Expected HasValues instance, got {type(bad_indexed.values[0])}"
    assert bad_indexed.values[0].values == 5


def test_variable_setitem_preserves_objects_without_values_property():
    """Test that objects without .values property still work as expected."""
    da = xr.DataArray([None])
    
    class RegularObject:
        def __init__(self):
            self.data = "test"
    
    obj = RegularObject()
    da.loc[{'dim_0': 0}] = obj
    
    # Should store the full object
    assert isinstance(da.values[0], RegularObject)
    assert da.values[0].data == "test"