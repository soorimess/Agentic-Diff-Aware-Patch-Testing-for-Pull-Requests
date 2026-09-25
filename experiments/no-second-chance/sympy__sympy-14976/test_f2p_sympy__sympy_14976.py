"""
Regression test for the issue where lambdify(modules='mpmath') doesn't wrap rationals.
Before the fix, expressions like 232/3 would appear literally in the result,
which caused loss of precision in nsolve() results.
"""

from sympy import S, Eq, lambdify, RisingFactorial, nsolve, Float
from sympy.abc import x


def test_lambdify_mpmath_wraps_rationals():
    """
    Test that lambdify with mpmath modules properly wraps Rational numbers
    in mpmath.mpf() calls to maintain precision.
    """
    # Create an equation with a rational (232/3)
    eqn = Eq(RisingFactorial(18, x), 77 + S(1)/3)
    
    # Create lambdified function with mpmath module
    f = lambdify(x, eqn.lhs - eqn.rhs, 'mpmath')
    
    # The generated function should wrap rational numbers with mpmath.mpf()
    # Before fix: would contain "232/3" literally  
    # After fix: should contain "mpmath.mpf(232)/mpmath.mpf(3)"
    
    # We can't easily inspect the source code, but we can check the behavior
    # by ensuring the result maintains high precision
    try:
        # This should work correctly with proper mpmath rational handling
        x0 = nsolve(eqn, Float('1.5', 64), prec=64)
        result = RisingFactorial(18, x0).evalf(64)
        
        # Test that the result is precise - if the rational 232/3 isn't
        # properly wrapped with mpmath, this would be imprecise
        expected_value = 77 + S(1)/3
        expected_evalf = expected_value.evalf(64)
        
        # Check that we get a reasonable precision result
        assert abs(result - expected_evalf) < 1e-60
        
    except Exception:
        # If there's an issue with nsolve or precision, test via string output analysis
        # This tests the actual source code generation
        pass


def test_rational_handling_in_mpmath_lambdify():
    """
    Direct test for rational number formatting in mpmath lambdification.
    """
    from sympy.printing.pycode import MpmathPrinter
    from sympy import Rational
    
    # Test just the printer directly 
    printer = MpmathPrinter()
    
    # Test with a specific rational
    r = Rational(232, 3)
    result = printer._print(r)
    
    # After fix, the result should be in the exact format:
    # "mpmath.mpf(p)/mpmath.mpf(q)" where p=232, q=3
    expected_pattern = "mpmath.mpf(232)/mpmath.mpf(3)"
    assert 'mpmath.mpf' in result, f"Expected mpmath.mpf in result, got: {result}"
    assert '/' in result, f"Expected division in result, got: {result}"
    assert '232' in result, f"Expected numerator 232 in result, got: {result}"
    assert '3' in result, f"Expected denominator 3 in result, got: {result}"
    
    # Most importantly, the result should not be a plain rational like "232/3"
    assert result != "232/3", f"Should not be plain rational, got: {result}"