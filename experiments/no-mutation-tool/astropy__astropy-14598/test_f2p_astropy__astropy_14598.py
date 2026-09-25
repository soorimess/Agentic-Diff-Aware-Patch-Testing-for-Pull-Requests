"""Regression test for FITS Card double quote handling issue."""

from astropy.io import fits


def test_card_double_quotes_basic():
    """Test basic double quote handling in FITS cards."""
    # Test the exact case from the bug report
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, f"Failed at n={n}: expected {card1.value}, got {card2.value}"


def test_card_double_quotes_in_middle():
    """Test double quotes in the middle of a string."""
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x"*10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, f"Failed at n={n}: expected {card1.value}, got {card2.value}"


def test_card_simple_double_quotes():
    """Test simple case with only double quotes."""
    card1 = fits.Card('CONFIG', "''")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, f"Failed: expected {card1.value}, got {card2.value}"


def test_card_single_quotes():
    """Test that single quotes are handled correctly (no change needed)."""
    card1 = fits.Card('CONFIG', "'test'")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, f"Failed: expected {card1.value}, got {card2.value}"


def test_card_mixed_quotes():
    """Test mixed use of single and double quotes."""
    card1 = fits.Card('CONFIG', "start''middle''end")
    card2 = fits.Card.fromstring(str(card1))
    assert card1.value == card2.value, f"Failed: expected {card1.value}, got {card2.value}"


def test_card_edge_cases():
    """Test edge cases around the reported problematic lengths."""
    # These specific problematic cases from the bug report
    problematic_cases = [
        "x" * 65 + "''",
        "x" * 67 + "''", 
        "x" * 68 + "''",
        "x" * 69 + "''", 
        "x" * 55 + "''" + "x" * 10,
        "x" * 56 + "''" + "x" * 10,
        "x" * 57 + "''" + "x" * 10,
        "x" * 58 + "''" + "x" * 10
    ]
    
    for i, value in enumerate(problematic_cases):
        card1 = fits.Card('CONFIG', value)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, f"Failed case {i}: expected {card1.value}, got {card2.value}"