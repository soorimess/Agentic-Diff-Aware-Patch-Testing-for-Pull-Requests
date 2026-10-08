from sympy.utilities.lambdify import implemented_function
from sympy.utilities.pytest import raises

def test_evalf_recursive_call():
    """Test that evalf calls _imp_ recursively on arguments"""
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test that individual functions work
    assert g(2).evalf() == 4.0
    
    # Test that nested function evaluation works
    # Before the fix, f(g(2)).evalf() would return f(g(2)) instead of 16.0
    result = f(g(2)).evalf()
    
    # The result should be 16.0 (since g(2) = 4, and f(4) = 16)
    # If the bug is present, result would be the unevaluated expression f(g(2))
    assert result == 16.0