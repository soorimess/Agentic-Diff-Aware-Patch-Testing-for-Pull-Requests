# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue with unit equality comparison with None.
Before the fix, comparing an UnrecognizedUnit with None would raise TypeError.
After the fix, it should return False without raising an exception.
"""

import pytest
from astropy import units as u
from astropy.units.core import UnrecognizedUnit


def test_unrecognized_unit_equality_with_none():
    """
    Test that comparing UnrecognizedUnit with None doesn't raise TypeError.
    
    This is a regression test for the bug where:
    x = u.Unit('asdf', parse_strict='silent')
    x == None  # Should be False, not raise TypeError
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Verify it's actually an UnrecognizedUnit
    assert isinstance(x, UnrecognizedUnit)
    
    # Before the fix, this would raise TypeError
    # After the fix, this should return False
    result = x == None
    
    # The comparison should return False, not raise an exception
    assert result is False


def test_none_equality_with_unrecognized_unit():
    """
    Test that comparing None with UnrecognizedUnit doesn't raise TypeError.
    
    This tests the reverse comparison which should also work properly.
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Verify it's actually an UnrecognizedUnit
    assert isinstance(x, UnrecognizedUnit)
    
    # This should also work without raising TypeError
    result = None == x
    
    # The comparison should return False, not raise an exception
    assert result is False