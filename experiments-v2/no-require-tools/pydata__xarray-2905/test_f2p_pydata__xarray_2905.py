import numpy as np
import pandas as pd
import pytest

import xarray as xr


def test_variable_setitem_objects_with_values_property_stored_as_is():
    """Test that objects with values property are stored as-is, not their .values attribute.
    
    This is a regression test for the bug where objects with a 'values' property
    were having their .values attribute extracted instead of being stored as-is.
    
    Before the fix, this would incorrectly store the integer 5 instead of the HasValues instance.
    """
    # Create DataArray to test the behavior
    da = xr.DataArray([None])
    
    class HasValues(object):
        values = 5
    
    # Test assignment with object that has values property
    da.loc[{'dim_0': 0}] = HasValues()
    
    # Check that the HasValues instance is stored, not its .values attribute
    result = da.values
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.object_
    assert len(result) == 1
    
    # This assertion should pass after the fix - the object should be stored as-is
    # Before the fix, result[0] would be the integer 5, not a HasValues instance
    stored_object = result[0]
    assert isinstance(stored_object, HasValues), f"Expected HasValues instance, got {type(stored_object)}"
    
    # Verify the object is the right one
    assert stored_object.values == 5  # The HasValues instance has values=5


def test_variable_setitem_pandas_objects_extract_values():
    """Test that pandas objects still get their .values extracted (preserves existing behavior).
    
    This ensures the fix doesn't break existing pandas functionality.
    """
    # Create a simple array to avoid shape issues
    da = xr.DataArray([0.0])  # Single element array
    
    # Create a pandas Series with values
    series = pd.Series([1, 2, 3])
    da.loc[{'dim_0': 0}] = series
    
    # This should extract the values from the pandas Series
    result = da.values
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.object_
    assert len(result) == 1
    # The pandas Series values should be extracted and stored
    assert np.array_equal(result[0], [1, 2, 3])


def test_variable_setitem_with_regular_objects():
    """Test that regular objects without values property still work."""
    da = xr.DataArray([None])
    
    # Create a regular object without values property
    class RegularObject:
        def __init__(self, value):
            self.value = value
    
    obj = RegularObject(42)
    da.loc[{'dim_0': 0}] = obj
    
    # Should store the object itself
    result = da.values
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.object_
    assert len(result) == 1
    assert result[0] is obj