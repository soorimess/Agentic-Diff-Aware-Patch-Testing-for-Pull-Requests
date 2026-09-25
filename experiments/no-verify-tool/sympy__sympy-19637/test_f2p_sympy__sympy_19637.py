"""
Regression test for kernS bug: 'kern' referenced before assignment.

The bug was that kernS raised UnboundLocalError when processing 
strings that have parentheses but no spaces.
"""
from sympy.core.sympify import kernS


def test_kernS_no_spaces_but_parentheses():
    """Test that kernS doesn't raise UnboundLocalError for inputs with parentheses but no spaces."""
    # This case specifically caused: UnboundLocalError: local variable 'kern' referenced before assignment
    text = "(2*x)/(x-1)"
    
    # Before the fix: this would raise UnboundLocalError
    # After the fix: this should work normally and return a symbolic expression 
    try:
        expr = kernS(text)
        # If we get here without exception, it means the fix worked
        assert expr is not None
    except UnboundLocalError:
        # This means the bug is still present
        raise AssertionError("UnboundLocalError still occurs with kernS")


def test_kernS_function_works():
    """Test that kernS works correctly with various inputs."""
    # Test that it doesn't crash with basic inputs  
    test_cases = [
        "(2*x)/(x-1)",
        "((x+1)/(x-1))",
        "2*(x+y)",
        "-(x+1)"
    ]
    
    for text in test_cases:
        try:
            expr = kernS(text)
            assert expr is not None
        except UnboundLocalError:
            raise AssertionError(f"UnboundLocalError with input: {text}")