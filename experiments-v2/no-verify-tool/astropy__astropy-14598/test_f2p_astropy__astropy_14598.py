"""
Regression test for FITS Card double quote handling issue.

This test ensures that double single quotes ('') in FITS card values
are properly preserved when cards are created and parsed back from strings.
"""

from astropy.io import fits


def test_double_single_quotes_preserved():
    """Test that double single quotes are preserved in card values."""
    # Test case 1: Double quotes at the end of a long string
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value} != {card2.value}"
        )

    # Test case 2: Double quotes in the middle of a string
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: {card1.value} != {card2.value}"
        )


def test_edge_cases():
    """Test edge cases with double quotes."""
    # Test with exactly 65 characters (the boundary mentioned in bug report)
    card1 = fits.Card('TEST', "x" * 65 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for 65 chars: {card1.value} != {card2.value}"
    )
    
    # Test with exactly 67 characters 
    card1 = fits.Card('TEST', "x" * 67 + "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for 67 chars: {card1.value} != {card2.value}"
    )
    
    # Test with double quotes at beginning
    card1 = fits.Card('TEST', "''" + "x" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for leading quotes: {card1.value} != {card2.value}"
    )
    
    # Test with double quotes in middle
    card1 = fits.Card('TEST', "x" * 10 + "''" + "x" * 10)
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, (
        f"Failed for middle quotes: {card1.value} != {card2.value}"
    )


if __name__ == "__main__":
    test_double_single_quotes_preserved()
    test_edge_cases()
    print("All tests passed!")