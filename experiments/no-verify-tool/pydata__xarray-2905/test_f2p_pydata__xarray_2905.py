"""
Regression test for bug where Variable.__setitem__ was coercing types
on objects with a values property.

This test ensures that when assigning objects with a 'values' attribute
to DataArray locations, the actual object is stored rather than its
.values property being extracted.
"""

import numpy as np
import xarray as xr


def test_object_with_values_property_stored_as_is():
    """Test that objects with values property are stored as the object itself."""
    
    # Create data arrays
    arr = xr.DataArray([None])
    
    class HasValues(object):
        values = 5
    
    # Assign object with values property
    arr.loc[{'dim_0': 0}] = HasValues()
    
    # The object should be stored as-is, not its .values attribute
    # In the broken version, this was array([5], dtype=object) 
    # In the correct version, this should be array([<HasValues instance>], dtype=object)
    
    stored_value = arr.values[0]
    
    # Should be the HasValues object, not the value 5
    assert isinstance(stored_value, HasValues), f"Expected HasValues instance, got {type(stored_value)}"
    assert stored_value.values == 5


def test_pandas_objects_still_extract_values():
    """Test that pandas objects still extract their .values attribute correctly."""
    
    import pandas as pd
    
    arr = xr.DataArray([None])
    
    # Test with pandas Series (should extract values)
    series = pd.Series([1, 2, 3])
    arr.loc[{'dim_0': 0}] = series
    
    # Should extract the .values from pandas objects (not the Series itself)
    stored_value = arr.values[0] 
    expected = np.array([1, 2, 3])
    np.testing.assert_array_equal(stored_value, expected)


def test_multiple_objects_with_values():
    """Test multiple objects with values property."""
    
    arr = xr.DataArray([None, None])
    
    class Obj1(object):
        values = "first"
    
    class Obj2(object):
        values = "second"
        
    obj1 = Obj1()
    obj2 = Obj2()
    
    arr.loc[{'dim_0': 0}] = obj1
    arr.loc[{'dim_0': 1}] = obj2
    
    # Both objects should be stored as-is
    stored1 = arr.values[0]
    stored2 = arr.values[1]
    
    assert isinstance(stored1, Obj1)
    assert isinstance(stored2, Obj2) 
    assert stored1.values == "first"
    assert stored2.values == "second"