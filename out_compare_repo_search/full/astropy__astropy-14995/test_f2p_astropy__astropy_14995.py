import numpy as np
from astropy.nddata import NDDataRef


def test_mask_propagation_with_operand_without_mask_bitwise_or():
    """Regression test for astropy#14995: when one operand has a mask and
    the other does not, mask propagation using a bitwise-or handler should
    copy the existing mask to the result rather than attempting to apply the
    handler to ``None`` (which raised TypeError in v5.3).
    """
    data = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    # use integer mask (bitmask) to exercise bitwise_or behaviour
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]], dtype=np.int64)

    nref_nomask = NDDataRef(data)
    nref_mask = NDDataRef(data, mask=mask)

    # This used to raise TypeError because operand.mask was None and the
    # handler (np.bitwise_or) was called with (mask, None). The correct
    # behaviour is to copy the existing mask to the result.
    result = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)

    assert result.mask is not None
    # mask should be copied unchanged
    assert np.array_equal(result.mask, mask)
