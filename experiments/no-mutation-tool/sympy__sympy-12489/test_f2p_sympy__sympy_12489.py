"""
Regression test for Permutation subclassing bug.
This test specifically targets the bug where Permutation subclasses
don't properly return instances of their own subclass type.
"""

from sympy.combinatorics.permutations import Permutation


def test_subclass_instance_creation():
    """
    Test that Permutation subclasses properly preserve type when created
    from other Permutation objects.
    
    BEFORE the fix: MyPermutation(Permutation([2, 1, 0])) would return a Permutation
    AFTER the fix: MyPermutation(Permutation([2, 1, 0])) should return a MyPermutation
    """
    
    class MyPermutation(Permutation):
        pass
    
    # This specifically tests the exact case mentioned in bug report
    # Creating a Permutation subclass from another Permutation instance
    original_perm = Permutation([2, 1, 0])
    subclass_instance = MyPermutation(original_perm)
    
    # The assertion that fails in the old code:
    # The bug was that this returns Permutation instead of MyPermutation
    assert isinstance(subclass_instance, MyPermutation), \
        "Permutation subclass should preserve its type when created from Permutation"