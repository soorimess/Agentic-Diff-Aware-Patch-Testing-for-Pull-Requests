"""
Test for regression of sqrtdenest IndexError issue.

This test ensures that when sqrtdenest encounters expressions
that would previously have caused IndexError due to improper 
condition checking, they are handled gracefully by returning
unchanged expressions.
"""

from sympy import sqrt, I
from sympy.simplify.sqrtdenest import sqrtdenest


def test_sqrtdenest_handles_negative_rational_squares():
    """
    Test expressions where argument squares are rational but not positive.
    
    Before fix: expressions like sqrt(2)*I + 1 would pass the condition
    all((x**2).is_Rational for x in pargs) -> True
    and then could lead to IndexError in split_surds processing.
    
    After fix: same expressions fail the stricter condition  
    all(sq.is_Rational and sq.is_positive for sq in sqargs) -> False
    and are handled gracefully.
    
    This test ensures the behavior change works correctly.
    """
    # Expression with I**2 = -1 which is rational but not positive
    expr = sqrt(2)*I + 1
    
    # Before the fix, this would pass the old condition check
    # and potentially cause IndexError
    # After the fix, it should not raise IndexError and should return unchanged
    try:
        result = sqrtdenest(expr)
        # Should return unchanged instead of crashing
        assert result == expr, f"Expected unchanged: {expr}, got: {result}"
    except IndexError:
        raise AssertionError("Expression with negative rational squares still raises IndexError")


def test_sqrtdenest_no_indexerror_on_reported_case():
    """
    Test the exact case reported in the bug that caused IndexError.
    
    This ensures the fundamental fix is working - that if an expression 
    cannot be denested properly, it should return unchanged instead of
    crashing with IndexError.
    """
    # The exact problematic expression from the bug report
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    try:
        result = sqrtdenest(expr)
        # Should return unchanged instead of raising IndexError
        assert result == expr, f"Expected unchanged: {expr}, got: {result}"
    except IndexError:
        raise AssertionError("Bug still present: IndexError raised on reported case")


def test_sqrtdenest_preserves_normal_functionality():
    """
    Test that normal function works without regression.
    """
    # This should work fine in both versions
    expr = sqrt(8)
    
    try:
        result = sqrtdenest(expr)
        # Just verify it doesn't crash
        assert result is not None
    except IndexError:
        raise AssertionError("Normal functionality broken: IndexError raised")