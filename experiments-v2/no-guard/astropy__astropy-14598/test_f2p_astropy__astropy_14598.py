"""
Regression test for FITS Card double quote handling bug.

This test verifies that FITS Card values with double single quotes ('') 
are properly preserved when round-tripping through Card creation and parsing.
"""
import pytest
from astropy.io import fits


def test_double_single_quotes_preserved_in_card_values():
    """Test that double single quotes in card values are preserved."""
    # Test case from the bug report - values that should preserve double quotes
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Double quotes not preserved for n={n}. "
            f"Original: {repr(card1.value)}, Parsed: {repr(card2.value)}"
        )


def test_double_single_quotes_in_middle_of_string():
    """Test that double single quotes in middle of string are preserved."""
    # Test case from the bug report - double quotes in middle of larger string
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Double quotes not preserved for n={n}. "
            f"Original: {repr(card1.value)}, Parsed: {repr(card2.value)}"
        )


def test_edge_cases_with_double_quotes():
    """Test edge cases around the problematic lengths."""
    # Test specific lengths that were mentioned in the bug report
    test_lengths = [65, 67, 68, 69, 55, 56, 57, 58, 59, 60, 61, 62, 65, 67, 68, 69]
    
    for n in test_lengths:
        # Test with double quotes at the end
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Double quotes not preserved for end case n={n}. "
            f"Original: {repr(card1.value)}, Parsed: {repr(card2.value)}"
        )
        
        # Test with double quotes in the middle
        card3 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card4 = fits.Card.fromstring(str(card3))
        assert card3.value == card4.value, (
            f"Double quotes not preserved for middle case n={n}. "
            f"Original: {repr(card3.value)}, Parsed: {repr(card4.value)}"
        )


def test_single_quotes_still_work():
    """Test that single quotes (not double) still work correctly."""
    # Single quotes should be handled properly
    card1 = fits.Card('CONFIG', "x'x")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Single quotes not handled correctly. "
        f"Original: {repr(card1.value)}, Parsed: {repr(card2.value)}"
    )