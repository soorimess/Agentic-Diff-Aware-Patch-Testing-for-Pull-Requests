"""
Regression tests for the funm_multiply_krylov function.

This test file ensures that the new Krylov method for computing f(A)b
works correctly and catches regressions in its behavior.
"""
import numpy as np
import pytest
from numpy.testing import assert_allclose

from scipy.sparse import csr_array


def test_funm_multiply_krylov_importable():
    """Test that funm_multiply_krylov is importable from scipy.sparse.linalg."""
    # This test will fail before the PR and pass after the PR
    from scipy.sparse.linalg import funm_multiply_krylov
    assert callable(funm_multiply_krylov)


def test_funm_multiply_krylov_basic_functionality():
    """Test basic functionality of funm_multiply_krylov."""
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    
    # Test case from the PR documentation - exact example
    A = csr_array([[3, 2, 0], [1, -1, 0], [0, 5, 1]], dtype=float)
    b = np.array([2, 4, -1], dtype=float)
    t = 0.1
    
    # Compute using the new Krylov method
    y = funm_multiply_krylov(expm, A, b, t=t)
    
    # Compare with reference solution - exact expected values from PR
    ref = expm(t * A.toarray()) @ b
    assert_allclose(y, ref, rtol=1e-12)
    
    # Test that we get the expected result values (not just any correct result)
    expected_values = np.array([3.6164913, 3.88421511, 0.96073457])
    assert_allclose(y, expected_values, rtol=1e-6)


def test_funm_multiply_krylov_parameter_validation():
    """Test parameter validation in funm_multiply_krylov."""
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    
    A = csr_array([[1, 2], [3, 4]], dtype=float)
    b = np.array([1, 1], dtype=float)
    
    # Test invalid assume_a parameter
    with pytest.raises(ValueError, match="not a recognized matrix structure"):
        funm_multiply_krylov(expm, A, b, assume_a='invalid')
    
    # Test invalid restart_every_m parameter
    with pytest.raises(ValueError, match="argument 'restart_every_m' must be positive"):
        funm_multiply_krylov(expm, A, b, restart_every_m=0)
        
    # Test invalid max_restarts parameter
    with pytest.raises(ValueError, match="argument 'max_restarts' must be positive"):
        funm_multiply_krylov(expm, A, b, max_restarts=0)


def test_funm_multiply_krylov_zero_vector():
    """Test that funm_multiply_krylov handles zero vectors correctly."""
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    
    A = csr_array([[1, 2], [3, 4]], dtype=float)
    b = np.array([0.0, 0.0], dtype=float)
    
    # Should return zero vector
    y = funm_multiply_krylov(expm, A, b)
    assert_allclose(y, b, rtol=1e-15)


def test_funm_multiply_krylov_complex_numbers():
    """Test that funm_multiply_krylov works with complex matrices and vectors."""
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    
    # Complex test case
    A = csr_array([[1+1j, 2-1j], [3+0j, 4-2j]], dtype=complex)
    b = np.array([1+0j, 1+0j], dtype=complex)
    
    # Compute using the new Krylov method
    y = funm_multiply_krylov(expm, A, b)
    
    # Compare with reference solution
    ref = expm(A.toarray()) @ b
    assert_allclose(y, ref, rtol=1e-12)


def test_funm_multiply_krylov_different_functions():
    """Test that funm_multiply_krylov works with different matrix functions."""
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import sinm, cosm
    
    A = csr_array([[1, 2], [3, 4]], dtype=float)
    b = np.array([1, 1], dtype=float)
    
    # Test with sine function
    y_sin = funm_multiply_krylov(sinm, A, b)
    ref_sin = sinm(A.toarray()) @ b
    assert_allclose(y_sin, ref_sin, rtol=1e-12)
    
    # Test with cosine function
    y_cos = funm_multiply_krylov(cosm, A, b)
    ref_cos = cosm(A.toarray()) @ b
    assert_allclose(y_cos, ref_cos, rtol=1e-12)