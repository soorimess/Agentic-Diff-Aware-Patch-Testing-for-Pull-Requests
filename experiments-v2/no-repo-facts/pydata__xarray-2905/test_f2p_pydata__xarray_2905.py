import numpy as np
import xarray as xr


def test_variable_setitem_coercing_types():
    """Test for bug where Variable.__setitem__ coerces types on objects with values property."""
    
    # Create test array
    bad_indexed = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This is where the bug occurs - setitem with an object that has a values property
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    
    # Check the behavior
    # Before the fix: bad_indexed.values would be array([array(5)], dtype=object) 
    # After the fix: bad_indexed.values should be array([<__main__.HasValues instance>], dtype=object)
    
    # The correct behavior is that the HasValues object should be stored as-is
    # not coerced to its .values attribute (which is 5)
    assert isinstance(bad_indexed.values[0], HasValues), f"Expected HasValues instance, got {type(bad_indexed.values[0])}"
    assert bad_indexed.values[0].values == 5  # The original values attribute should be preserved