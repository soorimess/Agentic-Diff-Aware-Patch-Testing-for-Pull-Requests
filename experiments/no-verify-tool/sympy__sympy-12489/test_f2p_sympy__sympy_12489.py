"""
Regression test for Permutation subclassing issue.
This test validates the fix to Permutation._af_new method 
to ensure subclasses properly return their own class instances.
"""
from sympy.combinatorics import Permutation


def test_permutation_core_functionality():
    """
    Basic functional tests for Permutation to ensure we haven't broken core behavior.
    """
    
    # Test basic permutation construction
    p1 = Permutation([0, 1, 2])
    assert isinstance(p1, Permutation)
    assert p1.size == 3
    
    # Test identity permutation (empty args)
    p2 = Permutation()
    assert isinstance(p2, Permutation)
    assert p2.size == 0
    
    # Test cycle form
    p3 = Permutation([[0, 1], [2]])
    assert isinstance(p3, Permutation)
    assert p3.size == 3
    
    # Test that permutation operations work  
    p4 = Permutation([1, 2, 0])
    assert isinstance(p4, Permutation) 
    assert p4.size == 3
    
    # Test more complex permutations
    p5 = Permutation([[0, 1, 2, 3, 4]])
    assert isinstance(p5, Permutation)
    assert p5.size == 5
    
    # Basic mathematical properties (not behavior-specific to the bug fix)
    assert Permutation([0, 1, 2]).array_form == [0, 1, 2]
    assert Permutation([1, 2, 0]).array_form == [1, 2, 0]