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
    
    # Test case from the PR documentation
    A = csr_array([[3, 2, 0], [1, -1, 0], [0, 5, 1]], dtype=float)
    b = np.array([2, 4, -1], dtype=float)
    t = 0.1
    
    # Compute using the new Krylov method
    y = funm_multiply_krylov(expm, A, b, t=t)
    
    # Compare with reference solution
    ref = expm(t * A.toarray()) @ b
    assert_allclose(y, ref, rtol=1e-12)


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