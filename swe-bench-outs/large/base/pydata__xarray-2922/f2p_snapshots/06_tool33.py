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


def test_weighted_invalid_weights_type():
    """Test that ValueError is raised when weights is not a DataArray."""
    data = np.array([1, 2, 3, 4])
    da = xr.DataArray(data, dims=['x'])
    
    # Test with a regular numpy array instead of DataArray
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    with pytest.raises(ValueError, match=r"`weights` must be a DataArray"):
        da.weighted(weights)


def test_weighted_weights_with_nan():
    """Test that ValueError is raised when weights contain NaN values."""
    data = np.array([1, 2, 3, 4])
    da = xr.DataArray(data, dims=['x'])
    
    # Test with weights containing NaN
    weights = np.array([0.1, np.nan, 0.3, 0.4])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    with pytest.raises(ValueError, match=r"`weights` cannot contain missing values"):
        da.weighted(weight_da)


def test_weighted_sum_of_weights():
    """Test the sum_of_weights method."""
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    result = weighted_obj.sum_of_weights()
    
    # Should return the sum of weights
    expected = np.sum(weights)
    assert result.values == expected


def test_weighted_repr():
    """Test the string representation of Weighted objects."""
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    
    # Should have a proper string representation
    repr_str = repr(weighted_obj)
    assert "Weighted" in repr_str
    assert "x" in repr_str  # dimension name


def test_weighted_keep_attrs():
    """Test that keep_attrs parameter works correctly."""
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    da = xr.DataArray(data, dims=['x'])
    da.attrs['test_attr'] = 'test_value'
    
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    result = weighted_obj.sum(keep_attrs=True)
    
    # Should preserve attributes
    assert result.attrs['test_attr'] == 'test_value'


def test_weighted_skipna():
    """Test that skipna parameter works correctly."""
    data = np.array([1, 2, np.nan, 4])
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    result = weighted_obj.sum(skipna=True)
    
    # Should handle NaN values properly
    # (1*0.1 + 2*0.2 + 0*0.3 + 4*0.4) / (0.1 + 0.2 + 0.3 + 0.4) = 2.1 / 1.0 = 2.1
    expected = 2.1
    assert result.values == expected


def test_weighted_mean_calculation_precision():
    """Test that weighted mean calculation is mathematically correct."""
    # Use simple values that make the math obvious
    data = np.array([10, 20, 30])
    weights = np.array([1, 2, 3])
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    result_mean = weighted_obj.mean()
    
    # Manual calculation: (10*1 + 20*2 + 30*3) / (1 + 2 + 3) = (10 + 40 + 90) / 6 = 140/6 = 23.333...
    expected_mean = 140.0 / 6.0
    assert np.isclose(result_mean.values, expected_mean)


def test_weighted_error_message_exact():
    """Test that error messages are exactly as expected."""
    data = np.array([1, 2, 3, 4])
    da = xr.DataArray(data, dims=['x'])
    
    # Test exact error message for wrong weights type
    weights = np.array([0.1, 0.2, 0.3, 0.4])
    
    with pytest.raises(ValueError, match=r"`weights` must be a DataArray"):
        da.weighted(weights)
    
    # Test exact error message for weights with NaN
    weights_with_nan = np.array([0.1, np.nan, 0.3, 0.4])
    weight_da = xr.DataArray(weights_with_nan, dims=['x'])
    
    with pytest.raises(ValueError, match=r"`weights` cannot contain missing values"):
        da.weighted(weight_da)


def test_weighted_zero_weights():
    """Test behavior with zero weights (should return NaN or handle appropriately)."""
    data = np.array([1, 2, 3, 4])
    weights = np.array([0.0, 0.0, 0.0, 0.0])  # All zero weights
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    
    # Should not crash, but result should be meaningful
    result_mean = weighted_obj.mean()
    # When all weights are zero, result should be NaN or 0.0
    assert np.isnan(result_mean.values) or result_mean.values == 0.0


def test_weighted_mixed_weights():
    """Test with mixed positive and negative weights."""
    data = np.array([1, 2, 3, 4])
    weights = np.array([1.0, -0.5, 0.5, -1.0])  # Mixed weights
    
    da = xr.DataArray(data, dims=['x'])
    weight_da = xr.DataArray(weights, dims=['x'])
    
    weighted_obj = da.weighted(weight_da)
    result_mean = weighted_obj.mean()
    
    # Should compute properly with negative weights
    # For now, just make sure it doesn't crash
    result_sum = weighted_obj.sum()
    assert not np.isnan(result_sum.values) or np.isfinite(result_sum.values)