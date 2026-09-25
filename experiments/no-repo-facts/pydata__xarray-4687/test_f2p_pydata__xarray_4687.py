import numpy as np
import xarray as xr


def test_where_preserves_attributes():
    """Test that xr.where preserves attributes from the second argument."""
    # Create a DataArray with attributes
    data = xr.DataArray(np.ones([10, 10], dtype=np.int8))
    data.attrs["attr_1"] = "test1"
    data.attrs["attr_2"] = "test2"
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # Check that attributes are preserved
    assert result.attrs == data.attrs, f"Expected {data.attrs}, got {result.attrs}"


def test_where_preserves_dtype():
    """Test that xr.where preserves dtype."""
    # Create a DataArray with specific dtype  
    data = xr.DataArray(np.ones([5, 5], dtype=np.int8))
    original_dtype = data.dtype
    
    # Apply where operation
    result = xr.where(data == 1, 5, 0)
    
    # Check that dtype is preserved
    assert result.dtype == original_dtype, f"Expected {original_dtype}, got {result.dtype}"


def test_where_with_more_complex_attributes():
    """Test xr.where with more complex attribute structures."""
    # Create a DataArray with more complex attributes
    data = xr.DataArray([1, 2, 3, 4, 5], dims="x")
    data.attrs["test_attr"] = "test_value"
    data.attrs["numeric_attr"] = 42
    data.attrs["list_attr"] = [1, 2, 3]
    
    # Apply where operation  
    cond = data > 2
    result = xr.where(cond, data * 2, 0)
    
    # Check that attributes are preserved
    assert result.attrs == data.attrs, f"Expected {data.attrs}, got {result.attrs}"


def test_where_dataset_attributes():
    """Test that xr.where preserves Dataset attributes."""
    # Create a Dataset with attributes
    ds = xr.Dataset({"var1": ("x", [1, 2, 3])})
    ds.attrs["dataset_attr"] = "dataset_value"
    ds["var1"].attrs["variable_attr"] = "variable_value"
    
    # Apply where operation
    cond = ds["var1"] > 1
    result = xr.where(cond, ds["var1"] * 2, 0)
    
    # Check that dataset attributes are preserved
    assert result.attrs == ds.attrs, f"Expected {ds.attrs}, got {result.attrs}"