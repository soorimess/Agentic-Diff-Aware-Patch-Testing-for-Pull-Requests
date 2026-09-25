"""
Regression test for issue where unit equality comparison with None
raises TypeError for UnrecognizedUnit instead of returning False.

This test verifies that x == None for UnrecognizedUnit does not raise TypeError.
"""
import pytest
import astropy.units as u


def test_unrecognized_unit_eq_none_no_typeerror():
    """Test that UnrecognizedUnit equality with None does not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should NOT raise TypeError
    # Previously this raised: TypeError: None is not a valid Unit
    try:
        result = x == None
        # If we get here without exception, that means the bug is fixed
        # The original bug was a TypeError being raised
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            pytest.fail("UnrecognizedUnit.__eq__ still raises TypeError when comparing to None")
        else:
            raise  # Re-raise if it's a different TypeError


def test_unrecognized_unit_ne_none_no_typeerror():
    """Test that UnrecognizedUnit inequality with None does not raise TypeError."""
    # Create an UnrecognizedUnit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should NOT raise TypeError
    try:
        result = x != None
        # If we get here without exception, that means the bug is fixed
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            pytest.fail("UnrecognizedUnit.__ne__ still raises TypeError when comparing to None")
        else:
            raise  # Re-raise if it's a different TypeError


def test_regular_unit_eq_none_no_typeerror():
    """Test that regular Unit equality with None does not raise TypeError."""
    # Create a regular Unit
    x = u.Unit('m')
    
    # This should NOT raise TypeError (it passes in current code)
    try:
        result = x == None
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            pytest.fail("Unit.__eq__ still raises TypeError when comparing to None")
        else:
            raise  # Re-raise if it's a different TypeError


def test_regular_unit_ne_none_no_typeerror():
    """Test that regular Unit inequality with None does not raise TypeError."""
    # Create a regular Unit
    x = u.Unit('m')
    
    # This should NOT raise TypeError (it passes in current code)
    try:
        result = x != None
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            pytest.fail("Unit.__ne__ still raises TypeError when comparing to None")
        else:
            raise  # Re-raise if it's a different TypeError