"""
Regression test for issue #2905: Variable.__setitem__ coercing types on objects 
with a values property.
"""
import numpy as np
import xarray as xr


def test_setitem_with_user_object_having_values_property():
    """Test that user objects with a 'values' property are stored as-is, not their .values attribute."""
    # Create DataArrays
    good_indexed = xr.DataArray([None])
    bad_indexed = xr.DataArray([None])

    # Define a class with a 'values' property (user object)
    class HasValues(object):
        values = 5
    
    # Test the assignment
    good_indexed.loc[{'dim_0': 0}] = set()
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # The good case should store the set
    assert isinstance(good_indexed.values[0], set)
    
    # The bad case should store the HasValues instance, not its .values attribute (5)
    # Before the fix, this would incorrectly store array([5]) instead of the object
    assert isinstance(bad_indexed.values[0], HasValues)
    assert not isinstance(bad_indexed.values[0], np.ndarray)
    assert bad_indexed.values[0].values == 5  # The .values attribute should be accessible


def test_setitem_with_user_object_having_values_property_in_dataset():
    """Test that user objects with a 'values' property work correctly in Dataset context."""
    # Create a Dataset
    ds = xr.Dataset({'var': ('time', [None, None])})
    
    # Define a class with a 'values' property (user object)
    class HasValues(object):
        values = 5
    
    # Test assignment to dataset
    ds['var'].loc[{'time': 0}] = HasValues()
    
    # Should store the HasValues instance, not its .values attribute
    assert isinstance(ds['var'].values[0], HasValues)
    assert ds['var'].values[0].values == 5