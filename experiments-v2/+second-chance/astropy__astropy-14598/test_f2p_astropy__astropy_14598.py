"""
Regression test for FITS Card double single-quote handling issue.

This test ensures that double single quotes ('') in FITS Card values are
properly handled and converted to single quotes ('), as reported in the bug.
"""

from astropy.io import fits


def test_fits_card_double_quotes_at_end():
    """Test that double single quotes at end of strings are properly handled."""
    
    # Test the exact case from the bug report
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value!r} != {card2.value!r}"
        )


def test_fits_card_double_quotes_in_middle():
    """Test that double single quotes in middle of strings are properly handled."""
    
    # Test the exact case from the bug report
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value!r} != {card2.value!r}"
        )