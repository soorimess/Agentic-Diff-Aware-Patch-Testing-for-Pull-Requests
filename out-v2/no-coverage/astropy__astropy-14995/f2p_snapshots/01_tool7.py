# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import pytest

from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_with_none_operand():
    """
    Test for bug where NDDataRef mask propagation fails when one operand
    does not have a mask.
    
    This is a regression test for the issue where multiplying an NDDataRef
    with a mask by one without a mask fails with a TypeError when using
    handle_mask=np.bitwise_or.
    """
    # Create test data
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    # Create NDDataRef instances - one with mask, one without
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # Test case 1: mask * no mask should work (this was failing before fix)
    result = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    # Should not raise TypeError and should preserve the mask from the operand with mask
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)
    
    # Test case 2: no mask * mask should work (this was also failing before fix)
    result = nref_nomask.multiply(nref_mask, handle_mask=np.bitwise_or)
    # Should not raise TypeError and should preserve the mask from the operand with mask
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)
    
    # Test case 3: mask * constant (no mask operand) should work
    result = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    # Should not raise TypeError and should preserve the mask from the operand with mask
    assert result.mask is not None
    np.testing.assert_array_equal(result.mask, mask)
    
    # Test case 4: no mask * constant (no mask operand) should work
    result = nref_nomask.multiply(1., handle_mask=np.bitwise_or)
    # Should not raise TypeError and should have no mask
    assert result.mask is None


def test_nddataref_mask_propagation_edge_cases():
    """
    Additional edge case tests for mask propagation.
    """
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # Test with different arithmetic operations
    operations = [
        ('add', lambda a, b: a.add(b, handle_mask=np.bitwise_or)),
        ('subtract', lambda a, b: a.subtract(b, handle_mask=np.bitwise_or)),
        ('multiply', lambda a, b: a.multiply(b, handle_mask=np.bitwise_or)),
        ('divide', lambda a, b: a.divide(b, handle_mask=np.bitwise_or)),
    ]
    
    for op_name, op_func in operations:
        # Test operand1 has mask, operand2 doesn't
        if op_name != 'divide':  # divide might have different behavior
            result = op_func(nref_mask, nref_nomask)
            assert result.mask is not None
            np.testing.assert_array_equal(result.mask, mask)
            
            # Test operand1 doesn't have mask, operand2 has
            result = op_func(nref_nomask, nref_mask)
            assert result.mask is not None
            np.testing.assert_array_equal(result.mask, mask)