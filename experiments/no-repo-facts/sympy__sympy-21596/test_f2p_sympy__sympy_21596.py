"""Regression test for bug in is_subset(Reals) - image sets intersected with Reals."""

from sympy import S, imageset, Lambda, I, Reals, FiniteSet
from sympy.abc import n


def test_image_set_intersect_real_bug():
    """Test for bug where 2 in S1.intersect(Reals) incorrectly returned True."""
    # Create the problematic ImageSet from the bug report
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # These should be False
    assert 2 not in S1
    assert 2 not in S1.intersect(Reals)
    
    # Test that correct members are included
    assert -1 in S1
    assert 1 in S1
    assert -1 in S1.intersect(Reals)
    assert 1 in S1.intersect(Reals)
    
    # Test that the intersection contains exactly the expected elements
    expected_reals = FiniteSet(-1, 1)
    actual_reals = S1.intersect(Reals)
    
    # Verify that actual contains exactly the expected elements
    assert actual_reals == expected_reals