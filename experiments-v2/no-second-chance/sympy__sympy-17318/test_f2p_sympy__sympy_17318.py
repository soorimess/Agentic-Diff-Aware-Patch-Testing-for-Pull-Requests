"""
Test for the sqrtdenest IndexError bug fix.

The bug was that sqrtdenest would raise an IndexError when trying to 
denest expressions that cannot be denested, instead of returning them unchanged.
"""
from sympy import sqrt, sqrtdenest, I

def test_sqrtdenest_no_indexerror():
    """
    Test that sqrtdenest doesn't raise IndexError for expressions that 
    cannot be denested.
    """
    # Test the main case from the bug report
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should NOT raise IndexError
    # It should return the expression unchanged (the fix behavior)
    try:
        result = sqrtdenest(expr)
        # Success - no IndexError raised
        assert result is not None
    except IndexError as e:
        raise AssertionError(f"sqrtdenest raised IndexError (bug not fixed): {e}")

def test_sqrtdenest_handles_complex_expressions():
    """
    Test that sqrtdenest handles complex expressions gracefully without IndexError.
    """
    # Test various complex expressions that might have caused issues
    test_cases = [
        sqrt(4 + 3*I),
        (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2,
        sqrt(2*I) + sqrt(3*I),
    ]
    
    for i, expr in enumerate(test_cases):
        try:
            result = sqrtdenest(expr)
            # If we get here without IndexError, it's good
        except IndexError as e:
            raise AssertionError(f"sqrtdenest raised IndexError on test case {i}: {e}")

def test_sqrtdenest_behavior_change():
    """
    Test the specific behavior change that was implemented.
    
    Before fix: sqrtdenest would raise IndexError for certain complex expressions
    After fix: sqrtdenest should return unchanged expressions instead of raising IndexError
    """
    # This is the key test - it should not raise IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # The behavior we want to verify:
    # 1. No IndexError should be raised
    # 2. The expression should be handled gracefully
    try:
        result = sqrtdenest(expr)
        # If we reach here without IndexError, the fix is working
        assert result is not None
    except IndexError:
        raise AssertionError("sqrtdenest still raises IndexError - fix not working")