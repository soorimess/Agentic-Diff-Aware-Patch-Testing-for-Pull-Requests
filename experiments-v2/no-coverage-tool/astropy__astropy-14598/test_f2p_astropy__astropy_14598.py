"""
Regression test for FITS Card double single-quote handling issue.

This test ensures that double single quotes ('') in FITS card values
are properly preserved when parsing cards, rather than being incorrectly
converted to single quotes (').
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_preserved_in_card_values():
    """Test that double single quotes are preserved in card values."""
    # Test case 1: Double quotes at end of long string
    # The bug occurs at specific lengths where double quotes get converted to single quotes
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical - double quotes should not be converted to single quotes
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_double_single_quotes_in_middle_of_string():
    """Test that double single quotes in middle of string are preserved."""
    # Test case 2: Double quotes in middle of string
    # The bug occurs at specific lengths where double quotes get converted to single quotes
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical - double quotes should not be converted to single quotes
        assert card1.value == card2.value, (
            f"Failed for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_specific_problematic_lengths():
    """Test the specific problematic lengths from the bug report."""
    # These are the exact lengths where the bug manifests
    problematic_lengths = [65, 67, 68, 69]
    
    for n in problematic_lengths:
        value = "x" * n + "''"
        card1 = fits.Card('CONFIG', value)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical - double quotes should not be converted to single quotes
        assert card1.value == card2.value, (
            f"Failed for length {n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_normal_single_quotes_still_work():
    """Test that normal single quotes still work correctly."""
    # Normal single quotes should still work
    card1 = fits.Card('CONFIG', "x'y")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    # Single quotes at beginning and end should be preserved
    card3 = fits.Card('CONFIG', "'test'")
    card4 = fits.Card.fromstring(str(card3))
    assert card3.value == card4.value


def test_empty_string_handling():
    """Test that empty strings are handled correctly."""
    card1 = fits.Card('CONFIG', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value