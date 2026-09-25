import numpy as np
import xarray as xr


def test_where_preserves_attributes_from_x():
    """
    Test that xr.where preserves attributes from the second parameter (x) when used with DataArrays.
    
    This test mirrors the bug described where xr.where drops attributes from 
    the input DataArray.
    
    Before fix: result.attrs = {} (empty)
    After fix:  result.attrs = {"test_attr": "test_value"} (preserved)
    """
    # Create a DataArray with attributes as described in bug report
    data = xr.DataArray(np.ones([3, 3], dtype=np.int8))
    data.attrs["test_attr"] = "test_value"

    # Apply where operation  
    result = xr.where(data == 1, 5, 0)
    
    # This assertion demonstrates the behavior that should change:
    # - Currently fails because attributes are not preserved (bug)
    # - Should pass after fix is applied
    expected_attrs = {"test_attr": "test_value"}
    assert result.attrs == expected_attrs, (
        f"Attributes not preserved by xr.where(). "
        f"Expected {expected_attrs}, but got {result.attrs}"
    )