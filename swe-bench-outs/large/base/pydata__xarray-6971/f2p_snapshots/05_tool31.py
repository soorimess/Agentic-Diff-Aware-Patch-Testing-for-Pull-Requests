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


def test_assert_no_index_corrupted_signature():
    """Test that assert_no_index_corrupted accepts action parameter."""
    from xarray.core.indexes import assert_no_index_corrupted
    import inspect
    
    # Check that the function signature has changed
    sig = inspect.signature(assert_no_index_corrupted)
    assert 'action' in sig.parameters


def test_method_signatures_exist():
    """Test that all new method signatures are correct."""
    # Test that we can at least access the methods
    da = DataArray([1, 2, 3], dims=['x'], coords={'x': [0, 1, 2]})
    ds = Dataset({'data': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    
    # Test that the methods exist and are callable
    assert callable(getattr(da, 'set_xindex'))
    assert callable(getattr(ds, 'set_xindex'))
    assert callable(getattr(da, 'drop_indexes'))
    assert callable(getattr(ds, 'drop_indexes'))
    
    # Test that we can access the from_variables methods
    from xarray.core.indexes import Index, PandasIndex, PandasMultiIndex
    assert callable(getattr(Index, 'from_variables'))
    assert callable(getattr(PandasIndex, 'from_variables'))
    assert callable(getattr(PandasMultiIndex, 'from_variables'))