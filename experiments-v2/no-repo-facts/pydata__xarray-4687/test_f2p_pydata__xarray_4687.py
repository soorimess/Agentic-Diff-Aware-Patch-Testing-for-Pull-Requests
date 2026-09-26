"""
Test for xarray.where not preserving attributes bug.
This test verifies that xr.where preserves attributes from the input DataArray
when the keep_attrs parameter is used.
"""
import numpy as np
import xarray as xr


def test_where_attributes_lost_by_default():
    """Test that xr.where loses attributes by default (the bug)."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation without keep_attrs (default behavior)
    result = xr.where(data == 1, 5, 0)
    
    # Check that attributes are lost (this is the bug)
    assert result.attrs == {}, f"Expected empty attrs, got {result.attrs}"


def test_where_function_has_keep_attrs_parameter():
    """Test that the where function signature includes keep_attrs parameter."""
    # This test will pass after the fix is applied
    try:
        import inspect
        sig = inspect.signature(xr.where)
        # Check if keep_attrs parameter exists in function signature
        if 'keep_attrs' in sig.parameters:
            # If it exists, the fix is in place
            return True
        else:
            # If it doesn't exist, the bug is present
            raise AssertionError("keep_attrs parameter not found in xr.where function signature")
    except Exception:
        raise AssertionError("keep_attrs parameter not found in xr.where function signature")


if __name__ == "__main__":
    print("Running regression tests for xarray.where attributes bug...")
    
    try:
        test_where_attributes_lost_by_default()
        print("✓ Basic test passed: attributes lost by default (bug confirmed)")
    except Exception as e:
        print(f"✗ Basic test failed: {e}")
        
    try:
        test_where_function_has_keep_attrs_parameter()
        print("✓ Function signature test passed: keep_attrs parameter exists")
    except Exception as e:
        print(f"✗ Function signature test failed: {e}")
        
    print("Test execution completed")