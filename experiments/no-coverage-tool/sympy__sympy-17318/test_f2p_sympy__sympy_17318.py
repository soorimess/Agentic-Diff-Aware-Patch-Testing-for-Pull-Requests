"""
Regression test for sqrtdenest IndexError bug fix.
The main behavior change: expressions that cannot be denested should be returned
unchanged instead of raising IndexError.
"""

from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_no_indexerror():
    """Main test: sqrtdenest should not raise IndexError for problematic inputs."""
    # This is the primary case from the bug report that was causing IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # The key assertion is that this call should not raise IndexError
    # The fix ensures expressions that can't be denested are returned unchanged
    result = sqrtdenest(expr)
    
    # If we get here without an IndexError, the fix worked
    # The behavior should be to return unchanged
    assert result == expr


if __name__ == "__main__":
    test_sqrtdenest_no_indexerror()
    print("Test passed - no IndexError raised for problematic input")