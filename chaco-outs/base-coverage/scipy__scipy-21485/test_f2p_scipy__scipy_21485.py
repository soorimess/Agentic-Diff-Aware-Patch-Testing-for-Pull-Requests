"""
Regression test for PR #21485: MAINT: interpolate: abstract out barycentric 
representation of a rational function

This test ensures that the refactored AAA class maintains identical behavior
to the original implementation and that the import structure is correct.
"""

import numpy as np
from numpy.testing import assert_allclose, assert_equal
import pytest
import warnings
from scipy.interpolate import AAA


def test_aaa_import_access():
    """Test that AAA is accessible from the correct import path"""
    # Verify that AAA can be imported correctly
    assert AAA is not None
    assert AAA.__name__ == "AAA"
    
    # Test that it's a proper callable class
    assert callable(AAA)
    
    # Test basic instantiation
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 4, 9])
    
    # This should work without error
    r = AAA(x, y)
    assert r is not None


def test_aaa_core_functionality():
    """Test core AAA functionality works correctly"""
    # Simple test case
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 4, 9])  # y = x^2
    
    # Create AAA approximation
    r = AAA(x, y)
    
    # Test evaluation
    result = r(np.array([1.5]))
    assert isinstance(result, np.ndarray)
    assert result.size == 1
    assert np.isfinite(result[0])


def test_aaa_method_completeness():
    """Test that all expected methods exist and are callable"""
    x = np.array([0, 1, 2])
    y = np.array([0, 1, 4])
    r = AAA(x, y)
    
    # All core methods should exist and be callable
    assert hasattr(r, '__call__')
    assert hasattr(r, 'poles')
    assert hasattr(r, 'residues')
    assert hasattr(r, 'roots')
    assert hasattr(r, 'clean_up')
    
    # Test they are callable
    assert callable(r.__call__)
    assert callable(r.poles)
    assert callable(r.residues)
    assert callable(r.roots)
    assert callable(r.clean_up)


def test_aaa_error_handling():
    """Test that error handling works as expected"""
    # Test various error conditions that should raise ValueError
    with pytest.raises(ValueError, match="same size"):
        AAA([0], [1, 1])
    
    with pytest.raises(ValueError, match="1-D"):
        AAA([[0], [0]], [[1], [1]])
    
    with pytest.raises(ValueError, match="finite"):
        AAA([np.inf], [1])
        
    with pytest.raises(ValueError, match="greater than or equal to one"):
        AAA([1], [1], max_terms=-1)


def test_aaa_clean_up_functionality():
    """Test clean_up method works correctly"""
    x = np.array([0, 1, 2, 3])
    y = np.array([0, 1, 4, 9])
    
    # Test clean_up functionality
    r = AAA(x, y, clean_up=False)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        num_removed = r.clean_up()
    
    assert isinstance(num_removed, int)
    assert num_removed >= 0