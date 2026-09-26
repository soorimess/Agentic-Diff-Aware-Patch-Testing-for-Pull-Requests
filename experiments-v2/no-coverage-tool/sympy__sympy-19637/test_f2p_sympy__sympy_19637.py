"""
Regression test for kernS bug where 'kern' is referenced before assignment.

The bug occurs when kernS is called with a string that does not contain spaces
but has parentheses, causing an UnboundLocalError when trying to reference
the 'kern' variable which was never defined.
"""

from sympy.core.sympify import kernS


def test_kernS_no_spaces_but_parentheses():
    """Test that kernS handles strings with parentheses but no spaces correctly.
    
    This specifically tests the case that caused:
    UnboundLocalError: local variable 'kern' referenced before assignment
    """
    # This exact case from the bug report should not raise an exception
    text = "(2*x)/(x-1)"
    expr = kernS(text)
    # Should return a valid sympy expression without error
    assert expr is not None


def test_kernS_no_spaces_no_parentheses():
    """Test that kernS handles strings with no spaces and no parentheses."""
    text = "x+y"
    expr = kernS(text)
    # Should return a valid sympy expression without error
    assert expr is not None


def test_kernS_with_spaces():
    """Test that kernS still works correctly when there are spaces in the string."""
    text = "(2 * x) / (x - 1)"
    expr = kernS(text)
    # Should return a valid sympy expression without error
    assert expr is not None