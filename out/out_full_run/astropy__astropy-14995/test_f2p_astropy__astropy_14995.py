import numpy as np
from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_when_one_operand_has_no_mask():
    """Test that when one NDDataRef has a mask and the other does not,
    the resulting mask is copied from the operand that has a mask when
    handle_mask is a bitwise-or-like callable.

    This was broken in a past release where passing an operand without a
    mask caused a TypeError because the mask-handling code attempted to
    apply the callable to ``None``.
    """
    data = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])

    nref_nomask = NDDataRef(data)
    nref_mask = NDDataRef(data, mask=mask)

    # Multiply masked by unmasked: the mask should be copied to the result.
    res = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)

    assert res.mask is not None
    assert np.array_equal(res.mask, mask)
