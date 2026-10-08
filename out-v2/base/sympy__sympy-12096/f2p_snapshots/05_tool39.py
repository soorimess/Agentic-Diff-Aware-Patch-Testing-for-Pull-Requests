from sympy.utilities.lambdify import implemented_function
from sympy import Float

def test_evalf_recursive_imp():
    """Test that evalf calls _imp_ recursively on arguments of implemented_function.
    
    This test ensures that when evalf is called on a composition of implemented 
    functions, the arguments are recursively evaluated before being passed to _imp_.
    
    The bug: f(g(2)).evalf() would return f(g(2)) unevaluated instead of 16.0
    The fix: f(g(2)).evalf() should evaluate to a Float (16.0)
    """
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test basic evalf works correctly
    result1 = f(2).evalf()
    assert result1 == Float(4)
    
    result2 = g(2).evalf()
    assert result2 == Float(4)
    
    # This is the main bug: f(g(2)).evalf() should evaluate to 16.0 but returns f(g(2))
    # because _eval_evalf doesn't recursively call evalf on arguments
    result3 = f(g(2)).evalf()
    
    # The key assertion: result3 should be a Float (evaluated), not the unevaluated expression
    # This is the core behavior that the pull request fixes
    assert isinstance(result3, Float), f"Expected a Float result, got {type(result3)}: {result3}"
    
    # Verify the numerical value is correct (16.0)
    assert abs(float(result3) - 16.0) < 1e-10