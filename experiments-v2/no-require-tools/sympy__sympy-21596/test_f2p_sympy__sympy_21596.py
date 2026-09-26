from sympy import symbols, S, imageset, Lambda, I, Reals, FiniteSet

def test_image_set_intersect_reals_bug():
    """Test for bug in is_subset(Reals) - intersection of ImageSet with Reals"""
    # Create the ImageSet as described in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test the bug conditions
    # 2 should not be in S1
    assert 2 not in S1
    
    # 2 should not be in S1.intersect(Reals) - this was incorrectly returning True
    assert 2 not in S1.intersect(Reals)
    
    # The intersection with Reals should be {-1, 1}
    result = S1.intersect(Reals)
    expected = FiniteSet(-1, 1)
    assert result == expected