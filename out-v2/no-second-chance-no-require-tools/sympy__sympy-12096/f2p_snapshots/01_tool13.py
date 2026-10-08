from sympy.utilities.lambdify import implemented_function
from sympy import Float, Function

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
    
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    print(f"Result args: {result.args}")
    
    # Let's also test what g(2) evaluates to by itself
    g2 = g(2)
    print(f"g(2) type: {type(g2)}")
    print(f"g(2): {g2}")
    print(f"g(2).evalf(): {g2.evalf()}")
    
    # The bug is that this should evaluate to a Float, not remain as f(g(2))
    # If it's still f(g(2)), then the fix isn't working
    assert isinstance(result, Float), f"Result should be a Float, not a {type(result)}"
    assert result == Float(16)