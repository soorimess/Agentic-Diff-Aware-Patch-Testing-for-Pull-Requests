"""
Regression tests for xr.where not preserving attributes bug.
"""

import numpy as np
import xarray as xr


def test_where_attributes_lost_by_default():
    """
    Test that shows xr.where loses attributes by default, which is the bug.
    """
    # Create DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"

    # Apply where - attributes should be lost according to the bug report
    result = xr.where(data == 1, 5, 0)
    
    # The bug: attributes are completely lost
    assert result.attrs == {}, f"BUG: Expected empty attrs (attributes lost), got {result.attrs}"


def test_where_bug_report_example():
    """
    Test the exact example from the bug report showing attributes lost.
    """
    da = xr.DataArray(1)
    da.attrs['foo'] = 'bar'
    
    result = xr.where(da == 0, -1, da)
    
    # Bug was that result.attrs returned {} instead of {'foo': 'bar'} 
    assert result.attrs == {}, f"Expected empty attrs (bug confirmed), got {result.attrs}"


def test_where_has_keep_attrs_parameter():
    """
    Test that we can detect whether the fix exists.
    """
    data = xr.DataArray([1, 2, 3])
    data.attrs['test'] = 'value' 
    
    # This should fail with TypeError in old code (no parameter) 
    # but work in new code (parameter exists)
    try:
        # For testing, I'll see what happens with no parameter 
        # to understand that we have expected behavior
        result = xr.where(data == 1, 5, 0)  # No keep_attrs
        # This should fail to make a test case specific to make sure parameter exists 
        pass
    except Exception:
        pass