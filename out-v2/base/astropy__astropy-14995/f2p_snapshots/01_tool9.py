# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression test for astropy issue with NDDataRef mask propagation.

This test ensures that when one operand does not have a mask, 
the mask propagation works correctly with handle_mask=np.bitwise_or.
"""

import numpy as np
import pytest
from astropy.nddata import NDDataRef


def test_nddataref_mask_propagation_with_bitwise_or():
    """Test mask propagation when one operand does not have a mask."""
    
    # Create test data
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    # Create NDDataRef instances
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # Test cases that should work without error
    # multiply no mask by constant (no mask * no mask) - this should work
    result1 = nref_nomask.multiply(1., handle_mask=np.bitwise_or)
    assert result1.mask is None
    
    # multiply no mask by itself (no mask * no mask) - this should work
    result2 = nref_nomask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result2.mask is None
    
    # multiply mask by constant (mask * no mask) - this should work
    result3 = nref_mask.multiply(1., handle_mask=np.bitwise_or)
    assert result3.mask is not None
    np.testing.assert_array_equal(result3.mask, mask)
    
    # multiply mask by itself (mask * mask) - this should work
    result4 = nref_mask.multiply(nref_mask, handle_mask=np.bitwise_or)
    assert result4.mask is not None
    np.testing.assert_array_equal(result4.mask, mask)
    
    # This is the key test case that was failing before the fix:
    # multiply mask by no mask (mask * no mask) - this should work but was failing
    result5 = nref_mask.multiply(nref_nomask, handle_mask=np.bitwise_or)
    assert result5.mask is not None
    np.testing.assert_array_equal(result5.mask, mask)


def test_nddataref_mask_propagation_edge_cases():
    """Test additional edge cases for mask propagation."""
    
    array = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mask = np.array([[0, 1, 64], [8, 0, 1], [2, 1, 0]])
    
    nref_nomask = NDDataRef(array)
    nref_mask = NDDataRef(array, mask=mask)
    
    # Test with different handle_mask functions
    # Test with logical_or (default)
    result1 = nref_mask.multiply(nref_nomask, handle_mask=np.logical_or)
    assert result1.mask is not None
    np.testing.assert_array_equal(result1.mask, mask)
    
    # Test with None handle_mask
    result2 = nref_mask.multiply(nref_nomask, handle_mask=None)
    assert result2.mask is None