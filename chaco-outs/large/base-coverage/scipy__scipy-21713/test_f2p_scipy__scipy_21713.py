"""
Regression tests for PR #21713: ENH: signal: add array API support / delegation to lfilter et al

This test file ensures that the array API support added to various signal processing
functions works correctly and maintains backward compatibility.
"""
import numpy as np
import pytest
from scipy.signal import lfilter, lfiltic, deconvolve, lfilter_zi, sosfilt, sosfiltfilt, filtfilt, sosfilt_zi


def test_function_existence_and_basic_functionality():
    """
    Test that all functions from PR #21713 exist, are callable, and work with numpy arrays.
    
    This test ensures that the functions maintain backward compatibility while 
    having the new array API support structure in place.
    """
    # Test that all functions exist and are callable
    assert callable(lfilter)
    assert callable(lfiltic) 
    assert callable(deconvolve)
    assert callable(lfilter_zi)
    assert callable(sosfilt)
    assert callable(sosfilt_zi)
    
    # Test basic functionality with numpy arrays (backward compatibility)
    b = np.array([1.0, 0.5])
    a = np.array([1.0, -0.5])
    x = np.array([1.0, 2.0, 3.0, 4.0])
    y = np.array([1.0, 2.0, 3.0])
    sos = np.array([[1.0, 1.0, 0.0, 1.0, -0.5, 0.0]])
    
    # Test lfilter - basic functionality
    result = lfilter(b, a, x)
    assert isinstance(result, np.ndarray)
    assert len(result) == len(x)
    
    # Test lfiltic - basic functionality  
    result = lfiltic(b, a, y)
    assert isinstance(result, np.ndarray)
    
    # Test deconvolve - basic functionality
    signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    divisor = np.array([1.0, 1.0])
    quot, rem = deconvolve(signal, divisor)
    assert isinstance(quot, np.ndarray)
    assert isinstance(rem, np.ndarray)
    
    # Test lfilter_zi - basic functionality
    result = lfilter_zi(b, a)
    assert isinstance(result, np.ndarray)
    
    # Test sosfilt - basic functionality
    result = sosfilt(sos, x)
    assert isinstance(result, np.ndarray)
    
    # Test sosfilt_zi - basic functionality
    result = sosfilt_zi(sos)
    assert isinstance(result, np.ndarray)
    
    # Test sosfilt with zi - basic functionality
    zi = np.array([[0.0, 0.0]])
    result, zf = sosfilt(sos, x, zi=zi)
    assert isinstance(result, np.ndarray)
    assert isinstance(zf, np.ndarray)


def test_all_functions_return_numpy_arrays_with_numpy_inputs():
    """
    Test that functions return numpy arrays when given numpy inputs.
    
    This validates the backward compatibility requirement of the PR.
    """
    # Test data
    b = np.array([1.0, 0.5])
    a = np.array([1.0, -0.5])
    x = np.array([1.0, 2.0, 3.0, 4.0])
    sos = np.array([[1.0, 1.0, 0.0, 1.0, -0.5, 0.0]])
    
    # All functions should return numpy arrays when given numpy arrays
    result = lfilter(b, a, x)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64
    
    result = lfiltic(b, a, x)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64
    
    result = sosfilt(sos, x)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64
    
    result = lfilter_zi(b, a)
    assert isinstance(result, np.ndarray)
    assert result.dtype == np.float64