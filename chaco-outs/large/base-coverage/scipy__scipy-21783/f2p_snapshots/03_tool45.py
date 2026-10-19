"""
Test for array API support in signal.windows functions.

This test verifies that PR #21783 successfully added array API support
to signal.windows functions by ensuring they accept xp and device parameters
and produce correct results.
"""
import numpy as np
import pytest


def test_window_functions_accept_xp_and_device_parameters():
    """
    Test that window functions accept xp and device parameters.
    
    This test verifies that the changes in PR #21783 have been applied,
    which add array API support to window functions.
    """
    # Test with a simple window function that should accept xp parameter
    M = 10
    
    # These calls should work after the changes are applied
    # If they fail with TypeError about unexpected keyword argument, 
    # it means the changes haven't been applied yet
    try:
        # Test boxcar function with xp parameter
        result = np.ones(M)  # This is just to make sure basic import works
        
        # Test that boxcar accepts xp parameter
        from scipy.signal.windows import boxcar
        result = boxcar(M, xp=np)
        assert isinstance(result, np.ndarray)
        assert len(result) == M
        
        # Test that boxcar accepts device parameter
        result = boxcar(M, device=None)
        assert isinstance(result, np.ndarray)
        assert len(result) == M
        
    except TypeError as e:
        if "unexpected keyword argument 'xp'" in str(e) or "unexpected keyword argument 'device'" in str(e):
            pytest.fail("Window functions do not accept xp or device parameters - PR #21783 changes not applied")
        raise


def test_get_window_accepts_xp_parameter():
    """
    Test that get_window accepts xp parameter for array API support.
    """
    try:
        # This should work after the changes
        from scipy.signal.windows import get_window
        result = get_window("blackman", 10, xp=np)
        assert isinstance(result, np.ndarray)
        assert len(result) == 10
    except TypeError as e:
        if "unexpected keyword argument 'xp'" in str(e):
            pytest.fail("get_window does not accept xp parameter - PR #21783 changes not applied")
        raise


def test_consistency_with_numpy_behavior():
    """
    Test that window functions produce consistent results with numpy behavior.
    """
    M = 8
    
    try:
        from scipy.signal.windows import boxcar
        
        # Test that results are consistent with numpy behavior
        result_old = boxcar(M)  # Old way
        result_new = boxcar(M, xp=np)  # New way with xp parameter
        
        # Results should be equal
        np.testing.assert_array_equal(result_old, result_new)
        
    except TypeError as e:
        if "unexpected keyword argument 'xp'" in str(e):
            pytest.fail("Window functions do not accept xp parameter - PR #21783 changes not applied")
        raise


def test_array_api_compatibility_basic():
    """
    Test basic array API compatibility.
    """
    M = 6
    
    try:
        from scipy.signal.windows import blackman, hamming
        
        # Test that functions work with xp parameter
        result1 = blackman(M, xp=np)
        result2 = hamming(M, xp=np)
        
        assert isinstance(result1, np.ndarray)
        assert isinstance(result2, np.ndarray)
        assert len(result1) == M
        assert len(result2) == M
        
    except TypeError as e:
        if "unexpected keyword argument 'xp'" in str(e):
            pytest.fail("Window functions do not accept xp parameter - PR #21783 changes not applied")
        raise


if __name__ == "__main__":
    # This is just for manual testing
    print("Test file created. Run with pytest to see behavior.")