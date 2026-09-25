"""
Regression test for FITS Card double quote handling issue.

This test ensures that double single quotes ('') in FITS card values are
properly preserved through round-trip serialization, not converted to single
quotes (''), which is the expected and correct behavior.
"""
from astropy.io import fits


def test_fits_card_double_quotes_preserved_on_roundtrip():
    """
    Test that double single quotes in card values are preserved during round-trip.
    
    Before the fix: When parsing cards containing double quotes, the behavior was 
    to incorrectly remove one of the quotes, so "''" became "'". This test 
    ensures this bug doesn't return.
    """
    # Test case 1: strings with double quotes at the end (from original bug report)
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        
        # The values should be identical - no transformation should occur during parsing
        assert card1.value == card2.value, f"Failed at n={n}: {card1.value} != {card2.value}"
        
        # Also check that string representations are identical
        assert str(card1) == str(card2), f"String representations differ at n={n}"


def test_fits_card_double_quotes_in_middle_preserved():
    """
    Test that double single quotes embedded in larger strings are preserved.
    
    This covers the second part of the original bug report where double quotes
    are embedded in the middle of strings.
    """
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        
        # The values should be identical - no transformation should occur 
        assert card1.value == card2.value, f"Failed at n={n}: {card1.value} != {card2.value}"
        
        # Also check that string representations are identical
        assert str(card1) == str(card2), f"String representations differ at n={n}"


def test_exact_problematic_cases():
    """
    Test the exact problematic cases identified in the bug report.
    """
    # These are the exact problematic cases from the bug report
    test_cases = [
        ("x" * 65 + "''", "x" * 65 + "''"),  # Should stay double quotes
        ("x" * 67 + "''", "x" * 67 + "''"),  
        ("x" * 68 + "''", "x" * 68 + "''"),
        ("x" * 69 + "''", "x" * 69 + "''"),
    ]
    
    for original_value, expected_value in test_cases:
        card1 = fits.Card('TEST', original_value)
        card2 = fits.Card.fromstring(str(card1))
        
        # Values should be equal - the fix applies the missing quote conversion
        assert card1.value == card2.value, f"Values don't match for {original_value} (expected: {expected_value})"
        assert card1.value == expected_value, f"Expected {expected_value}, got {card1.value}"