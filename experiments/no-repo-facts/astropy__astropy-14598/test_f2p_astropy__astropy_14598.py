# Licensed under a 3-clause BSD style license - see PYFITS.rst
"""Regression test for issue with double single-quote handling in FITS Card."""
import pytest
from astropy.io import fits


def test_double_single_quotes_in_card_values():
    """Test that double single quotes ('') are preserved correctly in Card values.
    
    Regression test for astropy/astropy#14598 - Inconsistency in double single-quote ('')
    management in FITS Card where double quotes are sometimes converted to single quotes
    when string length exceeds certain thresholds.
    
    This test specifically targets:
    1. Strings with double quotes at the end, at various lengths
    2. Strings with double quotes in the middle, at various lengths
    """
    # First test set: double quotes at the end of strings of varying lengths
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Value mismatch at length {n}: {repr(card1.value)} != {repr(card2.value)}"
        )
        
        # Also check that the string representation matches
        assert str(card1) == str(card2), (
            f"String representation mismatch at length {n}: {repr(str(card1))} != {repr(str(card2))}"
        )
    
    # Second test set: double quotes in the middle of strings of varying lengths  
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Value mismatch with middle quotes at length {n}: {repr(card1.value)} != {repr(card2.value)}"
        )
        
        # Also check that the string representation matches
        assert str(card1) == str(card2), (
            f"String representation mismatch with middle quotes at length {n}: {repr(str(card1))} != {repr(str(card2))}"
        )


def test_edge_cases_with_single_quotes():
    """Test edge cases specifically around quote handling."""
    # Test strings with single quotes that should NOT be converted
    test_cases = [
        ("test''string", "test''string"),  # Should preserve double quotes
        ("''", "''"),  # Empty string with double quotes
        ("x''y", "x''y"),  # Single quotes in middle
        ("x''", "x''"),  # Double quotes at the end
        ("''x", "''x"),  # Double quotes at the beginning
    ]
    
    for input_val, expected in test_cases:
        card1 = fits.Card('TEST', input_val)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Edge case failed: {repr(input_val)} != {repr(card2.value)}"
        )
        assert str(card1) == str(card2), (
            f"Edge case string repr failed: {repr(str(card1))} != {repr(str(card2))}"
        )