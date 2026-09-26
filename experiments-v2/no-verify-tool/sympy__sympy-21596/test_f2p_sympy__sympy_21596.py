"""
Regression test for bug in is_subset(Reals) for ImageSet.

This test checks that when an ImageSet is intersected with Reals,
the result is correct and doesn't incorrectly include values that
should not be in the intersection.
"""

from sympy import (S, symbols, Lambda, imageset, Reals, FiniteSet, I)
from sympy.sets.fancysets import Integers

def test_imageset_intersect_reals_bug():
    """
    Test that demonstrates the bug in ImageSet intersection with Reals.
    
    The bug is that 2 in S1.intersect(Reals) returns True when it should be False.
    """
    # Create the ImageSet as described in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test that 2 is not in S1 (this should be False)
    assert 2 not in S1
    
    # Test that 2 is not in S1.intersect(Reals) (this should be False, but was True before fix)
    assert 2 not in S1.intersect(Reals)
    
    # Test the correct result of S1.intersect(Reals) should be {-1, 1}
    result = S1.intersect(Reals)
    expected = FiniteSet(-1, 1)
    assert result == expected

def test_imageset_intersect_reals_correct_values():
    """
    Test that the intersection produces the correct real values.
    """
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The expression is n + (n-1)*(n+1)*I
    # For this to be real, the imaginary part must be 0
    # imaginary part = (n-1)*(n+1) = n^2 - 1
    # For this to be 0: n^2 - 1 = 0 => n = ±1
    # So the real values are:
    # n = 1: 1 + (1-1)*(1+1)*I = 1 + 0*I = 1
    # n = -1: -1 + (-1-1)*(-1+1)*I = -1 + 0*I = -1
    
    # These should be the only real values in the set
    real_values = S1.intersect(Reals)
    
    # Check that we get exactly {-1, 1} as the result
    assert real_values == FiniteSet(-1, 1)
    
    # Verify that 1 and -1 are indeed in the set
    assert 1 in S1
    assert -1 in S1
    
    # Verify that 2 is not in the set (and not in the intersection)
    assert 2 not in S1
    assert 2 not in S1.intersect(Reals)
    
    # Verify that 0 is not in the set (and not in the intersection)
    assert 0 not in S1
    assert 0 not in S1.intersect(Reals)