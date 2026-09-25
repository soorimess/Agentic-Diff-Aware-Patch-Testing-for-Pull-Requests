"""
Regression test for sqrtdenest IndexError bug fix.
Tests that expressions which previously caused IndexError are handled gracefully.
"""
from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_no_longer_raises_indexerror():
    """
    Test verifies that sqrtdenest no longer raises IndexError for expressions
    that would cause IndexError due to an empty surds list in _split_gcd.
    
    The fix in sympy/simplify/sqrtdenest.py changed the condition from:
    "all((x**2).is_Rational for x in pargs)" 
    to:
    "all(sq.is_Rational and sq.is_positive for sq in sqargs)"
    
    This prevents expressions with negative rational squares from being 
    processed through split_surds, which would previously have caused
    an IndexError when _split_gcd was called with an empty surds list.
    """
    # This is the main expression from the bug report that caused IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before fix: This would raise IndexError: tuple index out of range
    # After fix: This should return the expression unchanged without exception
    
    # The key assertion: no IndexError should be raised
    try:
        result = sqrtdenest(expr)
        # If we get here without exception, the fix worked
        # Return the expression unchanged as expected
        assert result == expr
    except IndexError as e:
        # This would indicate the bug is still present
        raise AssertionError("IndexError still raised - bug not fixed: %s" % str(e))


def test_sqrtdenest_handles_non_denestable_expressions():
    """
    Verify behavior for expressions that cannot be denested.
    
    The fix ensures that when expressions cannot be meaningfully processed 
    through the denesting algorithm, they are returned unchanged rather 
    than causing internal crashes.
    """
    from sympy import sqrt
    
    # Expressions that would cause the problematic path in old code
    expressions = [
        (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2,
        sqrt(-1),  # Simple case of negative square root
    ]
    
    for expr in expressions:
        # All should be handled gracefully without IndexError
        try:
            result = sqrtdenest(expr)
            # Should not raise IndexError - behavior is graceful failure
            assert result == expr  # Should be unchanged for non-denestable cases
        except IndexError:
            raise AssertionError("IndexError in non-denestable expression: %s" % expr)