"""
Regression test for sqrtdenest IndexError bug.

This test specifically addresses the issue where sqrtdenest would raise 
IndexError: tuple index out of range when processing certain expressions.

The bug was in the _split_gcd function in radsimp.py, which would be called
with empty arguments when split_surds was called on expressions that resulted
in empty surds lists.

This test ensures that:
1. No IndexError is raised when processing the problematic expression
2. The expression is returned unchanged (the expected behavior)
"""

from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_no_indexerror_on_problematic_input():
    """
    Test that sqrtdenest handles the specific problematic input without IndexError.
    
    Before the fix, this would raise:
    IndexError: tuple index out of range in _split_gcd function
    
    After the fix, it should return the expression unchanged.
    """
    # Expression that caused IndexError in the bug report
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should NOT raise IndexError
    # It should return the original expression unchanged
    result = sqrtdenest(expr)
    
    # Verify the fix: expression is returned unchanged
    assert result == expr


def test_sqrtdenest_preserves_mathematical_correctness():
    """
    Test that the behavior change is mathematically correct.
    
    When sqrtdenest cannot denest an expression, it should return the 
    original expression rather than raising an exception.
    """
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Should not raise any exception
    result = sqrtdenest(expr)
    
    # Should be mathematically equivalent to original
    assert result.equals(expr)