"""
Regression test for sqrtdenest IndexError bug fix.

This test ensures that the fix properly handles expressions with 
non-positive rational squares to prevent IndexError.
"""

from sympy import sqrt, I, sqrtdenest, S

def test_sqrtdenest_prevents_indexerror_on_complex_case():
    """
    Test that the specific complex expression from bug report doesn't crash.
    
    Before fix: IndexError when trying to process (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    After fix: Returns the expression unchanged
    """
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Should not raise IndexError
    result = sqrtdenest(expr)
    assert result == expr

def test_sqrtdenest_handles_negative_rational_square():
    """
    Test that expressions with negative rational squares are handled gracefully.
    
    The fix adds the check that squares must be positive rationals.
    This prevents problematic expressions from reaching the _split_gcd function.
    """
    # sqrt(-1) = I, square = -1 (rational but not positive)
    expr = sqrt(-1)  # This is I
    
    # Should return unchanged without raising exception
    result = sqrtdenest(expr)
    assert result == expr

def test_sqrtdenest_no_exception_for_problematic_expressions():
    """
    Core behavioral test: expressions that would cause IndexError should not crash.
    
    This test verifies the main fix behavior - that non-denestable expressions
    are returned unchanged instead of raising IndexError.
    """
    # Test cases that would have caused the IndexError in the old code
    test_cases = [
        (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2,  # From bug report
        sqrt(-1),  # I, square is -1
    ]
    
    for expr in test_cases:
        # These should all work without raising IndexError
        result = sqrtdenest(expr)
        # They should return unchanged (the fix behavior)
        assert result == expr, f"Failed for expression: {expr}"