"""
Test for the bug where evalf does not call _imp_ recursively.

This test verifies that when a function with an implemented function is
evaluated with evalf(), the arguments are properly evaluated to floating
point precision before being passed to the implementation function.
"""

from sympy.utilities.lambdify import implemented_function
from sympy import Float

def test_evalf_recursive_call():
    """Test that evalf calls _imp_ recursively on arguments."""
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # These should work fine
    result1 = f(2).evalf()
    assert result1 == Float(4)
    
    result2 = g(2).evalf()
    assert result2 == Float(4)
    
    # This is the problematic case - f(g(2)) should evaluate to 16.0
    # but currently returns f(g(2)) unevaluated
    result3 = f(g(2)).evalf()
    
    # The bug is that f(g(2)) is not being evaluated to a Float
    # It should return 16.0, not the unevaluated expression f(g(2))
    # The fix should make this evaluate to a Float
    assert isinstance(result3, Float), f"Result should be a Float, got {type(result3)}"
    
    # The correct result should be 16.0 (since g(2) = 4, f(4) = 16)
    expected = Float(16)
    assert result3 == expected, f"Expected {expected}, got {result3}"