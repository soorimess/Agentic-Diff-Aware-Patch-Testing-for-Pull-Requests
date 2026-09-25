"""
Regression test for the issue where unit equality comparison with None 
raises TypeError for UnrecognizedUnit.

This test should fail when run against the old code and pass when run 
against the fixed code.
"""

import pytest
import astropy.units as u


def test_unrecognized_unit_equality_with_none_returns_false():
    """
    Test that UnrecognizedUnit == None returns False instead of raising TypeError.
    This verifies the fix for the TypeError bug.
    """
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should NOT raise TypeError, but return False (the proper behavior)
    # The key assertion is that it doesn't raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_inequality_with_none_returns_true():
    """
    Test that UnrecognizedUnit != None returns True (not raising TypeError).
    """
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should NOT raise TypeError, but return True
    result = x != None
    assert result is True


def test_normal_unit_equality_with_none_returns_false():
    """Test that normal Unit == None returns False (should continue working)."""
    # Create a normal unit
    x = u.Unit('m')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_normal_unit_inequality_with_none_returns_true():
    """Test that normal Unit != None returns True (should continue working)."""
    # Create a normal unit
    x = u.Unit('m')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_unrecognized_unit_equality_with_same_name_returns_true():
    """
    Additional test to make sure that legitimate equality comparison still works.
    """
    # Create two unrecognized units with same name
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # These should be equal
    result = x == y
    assert result is True


def test_unrecognized_unit_equality_with_different_name_returns_false():
    """
    Additional test to make sure that legitimate equality comparison still works.
    """
    # Create two unrecognized units with different names
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('other', parse_strict='silent')
    
    # These should NOT be equal
    result = x == y
    assert result is False