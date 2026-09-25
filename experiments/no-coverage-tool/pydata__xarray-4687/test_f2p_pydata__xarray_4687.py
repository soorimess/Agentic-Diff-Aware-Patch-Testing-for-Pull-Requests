"""
Regression test for xr.where not preserving attributes.

This tests the specific behaviors mentioned in the bug report:
1. xr.where loses attributes (should preserve them like DataArray.where)
2. xr.where changes dtype (should preserve original dtype)
3. Missing keep_attrs parameter (should accept it after fix)
"""

import numpy as np
import xarray as xr


def test_where_attributes_preserved():
    """Test that attributes are preserved by xr.where (like DataArray.where)"""
    # Create DataArray with attributes exactly like in bug report
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"

    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # This assertion will pass after the fix and fail before the fix
    # Before fix: result.attrs == {} (attributes dropped)
    # After fix: result.attrs == data.attrs (attributes preserved)  
    assert result.attrs == data.attrs, f"Attributes not preserved: expected {data.attrs}, got {result.attrs}"


def test_where_dtype_preserved():
    """Test that dtype is preserved by xr.where"""
    # Create DataArray with specific dtype
    data = xr.DataArray(np.ones([5, 5], dtype=np.int8))
    original_dtype = data.dtype
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # This assertion will pass after the fix and fail before the fix
    # Before fix: result.dtype == np.int64 (dtype changed)  
    # After fix: result.dtype == original_dtype (dtype preserved)
    assert result.dtype == original_dtype, f"Dtype not preserved: expected {original_dtype}, got {result.dtype}"


def test_where_keep_attrs_parameter():
    """Test that keep_attrs parameter is accepted"""
    # This test looks for when the parameter exists
    data = xr.DataArray(np.ones([5, 5]))
    data.attrs["test"] = "value"
    
    try:
        # Try using keep_attrs parameter - should work after fix
        result = xr.where(data == 1, 5, 0, keep_attrs=True)
        # If we get here, the parameter works
        assert result is not None
    except TypeError as e:
        if "unexpected keyword argument 'keep_attrs'" in str(e):
            # This is expected in the current buggy version
            pytest.fail("keep_attrs parameter not implemented yet - this test should pass after fix")
        else:
            raise  # Some other type error, re-raise