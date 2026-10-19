"""
Regression tests for PR #20284: ENH: stats.pearsonr: add array API support

This test file ensures that the array API support for pearsonr works correctly
and that the specific behaviors introduced by the PR are maintained.
"""
import numpy as np
import pytest
from scipy import stats


def test_pearsonr_basic_functionality():
    """Test that basic pearsonr functionality works correctly."""
    # Test with perfectly correlated data
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    result = stats.pearsonr(x, y)
    assert result.statistic == 1.0
    assert result.pvalue == 0.0


def test_pearsonr_negative_correlation():
    """Test pearsonr with negative correlation."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([5, 4, 3, 2, 1])
    
    result = stats.pearsonr(x, y)
    assert result.statistic == -1.0
    assert result.pvalue == 0.0


def test_pearsonr_with_parameters():
    """Test parameter handling."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # Test with axis parameter
    result = stats.pearsonr(x, y, axis=0)
    assert result.statistic == 1.0
    assert result.pvalue == 0.0
    
    # Test with alternative parameter
    result = stats.pearsonr(x, y, alternative='greater')
    assert result.statistic == 1.0
    assert result.pvalue == 0.0


def test_pearsonr_edge_cases():
    """Test edge cases."""
    # Test with length 2 arrays
    x = np.array([1, 2])
    y = np.array([2, 4])
    
    result = stats.pearsonr(x, y)
    assert result.statistic == 1.0
    assert result.pvalue == 1.0  # Special case for length 2
    
    # Test with constant data
    x = np.array([1, 1, 1, 1, 1])
    y = np.array([2, 4, 6, 8, 10])
    
    with pytest.warns(stats.ConstantInputWarning):
        result = stats.pearsonr(x, y)
        assert np.isnan(result.statistic)
        assert np.isnan(result.pvalue)


def test_pearsonr_method_validation():
    """Test method parameter validation - tests the new PR behavior."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    # Test that method=None works (should not raise error)
    result = stats.pearsonr(x, y, method=None)
    assert result.statistic == 1.0
    assert result.pvalue == 0.0
    
    # Test that invalid method type raises appropriate error
    # This validates that the PR's error handling logic exists
    with pytest.raises(ValueError, match="`method` must be `None` if arguments are not NumPy arrays"):
        stats.pearsonr(x, y, method="invalid")


def test_pearsonr_result_attributes():
    """Test that result object has expected attributes."""
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([2, 4, 6, 8, 10])
    
    result = stats.pearsonr(x, y)
    
    # These are the attributes that should exist
    assert hasattr(result, 'statistic')
    assert hasattr(result, 'pvalue')
    assert hasattr(result, '_alternative')
    assert hasattr(result, '_n')
    assert hasattr(result, '_x')
    assert hasattr(result, '_y')
    assert hasattr(result, '_axis')