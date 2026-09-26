"""Test for the Rational handling in mpmath lambdify"""

from sympy import Eq, rf, S, Float, nsolve, lambdify, Symbol
from sympy.printing.pycode import MpmathPrinter
import inspect


def test_lambdify_rational_mpmath_precision():
    """Test that lambdify with mpmath modules properly handles Rational numbers"""
    
    # Create an equation with a rational number
    x = Symbol('x')
    eqn = Eq(rf(18, x), 77 + S(1)/3)
    
    # Create the lambdified function with mpmath module
    f = lambdify(x, eqn.lhs - eqn.rhs, 'mpmath')
    
    # Check that the generated function source contains properly wrapped rationals
    # Before the fix, this would show "232/3" instead of "mpf(232)/mpf(3)"
    source = inspect.getsource(f)
    
    # The fix should wrap rational numbers in mpf() calls (not mpmath.mpf)
    # This assertion checks that the rational is properly handled
    # Before fix: source contains "232/3"  
    # After fix: source should contain "mpf(232)/mpf(3)"
    assert 'mpf(' in source, f"Expected mpf in source, got: {source}"
    assert '232/3' not in source, f"Should not contain literal 232/3, got: {source}"
    
    # More specifically, test the precision issue mentioned in the bug report
    # The original problem was that 232/3 was not evaluated at full precision
    x0 = nsolve(eqn, Float('1.5', 64), prec=64)
    
    # This should give the correct precision now
    result = rf(18, x0).evalf(64)
    expected = 77 + S(1)/3
    expected_eval = expected.evalf(64)
    
    # The result should match the expected value with high precision
    # The bug was that without proper rational handling, precision was lost
    assert abs(result - expected_eval) < 1e-60


def test_mpmath_printer_rational_formatting():
    """Test that MpmathPrinter properly formats Rational numbers for mpmath"""
    
    # Test the MpmathPrinter directly
    printer = MpmathPrinter()
    
    # Test with a simple rational
    rational = S(232)/3
    result = printer._print(rational)
    
    # After the fix, this should return something like "mpf(232)/mpf(3)"
    assert 'mpf(' in result, f"Expected mpf in result, got: {result}"
    assert '/' in result, f"Expected division in result, got: {result}"
    
    # The result should be in the format: mpf(p)/mpf(q)
    assert result.count('mpf(') == 2, f"Expected 2 mpf calls, got: {result}"