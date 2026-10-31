"""
Test for the Greek letter parsing issue in sympify.

This test ensures that the main issue from the bug report is fixed.
"""

from sympy import sympify, Symbol


def test_greek_letter_sympify_returns_symbol():
    """Test that sympify returns a Symbol for Greek letters."""
    # The exact behavior: sympify("α") should return a Symbol object
    # This is the specific behavior change that was introduced
    result = sympify("α")
    
    # The assertion that tests what the code does: it returns a Symbol
    # not just any object, but specifically a Symbol instance
    assert isinstance(result, Symbol)
    
    # Additional assertion: it's the same type as regular symbol creation
    regular_result = sympify("alpha")
    assert type(result) is type(regular_result)


def test_regular_symbols_still_work():
    """Regression test: regular symbols should continue to work."""
    result = sympify("alpha")
    assert isinstance(result, Symbol)
    assert result.name == 'alpha'
    
    result = sympify("x")
    assert isinstance(result, Symbol)
    assert result.name == 'x'