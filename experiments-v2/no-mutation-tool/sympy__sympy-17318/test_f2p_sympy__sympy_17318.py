"""
Test for the sqrtdenest IndexError fix.

This test ensures that sqrtdenest does not raise an IndexError when
processing expressions that cannot be denested, but should return
the unchanged expression instead.
"""

from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_indexerror():
    """
    Test that sqrtdenest does not raise IndexError for expressions
    that cannot be denested.
    
    This is a regression test for the IndexError that occurred when
    processing expressions like (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    """
    # This expression should not raise an IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before the fix, this would raise IndexError: tuple index out of range
    # After the fix, it should return the expression unchanged
    result = sqrtdenest(expr)
    
    # The result should be the same as the input (unchanged)
    assert result == expr


def test_sqrtdenest_complex_no_sqrt():
    """
    Test that sqrtdenest handles complex expressions with no sqrt terms properly.
    """
    # Expression with complex numbers but no sqrt terms that would cause IndexError
    expr = 3 + 4*I
    
    # This should not raise IndexError
    result = sqrtdenest(expr)
    
    # The result should be the same as the input (unchanged)
    assert result == expr


def test_sqrtdenest_nested_sqrt_issue():
    """
    Test that sqrtdenest handles nested sqrt expressions that cannot be denested.
    """
    # This is a more complex case that could trigger the same IndexError
    expr = sqrt(2 + I*sqrt(3))
    
    # This should not raise IndexError
    result = sqrtdenest(expr)
    
    # The result should be the same as the input (unchanged)
    assert result == expr