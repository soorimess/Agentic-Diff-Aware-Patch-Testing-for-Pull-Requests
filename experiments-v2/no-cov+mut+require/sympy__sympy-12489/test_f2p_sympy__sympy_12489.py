"""
Test for Permutation subclassing issue.

This test verifies that Permutation subclasses properly return instances
of the subclass rather than the base Permutation class.
"""

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import Cycle


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_permutation_subclassing_from_cycle():
    """
    Test that Permutation subclasses return instances of the subclass
    when created from a Cycle.
    
    This is the core issue reported: Permutation.__new__ calls _af_new
    which is a static method that hardcodes the Permutation class instead
    of using the actual class being constructed.
    """
    # This should return a MyPermutation instance, not a Permutation instance
    perm_from_cycle = MyPermutation(Cycle(0, 1, 2))
    
    # This assertion should pass after the fix, fail before the fix
    assert isinstance(perm_from_cycle, MyPermutation), \
        "Permutation subclass should return MyPermutation instance when created from Cycle"
    
    # Verify it's still a Permutation too
    assert isinstance(perm_from_cycle, Permutation)