from sympy import sqrt, I, sqrtdenest


def test_sqrtdenest_prevents_indexerror():
    """
    Regression test that ensures sqrtdenest does not raise IndexError
    for expressions that cannot be properly denested.
    
    This test verifies the fix for issue where complex expressions 
    would trigger IndexError due to processing through split_surds with
    empty surds lists.
    """
    # Complex expression that could have triggered IndexError before fix
    # The specific problematic path involves _sqrt_match -> split_surds -> _split_gcd(*[])
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Before fix: This would raise IndexError: tuple index out of range
    # After fix: This should return unchanged, not raise exception
    try:
        result = sqrtdenest(expr)
        # If we got here without IndexError, that's the fix working
        assert result == expr, f"Expression should be returned unchanged, got {result}"
        # The important thing is no IndexError exception
    except IndexError as e:
        raise AssertionError(f"IndexError should not occur after fix: {e}")
    except Exception as e:
        # Other exceptions (like NotImplementedError) are acceptable  
        # as long as it's not IndexError
        if "IndexError" in str(type(e)):
            raise AssertionError(f"IndexError should not occur: {e}")


def test_sqrtdenest_handles_complex_unprocessable():
    """
    Test that complex expressions that cannot be processed are handled gracefully.
    
    The pull request ensures that when expressions cannot be denested,
    they are returned unchanged rather than raising internal errors.
    """
    # Test cases with complex sqrt terms that should not crash
    test_cases = [
        sqrt(-1) + sqrt(2),  # I + sqrt(2)  
        sqrt(3) + sqrt(-5),  # sqrt(3) + I*sqrt(5)
        sqrt(-10) + sqrt(7), # I*sqrt(10) + sqrt(7)
    ]
    
    for expr in test_cases:
        # These should not raise IndexError
        try:
            result = sqrtdenest(expr)
            # Result should be unchanged if cannot be denested
            assert result == expr
        except IndexError:
            raise AssertionError(f"IndexError should not occur for {expr}")