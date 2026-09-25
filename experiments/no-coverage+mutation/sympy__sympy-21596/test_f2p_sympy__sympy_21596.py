"""
Regression test for bug in is_subset(Reals) of ImageSet.

The bug was introduced in a change to intersection.py that alters how
ImageSet intersects with Reals. Specifically, the new logic uses numer() 
instead of as_numer_denom() and a different approach to solving for 
when imaginary part equals zero.

Before fix: 2 in S1.intersect(Reals) was returning True incorrectly 
After fix: 2 in S1.intersect(Reals) should return False

The correct behavior should be:
S1 = {n + i*(n-1)*(n+1) | n in Integers} 
S1.intersect(Reals) should only contain real elements: n + 0*i
This happens when (n-1)*(n+1) = 0, i.e., n = 1 or n = -1
So S1.intersect(Reals) = {-1, 1} 
Therefore 2 should NOT be in S1.intersect(Reals).
"""

from sympy import symbols, S, imageset, Lambda, I, Reals
from sympy.sets.fancysets import Integers

def test_imageset_intersect_reals_bug():
    """Test that demonstrates the bug in ImageSet intersection with Reals"""
    # Create the ImageSet exactly as mentioned in the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The core bug: 2 in S1.intersect(Reals) should be False but was True 
    # The issue happens because this intersection was computed incorrectly:
    # it was returning a set that incorrectly included non-real values
    assert 2 not in S1.intersect(Reals), "2 should not be in S1.intersect(Reals)"

def test_imageset_real_values_correct():
    """Test that only correct real values are included in the intersection"""
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Compute the intersection with Reals
    result = S1.intersect(Reals)
    
    # The only real elements in S1 occur when the imaginary part equals zero:
    # imaginary part = (n-1)*(n+1) = 0 when n = 1 or n = -1
    # Therefore, S1.intersect(Reals) = {-1, 1}
    
    # Verify that we get the correct real values  
    assert 1 in result
    assert -1 in result
    
    # Verify that non-real values are NOT included
    assert 2 not in result  # This was incorrectly True before the fix
    assert 0 not in result
    assert 3 not in result

def test_imageset_intersection_structure():
    """Test that the structure of the intersection is correct"""
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The intersection should return a finite set containing exactly the 
    # real elements from the image set
    result = S1.intersect(Reals)
    
    # The result should be finite set with -1 and 1
    # Verify it doesn't include any of the incorrect values like 2
    assert 2 not in result