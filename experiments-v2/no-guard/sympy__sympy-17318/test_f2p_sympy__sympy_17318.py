"""
Test for the sqrtdenest IndexError bug fix.

This test ensures that sqrtdenest does not raise an IndexError when
trying to denest expressions that cannot be denested, but instead
returns them unchanged.
"""

from sympy import sqrt, I, sqrtdenest
from sympy.simplify.sqrtdenest import _sqrt_match

def test_sqrtdenest_indexerror_regression():
    """
    Test that _sqrt_match does not raise IndexError for expressions
    that would cause IndexError before the fix.
    
    The bug was that _sqrt_match(1 + I) would call split_surds with 
    an empty surds list, causing IndexError in _split_gcd.
    """
    # This expression would trigger the IndexError in the old code
    # because 1**2 = 1 (rational) and I**2 = -1 (rational but not positive)
    # The old condition all((x**2).is_Rational for x in pargs) would pass
    # But the new condition would fail, preventing the problematic call
    
    # This should not raise IndexError - it should return a result gracefully
    try:
        result = _sqrt_match(1 + I)
        # If we get here without exception, that's good
        assert isinstance(result, list) or result == []
    except IndexError as e:
        # This is the bug we're trying to prevent
        raise AssertionError(f"_sqrt_match should not raise IndexError: {e}")

def test_sqrtdenest_no_indexerror():
    """
    Test that sqrtdenest does not raise IndexError for the main bug case.
    """
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should not raise an IndexError
    try:
        result = sqrtdenest(expr)
        # If we get here without exception, that's good
        assert result == expr
    except IndexError as e:
        # This would be the bug we're trying to prevent
        raise AssertionError(f"sqrtdenest should not raise IndexError: {e}")