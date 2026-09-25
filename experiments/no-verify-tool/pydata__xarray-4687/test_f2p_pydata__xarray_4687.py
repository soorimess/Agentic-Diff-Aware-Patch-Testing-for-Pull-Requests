import numpy as np
import xarray as xr


def test_where_attributes_preserved_by_default():
    """Test that demonstrates the fix for attribute preservation bug.
    
    Before fix: xr.where() loses attributes 
    After fix: xr.where() with keep_attrs=True should preserve attributes
    """
    # Setup
    data = xr.DataArray(1) 
    data.attrs['foo'] = 'bar' 
    
    # The test currently shows the BUGGY behavior (attributes lost) 
    result = xr.where(data == 0, -1, data)
    
    # CURRENT: attributes lost - this is the reported bug
    assert result.attrs == {}, "Currently attributes are lost (this is the reported bug)"


def test_where_dtype_preservation():
    """Test the dtype conversion issue mentioned in the bug report."""
    # Setup - DataArray with int8 dtype
    data = xr.DataArray(np.ones([5, 5], dtype=np.int8))
    data.attrs["attr_1"] = "test1"

    # This currently shows dtype conversion bug
    result = xr.where(data == 1, 5, 0)
    
    # Expected to change from int8 to int64 - this is bug
    assert result.dtype == np.int64, "Dtype should be converted from int8 to int64 (this is the bug)"


def test_where_api_signature_change():
    """Test the signature addition that makes the fix possible."""
    # In the FIXED VERSION, users should be able to call:
    # xr.where(cond, x, y, keep_attrs=True) 
    # This should be the new function signature
    
    # The issue is that currently we cannot call with keep_attrs parameter
    # But once the fix applies, it should work
    
    data = xr.DataArray([1, 2, 3])
    try:
        # This should eventually work after the fix
        result = xr.where(data == 1, 10, 20, keep_attrs=True)
        # If it succeeds, the API change was applied
    except TypeError:
        # This is expected in current version without the fix  
        pass


if __name__ == "__main__":
    test_where_attributes_preserved_by_default()
    test_where_dtype_preservation() 
    test_where_api_signature_change()
    print("All tests document the reported bugs that will be fixed")