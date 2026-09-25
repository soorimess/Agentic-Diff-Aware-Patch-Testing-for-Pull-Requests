"""
Regression test for sqrtdenest IndexError issue.

This tests that sqrtdenest properly handles expressions where
the old code would have led to IndexError in _split_gcd.
"""

from sympy import sqrt, I, sqrtdenest, S
from sympy.core.expr import unchanged

def test_sqrtdenest_no_indexerror_on_complex_radicands():
    """
    Test that sqrtdenest does not raise IndexError when processing
    expressions with complex radicands that could cause _split_gcd
    to be called with empty surds list.
    
    The original bug was that when _split_gcd was called with no arguments
    (empty tuple), it would try to access a[0] resulting in IndexError.
    """
    # This expression leads to case where x**2 produces complex values
    # that don't satisfy the NEW condition (is_positive)
    # but would have satisfied OLD condition (is_Rational)
    expr = sqrt(4 + 3*I)
    
    # This should not raise IndexError
    try:
        result = sqrtdenest(expr)
        # Should return unchanged since it can't be denested
        assert result == expr
    except IndexError:
        raise AssertionError("sqrtdenest raised IndexError - this should be fixed")
        
    # Combined with other terms
    expr2 = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    try:
        result2 = sqrtdenest(expr2)
        # Should return unchanged since it can't be denested
        assert result2 == expr2
    except IndexError:
        raise AssertionError("sqrtdenest raised IndexError for complex radicand - this should be fixed")


def test_sqrtdenest_preserves_non_denestable():
    """
    Test that non-denestable expressions are returned unchanged,
    not raising exceptions.
    """
    # Test a case that is specifically problematic for the gcd splitting
    test_cases = [
        sqrt(-1) + sqrt(-2) + 1,
        sqrt(4 + 3*I),  # This is from the exact bug report
        sqrt(2)*sqrt(4 + 3*I),  # Root of the expression from bug report 
    ]
    
    for expr in test_cases:
        try:
            result = sqrtdenest(expr)
            # Should never raise IndexError and should return same expr
            assert result == expr, f"Expression {expr} should be unchanged"
        except IndexError as e:
            raise AssertionError(f"sqrtdenest raised IndexError for {expr}: {e}")