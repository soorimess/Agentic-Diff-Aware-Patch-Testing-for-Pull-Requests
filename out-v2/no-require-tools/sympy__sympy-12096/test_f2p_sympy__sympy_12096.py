from sympy.utilities.lambdify import implemented_function

def test_evalf_recursive_call():
    """Test that evalf calls _imp_ recursively on arguments."""
    # Create implemented functions as in the bug report
    f = implemented_function('f', lambda x: x ** 2)
    g = implemented_function('g', lambda x: 2 * x)
    
    # Test individual function evaluations work
    assert str(f(2).evalf()) == "4.00000000000000"
    assert str(g(2).evalf()) == "4.00000000000000"
    
    # This is the key test: f(g(2)) should evaluate to a numeric value
    # but before the fix it would return f(g(2)) unevaluated
    result = f(g(2)).evalf()
    
    # The bug: result should NOT be the unevaluated expression f(g(2))
    # After the fix, it should be a numeric result
    assert str(result) != "f(g(2))"