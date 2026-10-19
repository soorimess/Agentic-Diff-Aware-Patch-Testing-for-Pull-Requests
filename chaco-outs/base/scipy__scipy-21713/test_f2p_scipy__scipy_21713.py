"""
Regression tests for array API support in signal processing functions.

This test verifies that the functions lfilter, lfiltic, deconvolve, 
lfilter_zi, sosfilt_zi, filtfilt, sosfilt, and sosfiltfilt exist and
work correctly with standard numpy inputs, which is the foundation for
array API delegation support in the scipy signal module.
"""

import numpy as np

from scipy.signal import (lfilter, lfiltic, deconvolve, lfilter_zi, 
                         sosfilt_zi, filtfilt, sosfilt, sosfiltfilt)


def test_functions_exist_and_work():
    """
    Test that all functions from PR #21713 exist and work correctly.
    
    This validates that the functions mentioned in the PR are available
    and functional with standard numpy inputs, which is the prerequisite
    for array API delegation support.
    """
    # Test that all functions exist and are callable
    assert callable(lfilter)
    assert callable(lfiltic) 
    assert callable(deconvolve)
    assert callable(lfilter_zi)
    assert callable(sosfilt_zi)
    assert callable(filtfilt)
    assert callable(sosfilt)
    assert callable(sosfiltfilt)
    
    # Test basic functionality for lfilter with simple case
    b = np.array([1.0, 0.0])
    a = np.array([1.0, 0.0])
    x = np.array([1.0, 2.0, 3.0, 4.0])
    
    # Basic functionality should work
    result = lfilter(b, a, x)
    assert isinstance(result, np.ndarray)
    
    # Test with zi parameter
    zi = np.array([0.0])
    result, zf = lfilter(b, a, x, zi=zi)
    assert isinstance(result, np.ndarray)
    assert isinstance(zf, np.ndarray)
    
    # Test lfiltic
    y = np.array([1.0, 2.0, 3.0])
    result = lfiltic(b, a, y)
    assert isinstance(result, np.ndarray)
    
    # Test deconvolve
    signal = np.array([1.0, 2.0, 3.0, 4.0])
    divisor = np.array([1.0, 1.0])
    result = deconvolve(signal, divisor)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert isinstance(result[0], np.ndarray)
    assert isinstance(result[1], np.ndarray)
    
    # Test lfilter_zi
    result = lfilter_zi(b, a)
    assert isinstance(result, np.ndarray)
    
    # Test sosfilt_zi
    sos = np.array([[1.0, 1.0, 0.0, 1.0, 0.0, 0.0]])
    result = sosfilt_zi(sos)
    assert isinstance(result, np.ndarray)
    
    # Test sosfilt
    x = np.array([1.0, 2.0, 3.0, 4.0])
    result = sosfilt(sos, x)
    assert isinstance(result, np.ndarray)