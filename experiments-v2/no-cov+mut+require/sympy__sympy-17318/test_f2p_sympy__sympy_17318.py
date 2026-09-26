"""
Regression test for sqrtdenest IndexError bug.

This test ensures that sqrtdenest handles expressions that would cause 
IndexError by returning them unchanged instead of raising exceptions.
"""

from sympy import sqrt, I, sqrtdenest

def test_sqrtdenest_no_indexerror_on_problematic_input():
    """
    Test that sqrtdenest handles the specific case from the bug report
    without raising IndexError.
    
    The bug: sqrtdenest((3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2) 
    would raise IndexError: tuple index out of range
    
    The fix: it should return the expression unchanged.
    """
    # This is the exact expression from the bug report that caused IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before the fix, this would raise IndexError
    # After the fix, it should return unchanged without error
    result = sqrtdenest(expr)
    
    # Should return the same expression unchanged (the expected behavior)
    assert result == expr