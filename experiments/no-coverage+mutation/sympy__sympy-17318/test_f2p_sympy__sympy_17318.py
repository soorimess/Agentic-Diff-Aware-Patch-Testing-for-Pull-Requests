"""
Regression test for sqrtdenest IndexError bug.

This test ensures that sqrtdenest handles expressions that cannot be denested
gracefully, returning them unchanged rather than raising an IndexError.
"""

from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_indexerror_regression():
    """
    Test that sqrtdenest does not raise IndexError for expressions 
    that cannot be denested.
    
    The bug was that when an expression contains surds whose squares 
    are rationals but cannot be processed properly by split_surds,
    an IndexError was raised in _split_gcd due to empty tuple access.
    
    The specific case was: (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    """
    # This is the specific problematic expression from the bug report 
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before the fix, this would raise IndexError: tuple index out of range
    # After the fix, it should return the expression unchanged
    result = sqrtdenest(expr)
    
    # The result should be the same as the input (unchanged)
    assert result == expr


def test_sqrtdenest_preserves_non_denestable():
    """
    Ensure that expressions that don't denest cleanly are returned unchanged
    rather than raising an exception.
    """
    # Construct expressions that could hit the problematic code paths
    # where original logic would pass but cause IndexError
    expr1 = sqrt(2) + sqrt(3) 
    expr2 = sqrt(5) + sqrt(7) 
    
    # These should not raise IndexError when processed by sqrtdenest
    result1 = sqrtdenest(expr1)
    result2 = sqrtdenest(expr2) 
    
    assert result1 == expr1
    assert result2 == expr2


def test_sqrtdenest_with_rational_square_terms():
    """
    Test specific case where all argument squares are Rational but might have
    structure that would cause issues in split_surds.
    """
    # The key insight from the bug fix is that the condition now requires
    # that squares be both rational AND positive
    
    # Create expression with terms whose squares are positive rationals
    # (relevant for the new condition)
    expr = sqrt(4) + sqrt(9)  # squares: 4 and 9, both positive rationals
    
    result = sqrtdenest(expr)
    assert result == expr