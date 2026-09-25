"""
Regression test for double quote handling in FITS Card
This test captures the inconsistency described in the bug report.
"""
import pytest
from astropy.io import fits


def test_double_single_quote_handling_in_card_values():
    """Test that double single quotes ('') are handled consistently in FITS card values."""
    
    # Test case 1: Basic case from bug report - string with double quotes at specific lengths
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The original bug: double quotes were inconsistently converted to single quotes
        # at certain string lengths  
        assert card1.value == card2.value, (
            f"String length {n}: Original value '{card1.value}' != parsed value '{card2.value}'"
        )


def test_double_single_quote_handling_with_suffix():
    """Test double quote handling when double quotes are in the middle of a string."""
    
    # Test case 2: String with double quotes in between other characters
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # This should test the consistent behavior
        assert card1.value == card2.value, (
            f"String length {n}: Original value '{card1.value}' != parsed value '{card2.value}'"
        )


def test_edge_cases_with_double_quotes():
    """Test several edge cases with double quotes to make sure behavior is consistent."""
    
    # Test various lengths and positions of double quotes 
    test_cases = [
        ("''", "Empty string with double quotes"),
        ("x''", "Single char + double quotes"),
        ("''x", "Double quotes + single char"),
        ("x''x", "Double quotes in middle"),
        ("x" * 64 + "''", "Long string of 64 + double quotes (bug case)"),
        ("x" * 65 + "''", "Long string of 65 + double quotes (bug case)"),
        ("x" * 67 + "''", "Long string of 67 + double quotes (bug case)"),
        ("x" * 68 + "''", "Long string of 68 + double quotes (bug case)"),
        ("x" * 69 + "''", "Long string of 69 + double quotes (bug case)"),
    ]
    
    for value, description in test_cases:
        card1 = fits.Card('TEST', value)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"{description}: Original value '{card1.value}' != parsed value '{card2.value}'"
        )


def test_string_length_boundaries():
    """Test behavior around the critical length boundaries where the bug occurs."""
    
    # These specific lengths are mentioned in the bug report 
    critical_lengths = [65, 67, 68, 69]
    
    for n in critical_lengths:
        # Test exactly the case that breaks
        original_value = "x" * n + "''"  
        card1 = fits.Card('TEST', original_value)
        card2 = fits.Card.fromstring(str(card1))
        
        # Before the fix, this would fail because double quotes get converted to single
        # The key assertion here is that the values should match after round-trip
        assert card1.value == card2.value, (
            f"Critical length {n}: Round-trip failed, expected '{original_value}' "
            f"but got '{card2.value}'"
        )