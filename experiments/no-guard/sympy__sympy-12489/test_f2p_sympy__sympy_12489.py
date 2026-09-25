"""
Regression test for Permutation subclassing issue.

This test verifies that Permutation subclasses properly return instances
of the subclass rather than always returning Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import Cycle


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_permutation_subclassing():
    """Test that Permutation subclasses return instances of the subclass."""
    # Create instance of MyPermutation - this should return MyPermutation, not Permutation
    perm = MyPermutation([0, 1, 2])
    
    # This assertion should fail before the fix and pass after the fix
    assert isinstance(perm, MyPermutation), "Subclass instances should be of the subclass type"
    
    # Test with Cycle constructor too
    cycle = Cycle(0, 1, 2)
    perm2 = MyPermutation(cycle)
    
    # This assertion should also fail before the fix and pass after the fix  
    assert isinstance(perm2, MyPermutation), "Subclass instances from Cycle should be of the subclass type"