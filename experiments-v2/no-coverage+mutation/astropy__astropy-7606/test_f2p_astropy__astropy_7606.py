# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue where unit equality comparison with None
raises TypeError for UnrecognizedUnit.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none():
    """Test that UnrecognizedUnit == None returns False, not TypeError."""
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none():
    """Test that UnrecognizedUnit != None returns True, not TypeError."""
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_unrecognized_unit_eq_none_with_regular_unit():
    """Test that regular unit comparison with None works correctly."""
    x = u.Unit('m')
    
    # Regular units should still work normally
    result = x == None
    assert result is False


def test_unrecognized_unit_eq_none_inverted():
    """Test that None == UnrecognizedUnit also works correctly."""
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should also return False, not raise TypeError
    result = None == x
    assert result is False