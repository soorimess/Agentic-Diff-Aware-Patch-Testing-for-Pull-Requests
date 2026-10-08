"""
Regression test for issue where evalf does not call _imp_ recursively
on arguments of implemented functions.

This test ensures that when we have nested implemented functions like
f(g(2)), the arguments are properly evaluated to floating point before
being passed to the implementation function.
"""

from sympy.utilities.lambdify import implemented_function
from sympy import Function, Float

def test_evalf_recursive_imp():
    """Test that evalf calls _imp_ recursively on arguments"""
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test individual functions work correctly
    assert f(2).evalf() == Float(4)
    assert g(2).evalf() == Float(4)
    
    # This is the key test - f(g(2)) should evaluate to a numeric value
    # Before the fix, this would return the symbolic expression f(g(2))
    # After the fix, this should return a numeric Float
    nested = f(g(2))
    evalf_result = nested.evalf()
    
    # The bug is that evalf_result remains symbolic instead of evaluating to a number
    # This assertion should pass after the fix is applied
    assert isinstance(evalf_result, Float), "evalf should return a Float, not symbolic expression"
    
    # The expected value is f(g(2)) = f(4) = 16.0
    # g(2) = 2*2 = 4, f(4) = 4^2 = 16
    assert evalf_result == Float(16)