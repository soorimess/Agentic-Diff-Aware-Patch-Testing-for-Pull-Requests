"""
Test for the sqrtdenest IndexError bug fix.

This test ensures that sqrtdenest does not raise an IndexError when
processing expressions that cannot be denested, but rather returns
the expression unchanged.
"""

from sympy import sqrt, I, sqrtdenest

def test_sqrtdenest_no_indexerror():
    """Test that sqrtdenest doesn't raise IndexError on problematic input."""
    # The bug report shows that this expression caused IndexError
    # After the fix, it should return unchanged instead of raising error
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This test verifies that the fix prevents IndexError
    # The function should return the unchanged expression
    try:
        result = sqrtdenest(expr)
        # If we get here without exception, the fix works
        assert result == expr, f"Expected {expr}, got {result}"
    except IndexError as e:
        raise AssertionError(f"Bug not fixed: sqrtdenest still raises IndexError: {e}")

def test_sqrtdenest_returns_unchanged():
    """Test that sqrtdenest returns unchanged for expressions it can't denest."""
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # The expression should be returned unchanged (the fix's behavior)
    result = sqrtdenest(expr)
    assert result == expr

def test_sqrtdenest_behavior_is_correct():
    """Test that the behavior change is correct - no crash, proper return."""
    # Test that the function doesn't crash with IndexError
    # and returns a reasonable result
    test_expr = sqrt(2) + I + sqrt(3)
    
    try:
        result = sqrtdenest(test_expr)
        # Should not raise IndexError - this is the core fix
        # Result may be same or different, but should not crash
        assert result is not None
    except IndexError:
        raise AssertionError("Function still raises IndexError - fix not working")