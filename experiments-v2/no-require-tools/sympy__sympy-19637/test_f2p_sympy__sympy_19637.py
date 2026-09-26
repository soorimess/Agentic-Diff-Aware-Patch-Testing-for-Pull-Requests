"""
Regression test for kernS UnboundLocalError bug.

The bug was that kernS would raise UnboundLocalError: local variable 'kern' 
referenced before assignment when the input string did not contain spaces.
"""

from sympy.core.sympify import kernS

def test_kernS_no_spaces():
    """Test kernS with a string that has no spaces - should not raise UnboundLocalError."""
    # This should not raise UnboundLocalError: local variable 'kern' referenced before assignment
    text = "(2*x)/(x-1)"
    expr = kernS(text)
    # Just verify it returns a valid expression
    assert expr is not None

def test_kernS_with_spaces():
    """Test kernS with a string that has spaces - should not raise UnboundLocalError."""
    # This should not raise UnboundLocalError: local variable 'kern' referenced before assignment
    text = "(2 * x) / (x - 1)"
    expr = kernS(text)
    # Just verify it returns a valid expression
    assert expr is not None

def test_kernS_returns_valid_expression():
    """Test that kernS returns valid expressions for various inputs."""
    # Test cases that should not crash
    test_cases = [
        "(2*x)/(x-1)",      # No spaces - the original bug case
        "(2 * x) / (x - 1)", # Has spaces but they get stripped
        "x + y",            # Has spaces, no parentheses
        "x*y",              # No spaces, no parentheses
    ]
    
    for text in test_cases:
        expr = kernS(text)
        # Just verify it returns a valid expression (not None)
        assert expr is not None, f"kernS failed on input: {text}"