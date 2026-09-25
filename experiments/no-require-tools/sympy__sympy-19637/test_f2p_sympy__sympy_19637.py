"""
Regression test for kernS bug: 'kern' referenced before assignment

This test ensures that kernS doesn't raise UnboundLocalError when 
there are no spaces in the input string, which is the exact case
that caused the bug reported in the issue.
"""
from sympy.core.sympify import kernS


def test_kernS_no_spaces_unboundlocalerror():
    """Test kernS with string that does not contain spaces - reproduces the original bug."""
    # This exact case from the bug report should not raise:
    # UnboundLocalError: local variable 'kern' referenced before assignment
    expr = kernS("(2*x)/(x-1)")
    # The expression should be successfully created
    assert expr is not None


def test_kernS_with_spaces_normal_functionality():
    """Test that normal functionality with spaces still works."""
    # This tests normal path through the kernS function
    expr = kernS("2 * x")
    assert expr is not None


def test_kernS_complex_expression_no_spaces():
    """Test complex expression with no spaces that would trigger the bug."""
    expr = kernS("-(x+1)")
    assert expr is not None