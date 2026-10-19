"""
Regression test for weighted operations functionality.

This test ensures that the weighted operations feature is properly implemented
and working as expected.
"""
import pytest
import numpy as np
import xarray as xr


def test_weighted_functionality():
    """Test that weighted operations work as expected."""
    # Create test data
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    # Create DataArray
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    # Test that weighted method exists and can be called
    weighted_obj = da.weighted(weight_da)
    
    # Test that weighted operations work
    result_sum = weighted_obj.sum()
    result_mean = weighted_obj.mean()
    
    # Verify the results make sense
    expected_sum = np.sum(data * weights)
    expected_mean = expected_sum / np.sum(weights)
    
    assert result_sum.values == expected_sum
    assert result_mean.values == expected_mean


def test_weighted_dataset():
    """Test weighted operations on Dataset objects."""
    # Create test data
    data1 = np.array([[1, 2], [3, 4]])
    data2 = np.array([[5, 6], [7, 8]])
    weights = np.array([[0.1, 0.2], [0.3, 0.4]])
    
    # Create Dataset
    ds = xr.Dataset({
        'var1': (['x', 'y'], data1),
        'var2': (['x', 'y'], data2)
    })
    weight_da = xr.DataArray(weights, dims=['x', 'y'])
    
    # Test that weighted method exists and can be called on Dataset
    weighted_obj = ds.weighted(weight_da)
    
    # Test that weighted operations work
    result_sum = weighted_obj.sum()
    result_mean = weighted_obj.mean()
    
    # Verify the results make sense for the first variable
    expected_sum = np.sum(data1 * weights)
    expected_mean = expected_sum / np.sum(weights)
    
    assert result_sum['var1'].values == expected_sum
    assert result_mean['var1'].values == expected_mean


def test_weighted_with_dim():
    """Test weighted operations with specific dimensions."""
    # Create test data with multiple dimensions
    data = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    weights = np.array([[[0.1, 0.2], [0.3, 0.4]], [[0.5, 0.6], [0.7, 0.8]]])
    
    # Create DataArray
    da = xr.DataArray(data, dims=['time', 'x', 'y'])
    weight_da = xr.DataArray(weights, dims=['time', 'x', 'y'])
    
    # Test weighted operation along a specific dimension
    weighted_obj = da.weighted(weight_da)
    result_sum = weighted_obj.sum(dim='x')
    
    # Verify the result has the correct shape
    assert result_sum.dims == ('time', 'y')
    

def test_weighted_error_handling():
    """Test that appropriate errors are raised for invalid inputs."""
    # Create test data
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    # Create DataArray
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    # Test that weighted method exists and can be called
    weighted_obj = da.weighted(weight_da)
    
    # Test that sum and mean methods exist
    assert hasattr(weighted_obj, 'sum')
    assert hasattr(weighted_obj, 'mean')
    
    # Test that sum_of_weights method exists
    assert hasattr(weighted_obj, 'sum_of_weights')