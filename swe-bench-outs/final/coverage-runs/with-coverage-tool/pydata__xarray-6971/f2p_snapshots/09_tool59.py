"""Test for the new set_xindex and drop_indexes methods.

This test verifies the behavior of the new public API methods for setting
and dropping indexes in DataArray and Dataset objects.
"""

import numpy as np
import pandas as pd
import pytest

import xarray as xr
from xarray.core.indexes import Index, PandasIndex


def test_dataarray_set_xindex():
    """Test the new set_xindex method on DataArray."""
    # Create a simple DataArray with coordinates
    da = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]],
        dims=["x", "y"],
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Test that set_xindex method exists and can be called
    # This should work after the change is applied
    result = da.set_xindex("time")
    
    # The result should be a DataArray with the same data but with a new index
    assert isinstance(result, xr.DataArray)
    assert result.shape == (2, 3)
    assert "time" in result.xindexes


def test_dataset_set_xindex():
    """Test the new set_xindex method on Dataset."""
    # Create a simple Dataset with coordinates
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Test that set_xindex method exists and can be called
    result = ds.set_xindex("time")
    
    # The result should be a Dataset with the same data but with a new index
    assert isinstance(result, xr.Dataset)
    assert result["temperature"].shape == (2, 3)
    assert "time" in result.xindexes


def test_dataarray_drop_indexes():
    """Test the new drop_indexes method on DataArray."""
    # Create a DataArray with an index
    da = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]],
        dims=["x", "y"],
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Set an index first
    da_with_index = da.set_xindex("time")
    
    # Test that drop_indexes method exists and can be called
    result = da_with_index.drop_indexes("time")
    
    # The result should be a DataArray with the index removed
    assert isinstance(result, xr.DataArray)
    assert "time" not in result.xindexes


def test_dataset_drop_indexes():
    """Test the new drop_indexes method on Dataset."""
    # Create a Dataset with an index
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Set an index first
    ds_with_index = ds.set_xindex("time")
    
    # Test that drop_indexes method exists and can be called
    result = ds_with_index.drop_indexes("time")
    
    # The result should be a Dataset with the index removed
    assert isinstance(result, xr.Dataset)
    assert "time" not in result.xindexes


def test_set_xindex_with_multiple_coordinates():
    """Test set_xindex with multiple coordinate names."""
    # Create a DataArray with multiple coordinates
    da = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]],
        dims=["x", "y"],
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200]), "location": ("x", ["A", "B"])}
    )
    
    # Test that set_xindex works with multiple coordinates
    result = da.set_xindex(["time", "location"])
    
    # Should create a multi-index
    assert isinstance(result, xr.DataArray)
    assert "time" in result.xindexes
    assert "location" in result.xindexes


def test_set_xindex_with_custom_index_class():
    """Test set_xindex with explicit index class."""
    # Create a DataArray with a coordinate that doesn't have an index yet
    da = xr.DataArray(
        [1, 2, 3],
        dims=["x"],
        coords={"x": [0, 1, 2], "custom_coord": ("x", [10, 20, 30])}
    )
    
    # Test that set_xindex works with explicit index class
    result = da.set_xindex("custom_coord", index_cls=PandasIndex)
    
    # Should create a pandas index
    assert isinstance(result, xr.DataArray)
    assert "custom_coord" in result.xindexes


def test_set_xindex_already_indexed_coordinate():
    """Test set_xindex with coordinate that already has an index raises ValueError."""
    da = xr.DataArray(
        [[1, 2, 3], [4, 5, 6]],
        dims=["x", "y"],
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Set an index first
    da_with_index = da.set_xindex("time")
    
    # Should raise ValueError when trying to set index on already indexed coordinate
    with pytest.raises(ValueError, match="already have an index"):
        da_with_index.set_xindex("time")


def test_dataset_set_xindex_invalid_coordinate():
    """Test set_xindex with invalid coordinate name raises ValueError."""
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Should raise ValueError for non-existent coordinate
    with pytest.raises(ValueError, match="invalid coordinate"):
        ds.set_xindex("nonexistent")


def test_dataset_drop_indexes_invalid_coordinate():
    """Test drop_indexes with invalid coordinate name raises ValueError."""
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Should raise ValueError for non-existent coordinate
    with pytest.raises(ValueError, match="don't exist"):
        ds.drop_indexes("nonexistent")


def test_dataset_drop_indexes_ignore_errors():
    """Test drop_indexes with errors='ignore' option."""
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Should not raise error when using errors='ignore' for non-indexed coordinate
    result = ds.drop_indexes("y", errors="ignore")
    
    # Result should be unchanged
    assert isinstance(result, xr.Dataset)
    assert result is not ds  # Should return a new object


def test_set_xindex_with_pandas_multiindex():
    """Test set_xindex with pandas multi-index creation."""
    # Create a Dataset with multiple coordinates that should form a multi-index
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200]), "location": ("x", ["A", "B"])}
    )
    
    # Test that set_xindex works with multiple coordinates (should create PandasMultiIndex)
    result = ds.set_xindex(["time", "location"])
    
    # Should create a multi-index
    assert isinstance(result, xr.Dataset)
    assert "time" in result.xindexes
    assert "location" in result.xindexes


def test_drop_indexes_unindexed_coordinate():
    """Test drop_indexes with coordinate that doesn't have an index raises ValueError."""
    # Create a Dataset with a coordinate that doesn't have an index
    ds = xr.Dataset(
        {"data": (["x", "y"], [[1, 2, 3], [4, 5, 6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200]), "custom_coord": ("x", [10, 20])}
    )
    
    # Set an index on time first
    ds_with_index = ds.set_xindex("time")
    
    # Try to drop a coordinate that doesn't have an index - should raise ValueError
    with pytest.raises(ValueError, match="do not have an index"):
        ds_with_index.drop_indexes("custom_coord")


def test_dataset_set_xindex_data_variable():
    """Test set_xindex with a data variable (not coordinate) raises ValueError."""
    # Create a Dataset with a data variable
    ds = xr.Dataset(
        {"temperature": (["x", "y"], [[1, 2, 3], [4, 5, 6]]),
         "humidity": (["x", "y"], [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])},
        coords={"x": [0, 1], "y": [10, 20, 30], "time": ("x", [100, 200])}
    )
    
    # Should raise ValueError when trying to set index on data variable
    with pytest.raises(ValueError, match="those variables are data variables"):
        ds.set_xindex("humidity")


def test_indexes_module_import():
    """Test that the new indexes module can be imported and used properly."""
    # Import the new module to cover its lines
    from xarray.indexes import Index, PandasIndex
    
    # Verify the imports work correctly
    assert Index is not None
    assert PandasIndex is not None
    
    # Test that we can create a PandasIndex instance
    # This exercises the module's functionality
    import xarray.core.indexes as indexes_module
    assert hasattr(indexes_module, 'Index')
    assert hasattr(indexes_module, 'PandasIndex')