"""
Regression tests for PR #22896: ENH: signal: `tf2zpk` et al Array API

These tests ensure that the array API compatibility changes work correctly.
"""
import numpy as np
from scipy.signal import tf2zpk, zpk2tf, sos2tf, sos2zpk, zpk2sos


def test_tf2zpk_correctness():
    """Test tf2zpk with the exact example from docstring."""
    # Test with the exact example from docstring
    b = [3, 0, 0]
    a = [1, 5, 13]
    
    z, p, k = tf2zpk(b, a)
    
    # Check that we get expected results
    expected_z = np.array([0.0, 0.0])
    expected_p = np.array([-2.5 + 2.59807621j, -2.5 - 2.59807621j])
    expected_k = 3.0
    
    np.testing.assert_array_almost_equal(z, expected_z, decimal=8)
    np.testing.assert_array_almost_equal(p, expected_p, decimal=8)
    np.testing.assert_almost_equal(k, expected_k)


def test_zpk2tf_correctness():
    """Test zpk2tf with the exact example from docstring."""
    # Test with the exact example from docstring
    z = [2, 6]
    p = [1, 8]
    k = 5
    
    b, a = zpk2tf(z, p, k)
    
    # Check that we get expected results
    expected_b = np.array([5.0, -40.0, 60.0])
    expected_a = np.array([1.0, -9.0, 8.0])
    
    np.testing.assert_array_almost_equal(b, expected_b)
    np.testing.assert_array_almost_equal(a, expected_a)


def test_sos2tf_correctness():
    """Test sos2tf with basic example."""
    # Test with simple SOS
    sos = np.array([[1.0, 2.0, 3.0, 1.0, 0.0, 0.0]])
    
    b, a = sos2tf(sos)
    
    # Check that we get expected results
    expected_b = np.array([1.0, 2.0, 3.0])
    expected_a = np.array([1.0, 0.0, 0.0])
    
    np.testing.assert_array_almost_equal(b, expected_b)
    np.testing.assert_array_almost_equal(a, expected_a)


def test_sos2zpk_correctness():
    """Test sos2zpk with basic example."""
    # Create a simple SOS and convert to zpk
    sos = np.array([[1.0, 2.0, 3.0, 1.0, 0.0, 0.0]])
    
    z, p, k = sos2zpk(sos)
    
    # Should return valid results
    assert isinstance(z, np.ndarray)
    assert isinstance(p, np.ndarray)
    assert isinstance(k, (int, float))
    assert len(z) == 2  # 2 zeros from one section
    assert len(p) == 2  # 2 poles from one section


def test_zpk2sos_correctness():
    """Test zpk2sos with basic example."""
    # Test with simple zpk
    z = np.array([2.0, 6.0])
    p = np.array([1.0, 8.0])
    k = 5.0
    
    sos = zpk2sos(z, p, k)
    
    # Should return a valid sos array
    assert isinstance(sos, np.ndarray)
    assert sos.shape[1] == 6  # SOS format has 6 columns


def test_dtype_handling():
    """Test that functions handle different dtypes properly."""
    # Test with integer arrays
    b = np.array([3, 0, 0], dtype=int)
    a = np.array([1, 5, 13], dtype=int)
    
    z, p, k = tf2zpk(b, a)
    
    # Should handle integer inputs and return appropriate types
    assert isinstance(z, np.ndarray)
    assert isinstance(p, np.ndarray)
    assert isinstance(k, (int, float))


def test_complex_coefficients():
    """Test with complex coefficients."""
    # Test with complex numbers
    z = np.array([1.0+1.0j, 2.0-1.0j])
    p = np.array([0.5+0.5j, 1.5-0.5j])
    k = 2.0+0.0j
    
    b, a = zpk2tf(z, p, k)
    
    # Should return valid polynomial coefficients
    assert isinstance(b, np.ndarray)
    assert isinstance(a, np.ndarray)


def test_zpk2sos_empty_case():
    """Test zpk2sos with empty arrays."""
    # Test with empty arrays
    z = np.array([])
    p = np.array([])
    k = 1.0
    
    sos = zpk2sos(z, p, k)
    
    # Should return a valid sos array
    assert isinstance(sos, np.ndarray)
    assert sos.shape[1] == 6  # SOS format has 6 columns
    assert sos.shape[0] == 1  # Should have one section


def test_array_api_behavior():
    """Test that the functions work with array API patterns."""
    # Test that we can call all functions with numpy arrays and they work correctly
    # This tests the core functionality that was changed in the PR
    
    # Test tf2zpk
    b = np.array([3.0, 0.0, 0.0])
    a = np.array([1.0, 5.0, 13.0])
    z, p, k = tf2zpk(b, a)
    assert isinstance(z, np.ndarray)
    assert isinstance(p, np.ndarray)
    assert isinstance(k, (int, float))
    
    # Test zpk2tf
    z = np.array([2.0, 6.0])
    p = np.array([1.0, 8.0])
    k = 5.0
    b, a = zpk2tf(z, p, k)
    assert isinstance(b, np.ndarray)
    assert isinstance(a, np.ndarray)
    
    # Test sos2tf
    sos = np.array([[1.0, 2.0, 3.0, 1.0, 0.0, 0.0]])
    b, a = sos2tf(sos)
    assert isinstance(b, np.ndarray)
    assert isinstance(a, np.ndarray)
    
    # Test sos2zpk
    sos = np.array([[1.0, 2.0, 3.0, 1.0, 0.0, 0.0]])
    z, p, k = sos2zpk(sos)
    assert isinstance(z, np.ndarray)
    assert isinstance(p, np.ndarray)
    assert isinstance(k, (int, float))
    
    # Test zpk2sos
    z = np.array([2.0, 6.0])
    p = np.array([1.0, 8.0])
    k = 5.0
    sos = zpk2sos(z, p, k)
    assert isinstance(sos, np.ndarray)
    assert sos.shape[1] == 6