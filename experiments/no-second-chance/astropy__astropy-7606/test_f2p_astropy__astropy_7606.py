"""Test for regression of UnrecognizedUnit equality comparison with None"""

import pytest
import astropy.units as u


def test_unrecognized_unit_eq_none():
    """Test that UnrecognizedUnit == None returns False, not TypeError"""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none():
    """Test that UnrecognizedUnit != None works properly"""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return True (not equal)
    result = x != None
    assert result is True


def test_unrecognized_unit_eq_other_unrecognized():
    """Test that comparing two UnrecognizedUnits works properly"""
    # Create two unrecognized units 
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # This should return True (they're the same unrecognized unit)
    result = x == y
    assert result is True


def test_unrecognized_unit_eq_different_unrecognized():
    """Test that comparing two different UnrecognizedUnits works properly"""
    # Create two different unrecognized units
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('other', parse_strict='silent')
    
    # This should return False (they're different unrecognized units)
    result = x == y
    assert result is False


if __name__ == "__main__":
    test_unrecognized_unit_eq_none()
    test_unrecognized_unit_ne_none()
    test_unrecognized_unit_eq_other_unrecognized()
    test_unrecognized_unit_eq_different_unrecognized()
    print("All tests passed!")