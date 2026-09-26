"""
Regression test for kernS bug where 'kern' was referenced before assignment.

This test ensures that kernS function doesn't raise UnboundLocalError
when called with expressions that don't contain spaces.
"""

from sympy.core.sympify import kernS


def test_kernS_no_space_raises_no_unboundlocalerror():
    """Test that kernS doesn't raise UnboundLocalError for expressions without spaces."""
    # This is the exact case from the bug report that caused UnboundLocalError
    text = "(2*x)/(x-1)"
    
    # Before the fix, this would raise:
    # UnboundLocalError: local variable 'kern' referenced before assignment
    # After the fix, this should work fine
    expr = kernS(text)
    
    # Verify it returns a valid expression
    assert expr is not None


def test_kernS_with_space_still_works():
    """Test that kernS still works correctly with expressions that contain spaces."""
    # This should work normally 
    text = "2 * x"
    expr = kernS(text)
    
    # Verify it returns a valid expression
    assert expr is not None


def test_kernS_complex_expression_no_spaces():
    """Test kernS with a more complex expression without spaces."""
    text = "2*x + 3*y - z"
    expr = kernS(text)
    
    # Verify it returns a valid expression
    assert expr is not None