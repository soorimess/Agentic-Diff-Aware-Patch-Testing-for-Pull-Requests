"""
Test for sqrtdenest IndexError bug fix.

This test specifically targets the code path that was changed to prevent IndexError.
"""

from sympy import sqrt, I, sqrtdenest, Add
from sympy.simplify.sqrtdenest import _sqrt_match


def test_sqrtdenest_condition_behavior():
    """
    Test the specific condition change that prevents IndexError.
    
    The fix changes:
    OLD: all((x**2).is_Rational for x in pargs)
    NEW: all(sq.is_Rational and sq.is_positive for sq in sqargs)
    
    This test ensures that expressions with negative rational squares
    don't go through the problematic code path.
    """
    # Create an expression that would pass the NEW condition (all positive rational squares)
    # This should go through the normal path
    expr1 = sqrt(4) + sqrt(9)  # Both squares are 4 and 9 (positive rationals)
    
    # While this gets simplified, let's make sure we test the behavior
    result1 = sqrtdenest(expr1)
    # Should not raise IndexError
    
    # Test with a case that would have been problematic before
    # This is more about ensuring the fix works for the intended cases
    expr2 = sqrt(-1) + 1  # sqrt(-1)^2 = -1 (negative rational)
    result2 = sqrtdenest(expr2)
    assert result2 == expr2  # Should return unchanged


def test_sqrtdenest_main_bug_case():
    """
    Test the main bug case from the issue report.
    """
    # The expression that was causing IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should not raise IndexError
    result = sqrtdenest(expr)
    assert result == expr


def test_sqrtdenest_unprocessable_cases():
    """
    Test various cases that should not raise IndexError.
    """
    # Cases that would have caused issues before the fix
    test_cases = [
        sqrt(-1),                    # Simple negative sqrt
        sqrt(-4) + sqrt(-9),         # Multiple negative sqrt terms  
        1 + sqrt(-1) + I,            # Mixed with complex
    ]
    
    for expr in test_cases:
        # These should not raise IndexError
        result = sqrtdenest(expr)
        assert result == expr