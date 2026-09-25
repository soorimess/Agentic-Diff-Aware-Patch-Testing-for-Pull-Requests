"""Regression test for sqrtdenest IndexError bug fix"""

from sympy import sqrt, sqrtdenest, I


def test_sqrtdenest_indexerror_regression():
    """This test verifies that the IndexError bug is fixed.
    
    The bug occurred when sqrtdenest tried to process an expression
    that would cause _split_gcd to be called with an empty tuple,
    leading to IndexError: tuple index out of range.
    """
    # Expression that would trigger the bug according to bug report
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should not raise an IndexError
    # Before fix: IndexError: tuple index out of range in _split_gcd
    # After fix: should return unchanged expression
    result = sqrtdenest(expr)
    
    # The assertion is that it doesn't crash - returning the unchanged expression
    # is the expected behavior when it can't be denested
    assert result == expr


def test_complex_surds_unchanged():
    """Test that complex surds expressions return unchanged."""
    expr1 = sqrt(4 + 3*I)
    expr2 = sqrt(1 + I)
    
    # These should all pass without IndexError
    result1 = sqrtdenest(expr1)
    result2 = sqrtdenest(expr2)
    
    assert result1 == expr1
    assert result2 == expr2