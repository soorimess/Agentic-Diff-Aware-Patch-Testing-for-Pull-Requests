from sympy.utilities.lambdify import implemented_function
from sympy import Float

def test_evalf_recursive_call():
    """Test that evalf calls _imp_ recursively on arguments"""
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test individual functions work
    assert f(2).evalf() == Float(4)
    assert g(2).evalf() == Float(4)
    
    # Test nested function - this is where the bug manifests
    # Before fix: f(g(2)).evalf() would return f(g(2)) (not evaluated)
    # After fix: f(g(2)).evalf() should return 16.0 (since g(2) = 4, f(4) = 16)
    result = f(g(2)).evalf()
    
    # The bug is that this should evaluate to a Float, not remain as f(g(2))
    # If it's still f(g(2)), then the fix isn't working
    assert isinstance(result, Float), f"Result should be a Float, not a {type(result)}"
    assert result == Float(16)
    
    # Additional test to ensure precision is handled correctly
    # Test with higher precision
    result_prec = f(g(2)).evalf(50)
    assert isinstance(result_prec, Float), f"Result with precision should be a Float, not a {type(result_prec)}"
    # Should be close to 16.0 with high precision
    assert abs(result_prec - Float(16)) < 1e-49