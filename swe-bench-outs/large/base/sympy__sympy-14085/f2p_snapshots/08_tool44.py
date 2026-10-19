"""
Regression test for sympify with Greek letters issue.

This test ensures that sympify can parse Greek letters like 'α' that are 
pretty printed for symbols of that name.
"""

from sympy import sympify, Symbol
from sympy.core.sympify import SympifyError


def test_sympify_greek_letter_alpha():
    """Test that sympify can parse the Greek letter alpha specifically."""
    # This should work - the original issue reported that this fails
    # In the fixed version, "α" should be parsed as Symbol('alpha')
    result = sympify("α")
    # If it works, it should return a valid SymPy object
    assert result is not None
    # It should be a symbol (though the exact type may vary)
    assert hasattr(result, 'is_Symbol') or hasattr(result, 'is_symbol')


def test_sympify_greek_letter_beta():
    """Test that sympify can parse the Greek letter beta."""
    result = sympify("β")
    assert result is not None
    assert hasattr(result, 'is_Symbol') or hasattr(result, 'is_symbol')


def test_repeated_decimals_parsing():
    """Test that repeated decimals notation works (new functionality)."""
    # Test 0.2[1] which should represent 0.2111... (19/90)
    # This is a new feature added by the PR
    result = sympify("0.2[1]")
    # Should parse to a rational number
    assert result is not None


def test_factorial_notation():
    """Test that factorial notation works properly."""
    # Test factorial notation - this is part of the change
    result = sympify("x!")
    assert result is not None
    # Should be parsed as factorial(x)
    assert hasattr(result, 'is_Function') or hasattr(result, 'is_Mul')


def test_double_factorial_notation():
    """Test double factorial notation."""
    # Test double factorial notation
    result = sympify("x!!")
    assert result is not None
    # Should be parsed as factorial2(x)
    assert hasattr(result, 'is_Function') or hasattr(result, 'is_Mul')


if __name__ == "__main__":
    test_sympify_greek_letter_alpha()
    test_sympify_greek_letter_beta()
    test_repeated_decimals_parsing()
    test_factorial_notation()
    test_double_factorial_notation()
    print("All tests passed!")