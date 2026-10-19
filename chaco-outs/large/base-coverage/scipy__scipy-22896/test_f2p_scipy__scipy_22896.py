"""
Regression tests for Array API compatibility changes in signal functions.

This test file ensures that the changes made in PR #22896 maintain the expected
behavior for tf2zpk, zpk2tf, sos2tf, sos2zpk, and zpk2sos functions.
"""
import numpy as np
from scipy.signal import tf2zpk, zpk2tf, sos2tf, sos2zpk, zpk2sos


def test_tf2zpk_integer_promotion():
    """Test that tf2zpk promotes integer inputs to floating point (Array API compatibility)."""
    # Test with integer arrays - should return float arrays (new Array API behavior)
    b = np.array([3, 0, 0], dtype=int)
    a = np.array([1, 5, 13], dtype=int)
    z, p, k = tf2zpk(b, a)
    
    # NEW behavior: integer inputs should be promoted to float for Array API compatibility
    # This ensures dtype consistency with Array API patterns
    assert z.dtype.kind == 'f', f"Expected float dtype for zeros, got {z.dtype}"
    assert p.dtype.kind == 'c', f"Expected complex dtype for poles, got {p.dtype}"
    assert isinstance(k, (float, np.floating)), f"Expected float gain, got {type(k)}"


def test_zpk2tf_integer_promotion():
    """Test that zpk2tf promotes integer inputs to floating point (Array API compatibility)."""
    # Test with integer arrays - should return float arrays (new Array API behavior)
    z = np.array([2, 6], dtype=int)
    p = np.array([1, 8], dtype=int)
    k = np.array([5], dtype=int)
    
    b, a = zpk2tf(z, p, k)
    
    # NEW behavior: integer inputs should be promoted to float for Array API compatibility
    # This ensures dtype consistency with Array API patterns
    assert b.dtype.kind == 'f', f"Expected float dtype for numerator, got {b.dtype}"
    assert a.dtype.kind == 'f', f"Expected float dtype for denominator, got {a.dtype}"


def test_sos2tf_boolean_promotion():
    """Test that sos2tf properly promotes boolean arrays (Array API compatibility)."""
    # Test with boolean sos array - should be promoted to float64 (new Array API behavior)
    sos = np.array([[True, True, True, True, True, True]], dtype=bool)
    
    b, a = sos2tf(sos)
    
    # NEW behavior: boolean arrays should be promoted to float64 for Array API compatibility
    # This ensures dtype consistency with Array API patterns
    assert b.dtype == np.float64, f"Expected float64 dtype for numerator, got {b.dtype}"
    assert a.dtype == np.float64, f"Expected float64 dtype for denominator, got {a.dtype}"


def test_zpk2sos_returns_numpy_array():
    """Test that zpk2sos returns numpy arrays (maintains compatibility)."""
    # Test that zpk2sos returns a numpy array (maintains compatibility)
    z = np.array([2.0, 6.0])
    p = np.array([1.0, 8.0])
    k = 5.0
    
    sos = zpk2sos(z, p, k)
    
    # Should return a numpy array for compatibility (XXX comment says convert to numpy, convert back on exit)
    assert isinstance(sos, np.ndarray), f"Expected numpy array, got {type(sos)}"
    assert sos.dtype == np.float64, f"Expected float64 dtype, got {sos.dtype}"


def test_sos2zpk_integer_promotion():
    """Test that sos2zpk promotes integer inputs to floating point (Array API compatibility)."""
    # Test with integer sos array - should return float arrays (new Array API behavior)
    sos = np.array([[1, 2, 3, 1, 2, 3]], dtype=int)
    z, p, k = sos2zpk(sos)
    
    # NEW behavior: integer inputs should be promoted to float for Array API compatibility
    # This ensures dtype consistency with Array API patterns
    assert z.dtype.kind == 'c', f"Expected complex dtype for zeros, got {z.dtype}"
    assert p.dtype.kind == 'c', f"Expected complex dtype for poles, got {p.dtype}"
    assert isinstance(k, (float, np.floating)), f"Expected float gain, got {type(k)}"


def test_edge_case_empty_arrays():
    """Test edge cases with empty arrays."""
    # Test with empty zeros and poles (should work)
    z = np.array([])
    p = np.array([])
    k = 1.0
    
    b, a = zpk2tf(z, p, k)
    
    # Should return [1.0] for both b and a (constant system)
    expected_b = np.array([1.0])
    expected_a = np.array([1.0])
    
    np.testing.assert_array_almost_equal(b, expected_b)
    np.testing.assert_array_almost_equal(a, expected_a)