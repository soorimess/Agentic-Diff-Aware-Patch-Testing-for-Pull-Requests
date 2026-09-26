"""
Test for Permutation subclassing issue.

This test ensures that Permutation subclasses properly create instances
of their own class rather than always returning Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_empty_permutation_subclassing():
    """Test that empty permutation creation preserves subclass type."""
    # This is the main bug case - empty constructor
    p = MyPermutation()
    assert isinstance(p, MyPermutation), f"Expected MyPermutation, got {type(p)}"
    assert p.array_form == []