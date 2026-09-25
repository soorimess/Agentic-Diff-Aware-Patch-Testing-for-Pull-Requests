# Licensed under a 3-clause BSD style license - see LICENSE.rst

"""
Test for FITS Card double quote handling bug.

This tests the regression where double single quotes ('') in FITS Card values
were incorrectly converted to single quotes (') when round-tripping through
Card.fromstring().
"""

import pytest
from astropy.io import fits


def test_double_single_quotes_at_end_not_converted():
    """
    Test that double single quotes at the end of a FITS card value 
    are preserved and not converted to single quotes.
    """
    # Test various lengths where the bug occurs
    for n in range(65, 70):
        original_value = "x" * n + "''"
        card1 = fits.Card('CONFIG', original_value)
        card2 = fits.Card.fromstring(str(card1))
        
        # The bug was that '' became ' 
        assert card1.value == card2.value, (
            f"Double quotes not preserved for length {n}: "
            f"original={repr(card1.value)}, "
            f"after round-trip={repr(card2.value)}"
        )


def test_double_single_quotes_in_middle_not_converted():
    """
    Test that double single quotes in the middle of a FITS card value 
    are preserved and not converted to single quotes.
    """
    # Test various positions where the bug occurs
    for n in range(55, 65):
        original_value = "x" * n + "''" + "x" * 10
        card1 = fits.Card('CONFIG', original_value)
        card2 = fits.Card.fromstring(str(card1))
        
        # The bug was that '' became ' 
        assert card1.value == card2.value, (
            f"Double quotes not preserved for middle position {n}: "
            f"original={repr(card1.value)}, "
            f"after round-trip={repr(card2.value)}"
        )


def test_double_single_quotes_at_end_with_spaces():
    """
    Test that double single quotes at the end are preserved even when 
    there are trailing spaces.
    """
    original_value = "test string''   "
    card1 = fits.Card('CONFIG', original_value)
    card2 = fits.Card.fromstring(str(card1))
    
    # The bug was that the trailing spaces would be stripped but '' would be converted to '
    assert card1.value == card2.value, (
        f"Double quotes not preserved with trailing spaces: "
        f"original={repr(card1.value)}, "
        f"after round-trip={repr(card2.value)}"
    )


def test_empty_string_double_quotes():
    """
    Test that empty string with double quotes is handled correctly.
    """
    original_value = "''"
    card1 = fits.Card('CONFIG', original_value)
    card2 = fits.Card.fromstring(str(card1))
    
    assert card1.value == card2.value, (
        f"Empty double quotes not preserved: "
        f"original={repr(card1.value)}, "
        f"after round-trip={repr(card2.value)}"
    )


def test_multiple_double_quotes():
    """
    Test that multiple instances of double quotes are preserved.
    """
    original_value = "start''middle''end"
    card1 = fits.Card('CONFIG', original_value)
    card2 = fits.Card.fromstring(str(card1))
    
    assert card1.value == card2.value, (
        f"Multiple double quotes not preserved: "
        f"original={repr(card1.value)}, "
        f"after round-trip={repr(card2.value)}"
    )