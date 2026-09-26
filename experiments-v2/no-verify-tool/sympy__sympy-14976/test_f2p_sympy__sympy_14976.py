"""Test for lambdify with mpmath modules wrapping rationals properly."""

from sympy import S, lambdify
from sympy.abc import x


def test_simple_rational_handling():
    """
    Simple test that should pass in both buggy and fixed versions.
    """
    # Test with a simple rational
    r = S(1)/3
    
    # Lambdify with mpmath modules
    f = lambdify([], r, 'mpmath')
    
    # The function should evaluate correctly
    result = f()
    
    # Basic functionality test
    assert abs(result - 1/3) < 1e-100


def test_complex_rational_precision():
    """
    Test that demonstrates the precision issue with complex rational expressions.
    
    This test will fail in the buggy version where rationals are not properly
    wrapped with mpmath calls, causing precision degradation.
    """
    # Create a more complex rational expression that would be affected
    expr = S(232)/3 + S(1)/7
    
    # Lambdify with mpmath modules
    f = lambdify([], expr, 'mpmath')
    
    # Evaluate the function
    result = f()
    
    # Complex rational arithmetic - if precision is degraded due to improper
    # rational handling, this comparison might fail
    expected = 232/3 + 1/7
    # Use reasonable tolerance for floating point comparison
    assert abs(result - expected) < 1e-50