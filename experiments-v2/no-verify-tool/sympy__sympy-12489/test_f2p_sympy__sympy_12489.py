"""
Test for Permutation subclassing issue.

This test verifies that subclasses of Permutation return instances of the subclass,
not the base Permutation class.
"""

from sympy.combinatorics.permutations import Permutation


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_subclass_instance_creation():
    """Test that subclass instances are of the correct type."""
    # Test instantiation from another permutation - this is the main bug
    p1 = Permutation([0, 1, 2])
    p2 = MyPermutation(p1)
    assert isinstance(p2, MyPermutation), f"Expected MyPermutation, got {type(p2)}"
    
    # Test basic instantiation works
    p3 = MyPermutation([0, 1, 2])
    assert isinstance(p3, MyPermutation), f"Expected MyPermutation, got {type(p3)}"


def test_subclass_operations_preserve_type():
    """Test that operations on subclass instances preserve the subclass type."""
    p = MyPermutation([0, 1, 2])
    
    # Test that operations preserve subclass type
    p2 = p * p  # multiplication should return MyPermutation
    assert isinstance(p2, MyPermutation), f"Expected MyPermutation, got {type(p2)}"
    
    # Test inversion
    p3 = ~p  # inversion should return MyPermutation
    assert isinstance(p3, MyPermutation), f"Expected MyPermutation, got {type(p3)}"
    
    # Test power
    p4 = p ** 2  # power should return MyPermutation
    assert isinstance(p4, MyPermutation), f"Expected MyPermutation, got {type(p4)}"