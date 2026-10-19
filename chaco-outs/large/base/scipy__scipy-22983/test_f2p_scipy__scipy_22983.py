"""
Regression tests for PR #22983: ENH: sparse.linalg: a restarted Krylov method 
for evaluating f(A)b.

This test file ensures that the new funm_multiply_krylov function works correctly
and that the behavior is properly tested.
"""
import numpy as np
import pytest


def test_funm_multiply_krylov_function_exists():
    """
    Test that funm_multiply_krylov function exists in sparse.linalg module.
    
    This test ensures that the function added by PR #22983 is available.
    """
    # Import and verify the function exists - this will fail before PR is applied
    from scipy.sparse.linalg import funm_multiply_krylov
    # Verify it's callable
    assert callable(funm_multiply_krylov)


def test_funm_multiply_krylov_basic_computation():
    """
    Test basic computation functionality of funm_multiply_krylov.
    
    Tests that the function can compute f(A)b for simple cases.
    """
    # Import the function
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    # Simple diagonal matrix case
    A = csr_array([[1, 0], [0, 2]], dtype=float)
    b = np.array([1.0, 2.0], dtype=float)
    
    # Test matrix exponential computation
    y = funm_multiply_krylov(expm, A, b)
    # Expected: expm([[1,0],[0,2]]) @ [1,2] = [e^1, 2*e^2]
    expected = np.array([np.exp(1.0), 2.0 * np.exp(2.0)])
    
    np.testing.assert_allclose(y, expected, rtol=1e-12)


def test_funm_multiply_krylov_hermitian_case():
    """
    Test funm_multiply_krylov with hermitian matrices.
    """
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    # Create a hermitian matrix (complex with real diagonal)
    A = csr_array([[2, 1j], [-1j, 3]], dtype=complex)
    b = np.array([1+0j, 2+0j], dtype=complex)
    
    # Test with hermitian assumption
    y = funm_multiply_krylov(expm, A, b, assume_a='hermitian')
    ref = expm(A.todense()) @ b
    np.testing.assert_allclose(y, ref, rtol=1e-12, atol=1e-12)


def test_funm_multiply_krylov_parameter_validation():
    """
    Test parameter validation in funm_multiply_krylov.
    
    Tests that appropriate errors are raised for invalid parameters.
    """
    # Import the function
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    A = csr_array([[1, 0], [0, 2]], dtype=float)
    b = np.array([1.0, 2.0], dtype=float)
    
    # Test invalid assume_a parameter
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b, assume_a='invalid')
        
    # Test invalid restart_every_m parameter
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b, restart_every_m=0)
        
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b, restart_every_m=-1)
        
    # Test invalid max_restarts parameter
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b, max_restarts=0)
        
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b, max_restarts=-1)
        
    # Test invalid b shape
    b_2d = np.array([[1.0, 2.0]], dtype=float)  # 2D array
    with pytest.raises(ValueError):
        funm_multiply_krylov(expm, A, b_2d)


def test_funm_multiply_krylov_zero_vector():
    """
    Test funm_multiply_krylov with zero vector.
    """
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    A = csr_array([[1, 0], [0, 2]], dtype=float)
    b = np.array([0.0, 0.0], dtype=float)
    
    y = funm_multiply_krylov(expm, A, b)
    np.testing.assert_allclose(y, b, rtol=1e-12, atol=1e-12)


def test_funm_multiply_krylov_with_different_assume_a():
    """
    Test funm_multiply_krylov with different assume_a values.
    """
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    A = csr_array([[1, 0], [0, 2]], dtype=float)
    b = np.array([1.0, 2.0], dtype=float)
    
    # Test with 'her' alias
    y1 = funm_multiply_krylov(expm, A, b, assume_a='her')
    # Test with 'general' alias
    y2 = funm_multiply_krylov(expm, A, b, assume_a='general')
    # Test with 'gen' alias
    y3 = funm_multiply_krylov(expm, A, b, assume_a='gen')
    
    ref = expm(A.todense()) @ b
    np.testing.assert_allclose(y1, ref, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(y2, ref, rtol=1e-12, atol=1e-12)
    np.testing.assert_allclose(y3, ref, rtol=1e-12, atol=1e-12)


def test_funm_multiply_krylov_with_custom_function():
    """
    Test funm_multiply_krylov with a custom function similar to the examples in docstring.
    """
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.sparse import csr_array
    
    # Create a test matrix
    A = csr_array([[3, 2, 0], [1, -1, 0], [0, 5, 1]], dtype=float)
    b = np.array([2, 4, -1], dtype=float)
    
    # Test with a polynomial function: f(X) = X^3 - X
    poly = lambda X: X @ X @ X - X
    y = funm_multiply_krylov(poly, A, b)
    ref = poly(A.todense()) @ b
    np.testing.assert_allclose(y, ref, rtol=1e-12, atol=1e-12)


def test_funm_multiply_krylov_edge_case_handling():
    """
    Test edge case handling to ensure robust operation.
    """
    from scipy.sparse.linalg import funm_multiply_krylov
    from scipy.linalg import expm
    from scipy.sparse import csr_array
    
    # Test with a matrix that might trigger numerical edge cases
    # This is a simple test to make sure the function handles various inputs correctly
    A = csr_array([[1e-10, 1], [1, 1e-10]], dtype=float)  # Very small diagonal elements
    b = np.array([1.0, 1.0], dtype=float)
    
    # This should not crash and should return reasonable results
    y = funm_multiply_krylov(expm, A, b)
    assert isinstance(y, np.ndarray)
    assert y.shape == (2,)
    
    # Test with a matrix that has a very small condition number
    # This might trigger the breakdown condition in Lanczos iteration
    A_small = csr_array([[1e-15, 1], [1, 1e-15]], dtype=float)
    y2 = funm_multiply_krylov(expm, A_small, b)
    assert isinstance(y2, np.ndarray)
    assert y2.shape == (2,)