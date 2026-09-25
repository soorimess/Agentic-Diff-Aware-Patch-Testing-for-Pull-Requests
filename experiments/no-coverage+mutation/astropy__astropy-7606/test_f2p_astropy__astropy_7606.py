"""
Regression test for UnrecognizedUnit equality with None.

This test checks that comparing an UnrecognizedUnit with None
doesn't raise a TypeError, but instead behaves properly.
"""

from astropy import units as u


def test_unrecognized_unit_equality_with_none_no_typeerror():
    """Test that UnrecognizedUnit equality with None doesn't raise TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError: "None is not a valid Unit"
    # The bug was that this would raise TypeError in older versions
    try:
        result = x == None
        # If we get here without exception, the fix is working
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            raise AssertionError("UnrecognizedUnit equality with None still raises TypeError")
        else:
            raise


def test_unrecognized_unit_inequality_with_none_no_typeerror():
    """Test that UnrecognizedUnit inequality with None doesn't raise TypeError."""
    # Create an unrecognized unit
    x = u.Unit('asdf', parse_strict='silent')
    
    # This should not raise TypeError: "None is not a valid Unit"  
    try:
        result = x != None
        # If we get here without exception, the fix is working
        assert True
    except TypeError as e:
        if "None is not a valid Unit" in str(e):
            raise AssertionError("UnrecognizedUnit inequality with None still raises TypeError")
        else:
            raise