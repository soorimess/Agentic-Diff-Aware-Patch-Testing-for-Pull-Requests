"""
Regression test for lambdify with modules='mpmath' not wrapping rationals.

This test ensures that when lambdifying expressions with mpmath modules,
rational numbers are properly wrapped with mpmath.mpf() calls to maintain
precision, instead of being represented as regular Python division.
"""

from sympy import symbols, Rational, lambdify, Eq, RisingFactorial, S, nsolve, Float
from sympy.printing.pycode import MpmathPrinter


def test_mpmath_printer_handles_rationals_with_mpmath_calls():
    """
    Test that MpmathPrinter properly formats Rational objects using mpmath.mpf calls.
    
    Before fix: Rational(1, 3) would be printed as "1/3"
    After fix: Rational(1, 3) should be printed as "mpmath.mpf(1)/mpmath.mpf(3)"
    """
    printer = MpmathPrinter()
    
    # Test with a simple rational that should trigger mpmath wrapping
    expr = Rational(1, 3)
    result = printer.doprint(expr)
    
    # This assertion should fail before the fix (returns "1/3")
    # and pass after the fix (returns "mpmath.mpf(1)/mpmath.mpf(3)")
    assert "mpmath.mpf(" in result, f"Expected mpmath.mpf usage, got: {result}"


def test_lambdify_with_mpmath_preserves_rational_precision():
    """
    Test that the mpmath module properly handles rational numbers in lambdified 
    expressions to avoid precision loss that would occur with raw Python division.
    """
    # This test actually compares encoding behavior for a basic case
    from sympy.printing.pycode import MpmathPrinter
    
    # Test that mpmath even handles some simple rational properly by checking 
    # that it doesn't return the raw literal without mpmath
    printer = MpmathPrinter()
    
    # In the specific context that caused the reported issue
    # A Rational like S(1)/3 should be formatted with mpmath for high precision
    rational_expr = S(1)/3
    formatted = printer.doprint(rational_expr)
    
    # The fix ensures it goes through mpmath.mpf construction
    assert "mpmath.mpf(" in formatted, f"Should use mpmath.mpf calls to preserve precision, got: {formatted}"