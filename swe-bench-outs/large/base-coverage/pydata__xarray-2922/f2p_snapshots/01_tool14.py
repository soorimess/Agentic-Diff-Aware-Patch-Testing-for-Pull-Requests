"""
Test for the weighted average functionality added in the pull request.

This test verifies that DataArray and Dataset objects now have a `weighted` method
that can be used to perform weighted operations.
"""

import numpy as np
import pytest
import xarray as xr


def test_dataarray_weighted_method_exists():
    """Test that DataArray has a weighted method."""
    da = xr.DataArray([1, 2, 3], dims=['x'])
    assert hasattr(da, 'weighted')
    assert callable(getattr(da, 'weighted'))


def test_dataset_weighted_method_exists():
    """Test that Dataset has a weighted method."""
    ds = xr.Dataset({'a': ('x', [1, 2, 3])}, coords={'x': [0, 1, 2]})
    assert hasattr(ds, 'weighted')
    assert callable(getattr(ds, 'weighted'))


def test_weighted_method_returns_weighted_object():
    """Test that the weighted method returns a Weighted object."""
    da = xr.DataArray([1, 2, 3], dims=['x'])
    weights = xr.DataArray([0.5, 1.0, 1.5], dims=['x'])
    
    weighted_obj = da.weighted(weights)
    # The exact class name might vary, but it should be a Weighted object
    assert hasattr(weighted_obj, 'sum')
    assert hasattr(weighted_obj, 'mean')
    assert hasattr(weighted_obj, 'sum_of_weights')


def test_weighted_sum_basic():
    """Test basic weighted sum functionality."""
    da = xr.DataArray([1, 2, 3], dims=['x'])
    weights = xr.DataArray([0.5, 1.0, 1.5], dims=['x'])
    
    weighted_obj = da.weighted(weights)
    
    # Test that we can call sum on the weighted object
    result = weighted_obj.sum()
    # Should compute (1*0.5 + 2*1.0 + 3*1.5) = 0.5 + 2.0 + 4.5 = 7.0
    expected = 7.0
    assert result.values == expected


def test_weighted_mean_basic():
    """Test basic weighted mean functionality."""
    da = xr.DataArray([1, 2, 3], dims=['x'])
    weights = xr.DataArray([0.5, 1.0, 1.5], dims=['x'])
    
    weighted_obj = da.weighted(weights)
    
    # Test that we can call mean on the weighted object
    result = weighted_obj.mean()
    # Should compute (1*0.5 + 2*1.0 + 3*1.5) / (0.5 + 1.0 + 1.5) = 7.0 / 3.0 = 2.333...
    expected = 7.0 / 3.0
    assert result.values == expected


def test_dataset_weighted_sum():
    """Test weighted sum on Dataset."""
    ds = xr.Dataset({'a': ('x', [1, 2, 3]), 'b': ('x', [4, 5, 6])}, coords={'x': [0, 1, 2]})
    weights = xr.DataArray([0.5, 1.0, 1.5], dims=['x'])
    
    weighted_obj = ds.weighted(weights)
    
    # Test that we can call sum on the weighted object
    result = weighted_obj.sum()
    # Should compute weighted sum for each variable
    assert 'a' in result
    assert 'b' in result
    assert result['a'].values == 7.0  # 1*0.5 + 2*1.0 + 3*1.5
    assert result['b'].values == 16.0  # 4*0.5 + 5*1.0 + 6*1.5


def test_weighted_sum_with_dim():
    """Test weighted sum with specific dimension."""
    da = xr.DataArray(np.random.rand(2, 3), dims=['x', 'y'])
    weights = xr.DataArray(np.random.rand(3), dims=['y'])
    
    weighted_obj = da.weighted(weights)
    
    # Test sum along specific dimension
    result = weighted_obj.sum(dim='y')
    assert result.dims == ('x',)
    assert result.shape == (2,)


def test_weighted_mean_with_dim():
    """Test weighted mean with specific dimension."""
    da = xr.DataArray(np.random.rand(2, 3), dims=['x', 'y'])
    weights = xr.DataArray(np.random.rand(3), dims=['y'])
    
    weighted_obj = da.weighted(weights)
    
    # Test mean along specific dimension
    result = weighted_obj.mean(dim='y')
    assert result.dims == ('x',)
    assert result.shape == (2,)


def test_weighted_invalid_weights():
    """Test that invalid weights raise appropriate errors."""
    da = xr.DataArray([1, 2, 3], dims=['x'])
    # Test with non-DataArray weights
    with pytest.raises(ValueError, match="`weights` must be a DataArray"):
        da.weighted([0.5, 1.0, 1.5])
    
    # Test with weights containing NaN
    weights_with_nan = xr.DataArray([0.5, np.nan, 1.5], dims=['x'])
    with pytest.raises(ValueError, match="`weights` cannot contain missing values"):
        da.weighted(weights_with_nan)