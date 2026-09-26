# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Regression test for issue with unit equality comparison with None
raising TypeError for UnrecognizedUnit.
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_equality_with_none():
    """
    Test that comparing UnrecognizedUnit with None does not raise TypeError.
    
    Before the fix, this would raise TypeError: "None is not a valid Unit"
    After the fix, this should return NotImplemented so that Python can 
    properly handle the comparison (None == unit should return False).
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError
    # Before fix: TypeError would be raised
    # After fix: NotImplemented should be returned (allowing Python to try reverse comparison)
    try:
        result = x == None
        # If we get here without exception, the behavior is correct
        # The result should be False (when Python tries reverse comparison)
        assert result is False or result is NotImplemented
    except TypeError as e:
        # If we get TypeError, that means the bug is still present
        assert "None is not a valid Unit" in str(e)
        raise


def test_unrecognized_unit_equality_with_none_reverse():
    """
    Test the reverse comparison None == UnrecognizedUnit.
    
    This should return False without raising an exception.
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False without raising TypeError
    result = None == x
    assert result is False


def test_regular_unit_equality_with_none():
    """
    Test that comparing regular Unit with None does not raise TypeError.
    
    This tests the change in the base Unit.__eq__ method.
    """
    # Create a regular unit
    x = u.Unit('m')  # meter
    
    # This should not raise TypeError
    try:
        result = x == None
        # Should return False (since regular units are not None)
        assert result is False
    except TypeError as e:
        # If we get TypeError, that means the bug is still present
        assert "None is not a valid Unit" in str(e)
        raise


def test_unrecognized_unit_equality_with_other_units():
    """
    Test that UnrecognizedUnit still works correctly with other units.
    """
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Compare with another UnrecognizedUnit with same name
    y = u.Unit('asdf', parse_strict='silent')
    assert x == y
    
    # Compare with a different UnrecognizedUnit
    z = u.Unit('other', parse_strict='silent')
    assert x != z
    
    # Compare with a regular unit
    regular_unit = u.Unit('m')
    assert x != regular_unit