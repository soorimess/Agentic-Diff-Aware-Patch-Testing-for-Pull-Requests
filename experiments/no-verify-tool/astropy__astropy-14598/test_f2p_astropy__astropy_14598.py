"""
Test to verify FITS Card handling of double single quotes ('')
This test pins down the specific behavior change in astropy PR.
"""
import pytest
from astropy.io import fits


def test_double_single_quotes_preserved():
    """Test that double single quotes are preserved, not converted to single quotes."""
    
    # Test case where double quotes get converted incorrectly in old version 
    # This should pass after the fix, fail before it
    card1 = fits.Card('CONFIG', "x" * 65 + "''")
    card2 = fits.Card.fromstring(str(card1))
    
    # The bug was that card1.value had "x"*65 + "''" but card2.value had "x"*65 + "'"
    # The fix ensures they stay as double quotes
    assert card1.value == card2.value
    assert card1.value.endswith("''")
    assert card2.value.endswith("''")
    
    # Additional test cases from the bug report  
    test_cases = [
        (67, "x" * 67 + "''"),
        (68, "x" * 68 + "''"), 
        (69, "x" * 69 + "''"),
    ]
    
    for length, value in test_cases:
        card1 = fits.Card('CONFIG', value)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value
        assert card1.value.endswith("''")


def test_double_quotes_in_middle_preserved():
    """Test that double quotes in middle of string are also preserved."""
    
    # Test case where quotes are in the middle of string
    card1 = fits.Card('CONFIG', "x" * 55 + "''" + "x"*10)
    card2 = fits.Card.fromstring(str(card1))
    
    assert card1.value == card2.value
    assert "''" in card1.value
    assert "''" in card2.value
    
    # Additional test cases
    test_cases = [
        (56, "x" * 56 + "''" + "x"*10),
        (57, "x" * 57 + "''" + "x"*10),
    ]
    
    for length, value in test_cases:
        card1 = fits.Card('CONFIG', value)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value
        assert "''" in card1.value
        assert "''" in card2.value


def test_no_regression_for_normal_values():
    """Test that normal values still work correctly."""
    
    # Test normal string without quotes
    card1 = fits.Card('CONFIG', "normal value")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    # Test string with single quotes (not double)
    card1 = fits.Card('COMMENT', "This is a 'quoted' value") 
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value