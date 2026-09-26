"""
Test for bug in is_subset(Reals) with ImageSet intersection.

This test verifies that when intersecting an ImageSet with Reals,
the result correctly excludes values that make the imaginary part non-zero.
"""

from sympy import S, imageset, Lambda, symbols, I, Reals
from sympy.sets.fancysets import Integers

def test_imageset_intersect_reals_bug():
    """Test that demonstrates the bug in ImageSet intersection with Reals."""
    # Create the ImageSet from the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # Test basic membership - should be False for 2
    assert 2 not in S1
    
    # Test intersection with Reals - this is where the bug manifests
    result = S1.intersect(Reals)
    
    # The bug: 2 incorrectly appears in the intersection when it shouldn't
    # The correct behavior is that only -1 and 1 should be in the intersection
    # So 2 should NOT be in the intersection
    assert 2 not in result
    
    # Test that -1 and 1 ARE in the intersection (they should be)
    assert -1 in result
    assert 1 in result
    
    # Test that 0 is NOT in the intersection (should be complex)
    assert 0 not in result