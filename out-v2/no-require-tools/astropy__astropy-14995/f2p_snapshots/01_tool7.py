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


def test_nddataref_mask_propagation_edge_cases():
    """
    Additional test cases for mask propagation edge cases.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # Test multiplication with constant (should preserve mask)
    result = nref_mask.multiply(2.0, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)

    # Test division with constant (should preserve mask) 
    result = nref_mask.divide(2.0, handle_mask=np.bitwise_or)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)

    # Test that operations with no mask on both sides work
    result = nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result.mask is None


if __name__ == "__main__":
    test_nddataref_mask_propagation_bug()
    test_nddataref_mask_propagation_edge_cases()
    print("All tests passed!")