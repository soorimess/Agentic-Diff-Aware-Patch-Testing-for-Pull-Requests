# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest
from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_with_none_mask():
    """
    Test for regression of bug where NDDataRef mask propagation fails 
    when one operand does not have a mask.
    
    This reproduces the specific case from the bug report:
    - nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or) should work
    - Should return the mask from nref_mask since nref_nomask has no mask
    """
    # Create test data exactly as in the bug report
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    # Create NDDataRef objects
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # These should work fine (from bug report)
    assert nref_nomask.multiply(1., handle_mask=np.bitwise_or).mask is None
    assert nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or).mask is None
    
    # These should also work but previously failed with TypeError
    # The bug was that when one operand has no mask, the operation failed
    result1 = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    assert result1.mask is not None
    np.testing.assert_array_equal(result1.mask, mask)
    
    result2 = nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result2.mask is not None
    np.testing.assert_array_equal(result2.mask, mask)
    
    # This is the main failing case from the bug report - should NOT raise TypeError
    result3 = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result3.mask is not None
    np.testing.assert_array_equal(result3.mask, mask)
    
    # Test the reverse case too - should also work
    result4 = nref_nomask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result4.mask is not None
    np.testing.assert_array_equal(result4.mask, mask)


def test_nddataref_mask_propagation_edge_cases():
    """
    Additional test cases for mask propagation edge cases.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask1 = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    mask2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    nref_no_mask1 = NDDataRef(array)
    nref_no_mask2 = NDDataRef(array * 2)
    nref_mask1 = NDDataRef(array, mask=mask1)
    nref_mask2 = NDDataRef(array, mask=mask2)

    # Test various combinations that should not raise errors
    # Both have masks
    result = nref_mask1.multiply(nref_mask2, handle_mask=np.bitwise_or)
    assert result.mask is not None
    
    # First has mask, second doesn't
    result = nref_mask1.multiply(nref_no_mask1, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask1)
    
    # First doesn't have mask, second has mask  
    result = nref_no_mask1.multiply(nref_mask1, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask1)
    
    # Neither have masks
    result = nref_no_mask1.multiply(nref_no_mask2, handle_mask=np.bitwise_or)
    assert result.mask is None


def test_nddataref_addition_operations():
    """
    Test that the fix works for addition operations specifically.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # Test addition operations specifically
    result1 = nref_mask.add(nref_nomask, handle_mask=np.bitwise_or)
    assert result1.mask is not None
    np.testing.assert_array_equal(result1.mask, mask)
    
    result2 = nref_nomask.add(nref_mask, handle_mask=np.bitwise_or)
    assert result2.mask is not None
    np.testing.assert_array_equal(result2.mask, mask)