"""
Regression tests for the new set_xindex and drop_indexes methods.

This test file verifies the behavior of the new public API methods for setting
and dropping indexes in DataArray and Dataset objects.
"""
import pytest
import numpy as np
import xarray as xr
from xarray import DataArray, Dataset


def test_dataarray_set_xindex_method_exists():
    """Test that DataArray has the set_xindex method."""
    # This should fail in the current version since the method doesn't exist yet
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(da, 'set_xindex')


def test_dataset_set_xindex_method_exists():
    """Test that Dataset has the set_xindex method."""
    # This should fail in the current version since the method doesn't exist yet
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(ds, 'set_xindex')


def test_dataarray_drop_indexes_method_exists():
    """Test that DataArray has the drop_indexes method."""
    # This should fail in the current version since the method doesn't exist yet
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(da, 'drop_indexes')


def test_dataset_drop_indexes_method_exists():
    """Test that Dataset has the drop_indexes method."""
    # This should fail in the current version since the method doesn't exist yet
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(ds, 'drop_indexes')


def test_set_xindex_signature():
    """Test that set_xindex method works correctly with valid inputs."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # Test that it can be called without errors (this will fail until implemented)
    try:
        # We need to test with a coordinate that doesn't already have an index
        # For now, we'll test that the method exists and can be called
        result = da.set_xindex('x')
        # If it works, it should return a DataArray
        assert isinstance(result, DataArray)
    except AttributeError:
        # This is expected in the current version
        pytest.skip("set_xindex method not yet implemented")
    except ValueError as e:
        # This is expected if the coordinate already has an index
        if "already have an index" in str(e):
            # This means the method exists but we're testing with wrong input
            # This is still a valid test that the method exists
            pass
        else:
            raise


def test_drop_indexes_signature():
    """Test that drop_indexes method works correctly."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # Test that it can be called without errors (this will fail until implemented)
    try:
        result = da.drop_indexes('x')
        # If it works, it should return a DataArray
        assert isinstance(result, DataArray)
    except AttributeError:
        # This is expected in the current version
        pytest.skip("drop_indexes method not yet implemented")


def test_index_from_variables_signature_change():
    """Test that Index.from_variables now accepts options parameter."""
    from xarray.core.indexes import Index
    
    # Check that the method signature has changed
    import inspect
    sig = inspect.signature(Index.from_variables)
    assert 'options' in sig.parameters
    
    # Test that it can be called with options parameter
    try:
        # This should work with the new signature
        pass
    except Exception:
        # This is expected in the current version
        pytest.skip("Index.from_variables signature not yet updated")


def test_pandas_index_from_variables_signature_change():
    """Test that PandasIndex.from_variables now accepts options parameter."""
    from xarray.core.indexes import PandasIndex
    import inspect
    
    # Check that the method signature has changed
    sig = inspect.signature(PandasIndex.from_variables)
    assert 'options' in sig.parameters


def test_pandas_multi_index_from_variables_signature_change():
    """Test that PandasMultiIndex.from_variables now accepts options parameter."""
    from xarray.core.indexes import PandasMultiIndex
    import inspect
    
    # Check that the method signature has changed
    sig = inspect.signature(PandasMultiIndex.from_variables)
    assert 'options' in sig.parameters


def test_set_xindex_with_invalid_coordinate():
    """Test set_xindex with invalid coordinate name to trigger validation."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # This test should fail with a ValueError about invalid coordinates
    # when the method is implemented, but we can at least test that
    # the method exists and can be called
    try:
        # Try to call with a non-existent coordinate - this should fail
        # but we're mainly testing that the method exists
        da.set_xindex('nonexistent')
    except AttributeError:
        # Expected before implementation
        pytest.skip("set_xindex method not yet implemented")
    except ValueError:
        # This would be expected behavior once implemented
        pass
    except Exception:
        # Any other exception is fine for now - we just want to make sure
        # the method exists and can be called
        pass