"""
Regression test for Permutation subclassing issue.

This test verifies that Permutation subclasses properly return instances
of the subclass rather than always returning Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation


def test_permutation_subclassing():
    """Test that subclasses of Permutation return instances of the subclass."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        custom_attr = "custom"
    
    # Test that creating a permutation from array form returns subclass instance
    perm = MyPermutation([0, 1, 2])
    assert isinstance(perm, MyPermutation)
    assert perm.custom_attr == "custom"
    
    # Test that creating from cycle form returns subclass instance
    perm2 = MyPermutation([[0, 1], [2]])
    assert isinstance(perm2, MyPermutation)
    assert perm2.custom_attr == "custom"
    
    # Test that creating from another permutation returns subclass instance
    perm3 = MyPermutation(perm)
    assert isinstance(perm3, MyPermutation)
    assert perm3.custom_attr == "custom"
    
    # Test that creating from size returns subclass instance
    perm4 = MyPermutation(size=3)
    assert isinstance(perm4, MyPermutation)
    assert perm4.custom_attr == "custom"


def test_permutation_subclassing_operations():
    """Test that operations on subclass instances return subclass instances."""
    
    class MyPermutation(Permutation):
        custom_attr = "custom"
    
    # Test multiplication returns subclass instance
    perm1 = MyPermutation([1, 2, 0])
    perm2 = MyPermutation([2, 0, 1])
    result = perm1 * perm2
    assert isinstance(result, MyPermutation)
    assert result.custom_attr == "custom"
    
    # Test power returns subclass instance
    perm = MyPermutation([1, 2, 0])
    result = perm ** 2
    assert isinstance(result, MyPermutation)
    assert result.custom_attr == "custom"