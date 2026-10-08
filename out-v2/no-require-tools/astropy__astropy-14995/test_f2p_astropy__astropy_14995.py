# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_bug():
    """
    Test for bug where NDDataRef mask propagation fails when one operand 
    does not have a mask.
    
    This reproduces the issue from astropy issue #14995 where:
    - multiplying a masked NDDataRef by an unmasked NDDataRef 
      with handle_mask=np.bitwise_or raises TypeError
    - The error is: TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
    """
    # Create test data
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    # Create NDDataRef objects
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # These should work fine (no mask propagation issues)
    assert nref_nomask.multiply(1., handle_mask=np.bitwise_or).mask is None
    assert nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or).mask is None
    assert nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or).mask is not None

    # These should NOT raise TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
    # The bug occurs when multiplying a masked NDDataRef by an unmasked one
    result1 = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    assert result1.mask is not None  # Should have the same mask as the original
    
    result2 = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result2.mask is not None  # Should have the same mask as the original
    
    # Verify the mask values are correct
    expected_mask = mask  # Should be the same as original mask
    np.testing.assert_array_equal(result2.mask, expected_mask)


def test_nddataref_mask_propagation_comprehensive():
    """
    Comprehensive test for various mask propagation scenarios.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask1 = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    mask2 = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    nref_no_mask1 = NDDataRef(array)
    nref_mask1 = NDDataRef(array, mask=mask1)
    nref_mask2 = NDDataRef(array, mask=mask2)

    # Test case 1: masked operand with no mask operand (this was the bug)
    result = nref_mask1.multiply(nref_no_mask1, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask1)

    # Test case 2: no mask operand with masked operand
    result = nref_no_mask1.multiply(nref_mask1, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask1)

    # Test case 3: both masked operands
    result = nref_mask1.multiply(nref_mask2, handle_mask=np.bitwise_or)
    assert result.mask is not None
    # Should be bitwise_or of the two masks
    expected = np.bitwise_or(mask1, mask2)
    np.testing.assert_array_equal(result.mask, expected)

    # Test case 4: both no mask operands
    result = nref_no_mask1.multiply(nref_no_mask1, handle_mask=np.bitwise_or)
    assert result.mask is None

    # Test case 5: masked operand with constant
    result = nref_mask1.multiply(2.0, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask1)


if __name__ == "__main__":
    test_nddataref_mask_propagation_bug()
    test_nddataref_mask_propagation_comprehensive()
    print("All tests passed!")