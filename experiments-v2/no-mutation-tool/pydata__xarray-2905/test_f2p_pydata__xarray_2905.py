import numpy as np
import pandas as pd
import xarray as xr


def test_variable_setitem_preserves_objects_with_values_property():
    """Test that objects with values property are not coerced to their values.
    
    This is a regression test for the bug where objects with a 'values' property
    were being incorrectly coerced when assigned to DataArray locations.
    """
    # Create test array
    arr = xr.DataArray([None])

    class HasValues(object):
        values = 5
    
    # This should preserve the HasValues object, not coerce it to its values property
    arr.loc[{'dim_0': 0}] = HasValues()
    
    # The bug was that this would return 5 (the values property) instead of the HasValues instance
    # After fix, it should return the HasValues instance
    assert isinstance(arr.values[0], HasValues)
    assert arr.values[0].values == 5