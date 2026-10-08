# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_bug_regression():
    """
    Regression test for NDDataRef mask propagation bug in v5.3.
    
    When one operand does not have a mask, the mask propagation should work
    correctly instead of raising TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'.
    
    Specifically tests the case where:
    - self has a mask 
    - operand exists but has no mask (operand.mask is None)
    - This should return the mask from self, not fail
    """
    # Create test data
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    # Create NDDataRef instances with and without masks
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # This is the exact failing case from the bug report:
    # mask * no mask (should not fail with TypeError)
    # Before fix: TypeError: unsupported operand type(s) for |: 'int' and 'NoneType'
    # After fix: should return the mask from nref_mask
    result = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    
    # Verify the result has the correct mask (should be the same as nref_mask.mask)
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)
    
    # Also test the other direction
    result2 = nref_nomask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result2.mask is not None
    np.testing.assert_array_equal(result2.mask, mask)