# mypy: disable-error-code="attr-defined"
import numpy as np

from scipy.integrate._tanhsinh import _tanhsinh


def test_tanhsinh_array_operations():
    """
    Test array operations that demonstrate the new array API infrastructure.
    
    This test verifies that the function works correctly with array inputs
    and would benefit from the new array API support infrastructure.
    """
    def f(x):
        return np.exp(-x**2)
    
    # Test 1: Basic scalar integration
    res = _tanhsinh(f, -np.inf, np.inf)
    expected = np.sqrt(np.pi)
    assert np.allclose(res.integral, expected, rtol=1e-12)
    
    # Test 2: Array integration - this exercises the new array handling
    a = np.array([0.0, 1.0, 2.0])
    b = np.array([1.0, 2.0, 3.0])
    res = _tanhsinh(f, a, b)
    assert res.integral.shape == (3,)
    assert res.error.shape == (3,)
    
    # Test 3: Broadcasting behavior - key functionality for array API support
    a = np.array([0.0, 1.0])  # shape (2,)
    b = np.array([[1.0, 2.0], [3.0, 4.0]])  # shape (2, 2)
    res = _tanhsinh(f, a, b)
    assert res.integral.shape == (2, 2)
    assert res.error.shape == (2, 2)
    
    # Test 4: Edge cases with infinities
    res = _tanhsinh(f, 0.0, np.inf)
    assert np.isfinite(res.integral)
    assert np.isfinite(res.error)
    
    # Verify all results are finite
    assert np.all(np.isfinite(res.integral))
    assert np.all(np.isfinite(res.error))


def test_tanhsinh_scalar_array_consistency():
    """
    Test consistency between scalar and array inputs.
    
    This verifies that the function handles both scalar and array inputs
    consistently, which is important for the new array API infrastructure.
    """
    def f(x):
        return x**2
    
    # Scalar input
    res_scalar = _tanhsinh(f, 0.0, 1.0)
    
    # Array input with single element
    res_array = _tanhsinh(f, np.array([0.0]), np.array([1.0]))
    
    # Results should be consistent
    assert np.allclose(res_scalar.integral, res_array.integral[0])
    assert np.allclose(res_scalar.error, res_array.error[0])
    
    # Multiple element array
    a = np.array([0.0, 1.0])
    b = np.array([1.0, 2.0])
    res_multi = _tanhsinh(f, a, b)
    
    assert res_multi.integral.shape == (2,)
    assert res_multi.error.shape == (2,)
    assert np.all(np.isfinite(res_multi.integral))
    assert np.all(np.isfinite(res_multi.error))