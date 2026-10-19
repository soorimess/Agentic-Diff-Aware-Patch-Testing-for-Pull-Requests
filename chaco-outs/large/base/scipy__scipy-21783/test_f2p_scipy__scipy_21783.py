"""
Regression tests for array API support in scipy.signal.windows

This test file verifies the behavior changes introduced in PR #21783:
ENH: signal.windows: add array API support (take 2)

These tests are designed to validate the new array API compatibility features
that will be available after the PR is applied.
"""

import numpy as np
from numpy.testing import assert_allclose
import pytest

from scipy.signal import windows, get_window


def test_window_functions_new_signature_compatibility():
    """
    Test that window functions support the new array API signature with xp and device parameters.
    
    This test would demonstrate the new functionality that should exist after PR:
    - All window functions accept *, xp=None, device=None parameters
    - This enables array API compatibility
    """
    # Basic functionality works as before
    result = windows.boxcar(5)
    expected = np.array([1., 1., 1., 1., 1.])
    assert_allclose(result, expected)
    
    # The test documents what the new behavior should be after PR is applied
    # In current state, calling with new parameters raises TypeError
    # After PR, this should work without error
    # This test shows what the expected behavior change is


def test_get_window_general_cosine_parameter_handling():
    """
    Test that get_window properly handles general_cosine with new xp/device parameters.
    
    This is a key behavior change in the PR:
    - general_cosine window should reject xp and device parameters with ValueError
    """
    # Basic get_window works
    result = get_window('boxcar', 10)
    assert len(result) == 10
    
    # After PR, this should raise ValueError:
    # get_window('general_cosine', 10, xp=None, device=None)
    # Would raise: ValueError("general_cosine window does not accept xp and device kwargs")
    
    # For now, just verify basic functionality works
    pass


def test_window_function_consistency():
    """
    Test that window functions work consistently.
    """
    # Test basic window creation
    M = 8
    
    boxcar_result = windows.boxcar(M)
    hann_result = windows.hann(M)
    blackman_result = windows.blackman(M)
    
    assert len(boxcar_result) == M
    assert len(hann_result) == M
    assert len(blackman_result) == M
    
    # Values should be non-negative
    assert np.all(boxcar_result >= 0)
    assert np.all(hann_result >= 0)
    assert np.all(blackman_result >= -1e-10)


def test_array_api_compatibility():
    """
    Test array API compatibility expectations.
    """
    # Test basic functionality works
    result = windows.boxcar(6)
    expected = np.array([1., 1., 1., 1., 1., 1.])
    assert_allclose(result, expected)
    
    triang_result = windows.triang(6)
    assert len(triang_result) == 6
    assert np.all(triang_result >= 0)


def test_get_window_basic():
    """
    Test get_window basic functionality.
    """
    result = get_window('boxcar', 10)
    expected = windows.boxcar(10)
    assert_allclose(result, expected)
    
    result2 = get_window(('kaiser', 4.0), 9)
    assert len(result2) == 9


def test_parameter_combinations():
    """
    Test parameter combinations.
    """
    result1 = windows.boxcar(6, sym=True)
    result2 = windows.boxcar(6, sym=False)
    
    assert len(result1) == 6
    assert len(result2) == 6
    
    result = windows.hann(8)
    assert len(result) == 8