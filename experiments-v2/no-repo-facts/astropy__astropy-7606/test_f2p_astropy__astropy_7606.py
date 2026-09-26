# -*- coding: utf-8 -*-
"""
Test for regression of UnrecognizedUnit equality comparison with None.
This tests that UnrecognizedUnit == None returns False instead of raising TypeError.
"""
import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none():
    """Test that UnrecognizedUnit equality comparison with None works correctly."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError - it should return False
    # Test forward comparison
    result = x == None
    assert result is False
    
    # Test reverse comparison  
    result = None == x
    assert result is False


def test_unrecognized_unit_eq_other_units():
    """Test that UnrecognizedUnit equality comparison with other units works correctly."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Compare with other units - should return False
    result = x == u.meter
    assert result is False
    
    # Compare with another UnrecognizedUnit with same name
    y = u.Unit('asdf', parse_strict='silent')
    result = x == y
    assert result is True
    
    # Compare with another UnrecognizedUnit with different name
    z = u.Unit('different', parse_strict='silent')
    result = x == z
    assert result is False


def test_unit_eq_none():
    """Test that regular Unit equality comparison with None works correctly."""
    # Create a regular unit
    x = u.meter
    
    # This should not raise TypeError - it should return False
    result = x == None
    assert result is False
    
    # Test reverse comparison  
    result = None == x
    assert result is False