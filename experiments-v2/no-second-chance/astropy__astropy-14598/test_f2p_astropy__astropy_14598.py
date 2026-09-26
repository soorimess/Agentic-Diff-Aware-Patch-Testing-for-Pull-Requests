"""
Regression test for FITS Card double single-quote handling issue.

This test ensures that double single quotes ('') in FITS card values are properly
handled and converted to single quotes ('), as they should be according to FITS
standards.
"""

from astropy.io import fits


def test_fits_card_double_quotes_roundtrip():
    """Test that double single quotes in card values are properly converted during round-trip."""
    # Test case from the bug report - this should not fail
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        # The values should be equal after round-trip
        assert card1.value == card2.value, (
            f"Card values don't match for n={n}: "
            f"original='{card1.value}', parsed='{card2.value}'"
        )


def test_fits_card_double_quotes_in_middle_roundtrip():
    """Test that double single quotes in the middle of card values are properly converted during round-trip."""
    # Test case from the bug report - this should not fail
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        # The values should be equal after round-trip
        assert card1.value == card2.value, (
            f"Card values don't match for n={n}: "
            f"original='{card1.value}', parsed='{card2.value}'"
        )


def test_fits_card_double_quotes_boundary_cases():
    """Test boundary cases where the issue occurs."""
    # Test the specific boundary cases from the bug report
    card1 = fits.Card('TEST', "x" * 65 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    card1 = fits.Card('TEST', "x" * 67 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value


def test_fits_card_simple_cases():
    """Test simple cases that should work correctly."""
    # Simple case with no quotes
    card1 = fits.Card('TEST', "simple_value")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    # Case with single quotes (should remain as-is)
    card1 = fits.Card('TEST', "'single'")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value
    
    # Case with double quotes at end
    card1 = fits.Card('TEST', "value''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value