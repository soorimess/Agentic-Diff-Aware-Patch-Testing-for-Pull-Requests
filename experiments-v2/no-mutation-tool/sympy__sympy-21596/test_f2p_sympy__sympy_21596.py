from sympy import S, imageset, Lambda, symbols, Reals, I, FiniteSet
from sympy.sets.fancysets import Integers

def test_image_set_intersect_reals_bug():
    """Test for bug in is_subset(Reals) - issue #19513"""
    # Create the set as described in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The main bug: 2 in S1.intersect(Reals) should be False but is True
    # This is the key assertion that should fail with the buggy code
    assert 2 not in S1.intersect(Reals), "Bug: 2 should not be in S1.intersect(Reals)"
    
    # Additional checks to make sure the behavior is correct
    assert 1 in S1.intersect(Reals), "1 should be in S1.intersect(Reals)"
    assert -1 in S1.intersect(Reals), "-1 should be in S1.intersect(Reals)"
    
    # Check that 2 is not in S1 itself (this is correct)
    assert 2 not in S1, "2 should not be in S1"
    
    # The intersection should be a finite set with only -1 and 1
    result = S1.intersect(Reals)
    # The correct result should be FiniteSet(-1, 1)
    # But let's just check the key property that 2 is not in it
    assert 2 not in result, "2 should not be in the intersection result"