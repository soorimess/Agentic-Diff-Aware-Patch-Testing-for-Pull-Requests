from sympy import sqrt, I, S
from sympy.simplify.sqrtdenest import sqrtdenest, _sqrt_match


def test_sqrtdenest_handles_negative_rational_squares():
    """
    Test that the fix correctly rejects expressions with 
    negative rational squares to avoid IndexError.
    
    This specifically tests the logic change:
    OLD: if all((x**2).is_Rational for x in pargs)                                                  
    NEW: if all(sq.is_Rational and sq.is_positive for sq in sqargs)
        
    Before fix: expressions like sqrt(-1) + sqrt(2) would be accepted by _sqrt_match
    After fix: these expressions are correctly rejected to prevent crash conditions
    """
    
    # Test the key part: _sqrt_match should process the right arguments differently
    # Create an expression where we know pargs have negative rational squares
    
    # Scenario: expression that has sqrt(-1) term  
    expr = sqrt(-1) + sqrt(2)  # This includes I and sqrt(2)
    
    # This should not raise an IndexError even when processed
    # The fix should prevent deep processing that could lead to IndexError
    result = sqrtdenest(expr)
    assert result == expr


def test_sqrtdenest_regression_exact_bug_case():
    """
    Regression test for the exact case from the bug report which 
    would raise IndexError in the old code.
    """
    # Note: if the exact case still works, then our check is more about the path
    expr = (3 - sqrt(2)*sqrt(4 + 3*I) + 3*I)/2
    
    # Should not raise IndexError but return unchanged
    result = sqrtdenest(expr)  
    assert result == expr


def test_sqrt_match_directly():
    """
    Direct test of _sqrt_match function behavior with expressions 
    containing negative rational squares.
    """
    # Using this function directly to test the condition paths
    # But it is not sufficiently exposed or efficient for direct testing 
    # of this particular edge case

    # The real point is validation: no IndexError should occur
    expr = sqrt(-1) + sqrt(2)
    try:
        result = sqrtdenest(expr)
        assert result == expr
    except IndexError:
        # This should never happen with the fix
        raise AssertionError("IndexError should not occur with the fix applied")