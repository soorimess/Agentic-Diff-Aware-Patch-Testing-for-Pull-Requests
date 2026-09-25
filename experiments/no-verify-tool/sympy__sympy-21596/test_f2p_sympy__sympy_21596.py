"""
Regression tests for specific bug in is_subset(Reals) handling.
This tests the bug that was introduced where ImageSet.intersect(Reals) 
was returning incorrect results.
"""

from sympy import S, symbols, Lambda, ImageSet, Reals, I
from sympy.sets import imageset

def test_imageset_intersect_reals_bug():
    """Test that demonstrates the bug in ImageSet intersect Reals."""
    # Create the specific example from the bug report
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # The original bug report shows these
    # 2 in S1 should be False 
    assert 2 not in S1
    
    # This was the buggy behavior - should be False
    # 2 in S1.intersect(Reals) was True (incorrect), should be False
    assert 2 not in S1.intersect(Reals)
    
    # Test that the computed intersection result is correct
    # Only values of n that make n + (n-1)(n+1)*I real are n = -1 and n = 1
    # Which give results 1 and -1 respectively  
    result = S1.intersect(Reals)  
    # Check that the computed result treats 2 not as a member
    # (this is a key assertion because 2 should not be in result but 
    # various wrong implementations make it appear as member)
    assert 2 not in result

def test_imageset_real_values():
    """Test actual real values in the set."""
    n = symbols('n')
    S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
    
    # These are the integer n values that produce real outputs
    # When n = -1: -1 + (-1-1)(-1+1)*I = -1 + 0*I = -1
    # When n = 1: 1 + (1-1)(1+1)*I = 1 + 0*I = 1  
    assert -1 in S1
    assert 1 in S1
    
    # These are non-real outputs
    assert 0 not in S1  # 0 + (0-1)(0+1)*I = 0 - I = -I (not real) 
    assert 2 not in S1  # 2 + (2-1)(2+1)*I = 2 + 3*I (not real)
    
    # The intersection with Reals should only contain -1 and 1 
    result = S1.intersect(Reals)
    
    # Validate the intersection results are proper elements
    real_values = []
    for val in [-1, 1, 2, 0]:
        if val in result:
            real_values.append(val)
    
    assert real_values == [-1, 1], f"Found real values {real_values}, expected [-1, 1]"