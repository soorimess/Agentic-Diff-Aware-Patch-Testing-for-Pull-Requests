"""
Regression test for FITS Card double quote handling bug.

This test ensures that FITS Card values containing double single quotes ('')
are handled correctly when round-tripping through string conversion.
"""

from astropy.io import fits


def test_fits_card_double_quotes_roundtrip():
    """Test that double single quotes in card values are preserved."""
    # Test case from the bug report - values around the threshold where the bug occurs
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Value mismatch for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_fits_card_double_quotes_in_middle():
    """Test that double single quotes in the middle of card values are preserved."""
    # Test case from the bug report - values with '' in the middle
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Value mismatch for n={n}: expected {card1.value!r}, got {card2.value!r}"
        )


def test_fits_card_simple_double_quotes():
    """Test simple case with just double quotes."""
    card1 = fits.Card('TEST', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Simple double quotes failed: expected {card1.value!r}, got {card2.value!r}"
    )


def test_fits_card_mixed_quotes():
    """Test mixed single and double quotes."""
    card1 = fits.Card('TEST', "a''b''c")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Mixed quotes failed: expected {card1.value!r}, got {card2.value!r}"
    )