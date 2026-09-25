"""
Regression test for the issue where Unit('asdf', parse_strict='silent') == None
raises TypeError instead of returning False.
"""

import pytest
import astropy.units as u


def test_unrecognized_unit_equality_with_none():
    """Test that UnrecognizedUnit equality with None returns False, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, but return False
    result = x == None
    assert result is False


def test_unrecognized_unit_inequality_with_none():
    """Test that UnrecognizedUnit inequality with None returns True, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, but return True
    result = x != None
    assert result is True


def test_regular_unit_equality_with_none():
    """Test that regular Unit equality with None returns False, not TypeError."""
    # Create a regular unit
    x = u.Unit('m')
    
    # This should not raise TypeError, but return False
    result = x == None
    assert result is False


def test_regular_unit_inequality_with_none():
    """Test that regular Unit inequality with None returns True, not TypeError."""
    # Create a regular unit
    x = u.Unit('m')
    
    # This should not raise TypeError, but return True
    result = x != None
    assert result is True


def test_unrecognized_unit_equality_with_same_name_unrecognized_unit():
    """Test that UnrecognizedUnit equality with another UnrecognizedUnit of same name returns True."""
    # Create two unrecognized units with same name 
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # This should return True
    result = x == y
    assert result is True


def test_unrecognized_unit_equality_with_different_name_unrecognized_unit():
    """Test that UnrecognizedUnit equality with another UnrecognizedUnit of different name returns False."""  
    # Create two unrecognized units with different names
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('other', parse_strict='silent')
    
    # This should return False
    result = x == y
    assert result is False


def test_unrecognized_unit_equality_with_valid_unit():
    """Test that UnrecognizedUnit equality with a valid Unit returns False."""
    # Create an unrecognized unit and valid unit
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('m')
    
    # This should return False
    result = x == y
    assert result is False