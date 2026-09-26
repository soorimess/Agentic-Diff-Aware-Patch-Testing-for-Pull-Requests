"""
Test for the sqrtdenest IndexError bug fix.

This test ensures that sqrtdenest does not raise an IndexError
when processing expressions that cannot be denested.
"""

from sympy import sqrt, I, sqrtdenest

def test_sqrtdenest_indexerror():
    """Test that sqrtdenest doesn't raise IndexError on problematic input."""
    # This is the exact expression from the bug report that caused IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before the fix, this would raise IndexError: tuple index out of range
    # After the fix, it should return the expression unchanged
    result = sqrtdenest(expr)
    
    # The result should be the same as the input (expression unchanged)
    assert result == expr

def test_sqrtdenest_complex_with_negative_squares():
    """Test that expressions with complex terms don't raise IndexError."""
    # This expression would have caused IndexError in the old code
    # because when computing squares of terms, some would be negative rationals
    expr = sqrt(2 - I) + sqrt(1 + I)
    
    # This should not raise IndexError and should return unchanged
    result = sqrtdenest(expr)
    assert result == expr