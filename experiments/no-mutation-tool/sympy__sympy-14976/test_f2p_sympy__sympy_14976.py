"""
Regression test for rational printing with mpmath lambdify

The bug was that when using lambdify with modules='mpmath', rational numbers
like 232/3 were not being converted to mpmath format, leading to reduced precision.

This test ensures that MpmathPrinter._print_Rational exists and produces correct format.
"""

from sympy import S
from sympy.printing.pycode import MpmathPrinter


def test_rational_printing():
    """Test that MpmathPrinter handles Rational numbers correctly."""
    # Create a rational number
    r = S(232)/3
    
    # Use MpmathPrinter
    printer = MpmathPrinter()
    
    # Try to call the _print_Rational method
    # This should work if the fix is applied
    result = printer._print_Rational(r)
    
    # Expected result after the fix
    expected = "mpmath.mpf(232)/mpmath.mpf(3)"
    
    assert result == expected, f"Expected '{expected}', got '{result}'"