"""
Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals.

This test ensures that Rational numbers are properly converted to mpmath
expressions when using the mpmath module in lambdify, rather than being
left as Python expressions that lose precision.
"""

from sympy import S, Symbol
from sympy.printing.pycode import MpmathPrinter


def test_mpmath_printer_handles_rational_correctly():
    """Test that MpmathPrinter properly handles Rational numbers with mpmath.mpf."""
    from sympy import Rational
    
    # Create a MpmathPrinter instance
    printer = MpmathPrinter()
    
    # Test with a simple rational that would lose precision
    r = Rational(232, 3)
    
    # This should produce a properly formatted mpmath expression to preserve precision
    result = printer._print(r)
    
    # The fix adds _print_Rational method that should return:
    # '{0}({1})/{0}({2})'.format(self._module_format('mpmath.mpf'), e.p, e.q)
    # Which should produce something like "mpmath.mpf(232)/mpmath.mpf(3)"
    
    # Check that it contains the expected mpmath.mpf format
    assert "mpmath.mpf" in result, f"Rational should be wrapped with mpmath.mpf, got: {result}"
    
    # More specifically, check that it's a fraction format with mpmath.mpf calls
    assert "/" in result, f"Rational should be in fraction form, got: {result}"
    
    # Verify it's the right kind of format - should have mpmath.mpf(232)/mpmath.mpf(3) pattern
    # This ensures it's not just any string containing mpmath.mpf but the specific format
    assert "mpmath.mpf(" in result, f"Should have mpmath.mpf() calls, got: {result}"