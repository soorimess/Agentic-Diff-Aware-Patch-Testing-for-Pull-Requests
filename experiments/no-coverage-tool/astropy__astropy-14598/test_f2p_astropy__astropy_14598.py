"""
Regression test for FITS Card double quote handling bug.

This test verifies the behavior of FITS Card objects when they contain 
double single quotes ('') in their values, particularly to ensure that
double quotes are preserved/untouched during card serialization/deserialization.
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_preserved_in_fits_card():
    """
    Test that double single quotes ('') in FITS Card values are preserved and not 
    incorrectly converted to single quotes (') during serialization/deserialization.
    
    This is a regression test for: "Inconsistency in double single-quote ('') management 
    in FITS Card" - before the fix, values containing '' would sometimes be converted to '.
    """
    
    # The core bug case - these should preserve double quotes
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # This should be True after the fix is applied
        assert card1.value == card2.value, (
            f"Card value mismatch for length {n}: "
            f"expected '{card1.value}', got '{card2.value}'"
        )


def test_double_single_quotes_in_middle_of_value():
    """
    Test that double single quotes are preserved even when they appear in the middle 
    of a larger value string.
    """
    
    # Test case with '' in the middle
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # This should also be True after the fix is applied
        assert card1.value == card2.value, (
            f"Card value mismatch for middle case, length {n}: "
            f"expected '{card1.value}', got '{card2.value}'"
        )


def test_edge_cases_double_quotes():
    """
    Test specifically the edge cases noted in the bug report
    """
    # These specific lengths were mentioned in the bug report as having issues
    problematic_lengths = [65, 67, 68, 69]  # From first example in bug report
    
    for n in problematic_lengths:
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # They should match - but currently fail due to bug
        assert card1.value == card2.value, (
            f"Critical edge case failed for {n}: "
            f"expected '{card1.value}', got '{card2.value}'"
        )


def test_single_quotes_at_boundaries():
    """
    Test various cases with single quotes at boundaries to ensure comprehensive 
    handling of quote patterns.
    """
    test_cases = [
        "''",                    # Just double quotes
        "''test",                # Double quotes at start  
        "test''",                # Double quotes at end
        "test''middle",          # Double quotes in middle
        "x" * 60 + "''" + "x" * 5, # Double quotes in middle with more content
    ]
    
    for val in test_cases:
        card1 = fits.Card('TEST', val)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Boundary case failed for value '{val}': "
            f"expected '{card1.value}', got '{card2.value}'"
        )


def test_no_regression_for_single_quotes():
    """
    Ensure that single quotes that are not double quotes are handled normally.
    """
    # Single quotes shouldn't be changed at all
    test_cases = [
        "'",                     # Single quote
        "test'other",            # Single quote in middle
        "'test",                 # Single quote at start  
        "test'",                 # Single quote at end
    ]
    
    for val in test_cases:
        card1 = fits.Card('TEST', val)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Single quote case failed for value '{val}': "
            f"expected '{card1.value}', got '{card2.value}'"
        )