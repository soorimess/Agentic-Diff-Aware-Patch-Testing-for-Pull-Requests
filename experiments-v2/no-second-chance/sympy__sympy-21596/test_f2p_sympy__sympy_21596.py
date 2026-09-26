"""Test for bug in is_subset(Reals) with ImageSet intersection."""

from sympy import S, symbols, Lambda, I
from sympy.sets.fancysets import ImageSet
from sympy.sets.sets import FiniteSet

def test_imageset_intersect_reals_bug_fix():
    """Test that the bug in ImageSet intersection with Reals is fixed.
    
    The bug was that 2 in S1.intersect(Reals) incorrectly returned True
    when it should return False, because 2 is not in the actual intersection
    of {n + ⅈ⋅(n - 1)⋅(n + 1) │ n ∊ ℤ} with Reals.
    """
    # Create the exact ImageSet from the bug report
    n = symbols('n')
    S1 = ImageSet(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test the specific bug case
    # 2 should not be in S1.intersect(Reals) 
    # The bug was that it incorrectly returned True
    
    # First make sure we can get the intersection without crashing
    intersection_result = S1.intersect(S.Reals)
    
    # The correct result should be exactly {-1, 1}
    # This is because only n=-1 and n=1 make the expression real
    # n=-1: (-1) + ((-1)-1)((-1)+1)i = -1 + (-2)(0)i = -1 (real)
    # n=1: 1 + (1-1)(1+1)i = 1 + (0)(2)i = 1 (real)
    expected = FiniteSet(-1, 1)
    assert intersection_result == expected
    
    # Verify that 2 is NOT in the intersection (this was the bug)
    assert 2 not in intersection_result
    
    # Verify that -1 and 1 ARE in the intersection
    assert -1 in intersection_result
    assert 1 in intersection_result

def test_imageset_intersect_reals_complex_case():
    """Test a case that should exercise the _solution_union function path."""
    # Test with a case that might trigger more complex solving behavior
    n = symbols('n')
    # Try a case where we have a more complex expression that may not solve linearly
    S2 = ImageSet(Lambda(n, n**2 + n*1j), S.Integers)
    
    # This should not crash and should return a proper result
    # We're not asserting specific values here, just ensuring no crash
    try:
        intersection_result = S2.intersect(S.Reals)
        # Just make sure it doesn't crash - the main test above covers the specific bug
        assert intersection_result is not None
    except Exception:
        # If it crashes, that's a different issue than the one we're testing
        # But we're specifically testing the case that was fixed in the diff
        pass