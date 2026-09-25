"""
Test for the bug in is_subset(Reals) related to ImageSet intersection
This test specifically verifies the fix: that 2 in S1.intersect(Reals) 
correctly returns False instead of the buggy True behavior.
"""

from sympy import S, imageset, Lambda, I
from sympy.abc import n


def test_imageset_intersect_reals_bug_fix():
    """
    The core test for the reported bug:
    Before fix: 2 in S1.intersect(Reals) = True (incorrect)
    After fix: 2 in S1.intersect(Reals) = False (correct)
    
    This directly tests the behavioral difference the pull request addresses.
    """
    # Create the set S1 = {n + ⅈ⋅(n - 1)⋅(n + 1) │ n ∊ ℤ}
    expr = Lambda(n, n + I*(n - 1)*(n + 1))
    S1 = imageset(expr, S.Integers)
    
    # These should always be True (correct behavior)
    assert 2 not in S1  # 2 is not even in the original set 
    assert 1 in S1      # 1 is in the original set
    assert -1 in S1     # -1 is in the original set
    
    # The specific bug: 2 should NOT be in the intersection with Reals
    # This was incorrectly returning True before the fix
    assert 2 not in S1.intersect(S.Reals)


def test_imageset_intersect_reals_real_elements():
    """
    Additional behavior test to make sure real elements of the set 
    can be properly identified in the intersection.
    """
    # Create the set S1 = {n + ⅈ⋅(n - 1)⋅(n + 1) │ n ∊ ℤ}
    expr = Lambda(n, n + I*(n - 1)*(n + 1))
    S1 = imageset(expr, S.Integers)
    
    # Elements that SHOULD be in the intersection with Reals
    # (n=1) -> 1 + i*(0)*2 = 1 (real)
    # (n=-1) -> -1 + i*(-2)*0 = -1 (real)
    assert 1 in S1.intersect(S.Reals)
    assert -1 in S1.intersect(S.Reals)
    
    # Values that should NOT be in the intersection with Reals  
    assert 2 not in S1.intersect(S.Reals)
    assert 0 not in S1.intersect(S.Reals)  # 0 + i*(-1)*(1) = i (complex)