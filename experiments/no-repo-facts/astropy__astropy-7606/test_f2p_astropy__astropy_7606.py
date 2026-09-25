# -*- coding: utf-8 -*-
"""
Test for the bug where UnrecognizedUnit equality comparison with None raises TypeError.
Regression test for astropy/astropy#7606
"""

import astropy.units as u


def test_unrecognized_unit_eq_none_no_longer_raises():
    """Core test: UnrecognizedUnit == None should not raise TypeError."""
    # Create an UnrecognizedUnit 
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, should return False (the fix)
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none_no_longer_raises():
    """Core test: UnrecognizedUnit != None should not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, should return True (the fix)
    result = x != None
    assert result is True


def test_unrecognized_unit_eq_none_reversed_no_longer_raises():
    """Core test: None == UnrecognizedUnit should not raise TypeError.""" 
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, should return False (the fix)  
    result = None == x
    assert result is False


def test_unrecognized_unit_ne_none_reversed_no_longer_raises():
    """Core test: None != UnrecognizedUnit should not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, should return True (the fix)
    result = None != x
    assert result is True


def test_unrecognized_unit_equal_instances():
    """Test that two UnrecognizedUnits with same name are equal."""
    # Create two UnrecognizedUnits with same name
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # Should be equal - testing line 1718 execution path
    result = x == y
    assert result is True


def test_unrecognized_unit_different_instances():
    """Test that two UnrecognizedUnits with different names are not equal.""" 
    # Create two UnrecognizedUnits with different names
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('other', parse_strict='silent')
    
    # Should not be equal - testing line 1718 execution path
    result = x == y
    assert result is False