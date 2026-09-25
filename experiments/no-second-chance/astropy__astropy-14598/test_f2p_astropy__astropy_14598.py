"""
Regression tests for FITS Card double single-quote handling bug.

This tests the inconsistency where double single quotes ('') in FITS Card values
were sometimes transformed into single single quotes ('), depending on string length.
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_at_end():
    """Test that double single quotes at end of card values are preserved."""
    # These cases show the bug where double quotes become single quotes
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical
        assert card1.value == card2.value, (
            f"Length {n}: expected '{card1.value}', got '{card2.value}'"
        )


def test_double_single_quotes_in_middle():
    """Test that double single quotes in middle of card values are preserved."""
    # These cases show the bug where double quotes become single quotes
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical
        assert card1.value == card2.value, (
            f"Length {n}: expected '{card1.value}', got '{card2.value}'"
        )


def test_double_single_quotes_with_comment():
    """Test that double single quotes work with comments."""
    # Test case with double quotes and comment
    card1 = fits.Card('TEST', "value with '' quotes", "some comment")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    assert card1.comment == card2.comment


def test_simple_double_quotes():
    """Test simple cases with double quotes."""
    card1 = fits.Card('TEST', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value

    card1 = fits.Card('TEST', "x''y")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_spaces_around_double_quotes():
    """Test that spaces around double quotes are handled properly."""
    # Testing that trailing spaces are removed but quotes are preserved
    card1 = fits.Card('TEST', "value with '' quotes   ")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    # Testing with leading whitespace too
    card1 = fits.Card('TEST', "   value with '' quotes")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value