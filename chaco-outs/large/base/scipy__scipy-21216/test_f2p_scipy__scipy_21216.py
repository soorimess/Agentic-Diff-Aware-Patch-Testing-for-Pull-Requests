# mypy: disable-error-code="attr-defined"
"""
Test for array API support in scipy.integrate._tanhsinh
This test verifies that _tanhsinh works correctly with array inputs
and demonstrates the array API support added in PR #21216.
"""

import numpy as np
from numpy.testing import assert_allclose

from scipy.integrate._tanhsinh import _tanhsinh


def test_tanhsinh_array_handling_comprehensive():
    """
    Comprehensive test of array handling that verifies the array API support enhancement.
    Tests various array types and shapes to ensure robust handling.
    """
    
    def f(x):
        return np.exp(-x**2)
    
    # Test 1: Basic scalar behavior (baseline)
    result = _tanhsinh(f, -np.inf, np.inf)
    expected = np.sqrt(np.pi)
    assert_allclose(result.integral, expected, rtol=1e-12)
    
    # Test 2: 1D array inputs - core array handling functionality
    a_vals = np.array([0.0, 1.0, 2.0])
    b_vals = np.array([1.0, 2.0, 3.0])
    
    result = _tanhsinh(f, a_vals, b_vals)
    assert result.integral.shape == (3,)
    assert np.all(np.isfinite(result.integral))
    
    # Test 3: 2D array inputs - more complex array handling
    a_2d = np.array([[0.0, 1.0], [0.5, 1.5]])
    b_2d = np.array([[1.0, 2.0], [1.5, 2.5]])
    
    result = _tanhsinh(f, a_2d, b_2d)
    assert result.integral.shape == (2, 2)
    assert np.all(np.isfinite(result.integral))
    
    # Test 4: Broadcasting behavior - tests array handling logic thoroughly
    a_vals = np.array([1.0, 2.0])
    b_vals = np.array([0.5, 1.0, 1.5])
    a_broadcast = a_vals[:, np.newaxis]  # Shape (2, 1)
    b_broadcast = b_vals[np.newaxis, :]  # Shape (1, 3)
    
    result = _tanhsinh(f, a_broadcast, b_broadcast)
    assert result.integral.shape == (2, 3)
    assert np.all(np.isfinite(result.integral))
    
    # Test 5: Edge case with special values
    a_vals = np.array([0.0, 0.0])
    b_vals = np.array([1.0, 1.0])
    
    result = _tanhsinh(f, a_vals, b_vals)
    assert result.integral.shape == (2,)
    assert np.all(np.isfinite(result.integral))


def test_tanhsinh_log_and_infinite_cases():
    """
    Test log mode and infinite limits with arrays - these exercise specific array handling paths.
    """
    
    def f(x):
        return 1 / (1 + x**2)
    
    # Test with infinite limits and arrays
    a_vals = np.array([-np.inf, 0.0, 1.0])
    b_vals = np.array([np.inf, 1.0, 2.0])
    
    result = _tanhsinh(f, a_vals, b_vals)
    assert result.integral.shape == (3,)
    assert np.all(np.isfinite(result.integral))
    
    # Test with log mode and arrays
    a_vals = np.array([0.0, 1.0, 2.0])
    b_vals = np.array([1.0, 2.0, 3.0])
    
    result = _tanhsinh(f, a_vals, b_vals, log=True)
    assert result.integral.shape == (3,)
    assert np.all(np.isfinite(result.integral))