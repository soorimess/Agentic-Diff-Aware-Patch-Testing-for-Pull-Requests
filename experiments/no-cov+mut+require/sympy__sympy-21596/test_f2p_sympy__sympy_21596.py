"""Test for bug in ImageSet intersection with Reals"""

from sympy import S, symbols, imageset, Lambda, I, Reals, FiniteSet
from sympy.sets.fancysets import Integers

def test_imageset_intersect_reals_correct_behavior():
    """Test that ImageSet.intersect(Reals) works correctly with the bug fix.
    
    The bug was that 2 in S1.intersect(Reals) incorrectly returned True, 
    when it should be False. Also, S1.intersect(Reals) should return {-1, 1}.
    """
    # Create the ImageSet: {n + ⅈ⋅(n - 1)⋅(n + 1) │ n ∊ ℤ}
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test that 2 is not in S1 (this should be False)
    assert 2 not in S1
    
    # Test that 2 is not in S1.intersect(Reals) - this was incorrectly True
    assert 2 not in S1.intersect(Reals)
    
    # Test the intersection itself - should be {-1, 1}
    result = S1.intersect(Reals)
    expected = FiniteSet(-1, 1)
    assert result == expected