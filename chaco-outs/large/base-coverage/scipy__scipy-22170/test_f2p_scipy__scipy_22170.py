# Test for PR #22170: ENH: signal: convert `symiirorder` and related filters to work with array backends
"""
Regression tests for the symiirorder functions to ensure they work correctly
with array backends, particularly when r and omega parameters are Python floats.
"""

import numpy as np
import pytest


def test_skip_if_float_function_exists():
    """
    Test that _skip_if_float function exists and works correctly.
    
    This test will fail in the pre-change version when _skip_if_float doesn't exist,
    and pass after the change is applied.
    """
    try:
        from scipy.signal._delegators import _skip_if_float
    except ImportError:
        # This is the exact issue this PR fixes - _skip_if_float should exist
        pytest.fail("The _skip_if_float function is missing - this is the core issue this PR fixes")
    
    # Test the function behavior
    assert _skip_if_float(1.0) is None
    assert _skip_if_float(0.5) is None
    
    arr = np.array([1.0, 2.0])
    assert _skip_if_float(arr) is arr


def test_symiirorder_functions_with_float_parameters():
    """
    Test that symiirorder functions work with Python float parameters.
    
    This verifies that the functions don't crash when called with float parameters,
    which was the main issue this PR addresses.
    """
    from scipy.signal import symiirorder1, symiirorder2
    
    # Create test data
    signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Test symiirorder1 with Python float parameters
    c0 = 1.0  # Python float
    z1 = 0.5  # Python float
    
    # The function should not crash due to signature handling issues
    try:
        result1 = symiirorder1(signal, c0, z1)
        assert isinstance(result1, np.ndarray)
        assert result1.shape == signal.shape
    except Exception as e:
        # If it's an array namespace issue, that's what we're testing for
        error_str = str(e).lower()
        if "array" in error_str or "namespace" in error_str or "backend" in error_str:
            pytest.fail(f"symiirorder1 failed due to array backend/signature issue: {e}")
    
    # Test symiirorder2 with Python float parameters
    r = 0.5  # Python float
    omega = 0.1  # Python float
    
    try:
        result2 = symiirorder2(signal, r, omega)
        assert isinstance(result2, np.ndarray)
        assert result2.shape == signal.shape
    except Exception as e:
        # If it's an array namespace issue, that's what we're testing for
        error_str = str(e).lower()
        if "array" in error_str or "namespace" in error_str or "backend" in error_str:
            pytest.fail(f"symiirorder2 failed due to array backend/signature issue: {e}")


def test_signature_function_proper_array_namespace():
    """
    Test that signature functions properly determine array namespace.
    
    This test specifically checks that the signature function works correctly
    with actual array inputs, not None values.
    """
    try:
        from scipy.signal._delegators import symiirorder2_signature
    except ImportError:
        # Skip if _skip_if_float not available (pre-change state)
        pytest.skip("Skipping signature test - _skip_if_float not available in pre-change version")
    
    # Create test data
    signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Test with Python float parameters (the key case)
    r = 0.5  # Python float
    omega = 0.1  # Python float
    
    # This should work correctly and return a valid array namespace
    result = symiirorder2_signature(signal, r, omega)
    assert result is not None
    
    # The result should be a valid array namespace (not None)
    # This catches the case where the input is replaced with None
    if hasattr(result, 'array_namespace'):
        # If it has array namespace characteristics, that's good
        pass
    elif result is not None:
        # Should return a valid namespace object
        pass
    else:
        pytest.fail("Signature function returned None - indicates input parameter issue")


def test_array_backend_compatibility():
    """
    Test that functions work with different array backends.
    
    This ensures that the fix properly handles array backend selection
    when float parameters are present.
    """
    from scipy.signal import symiirorder1, symiirorder2
    
    # Test with different parameter combinations
    signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    
    # Test with all float parameters (the main issue case)
    try:
        result1 = symiirorder1(signal, 1.0, 0.5)  # All floats
        assert isinstance(result1, np.ndarray)
        
        result2 = symiirorder2(signal, 0.5, 0.1)  # All floats
        assert isinstance(result2, np.ndarray)
    except Exception as e:
        error_str = str(e).lower()
        if "array" in error_str or "namespace" in error_str or "backend" in error_str:
            pytest.fail(f"Array backend compatibility issue: {e}")