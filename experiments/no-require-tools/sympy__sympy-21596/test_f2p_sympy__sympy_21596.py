"""
Regression test for bug in is_subset(Reals) 

Test to verify the fix for ImageSet intersection with Reals produces correct results.
"""

from sympy import S, imageset, Lambda, symbols, Reals, FiniteSet, I
from sympy.sets.fancysets import Integers

def test_imageset_intersect_reals_bug():
    """Test the specific bug case where S1.intersect(Reals) incorrectly returns True for 2"""
    # Create the ImageSet as described in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test that 2 is not in S1 (correct)
    assert 2 not in S1
    
    # Test the bug: 2 should NOT be in S1.intersect(Reals) 
    # But before the fix, it was incorrectly returning True
    assert 2 not in S1.intersect(Reals)
    
    # Also check that the actual intersection result is correct
    # S1.intersect(Reals) should return {-1, 1}
    result = S1.intersect(Reals)
    expected = FiniteSet(-1, 1)
    assert result == expected

def test_imageset_intersect_reals_members():
    """Test that only -1 and 1 are in the intersection"""
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Check that -1 and 1 are in the intersection
    assert -1 in S1.intersect(Reals)
    assert 1 in S1.intersect(Reals)
    
    # Check that other values like 2 are NOT in the intersection
    assert 2 not in S1.intersect(Reals)

def test_more_complex_imageset():
    """Test with a more complex case to potentially trigger more code paths"""
    n = symbols('n')
    # Try another ImageSet to see if we can hit different code paths
    S2 = imageset(Lambda(n, n + (n**2 - 4)*I), S.Integers)
    
    # For this set, imaginary part is n^2 - 4 = 0 means n = ±2
    # So S2.intersect(Reals) should be {-2, 2}
    result = S2.intersect(Reals)
    # In the buggy version, this might be calculated incorrectly
    assert -2 in S2.intersect(Reals)
    assert 2 in S2.intersect(Reals) 
    assert 0 not in S2.intersect(Reals)  # This should not be in the intersection