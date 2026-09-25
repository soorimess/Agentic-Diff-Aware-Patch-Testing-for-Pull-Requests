"""
Regression test for bug where unit equality comparison with None
raises TypeError for UnrecognizedUnit.

This test ensures the behavior described in the issue:
https://github.com/astropy/astropy/issues/7606
"""

import pytest
from astropy import units as u


def test_unrecognized_unit_eq_none_returns_false():
    """Test that comparing UnrecognizedUnit with None returns False, not TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Before fix: TypeError raised  
    # After fix: should return False without raising TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none_returns_true():
    """Test that comparing UnrecognizedUnit with None via != returns True, not TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # Before fix: TypeError raised
    
    # After fix: should return True without raising TypeError
    result = x != None
    assert result is True


def test_unrecognized_unit_eq_unrecognized_unit():
    """Test that UnrecognizedUnit equality comparison with another UnrecognizedUnit works properly."""
    # Create two different UnrecognizedUnits with same name
    x = u.Unit('test', parse_strict='silent')
    y = u.Unit('test', parse_strict='silent')
    
    # Both should be equal (same name)
    # This tests that type(self) comparison works (new behavior)
    result = x == y
    assert result is True


def test_regular_unit_comparison_with_none():
    """Test that regular units don't erroneously raise TypeError with None."""
    # Test that regular unit equality with None works (uses UnitBase.__eq__)
    x = u.meter
    
    # Should NOT raise TypeError
    result = x == None
    # May return NotImplemented or False depending on Python's comparison protocol
    # but definitely should not raise TypeError
    # Here we're just making sure the TypeError is covered, not testing specific return value
    try:
        result = x == None
        # If we get here without TypeError, this is success
        assert True  # Just to make test pass
    except TypeError:
        pytest.fail("Regular Unit == None raised TypeError when it shouldn't")