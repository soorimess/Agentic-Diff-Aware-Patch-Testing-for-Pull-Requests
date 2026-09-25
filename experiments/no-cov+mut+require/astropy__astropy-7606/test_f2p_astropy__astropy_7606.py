"""
Regression test for astropy issue with UnrecognizedUnit equality comparison with None

This test ensures that comparing an UnrecognizedUnit with None returns False,
not a TypeError.
"""
import astropy.units as u


def test_unrecognized_unit_eq_none_returns_false():
    """Test that UnrecognizedUnit equality comparison with None returns False (not TypeError)"""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False


def test_unrecognized_unit_ne_none_returns_true():
    """Test that UnrecognizedUnit inequality comparison with None returns True (not TypeError)"""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should return True, not raise TypeError
    result = x != None
    assert result is True


def test_regular_unit_eq_none_returns_false():
    """Test that regular Unit equality comparison with None returns False (not TypeError)"""
    # Create a regular unit
    x = u.Unit('m')
    
    # This should return False, not raise TypeError
    result = x == None
    assert result is False