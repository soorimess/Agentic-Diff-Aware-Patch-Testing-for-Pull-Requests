"""
Regression test for FITS Card double single-quote handling bug.

This test ensures that double single quotes ('') in FITS card values
are handled consistently and not incorrectly converted to single quotes (').
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_in_card_values():
    """Test that double single quotes in card values are preserved correctly."""
    
    # Test case 1: The main bug reported - strings with '' at the end
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )
    
    # Test case 2: Strings with '' in the middle
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_edge_cases_with_double_quotes():
    """Test edge cases with double quotes to ensure they work properly."""
    
    # Test with just double quotes
    card1 = fits.Card('TEST', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for just double quotes: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with single quote at start and end
    card1 = fits.Card('TEST', "'hello'")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for single quoted string: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with empty string
    card1 = fits.Card('TEST', "")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for empty string: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with trailing whitespace (should be stripped)
    card1 = fits.Card('TEST', "hello   ")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for trailing whitespace: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with leading whitespace (should be stripped)
    card1 = fits.Card('TEST', "   hello")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for leading whitespace: expected {card1.value!r}, got {card2.value!r}"
    )
    
    # Test with both leading and trailing whitespace (should be stripped)
    card1 = fits.Card('TEST', "   hello   ")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for both whitespace: expected {card1.value!r}, got {card2.value!r}"
    )