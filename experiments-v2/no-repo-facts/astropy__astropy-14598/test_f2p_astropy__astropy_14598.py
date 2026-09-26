"""
Test for FITS Card double quote handling issue.
This reproduces the bug where double single quotes ('') are incorrectly 
converted to single quotes ('), particularly around certain string lengths.
"""

import pytest
from astropy.io import fits


def test_card_double_single_quotes_handling():
    """Test that double single quotes are preserved correctly in FITS cards."""
    
    # Test case 1: String with double quotes at the end (from the bug report)
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )
        
    # Test case 2: String with double quotes in the middle (from the bug report)
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_card_double_quotes_edge_cases():
    """Test edge cases with double quotes."""
    
    # Test with exactly 65 characters (the boundary mentioned in bug report)
    card1 = fits.Card('TEST', "x" * 65 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for 65 chars: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with exactly 67 characters (another boundary)
    card1 = fits.Card('TEST', "x" * 67 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for 67 chars: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with double quotes in the middle
    card1 = fits.Card('TEST', "x" * 55 + "''" + "y" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for middle quotes: expected {card1.value!r}, got {card2.value!r}"
    )