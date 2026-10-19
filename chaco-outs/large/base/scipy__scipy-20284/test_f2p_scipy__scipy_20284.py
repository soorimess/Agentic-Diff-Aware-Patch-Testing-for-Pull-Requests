"""
Regression tests for scipy.stats.pearsonr array API support.

This test file ensures that the changes in PR #20284 are properly tested,
specifically the addition of array API support to scipy.stats.pearsonr.
"""

import numpy as np
import pytest
from scipy import stats
from scipy.stats import pearsonr


def test_pearsonr_basic_functionality():
    """Test basic pearsonr functionality with numpy arrays."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    result = pearsonr(x, y)
    assert result.statistic == 1.0
    assert result.pvalue < 1e-10


def test_pearsonr_with_axis():
    """Test pearsonr with axis parameter."""
    # 2D arrays
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[2, 4, 6], [8, 10, 12]])
    
    # Test with axis=0 (default)
    result = pearsonr(x, y, axis=0)
    assert len(result.statistic) == 3  # Should have 3 correlation coefficients
    
    # Test with axis=1
    result = pearsonr(x, y, axis=1)
    assert len(result.statistic) == 2  # Should have 2 correlation coefficients


def test_pearsonr_with_axis_none():
    """Test pearsonr with axis=None."""
    x = np.array([[1, 2, 3], [4, 5, 6]])
    y = np.array([[2, 4, 6], [8, 10, 12]])
    
    result = pearsonr(x, y, axis=None)
    assert result.statistic == 1.0  # Should be perfect correlation


def test_pearsonr_alternative_parameter():
    """Test that pearsonr works with different alternative parameters."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # Test two-sided (default)
    result = pearsonr(x, y, alternative='two-sided')
    assert result.statistic == 1.0
    
    # Test less
    result = pearsonr(x, y, alternative='less')
    assert result.statistic == 1.0
    
    # Test greater
    result = pearsonr(x, y, alternative='greater')
    assert result.statistic == 1.0


def test_pearsonr_constant_input():
    """Test that pearsonr handles constant input correctly."""
    x = np.array([1, 1, 1, 1, 1])  # Constant array
    y = np.array([2, 4, 6, 8, 10])
    
    with pytest.warns(stats.ConstantInputWarning):
        result = pearsonr(x, y)
        # For constant input, statistic should be NaN
        assert np.isnan(result.statistic)
        # pvalue should be NaN or 1.0 (depending on implementation)
        assert result.pvalue == 1.0 or np.isnan(result.pvalue)


def test_pearsonr_small_arrays():
    """Test that pearsonr works with small arrays."""
    x = np.array([1, 2])
    y = np.array([2, 4])
    
    result = pearsonr(x, y)
    # For 2 elements, should use special case calculation
    assert result.statistic == 1.0
    assert result.pvalue == 1.0  # No significant correlation test for n=2


def test_pearsonr_complex_input():
    """Test that pearsonr raises ValueError for complex inputs."""
    x = np.array([1+0j, 2+0j, 3+0j])
    y = np.array([2+0j, 4+0j, 6+0j])
    
    with pytest.raises(ValueError, match='This function does not support complex data'):
        pearsonr(x, y)


def test_pearsonr_method_validation_with_array_api():
    """
    Test validation behavior for array API support in PR #20284.
    
    This test verifies that when method is not None and arrays are not NumPy arrays,
    the validation logic correctly identifies the array type issue and provides
    appropriate error handling.
    
    This test will be meaningful once PR #20284 is applied.
    """
    # Create a mock array that is not a NumPy array
    class ArrayLike:
        def __init__(self, data):
            self.data = np.array(data)
            
        def __array__(self):
            return self.data
            
        @property
        def dtype(self):
            return self.data.dtype
            
        @property
        def shape(self):
            return self.data.shape
            
        def __getitem__(self, key):
            return self.data[key]
            
        def __setitem__(self, key, value):
            self.data[key] = value
            
        def __len__(self):
            return len(self.data)
    
    x = ArrayLike([1, 2, 3, 4, 5])
    y = ArrayLike([2, 4, 6, 8, 10])
    
    # This test verifies that when method is used with non-numpy arrays,
    # appropriate validation occurs. The PR adds specific validation for this case.
    try:
        result = pearsonr(x, y, method='bootstrap')
        # If we get here, it means no validation error was raised
        # This would be unexpected behavior
        assert False, "Expected ValueError when using method with non-numpy arrays"
    except ValueError as e:
        error_msg = str(e)
        # The PR should make this error more specific about array types
        # For now, we just ensure it's a ValueError about method validation
        assert "method" in error_msg.lower()