"""
Regression test for bug in is_subset(Reals) related to ImageSet intersection.

This test ensures that ImageSet intersections with Reals are computed correctly
and that values that should not be in the intersection are properly excluded.
"""

from sympy import S, symbols, imageset, Lambda, I, Reals, FiniteSet

def test_image_set_intersect_reals_bug():
    """Test the specific bug where 2 in S1.intersect(Reals) incorrectly returned True."""
    # Create the ImageSet: {n + ⅈ⋅(n - 1)⋅(n + 1) | n ∊ ℤ}
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test 1: 2 should not be in S1 (correct - it's a complex number)
    assert 2 not in S1
    
    # Test 2: 2 should not be in S1.intersect(Reals) (this was incorrectly True before fix)
    assert 2 not in S1.intersect(Reals)
    
    # Test 3: Check that S1.intersect(Reals) produces the correct result
    # Should be {-1, 1} because only n = ±1 produce real numbers from this ImageSet
    intersection_result = S1.intersect(Reals)
    expected = FiniteSet(-1, 1)
    assert intersection_result == expected
    
    # Test 4: Values that SHOULD be in intersection should be present
    assert -1 in S1.intersect(Reals)
    assert 1 in S1.intersect(Reals)
    
    # Test 5: Verify intersection result contains only real values from the set
    # n = -1: -1 + (−2)*(0)*I = -1 (real)
    # n = 1: 1 + (0)*(2)*I = 1 (real) 
    assert len(intersection_result) == 2
    assert -1 in intersection_result
    assert 1 in intersection_result