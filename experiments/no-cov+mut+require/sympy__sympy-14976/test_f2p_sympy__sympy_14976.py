"""Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals."""

from sympy import S, Rational
from sympy.printing.pycode import MpmathPrinter


def test_mpmath_printer_handles_rational_with_mpf():
    """Test that MpmathPrinter properly wraps Rational numbers with mpmath.mpf() 
    for high precision handling."""
    
    # MpmathPrinter should wrap rationals with mpmath.mpf() for scientific precision
    printer = MpmathPrinter()
    rational = Rational(232, 3)
    
    # This should use mpmath.mpf() for precision 
    result = printer._print(rational)
    
    # Before fix: result = "232/3" 
    # After fix: result should be "mpmath.mpf(232)/mpmath.mpf(3)"
    # Our test verifies that the result correctly has mpmath precision handling
    assert 'mpmath.mpf' in result, \
        f"Rational should be wrapped with mpmath.mpf() for precision, got: {result}"