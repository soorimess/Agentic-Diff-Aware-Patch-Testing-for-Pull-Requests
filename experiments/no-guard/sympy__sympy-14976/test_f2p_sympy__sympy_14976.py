"""Test for the bug where lambdify(modules='mpmath') doesn't wrap rationals."""

from sympy import S, lambdify
import inspect


def test_mpmath_rational_handling():
    """Test that mpmath module handles rational constants properly."""
    # The bug report shows that 77 + S(1)/3 incorrectly becomes 232/3 
    # in the lambdified output, without proper mpmath.mpf() wrapping
    
    expr = S(232)/3  # This is what 77 + S(1)/3 evaluates to
    
    # When lambdified with mpmath, this should be wrapped properly  
    f = lambdify(S('x'), expr, 'mpmath')
    source = inspect.getsource(f)
    
    # The core issue: Bug causes literal 232/3 to appear
    # Fix should make mpmath.mpf(232)/mpmath.mpf(3) appear instead
    # This test represents what should work after the change
    # Currently fails because the fix is not in place
    
    # This test expresses what we expect to work after the fix
    # and will be the indication that our fix behavior is working
    assert 'mpmath.mpf(' in source