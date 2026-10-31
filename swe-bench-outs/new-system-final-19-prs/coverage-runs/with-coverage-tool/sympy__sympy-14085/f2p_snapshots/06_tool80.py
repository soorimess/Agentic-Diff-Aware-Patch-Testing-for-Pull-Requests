"""
Test for the Greek letter parsing issue in sympify.

This test ensures that the main issue from the bug report is fixed and covers 
the changed functionality in the parser.
"""

from sympy import sympify, Symbol, Rational
from sympy.parsing.sympy_parser import parse_expr, TokenError


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


def test_factorial_notation_works():
    """Test that factorial notation works (new functionality in the change)."""
    # Test the new factorial notation handling from the PR
    # This should parse 5! correctly
    result = parse_expr('5!')
    from sympy import factorial
    assert result == factorial(5)
    
    # Test that invalid factorial expressions still raise TokenError
    try:
        parse_expr('x!!!')
        assert False, "Should have raised TokenError"
    except TokenError:
        assert True  # Expected


def test_repeated_decimals_functionality():
    """Test that repeated decimals parsing works (new functionality in the change)."""
    # Test the new repeated_decimals functionality from the PR
    # This should parse 3.[3] as Rational(10, 3) 
    result = parse_expr('3.[3]')
    assert result == Rational(10, 3)


def test_regular_symbols_still_work():
    """Regression test: regular symbols should continue to work."""
    result = sympify("alpha")
    assert isinstance(result, Symbol)
    assert result.name == 'alpha'
    
    result = sympify("x")
    assert isinstance(result, Symbol)
    assert result.name == 'x'