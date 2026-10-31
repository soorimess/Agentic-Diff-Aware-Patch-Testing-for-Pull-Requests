"""
Test for the Greek letter parsing issue in sympify.

The issue is that sympify(u"α") does not work, but it should work like sympify("alpha").
This test ensures that the main issue from the bug report is fixed.
"""

from sympy import sympify, Symbol


def test_greek_letter_sympify_returns_symbol():
    """Test that sympify returns a Symbol for Greek letters."""
    # The exact behavior change: sympify("α") should return a Symbol object
    # rather than raising NameError or SympifyError
    result = sympify("α")
    
    # Assert on the exact return value - it should be a Symbol instance
    assert type(result) == Symbol
    
    # Test that it's the same type as what we'd get from "alpha"
    result_alpha = sympify("alpha")
    assert type(result) == type(result_alpha)


def test_regular_symbols_still_work():
    """Regression test: regular symbols should continue to work."""
    result = sympify("alpha")
    assert isinstance(result, Symbol)
    assert result.name == 'alpha'
    
    result = sympify("x")
    assert isinstance(result, Symbol)
    assert result.name == 'x'