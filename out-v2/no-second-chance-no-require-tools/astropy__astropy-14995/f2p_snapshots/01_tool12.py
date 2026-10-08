# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_with_none_mask():
    """
    Test for bug where NDDataRef mask propagation fails when one operand
    does not have a mask.
    
    In v5.3, when one operand does not have a mask, the mask propagation
    with handle_mask=np.bitwise_or fails with TypeError: unsupported operand
    type(s) for |: 'int' and 'NoneType'.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)

    # Test cases that should work without error
    # multiply no mask by constant (no mask * no mask)
    result1 = nref_nomask.multiply(1., handle_mask=np.bitwise_or)
    assert result1.mask is None

    # multiply no mask by itself (no mask * no mask)
    result2 = nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result2.mask is None

    # multiply mask by constant (mask * no mask) - this was failing
    result3 = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    assert result3.mask is not None
    np.testing.assert_array_equal(result3.mask, mask)

    # multiply mask by itself (mask * mask)
    result4 = nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or)
    np.testing.assert_array_equal(result4.mask, mask)

    # multiply mask by no mask (mask * no mask) - this was failing
    result5 = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result5.mask is not None
    np.testing.assert_array_equal(result5.mask, mask)