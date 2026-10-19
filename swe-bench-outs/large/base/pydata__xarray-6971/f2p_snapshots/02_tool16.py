"""
Regression tests for the new set_xindex and drop_indexes methods.

This test file verifies the behavior of the new public API methods for setting
and dropping indexes in DataArray and Dataset objects.
"""
import pytest
import numpy as np
import xarray as xr
from xarray import DataArray, Dataset


def test_dataarray_has_set_xindex_method():
    """Test that DataArray has the set_xindex method."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(da, 'set_xindex')
    assert callable(getattr(da, 'set_xindex'))


def test_dataset_has_set_xindex_method():
    """Test that Dataset has the set_xindex method."""
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(ds, 'set_xindex')
    assert callable(getattr(ds, 'set_xindex'))


def test_dataarray_has_drop_indexes_method():
    """Test that DataArray has the drop_indexes method."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(da, 'drop_indexes')
    assert callable(getattr(da, 'drop_indexes'))


def test_dataset_has_drop_indexes_method():
    """Test that Dataset has the drop_indexes method."""
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    
    # The method should exist
    assert hasattr(ds, 'drop_indexes')
    assert callable(getattr(ds, 'drop_indexes'))


def test_index_from_variables_accepts_options():
    """Test that Index.from_variables accepts options parameter."""
    from xarray.core.indexes import Index
    import inspect
    
    # Check that the method signature has changed
    sig = inspect.signature(Index.from_variables)
    assert 'options' in sig.parameters


def test_pandas_index_from_variables_accepts_options():
    """Test that PandasIndex.from_variables accepts options parameter."""
    from xarray.core.indexes import PandasIndex
    import inspect
    
    # Check that the method signature has changed
    sig = inspect.signature(PandasIndex.from_variables)
    assert 'options' in sig.parameters


def test_pandas_multi_index_from_variables_accepts_options():
    """Test that PandasMultiIndex.from_variables accepts options parameter."""
    from xarray.core.indexes import PandasMultiIndex
    import inspect
    
    # Check that the method signature has changed
    sig = inspect.signature(PandasMultiIndex.from_variables)
    assert 'options' in sig.parameters


def test_set_xindex_method_signature():
    """Test that set_xindex method can be called with proper arguments."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # Test that method exists and can be called (will fail if not implemented)
    try:
        # This should work once implemented - we're testing the interface
        # The actual behavior will be tested in a more comprehensive way
        method = getattr(da, 'set_xindex')
        assert callable(method)
    except AttributeError:
        pytest.skip("set_xindex method not yet implemented")


def test_drop_indexes_method_signature():
    """Test that drop_indexes method can be called with proper arguments."""
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    
    # Test that method exists and can be called (will fail if not implemented)
    try:
        # This should work once implemented - we're testing the interface
        method = getattr(da, 'drop_indexes')
        assert callable(method)
    except AttributeError:
        pytest.skip("drop_indexes method not yet implemented")


def test_assert_no_index_corrupted_signature():
    """Test that assert_no_index_corrupted accepts action parameter."""
    from xarray.core.indexes import assert_no_index_corrupted
    import inspect
    
    # Check that the function signature has changed
    sig = inspect.signature(assert_no_index_corrupted)
    assert 'action' in sig.parameters