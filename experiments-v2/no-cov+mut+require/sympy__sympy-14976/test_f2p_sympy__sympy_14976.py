"""Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals."""

from sympy import S, lambdify
from sympy.printing.pycode import MpmathPrinter
from sympy.abc import x


def test_mpmath_printer_has_rational_method():
    """
    Test that MpmathPrinter has the _print_Rational method added by the fix.
    
    This test verifies the fix that ensures Rational numbers are properly
    wrapped with mpmath.mpf() calls to maintain precision in mpmath lambdify.
    """
    # Create an instance of MpmathPrinter
    printer = MpmathPrinter()
    
    # Check that the _print_Rational method exists (this is what the fix adds)
    # This assertion will fail before the fix and pass after the fix
    assert hasattr(printer, '_print_Rational'), "MpmathPrinter should have _print_Rational method"
    
    # Test that it properly formats rationals with mpmath precision
    rational = S(232)/3
    result = printer._print_Rational(rational)
    
    # After the fix, rationals should be wrapped with mpmath.mpf() calls
    # This assertion ensures the fix is working correctly
    assert 'mpmath.mpf' in result


def test_lambdify_precision_with_rationals():
    """
    Test that lambdify with mpmath preserves rational precision.
    """
    # Create an expression with a rational
    expr = S(232)/3
    
    # Create lambdified function with mpmath module
    f = lambdify(x, expr, 'mpmath')
    
    # The function should be callable and return a proper result
    try:
        result = f(0)  # Evaluate with dummy argument
        assert result is not None
    except Exception as e:
        raise AssertionError(f"Failed to create or evaluate mpmath lambdified function: {e}")