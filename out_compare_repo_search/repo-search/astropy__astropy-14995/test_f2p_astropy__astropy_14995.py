# Regression test for astropy/astropy#14995
# Ensure mask propagation does not fail when one operand has no mask

import numpy as np
from numpy.testing import assert_array_equal

from astropy.nddata import NDDataRef


def test_mask_propagation_when_one_operand_has_no_mask_bitwise_or():
    """If one NDDataRef has a mask and the other doesn't, using a
    bitwise_or handle_mask should copy the existing mask to the result
    rather than attempting to operate with None (which raised TypeError).
    """
    data = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    nref_nomask = NDDataRef(data)
    nref_mask = NDDataRef(data, mask=mask)

    # Multiplying masked by a scalar (no mask) should return a copy of the mask
    # even when using a bitwise_or as the handle_mask.
    result = nref_mask.multiply(1.0, handle_mask=np.bitwise_or)

    # The result should have the mask copied from the masked operand
    assert_array_equal(result.mask, mask)
