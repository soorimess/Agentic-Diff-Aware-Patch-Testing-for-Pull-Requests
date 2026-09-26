"""Test for the bug in is_subset(Reals) for ImageSet intersection."""

from sympy import S, symbols, Lambda, imageset, Reals, I

def test_imageset_intersect_reals_bug():
    """Test that 2 is not in S1.intersect(Reals) - the main bug reported."""
    # Create the ImageSet as described in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The bug: 2 in S1.intersect(Reals) incorrectly returns True
    # It should return False because 2 is not in the real part of S1
    # Only n = -1 and n = 1 make the imaginary part zero
    assert 2 not in S1.intersect(Reals)