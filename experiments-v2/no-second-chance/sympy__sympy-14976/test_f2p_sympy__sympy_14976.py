"""
Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals.

This test ensures that rational numbers are properly converted to mpmath
precision format when using lambdify with mpmath module.
"""

from sympy import lambdify, Eq, rf, S, Float, Symbol
from sympy.printing.pycode import MpmathPrinter
import inspect


def test_mpmath_printer_has_rational_method():
    """Test that MpmathPrinter has a _print_Rational method."""
    
    # Create a MpmathPrinter instance
    printer = MpmathPrinter()
    
    # Check that _print_Rational method exists
    assert hasattr(printer, '_print_Rational'), "MpmathPrinter should have _print_Rational method"


def test_mpmath_printer_rational_formatting():
    """Test that MpmathPrinter properly formats Rational numbers."""
    
    from sympy import Rational
    
    # Create a MpmathPrinter instance
    printer = MpmathPrinter()
    
    # Test with a simple rational
    r = Rational(2, 3)
    
    # This should return a string that wraps the rational in mpmath.mpf calls
    result = printer._print_Rational(r)
    
    # The result should be in the form 'mpmath.mpf(p)/mpmath.mpf(q)'
    expected = 'mpmath.mpf(2)/mpmath.mpf(3)'
    assert result == expected, f"Expected {expected}, got {result}"


def test_mpmath_printer_rational_formatting_simple():
    """Test that MpmathPrinter properly formats a simple rational number."""
    
    from sympy import Rational
    
    # Create a MpmathPrinter instance
    printer = MpmathPrinter()
    
    # Test with a simple rational
    r = Rational(5, 2)
    
    # This should return a string that wraps the rational in mpmath.mpf calls
    result = printer._print_Rational(r)
    
    # The result should be in the form 'mpmath.mpf(p)/mpmath.mpf(q)'
    expected = 'mpmath.mpf(5)/mpmath.mpf(2)'
    assert result == expected, f"Expected {expected}, got {result}"