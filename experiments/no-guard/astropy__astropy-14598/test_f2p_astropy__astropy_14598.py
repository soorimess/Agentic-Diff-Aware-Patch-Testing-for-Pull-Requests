"""
Regression tests for the FITS Card double quote handling bug.

This test verifies that FITS Card values containing double single quotes ('')
are preserved exactly as input, rather than being incorrectly converted to
single single quotes (').
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_preserved_in_card_values():
    """Test that double single quotes in card values are preserved exactly."""
    # Test case 1: double quotes at the end of string
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be exactly equal, not converted
        assert card1.value == card2.value, f"Failed for n={n}: {card1.value} != {card2.value}"
    
    # Test case 2: double quotes in the middle of string
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be exactly equal, not converted
        assert card1.value == card2.value, f"Failed for n={n}: {card1.value} != {card2.value}"


def test_double_single_quotes_at_beginning():
    """Test that double single quotes at the beginning are preserved."""
    card1 = fits.Card('CONFIG', "''" + "some_value")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_double_single_quotes_at_end():
    """Test that double single quotes at the end are preserved."""
    card1 = fits.Card('CONFIG', "some_value" + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_double_single_quotes_in_middle():
    """Test that double single quotes in the middle are preserved."""
    card1 = fits.Card('CONFIG', "start''middle''end")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_multiple_double_quotes():
    """Test that multiple consecutive double quotes are preserved."""
    card1 = fits.Card('CONFIG', "a''b''c''d")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_empty_string_with_double_quotes():
    """Test empty string with double quotes."""
    card1 = fits.Card('CONFIG', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_numeric_values_with_double_quotes():
    """Test numeric values with double quotes should still work correctly."""
    # No double quotes, should work normally
    card1 = fits.Card('NUM', 123)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value