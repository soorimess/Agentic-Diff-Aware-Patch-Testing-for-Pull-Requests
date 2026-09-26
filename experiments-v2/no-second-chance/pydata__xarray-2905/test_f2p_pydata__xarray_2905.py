import numpy as np
import xarray as xr


def test_variable_setitem_coercing_types():
    """
    Regression test for xarray issue #2905.
    
    Variable.__setitem__ was coercing types on objects with a values property.
    
    Before fix: User objects with 'values' attribute were incorrectly coerced
    After fix:  User objects with 'values' attribute are stored as-is
    
    This test fails on current code (demonstrating the bug) and passes after fix.
    """
    
    # Test case from the bug report
    bad_indexed = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This assignment should store the HasValues object, not coerce it to values=5
    bad_indexed.loc[{'dim_0': 0}] = HasValues()

    # The assertion that currently fails but should pass after fix
    assert isinstance(bad_indexed.values[0], HasValues)
    assert bad_indexed.values.dtype == np.dtype(object)