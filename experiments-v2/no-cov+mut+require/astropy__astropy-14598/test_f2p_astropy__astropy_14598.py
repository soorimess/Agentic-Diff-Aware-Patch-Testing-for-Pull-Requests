"""
Regression test for FITS Card double single-quote handling issue.

This test verifies that FITS cards properly handle double single quotes ('')
in string values, particularly when they represent null strings.
"""

import pytest
from astropy.io import fits


def test_fits_card_double_single_quotes():
    """Test that double single quotes are properly handled in FITS cards."""
    
    # Test case 1: String with double quotes at the end (from bug report)
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be equal - this was failing before the fix
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value} != {card2.value}"
        )
    
    # Test case 2: String with double quotes in the middle (from bug report)
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be equal - this was failing before the fix
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value} != {card2.value}"
        )


def test_fits_card_null_string_handling():
    """Test specific null string handling in FITS cards."""
    
    # Test with exactly the problematic cases from the bug report
    card1 = fits.Card('CONFIG', "x" * 65 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('CONFIG', "x" * 67 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('CONFIG', "x" * 68 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('CONFIG', "x" * 69 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_fits_card_string_with_quotes_in_middle():
    """Test strings with quotes in the middle."""
    
    # Test with quotes in the middle
    card1 = fits.Card('CONFIG', "x" * 55 + "''" + "x" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('CONFIG', "x" * 56 + "''" + "x" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('CONFIG', "x" * 57 + "''" + "x" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value