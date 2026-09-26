"""Test for sqrtdenest IndexError bug fix"""

from sympy import sqrt, I, S, sqrtdenest

def test_sqrtdenest_no_indexerror():
    """
    Test that sqrtdenest does not raise IndexError for expressions
    that cannot be denested.
    
    This specifically tests the case that was causing:
    IndexError: tuple index out of range in _split_gcd function
    """
    
    # The exact expression from the bug report that caused IndexError
    # This should return unchanged instead of raising IndexError
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # This should not raise IndexError - the fix prevents this crash
    result = sqrtdenest(expr)
    
    # The result should be the same as the input since it cannot be denested
    assert result == expr, f"Expected {expr}, got {result}"

def test_sqrtdenest_with_negative_rational():
    """
    Test that expressions with negative rational squares are handled properly.
    This validates the fix that checks for positive rationals.
    """
    # Test with sqrt(-1) which has square -1 (negative rational)
    expr = sqrt(-1)  # This is I
    
    # This should not raise IndexError
    result = sqrtdenest(expr)
    
    # Should return unchanged (cannot be denested)
    assert result == expr, f"Expected {expr}, got {result}"

def test_sqrtdenest_no_crash_on_complex():
    """
    Test that complex expressions don't crash with IndexError.
    This validates the core fix - that we don't call split_surds
    when the conditions aren't met.
    """
    # The main goal is to ensure no IndexError is raised
    # This validates that the fix prevents the problematic code path
    
    # We don't need to assert specific results, just that no crash occurs
    try:
        # This expression would have caused the IndexError in the old code
        # by triggering the path that leads to _split_gcd with empty surds
        expr = sqrt(1 + I)  # This has a non-rational square
        result = sqrtdenest(expr)
        # If we get here without IndexError, the fix works
        # The exact result is not important for this test
    except IndexError:
        raise AssertionError("IndexError still occurs - bug not fixed")

if __name__ == "__main__":
    test_sqrtdenest_no_indexerror()
    test_sqrtdenest_with_negative_rational()
    test_sqrtdenest_no_crash_on_complex()
    print("All tests passed!")