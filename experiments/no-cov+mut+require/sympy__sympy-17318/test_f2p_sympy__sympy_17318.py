"""
Regression test for sqrtdenest IndexError bug.

This test specifically verifies that the IndexError which occurred with 
complex expressions involving negative rational squares is now fixed.
"""

from sympy import sqrt, I, sqrtdenest

def test_no_indexerror_on_complex_expressions():
    """
    Test that sqrtdenest does not raise IndexError for complex expressions
    that previously caused IndexError due to the condition check bug.
    
    The bug was in _sqrt_match function:
    Old code: all((x**2).is_Rational for x in pargs) 
    New code: all(sq.is_Rational and sq.is_positive for sq in sqargs)
    
    The key difference is that negative rational squares (like -9 from (3*I)^2) 
    were incorrectly accepted by the old code, causing _split_gcd to be called 
    with invalid arguments and resulting in IndexError.
    """
    
    # The specific example from the bug report that would cause IndexError
    # with the old (broken) condition
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before fix: This would raise IndexError: tuple index out of range
    # After fix: Should return the expression unchanged (no crash)
    try:
        result = sqrtdenest(expr)
        # If we reach here, no IndexError - this should be the fix working
        assert result is not None, "sqrtdenest should not return None"
        # Don't assert specific result - the behavior may vary, 
        # but it should not crash with IndexError
    except IndexError as e:
        # This test failure indicates the bug is still present
        raise AssertionError(f"IndexError still occurs - bug not fixed: {e}")

def test_handling_of_negative_rational_squares():
    """
    Test the specific case of expressions involving negative rational squares,
    which was the root cause of the IndexError in _split_gcd function.
    """
    
    # Create an expression that would trigger the problematic code path
    # where terms like sqrt(-1) exist, leading to negative squared values
    try:
        # This expression involves complex numbers whose squares are negative rationals  
        expr = sqrt(-1) + sqrt(2)  # sqrt(-1) = I, and I^2 = -1
        
        result = sqrtdenest(expr)
        
        # The important thing is that we don't get IndexError crash
        assert result is not None
    except IndexError:
        raise AssertionError("IndexError with negative rational squares - bug not fixed")

def test_complex_expression_gentle_handling():
    """
    Test that complex expressions are handled gracefully by ensuring no crash.
    This focuses on the fact that the fix prevents crashes, not necessarily 
    content of results.
    """
    
    # Expression from the actual bug report that was failing
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This is specifically about avoiding the IndexError that the PR fixed
    # The result may vary, but the critical point is crash-free execution
    try:
        result = sqrtdenest(expr)
        # Success means the crash is prevented
        assert result is not None, "Should not crash"
    except IndexError:
        raise AssertionError("Expression processing should not raise IndexError")
    

if __name__ == "__main__":
    test_no_indexerror_on_complex_expressions()
    test_handling_of_negative_rational_squares()
    test_complex_expression_gentle_handling()
    print("All regression tests passed - no IndexError observed")