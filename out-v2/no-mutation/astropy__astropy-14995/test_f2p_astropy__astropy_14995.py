"""
Regression test for NDDataRef mask propagation bug.

This test ensures that when one operand does not have a mask, 
mask propagation works correctly with handle_mask=np.bitwise_or.
"""
import numpy as np
import pytest
from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_bug_case_1():
    """Test the specific case from the bug report that fails."""
    # Create test data exactly as in the bug report
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    # Create NDDataRef instances
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # This should NOT raise TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
    # The bug occurs in: nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    result = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    # Should have a mask (the original mask from nref_mask)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)


def test_nddataref_mask_propagation_bug_case_2():
    """Test the other failing case from the bug report."""
    # Create test data exactly as in the bug report
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    # Create NDDataRef instances
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # This should NOT raise TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
    # The bug occurs in: nref_mask.multiply(1., handle_mask=np.bitwise_or)
    result = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    # Should have a mask (the original mask from nref_mask)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)


def test_nddataref_mask_propagation_comprehensive():
    """Test various combinations of mask propagation."""
    # Create test data
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    # Create NDDataRef instances
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # Test case 1: mask * no mask (should preserve mask)
    result1 = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result1.mask is not None
    np.testing.assert_array_equal(result1.mask, mask)
    
    # Test case 2: no mask * mask (should preserve mask) 
    result2 = nref_nomask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result2.mask is not None
    np.testing.assert_array_equal(result2.mask, mask)
    
    # Test case 3: mask * constant (should preserve mask)
    result3 = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    assert result3.mask is not None
    np.testing.assert_array_equal(result3.mask, mask)
    
    # Test case 4: no mask * constant (should not have mask)
    result4 = nref_nomask.multiply(1., handle_mask=np.bitwise_or)
    assert result4.mask is None
    
    # Test case 5: both have masks (should combine masks)
    result5 = nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result5.mask is not None
    np.testing.assert_array_equal(result5.mask, mask)
    
    # Test case 6: neither has masks (should not have mask)
    result6 = nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result6.mask is None