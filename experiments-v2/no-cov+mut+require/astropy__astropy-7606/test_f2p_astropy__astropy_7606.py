# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
Regression tests for UnrecognizedUnit equality comparison with None.
"""
import pytest

from astropy import units as u


def test_unrecognized_unit_equality_with_none():
    """
    Test that comparing UnrecognizedUnit with None returns False, not TypeError.
    
    This is a regression test for the bug where:
    x = u.Unit('asdf', parse_strict='silent')
    x == None  # Should be False, not raise TypeError
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False
    
    # Also test the != operator
    result = x != None
    assert result is True


def test_unrecognized_unit_equality_with_none_reverse():
    """
    Test that comparing None with UnrecognizedUnit also works correctly.
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should also return False, not raise TypeError
    result = None == x
    assert result is False
    
    # Also test the != operator
    result = None != x
    assert result is True