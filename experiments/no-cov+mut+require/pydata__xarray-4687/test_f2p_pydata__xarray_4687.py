import numpy as np
import xarray as xr


def test_where_should_preserve_attributes_by_default():
    """
    Test that xr.where preserves attributes from the second argument (x) by default.
    
    Before the fix: attributes are lost (empty dict returned)
    After the fix: attributes should be preserved (same as x.attrs) 
    """
    # Create a DataArray with attributes like the bug report
    data = xr.DataArray(np.ones([10,10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation - attributes should be preserved
    result = xr.where(data == 1, 5, 0)
    
    # This assertion should pass after the fix is applied
    # It should fail before the fix (attributes are lost)
    assert result.attrs == data.attrs


def test_where_dtype_preservation():
    """
    Test that xr.where preserves the dtype of the input data array.
    
    Before the fix: dtype might change (e.g., int8 -> int64) 
    After the fix: dtype should be preserved
    """
    # Create a DataArray with specific dtype
    data = xr.DataArray(np.ones([5,5], dtype=np.int8))
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # This assertion should pass after fix - dtype should be preserved
    assert result.dtype == data.dtype


def test_where_default_behavior_change():
    """
    Test the specific change that the fix introduces.
    
    The change ensures xr.where behaves consistently with DataArray.where and Dataset.where
    by preserving attributes by default from the second argument (x).
    """
    # Create test DataArray with attributes 
    data = xr.DataArray([1, 2, 3], attrs={"source": "test_data"})
    
    # Apply xr.where operation (this is what the fix intends to make consistent) 
    result = xr.where(data > 1, data, 0)
    
    # Before fix: would not preserve attributes (result.attrs would be {})
    # After fix: should preserve attributes from data (result.attrs should be {"source": "test_data"})
    expected_attrs = data.attrs
    assert result.attrs == expected_attrs