"""
Regression test for Permutation subclassing issue.

This test verifies that Permutation subclasses properly return instances
of the subclass type rather than always returning Permutation instances.
"""

from sympy.combinatorics import Permutation
from sympy.combinatorics import Cycle


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_subclass_empty_constructor():
    """Test that empty permutation constructor returns subclass."""
    empty_perm = MyPermutation()
    assert type(empty_perm) == MyPermutation


def test_subclass_identity_constructor():
    """Test that integer argument constructor returns subclass."""
    identity_perm = MyPermutation(3)
    assert type(identity_perm) == MyPermutation


def test_subclass_cycle_constructor():
    """Test that Cycle argument constructor returns subclass."""
    cycle = Cycle(0, 1, 2)
    cycle_perm = MyPermutation(cycle)
    assert type(cycle_perm) == MyPermutation