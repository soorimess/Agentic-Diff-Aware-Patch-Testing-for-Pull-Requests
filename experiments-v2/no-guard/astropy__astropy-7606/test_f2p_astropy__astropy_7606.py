"""
Regression test for bug where unit equality comparison with None
raises TypeError for UnrecognizedUnit.

This test ensures that comparing an UnrecognizedUnit with None
returns False instead of raising a TypeError.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_equality_with_none():
    """Test that UnrecognizedUnit == None returns False, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_inequality_with_none():
    """Test that UnrecognizedUnit != None returns True, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_unrecognized_unit_equality_with_same_name():
    """Test that UnrecognizedUnit equality works with same name."""
    # Create two unrecognized units with same name
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # These should be equal
    assert x == y


def test_unrecognized_unit_equality_with_different_name():
    """Test that UnrecognizedUnit inequality works with different name."""
    # Create two unrecognized units with different names
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('other', parse_strict='silent')
    
    # These should not be equal
    assert x != y


def test_unrecognized_unit_equality_with_regular_unit():
    """Test that UnrecognizedUnit != regular unit."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    # Create a regular unit
    y = u.meter
    
    # These should not be equal
    assert x != y


def test_regular_unit_equality_with_problematic_value():
    """
    Test that regular Unit.__eq__ properly handles exceptions.
    This tests the change in base Unit.__eq__ method where it now
    returns NotImplemented instead of False when Unit(other, parse_strict='silent')
    raises an exception.
    """
    # Create a regular unit
    x = u.meter
    
    # Test with a value that will cause Unit() to raise TypeError
    # This should not raise TypeError but should return NotImplemented
    # which will cause Python to try the other operand's __eq__ method
    try:
        result = x == None
        # If we get here without exception, it should be False (since None != meter)
        assert result is False
    except TypeError:
        # If we get TypeError, that means the fix isn't working
        pytest.fail("Regular Unit comparison with None should not raise TypeError")