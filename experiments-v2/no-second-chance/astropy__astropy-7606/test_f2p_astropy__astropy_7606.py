# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue where unit equality comparison with None
raises TypeError for UnrecognizedUnit.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_equality_with_none():
    """Test that comparing UnrecognizedUnit to None returns False, not TypeError.
    
    This is a regression test for the bug where:
    x = u.Unit('asdf', parse_strict='silent')
    x == None  # Should be False, not raise TypeError
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # These should not raise TypeError but should return False
    result = x == None
    assert result is False
    
    result = None == x
    assert result is False
    
    result = x != None
    assert result is True
    
    result = None != x
    assert result is True


def test_unrecognized_unit_equality_with_another_unrecognized_unit():
    """Test that UnrecognizedUnit equality works with another UnrecognizedUnit.
    
    This ensures the isinstance check change (line 1718) works correctly:
    isinstance(other, type(self)) instead of isinstance(other, UnrecognizedUnit)
    """
    # Create two UnrecognizedUnits with the same name
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # They should be equal
    assert x == y
    
    # Create two UnrecognizedUnits with different names
    z = u.Unit('other', parse_strict='silent')
    
    # They should not be equal
    assert x != z


def test_regular_unit_equality_with_invalid_input():
    """Test that regular Unit equality with invalid inputs returns NotImplemented.
    
    This tests the first change in the diff - in main Unit.__eq__ method.
    When an invalid input is passed to Unit() constructor, it should return NotImplemented
    instead of raising an exception.
    """
    # Create a regular unit
    x = u.Unit('m')
    
    # This should return NotImplemented (not raise TypeError)
    # The exact return value depends on Python's comparison protocol,
    # but the key thing is no TypeError should be raised
    try:
        result = x.__eq__(None)
        # If we get here without TypeError, that's what we want
        # The actual return value may be NotImplemented or False, but not TypeError
        assert result is not True  # We don't care about exact return, just no TypeError
    except TypeError:
        pytest.fail("Regular Unit.__eq__ should not raise TypeError when comparing to None")