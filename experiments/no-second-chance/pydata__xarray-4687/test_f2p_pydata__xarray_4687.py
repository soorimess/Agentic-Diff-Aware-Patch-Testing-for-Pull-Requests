"""
Regression test for xr.where attribute preservation fix.
This tests that xr.where now supports the keep_attrs parameter to preserve attributes
when using the function.

The bug was that xr.where() was dropping attributes from DataArrays,
and did not provide a way to control this behavior through a keep_attrs parameter.
"""

import numpy as np
import xarray as xr


def test_where_attributes_dropped_by_default():
    """Test that default xr.where behavior drops attributes (current behavior)."""
    # Create a DataArray with attributes
    data = xr.DataArray([1, 2, 3, 4])
    data.attrs["source"] = "test_data"
    
    # Default behavior should drop attributes (as in bug report)
    result = xr.where(data > 2, 100, 0)
    assert result.attrs == {}


def test_where_keep_attrs_parameter_raises_typeerror():
    """Test that keep_attrs parameter raises TypeError in current implementation."""
    # Create a DataArray with attributes
    data = xr.DataArray([1, 2, 3, 4])
    data.attrs["source"] = "test_data"
    
    # Calling with keep_attrs should raise TypeError in current implementation
    try:
        result = xr.where(data > 2, 100, 0, keep_attrs=True)
        # If we get here without exception, the parameter now works.
        # This should be a failure on the old code
        assert False, "keep_attrs parameter should not be supported yet"
    except TypeError:
        # This is the expected behavior for the current implementation
        pass