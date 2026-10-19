"""
Regression tests for PR #20137: ENH: stats.pearsonr: add support for `axis` argument

This test file ensures that the new axis argument functionality in pearsonr
works correctly and that the behavior is properly tested.
"""
import numpy as np
from numpy.testing import assert_allclose
import pytest
from scipy import stats


def test_pearsonr_axis_argument_exists():
    """Test that the axis argument can be passed to pearsonr function."""
    # Test that axis parameter can be passed without error
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # This should not raise an error with axis parameter
    result = stats.pearsonr(x, y, axis=0)
    
    # Basic functionality should still work
    assert hasattr(result, 'statistic')
    assert hasattr(result, 'pvalue')


def test_pearsonr_axis_1d_arrays():
    """Test that 1D arrays work the same as before with axis parameter."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # Test with axis=0 (default)
    result_default = stats.pearsonr(x, y, axis=0)
    result_old_style = stats.pearsonr(x, y)
    
    # Results should be equivalent
    assert_allclose(result_default.statistic, result_old_style.statistic)
    assert_allclose(result_default.pvalue, result_old_style.pvalue)


def test_pearsonr_axis_2d_columns():
    """Test pearsonr with 2D arrays along columns (axis=0)."""
    # Create 2D arrays where each column should have a correlation
    np.random.seed(42)
    x = np.random.randn(10, 5)  # 10 samples, 5 features
    y = np.random.randn(10, 5)  # 10 samples, 5 features
    
    # Calculate correlations along columns (axis=0)
    result = stats.pearsonr(x, y, axis=0)
    
    # Should return 5 correlation coefficients (one per column)
    assert result.statistic.shape == (5,)
    assert result.pvalue.shape == (5,)


def test_pearsonr_axis_2d_rows():
    """Test pearsonr with 2D arrays along rows (axis=1)."""
    # Create 2D arrays where each row should have a correlation
    np.random.seed(42)
    x = np.random.randn(5, 10)  # 5 samples, 10 features
    y = np.random.randn(5, 10)  # 5 samples, 10 features
    
    # Calculate correlations along rows (axis=1)
    result = stats.pearsonr(x, y, axis=1)
    
    # Should return 5 correlation coefficients (one per row)
    assert result.statistic.shape == (5,)
    assert result.pvalue.shape == (5,)


def test_pearsonr_axis_broadcasting():
    """Test pearsonr with broadcasting between arrays."""
    np.random.seed(42)
    x = np.random.randn(8, 15)
    y = np.random.randn(8, 15)
    
    # Test broadcasting for pairwise comparisons
    result = stats.pearsonr(x[:, np.newaxis, :], y, axis=-1)
    
    # Should return shape (8, 8) for all pairwise correlations
    assert result.statistic.shape == (8, 8)


def test_pearsonr_axis_shape_consistency():
    """Test that the axis parameter affects result shapes correctly."""
    np.random.seed(123)
    
    # 3D arrays
    x = np.random.randn(4, 5, 6)
    y = np.random.randn(4, 5, 6)
    
    # Test different axis values
    for axis in [0, 1, 2]:
        result = stats.pearsonr(x, y, axis=axis)
        expected_shape = tuple(s for i, s in enumerate(x.shape) if i != axis)
        assert result.statistic.shape == expected_shape


def test_pearsonr_axis_none():
    """Test pearsonr with axis=None (ravel arrays first)."""
    np.random.seed(42)
    x = np.random.randn(3, 4)
    y = np.random.randn(3, 4)
    
    # With axis=None, arrays should be raveled first
    result = stats.pearsonr(x, y, axis=None)
    
    # Should return a scalar correlation coefficient (single value)
    # The result should be a 0-d array or scalar
    assert np.isscalar(result.statistic) or result.statistic.ndim == 0
    assert np.isscalar(result.pvalue) or result.pvalue.ndim == 0


def test_pearsonr_axis_invalid_integer():
    """Test error handling for invalid axis type (non-integer)."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # Test invalid axis type (should raise ValueError)
    with pytest.raises(ValueError, match='`axis` must be an integer'):
        stats.pearsonr(x, y, axis=0.5)


if __name__ == "__main__":
    # Run the tests
    test_pearsonr_axis_argument_exists()
    test_pearsonr_axis_1d_arrays()
    test_pearsonr_axis_2d_columns()
    test_pearsonr_axis_2d_rows()
    test_pearsonr_axis_broadcasting()
    test_pearsonr_axis_shape_consistency()
    test_pearsonr_axis_none()
    test_pearsonr_axis_invalid_integer()
    print("All tests passed!")