"""
Regression test for FITS Card double single-quote handling issue.

This test ensures that double single quotes ('') in FITS card values
are properly preserved when creating cards and parsing them back,
rather than being converted to single quotes (').
"""

from astropy.io import fits


def test_double_single_quotes_preserved():
    """Test that double single quotes are preserved in FITS card values."""
    # Test case from the bug report - these should all be True but were failing
    for n in range(60, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''")
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: original='{card1.value}', parsed='{card2.value}'"
        )


def test_double_single_quotes_in_middle():
    """Test that double single quotes in the middle of values are preserved."""
    # Test case from the bug report with quotes in the middle
    for n in range(50, 70):
        card1 = fits.Card('CONFIG', "x" * n + "''" + "x" * 10)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for n={n}: original='{card1.value}', parsed='{card2.value}'"
        )


def test_edge_cases():
    """Test edge cases around the problematic lengths."""
    # Test some specific problematic lengths mentioned in the bug report
    test_cases = [
        "''",  # Just double quotes
        "x''",  # Double quotes at end
        "''x",  # Double quotes at start
        "x''x",  # Double quotes in middle
        "x" * 65 + "''",  # Length that was failing in bug report
        "x" * 55 + "''" + "x" * 10,  # Middle case that was failing
    ]
    
    for i, value in enumerate(test_cases):
        card1 = fits.Card('TEST', value)
        card2 = fits.Card.fromstring(str(card1))
        assert card1.value == card2.value, (
            f"Failed for test case {i}: original='{card1.value}', parsed='{card2.value}'"
        )