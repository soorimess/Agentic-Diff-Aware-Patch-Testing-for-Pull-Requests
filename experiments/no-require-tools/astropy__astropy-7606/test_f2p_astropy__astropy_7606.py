"""
Regression test for the bug: Unit equality comparison with None raises TypeError for UnrecognizedUnit

This test should ensure that comparing UnrecognizedUnit with None does not raise
TypeError and instead returns a reasonable value.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none_no_typeerror():
    """Test that comparing UnrecognizedUnit with None does not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError in the fixed version
    result = x == None
    # If it works without TypeError, the fix is working 
    # (result could be False or NotImplemented, but not TypeError)


def test_unrecognized_unit_ne_none_no_typeerror():
    """Test that comparing UnrecognizedUnit with None using != does not raise TypeError."""
    # Create an UnrecognizedUnit  
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError in the fixed version
    result = x != None
    # If it works without TypeError, the fix is working


def test_regular_unit_eq_none_works():
    """Test that comparing regular Unit with None works correctly.""" 
    # Create a regular Unit
    x = u.Unit('meter')
    
    # This should return False (not raise TypeError)
    result = x == None 
    assert result is False


def test_unrecognized_unit_same_name_eq_works():
    """Test that comparing two UnrecognizedUnits with same name works."""
    # Create two UnrecognizedUnits 
    x = u.Unit('asdf', parse_strict='silent')
    y = u.Unit('asdf', parse_strict='silent')
    
    # This should return True when comparing same names
    result = x == y
    assert result is True