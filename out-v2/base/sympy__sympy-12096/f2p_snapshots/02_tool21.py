from sympy.utilities.lambdify import implemented_function
from sympy import Float

def test_evalf_recursive_imp():
    """Test that evalf calls _imp_ recursively on arguments of implemented_function."""
    # Create implemented functions as described in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test basic evalf works
    result1 = f(2).evalf()
    assert result1 == Float(4)
    
    result2 = g(2).evalf()
    assert result2 == Float(4)
    
    # This is the bug: f(g(2)).evalf() should evaluate to 16.0 but returns f(g(2))
    # because _eval_evalf doesn't recursively call evalf on arguments
    result3 = f(g(2)).evalf()
    
    # Before the fix, this would return f(g(2)) unevaluated
    # After the fix, this should return a Float (16.0)
    # The key test: result3 should be a Float, not the unevaluated expression
    assert isinstance(result3, Float), f"Expected a Float result, got {type(result3)}: {result3}"
    
    # Also verify the numerical value is correct (16.0)
    # We can't directly compare Floats due to precision, so check it's reasonably close
    assert abs(float(result3) - 16.0) < 1e-10