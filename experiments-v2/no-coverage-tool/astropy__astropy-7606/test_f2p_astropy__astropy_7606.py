# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue where unit equality comparison with None
raises TypeError for UnrecognizedUnit.
"""

from astropy import units as u


def test_unrecognized_unit_equality_with_none():
    """Test that UnrecognizedUnit equality comparison with None returns False, not TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, but should return False
    # The bug was: TypeError: None is not a valid Unit
    # The fix should make it return False instead
    result = x == None
    assert result is False


def test_unrecognized_unit_inequality_with_none():
    """Test that UnrecognizedUnit inequality comparison with None returns True."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError, but should return True
    # Since x != None should be True (they are not equal)
    result = x != None
    assert result is True