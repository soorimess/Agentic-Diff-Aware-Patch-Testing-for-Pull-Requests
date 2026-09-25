"""
Regression test for FITS Card double quote handling bug.

This test catches the inconsistency in double single-quote ('') management in
FITS Card where null strings were sometimes transformed into single single
quotes ('), depending on string length and position.
"""

import pytest
from astropy.io import fits


def test_fits_card_double_quotes_preserved():
    """Test that double quotes in FITS card values are preserved correctly."""
    # Test case from the bug report: strings ending with ''
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical - this caught the bug
        assert card1.value == card2.value, (
            f"Failed for n={n}: original value '{card1.value}' "
            f"!= parsed value '{card2.value}'"
        )


def test_fits_card_double_quotes_in_middle():
    """Test that double quotes in the middle of FITS card values are preserved correctly."""
    # Test case from the bug report: strings with '' in the middle
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical - this caught the bug
        assert card1.value == card2.value, (
            f"Failed for n={n}: original value '{card1.value}' "
            f"!= parsed value '{card2.value}'"
        )


def test_fits_card_edge_cases():
    """Test edge cases around the problematic lengths."""
    # Test cases around the boundaries mentioned in the bug report
    test_cases = [
        ("x" * 65 + "''", "x" * 65 + "''"),  # This should stay as double quotes  
        ("x" * 67 + "''", "x" * 67 + "''"),  # This should stay as double quotes
        ("x" * 68 + "''", "x" * 68 + "''"),  # This should stay as double quotes
        ("x" * 69 + "''", "x" * 69 + "''"),  # This should stay as double quotes
        ("x" * 55 + "''" + "x" * 10, "x" * 55 + "''" + "x" * 10),  # This should stay as double quotes
        ("x" * 56 + "''" + "x" * 10, "x" * 56 + "''" + "x" * 10),  # This should stay as double quotes
    ]
    
    for i, (input_value, expected_value) in enumerate(test_cases):
        card1 = fits.Card('TEST', input_value)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be identical
        assert card1.value == card2.value, (
            f"Failed for test case {i}: input '{input_value}' "
            f"-> original '{card1.value}' != parsed '{card2.value}'"
        )


if __name__ == "__main__":
    test_fits_card_double_quotes_preserved()
    test_fits_card_double_quotes_in_middle()
    test_fits_card_edge_cases()
    print("All tests passed!")