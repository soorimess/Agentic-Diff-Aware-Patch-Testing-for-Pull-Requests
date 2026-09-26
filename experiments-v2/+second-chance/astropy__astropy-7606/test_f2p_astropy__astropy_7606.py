"""
Regression test for issue where unit equality comparison with None raises TypeError
for UnrecognizedUnit.

Before the fix, comparing an UnrecognizedUnit to None would raise a TypeError
because the UnrecognizedUnit.__eq__ method didn't handle the exception properly.
"""
import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none():
    """Test that UnrecognizedUnit equality with None returns False, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none():
    """Test that UnrecognizedUnit inequality with None returns True, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_regular_unit_eq_none():
    """Test that regular Unit equality with None returns False, not TypeError."""
    # Create a regular unit
    x = u.Unit('m')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_regular_unit_ne_none():
    """Test that regular Unit inequality with None returns True, not TypeError."""
    # Create a regular unit
    x = u.Unit('m')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_unrecognized_unit_eq_same_name():
    """Test that two UnrecognizedUnits with same name are equal."""
    # Create two unrecognized units with the same name
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # This should return True
    result = x == y
    assert result is True


def test_unrecognized_unit_eq_different_name():
    """Test that two UnrecognizedUnits with different names are not equal."""
    # Create two unrecognized units with different names
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('qwer', parse_strict='silent')
    
    # This should return False
    result = x == y
    assert result is False