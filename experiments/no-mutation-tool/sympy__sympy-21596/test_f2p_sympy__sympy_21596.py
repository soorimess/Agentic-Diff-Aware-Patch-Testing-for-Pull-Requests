"""
Regression test for bug with is_subset(Reals) in ImageSets.

This captures the exact behavior change from the bug report.  
"""
from sympy import S, imageset, Lambda, I, Reals, Integers, symbols

def test_imageset_intersect_reals_membership_bug():
    """Test for the specific bug where 2 in S1.intersect(Reals) incorrectly returns True."""
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # From the bug report:
    # 2 in S1 should be False (this is correct)
    # 2 in S1.intersect(Reals) should be False (but was incorrectly True)
    
    # Test the specific failing assertion 
    result = 2 in S1.intersect(Reals)
    
    # This will fail _before_ the fix and pass _after_ the fix  
    assert result is False, f"Bug: 2 in S1.intersect(Reals) should be False but got {result}"