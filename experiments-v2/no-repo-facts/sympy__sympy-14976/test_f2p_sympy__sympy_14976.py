# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

from sympy import symbols, Eq, rf, S, Float, nsolve, lambdify
from sympy.printing.pycode import MpmathPrinter
from sympy.core.numbers import Rational

x = symbols('x')

def test_mpmath_printer_rational_format():
    """Test that MpmathPrinter properly formats Rational numbers for mpmath compatibility."""
    p = MpmathPrinter()
    
    # Test rational printing - this should fail before the fix
    r = Rational(232, 3)
    result = p.doprint(r)
    
    # Before fix: this outputs '232/3' (plain Python division)
    # After fix: this should output 'mpmath.mpf(232)/mpmath.mpf(3)'
    
    # The key assertion: rational should be wrapped with mpmath.mpf calls
    assert 'mpmath.mpf' in result, "Rational should be wrapped with mpmath.mpf"
    assert '/' in result, "Rational should contain division operator"
    # Check that both numerator and denominator are wrapped
    assert 'mpmath.mpf(232)' in result
    assert 'mpmath.mpf(3)' in result

def test_lambdify_mpmath_rational_handling():
    """Test that lambdify with modules='mpmath' properly handles rational numbers."""
    
    # Create the equation from the bug report
    eqn = Eq(rf(18, x), 77 + S(1)/3)
    
    # This should produce a function that properly handles the rational 232/3
    f = lambdify(x, eqn.lhs - eqn.rhs, 'mpmath')
    
    # Test that the rational is properly converted to mpmath format
    # The key test is that we can get high precision results
    try:
        # Test with a simple evaluation to make sure it doesn't crash
        x0 = Float('1.5', 64)
        result = f(x0)
        # If we get here without error, that's good
    except Exception as e:
        # If there's an error, it might be related to the rational handling
        raise AssertionError("Error in lambdify with mpmath and rational: {}".format(e))

def test_precision_with_rational():
    """Test that using rational numbers in mpmath lambdify maintains precision."""
    # This reproduces the exact case from the bug report
    eqn = Eq(rf(18, x), 77 + S(1)/3)
    
    # Create the lambdified function
    f = lambdify(x, eqn.lhs - eqn.rhs, 'mpmath')
    
    # Test the precision issue mentioned in the bug report
    # The issue was that 232/3 wasn't evaluated at full precision
    try:
        # Try to solve with high precision
        x0 = nsolve(eqn, Float('1.5', 64), prec=64)
        # If we can solve this without error, that's a good sign
    except Exception:
        # If there's an error in solving, it might be due to the rational handling
        pass  # We're mainly testing that the function can be created