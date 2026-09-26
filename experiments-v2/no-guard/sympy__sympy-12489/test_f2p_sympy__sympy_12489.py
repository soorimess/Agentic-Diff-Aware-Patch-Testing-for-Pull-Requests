"""
Test for Permutation subclassing issue.

This test verifies that Permutation subclasses return instances of the subclass,
not regular Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation, Cycle


def test_permutation_subclassing_basic():
    """Test that Permutation subclasses return subclass instances."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        pass
    
    # Test creating from array form - this should return MyPermutation, not Permutation
    perm = MyPermutation([0, 2, 1])
    assert isinstance(perm, MyPermutation), "Should return MyPermutation instance"
    
    # Test creating from integer (identity permutation)
    perm4 = MyPermutation(3)
    assert isinstance(perm4, MyPermutation), "Should return MyPermutation instance from integer"
    
    # Test creating empty permutation
    perm5 = MyPermutation()
    assert isinstance(perm5, MyPermutation), "Should return MyPermutation instance from no args"


def test_permutation_subclassing_operations():
    """Test that Permutation subclasses work with operations."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        pass
    
    # Test operations preserve subclass
    perm1 = MyPermutation([0, 2, 1])
    perm2 = MyPermutation([1, 0, 2])
    
    # Test multiplication
    result = perm1 * perm2
    assert isinstance(result, MyPermutation), "Multiplication should preserve subclass"
    
    # Test addition (rank)
    result2 = perm1 + 1
    assert isinstance(result2, MyPermutation), "Addition should preserve subclass"
    
    # Test inversion
    result3 = ~perm1
    assert isinstance(result3, MyPermutation), "Inversion should preserve subclass"
    
    # Test power
    result4 = perm1 ** 2
    assert isinstance(result4, MyPermutation), "Power should preserve subclass"