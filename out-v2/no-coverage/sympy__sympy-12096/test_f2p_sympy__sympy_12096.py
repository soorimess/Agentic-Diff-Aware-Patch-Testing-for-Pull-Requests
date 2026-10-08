"""
Regression test for evalf not calling _imp_ recursively.

This test ensures that when a function with implemented_function is evaluated
with evalf(), the arguments are also evaluated with evalf() before being
passed to _imp_.
"""

from sympy.utilities.lambdify import implemented_function
from sympy import Float

def test_evalf_recursive_imp():
    """Test that evalf calls _imp_ recursively on arguments."""
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test individual functions work
    assert f(2).evalf() == Float(4)
    assert g(2).evalf() == Float(4)
    
    # This is the key test: f(g(2)) should evaluate to 16.0, not remain as f(g(2))
    # Because g(2) = 4, and f(4) = 16
    result = f(g(2)).evalf()
    
    # Before the fix, this would return f(g(2)) unevaluated
    # After the fix, this should return 16.0
    assert result == Float(16)

def test_nested_evalf():
    """Test nested function calls with evalf."""
    # Create more complex nested functions
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: x + 1)
    
    # Test nested evaluation: g(2) = 3, f(3) = 9
    result = f(g(2)).evalf()
    
    # Should evaluate to (2+1)^2 = 9
    assert result == Float(9)

def test_evalf_returns_numeric_result():
    """Test that evalf returns a numeric Float, not a symbolic expression."""
    # Create functions that would fail if arguments aren't evaluated
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test that we get a numeric result, not a symbolic one
    result = f(g(2)).evalf()
    
    # The result should be a Float, not a function object
    assert isinstance(result, Float)
    assert str(result) == '16.0000000000000'
    
    # Also test that the result is actually numeric and not symbolic
    # This ensures that the recursive evalf call happened
    assert result.is_number