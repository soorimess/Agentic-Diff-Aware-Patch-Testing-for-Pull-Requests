"""
Regression test for sqrtdenest IndexError bug fix.

This test ensures that expressions which would cause IndexError in the 
old code are handled properly by returning unchanged.
"""
from sympy import sqrtdenest, sqrt, I

def test_sqrtdenest_indexerror_regression():
    """
    Test that expressions previously causing IndexError are now handled gracefully.
    
    Before the fix, expressions with complex surds or non-positive rational squares
    would raise IndexError during the sqrtdenest process instead of returning 
    the unchanged expression as expected.
    """
    # Test case 1: Expression with sqrt(-1) that has a negative rational square  
    expr1 = sqrt(-1) + sqrt(2)  # sqrt(-1)^2 = -1 is rational but not positive
    result1 = sqrtdenest(expr1)
    # Should not raise IndexError and should return unchanged
    assert result1 == expr1
    
    # Test case 2: Expression with sqrt(0) that has zero square
    expr2 = sqrt(0) + sqrt(5)   # sqrt(0)^2 = 0 is rational but not positive  
    result2 = sqrtdenest(expr2)
    # Should not raise IndexError and should return unchanged
    assert result2 == expr2

def test_sqrtdenest_original_bug_case():
    """
    Test the original reported bug case to make sure it doesn't raise IndexError.
    """
    # This was the exact example from the bug report that caused IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    result = sqrtdenest(expr)
    # Should handle gracefully and return unchanged (not raise IndexError)
    assert result == expr