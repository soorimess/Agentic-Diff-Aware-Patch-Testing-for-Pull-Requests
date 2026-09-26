"""
Test for Permutation subclassing bug.

This test verifies that Permutation subclasses properly return instances
of the subclass rather than always returning Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_subclass_identity():
    """Test that subclass instances are of the correct type."""
    # This is the core test - when we create MyPermutation() it should be a MyPermutation
    p = MyPermutation()
    # Before fix: p would be of type Permutation
    # After fix: p should be of type MyPermutation
    assert type(p) == MyPermutation, "Subclass instances should be of subclass type"