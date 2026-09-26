# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue where unit equality comparison with None
raises TypeError for UnrecognizedUnit.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none():
    """Test that comparing UnrecognizedUnit with None does not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Before the fix, this would raise TypeError: None is not a valid Unit
    # After the fix, this should return False (not raise an exception)
    # The comparison should not raise an exception
    result = x == None
    
    # The comparison should return False, not raise an exception
    assert result is False


def test_unrecognized_unit_ne_none():
    """Test that comparing UnrecognizedUnit with None for inequality does not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should also not raise TypeError
    result = x != None
    
    # The comparison should return True (not raise an exception)
    assert result is True