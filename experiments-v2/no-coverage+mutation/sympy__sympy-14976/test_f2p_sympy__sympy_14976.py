"""Test for rational number handling in lambdify with mpmath module."""

from sympy import S
from sympy.printing.pycode import MpmathPrinter


def test_mpmath_printer_rational_conversion():
    """Test that MpmathPrinter properly converts Rational numbers to mpmath format.
    
    This test ensures that the fix for the issue where Rational numbers like 232/3
    were not being converted to full precision mpmath format is in place.
    
    Before the fix: Rational numbers are printed as plain Python division (e.g., '232/3')
    After the fix: Rational numbers are printed as mpmath.mpf() calls (e.g., 'mpmath.mpf(232)/mpmath.mpf(3)')
    """
    # Test the MpmathPrinter directly with a Rational number
    printer = MpmathPrinter()
    rational = S(232)/3
    
    # This should produce mpmath.mpf(232)/mpmath.mpf(3) after the fix
    result = printer.doprint(rational)
    
    # The fix ensures that Rational numbers are converted to mpmath format
    # for proper precision handling in mpmath-based lambdify functions
    assert 'mpmath.mpf' in result, f"Expected mpmath.mpf in result, got: {result}"