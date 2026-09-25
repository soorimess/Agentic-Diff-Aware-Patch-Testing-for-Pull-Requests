"""
Regression test for kernS unboundLocalError issue.

This test verifies that kernS handles strings properly without raising 
UnboundLocalError when 'kern' variable would be referenced before assignment.
"""

from sympy.core.sympify import kernS


def test_kernS_no_spaces_returns_valid_expression():
    """Test kernS with expression that contains no spaces but has parentheses.
    
    This tests the specific case from the bug report that caused:
    UnboundLocalError: local variable 'kern' referenced before assignment
    """
    # This should not raise UnboundLocalError
    text = "(2*x)/(x-1)"
    result = kernS(text)
    
    # The result should be a valid sympy expression
    assert result is not None


def test_kernS_with_spaces_works():
    """Test kernS with expression that contains spaces (should work in both versions).
    
    This test makes sure the 'kern' assignment path also works correctly.
    """
    # Test expression with spaces - should trigger the if ' ' in s path
    text = "(2*x) / (x-1)"
    result = kernS(text)
    
    # The result should be a valid sympy expression
    assert result is not None


def test_kernS_simple_expression():
    """Test kernS with simple expressions without spaces."""
    text = "x+1"
    result = kernS(text)
    
    # The result should be a valid sympy expression
    assert result is not None


def test_kernS_complex_no_spaces():
    """Test more complex expression without spaces."""
    text = "x**2 + 2*x + 1"
    result = kernS(text)
    
    # The result should be a valid sympy expression 
    assert result is not None