"""
Regression test for the bug where lambdify(modules='mpmath') doesn't wrap rationals.

This test verifies the behavior that was broken before the fix:
- Rational numbers in mpmath lambdified expressions should be converted to use mpmath.mpf()
- Before the fix: they were left as literal Python expressions like "232/3" 
- After the fix: they should be converted to "mpmath.mpf(232)/mpmath.mpf(3)"
"""

from sympy import lambdify, Eq, rf, S
from sympy.printing.pycode import MpmathPrinter
import inspect


def test_mpmath_lambdify_rational_not_wrapped():
    """
    Test that demonstrates the bug: Rational numbers are NOT wrapped in mpmath.mpf()
    in mpmath lambdified expressions.
    
    Before the fix: '232/3' in source and 'mpmath.mpf(' not in source
    After the fix: both should be true (both literals and mpmath wrappers)
    """
    # Create equation like in the bug report
    eqn = Eq(rf(18, S('x')), 77 + S(1)/3)
    
    # Create lambdified function with mpmath module
    f = lambdify(S('x'), eqn.lhs - eqn.rhs, 'mpmath')
    
    # Get the generated source
    source = inspect.getsource(f)
    
    # This demonstrates that the bug exists
    assert '232/3' in source, "Rational should appear as literal in source (demonstrates the bug)"
    assert 'mpmath.mpf(' not in source, "mpmath.mpf() should NOT be used yet (this is the bug)"


def test_mpmath_printer_missing_rational_handler():
    """
    Test that MpmathPrinter doesn't handle Rational numbers specially (before fix).
    """
    from sympy import Rational
    
    r = Rational(232, 3)
    printer = MpmathPrinter()
    
    # The MpmathPrinter should fall back to default behavior
    result = printer._print(r)
    
    # Should return the simple string representation without mpmath wrapping
    assert result == '232/3', "MpmathPrinter returns literal rational (demonstrates bug)"


def test_mpmath_lambdify_should_wrap_rationals():
    """
    Test for the expected behavior after fix is applied:
    Rational numbers in mpmath lambdified expressions SHOULD be wrapped.
    
    This assertion will FAIL on the current (broken) version but PASS after fix.
    """
    # Create equation like in the bug report 
    eqn = Eq(rf(18, S('x')), 77 + S(1)/3)
    f = lambdify(S('x'), eqn.lhs - eqn.rhs, 'mpmath')
    source = inspect.getsource(f)
    
    # After fix, we should see mpmath.mpf used for rationals
    # This test will pass when the fix is applied
    assert 'mpmath.mpf(' in source, "After fix, mpmath.mpf() should be used for rationals"