"""Test for lambdify with modules='mpmath' not wrapping rationals properly."""

from sympy import Eq, rf, S, Float, nsolve, lambdify, Symbol
from sympy.abc import x
from sympy.printing.pycode import PythonCodePrinter
import inspect


def test_lambdify_mpmath_rational_handling():
    """Test that lambdify with modules='mpmath' properly handles rationals."""
    # Create a simple expression with a rational number
    expr = S(1)/3
    
    # Lambdify with mpmath module
    f = lambdify(x, expr, 'mpmath')
    
    # Check that the generated function properly formats rationals for mpmath
    source = inspect.getsource(f)
    
    # Before the fix, this would generate "1/3" 
    # After the fix, it should generate "mpf(1)/mpf(3)" (or similar mpmath format)
    # The core issue: rationals should be wrapped with mpmath functions to maintain precision
    assert "mpf(1)/mpf(3)" in source or "mpmath.mpf(1)/mpmath.mpf(3)" in source, f"Expected mpmath formatting not found in source: {source}"


def test_lambdify_mpmath_original_bug_case():
    """Test the exact case from the original bug report."""
    # This recreates the exact scenario from the bug report
    eqn = Eq(rf(18, x), 77 + S(1)/3)
    
    # Lambdify with mpmath module - this is where the bug manifests
    f = lambdify(x, eqn.lhs - eqn.rhs, 'mpmath')
    
    # Check that the generated function properly handles the rational part
    source = inspect.getsource(f)
    
    # The bug was that 232/3 was not wrapped in mpmath formatting
    # After fix, it should be properly formatted for mpmath precision
    assert "mpf" in source or "mpmath.mpf" in source, f"Expected mpmath formatting not found in source: {source}"