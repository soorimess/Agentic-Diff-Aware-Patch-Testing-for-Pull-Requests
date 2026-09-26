"""
Test for Permutation subclassing issue.

This test verifies that Permutation subclasses properly return instances
of the subclass rather than the base Permutation class.
"""

from sympy.combinatorics.permutations import Permutation


def test_permutation_subclassing():
    """Test that subclassing Permutation works correctly."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        def custom_method(self):
            return "custom"
    
    # Test that the subclass properly creates instances of itself
    # This should work after the fix but fail before the fix
    perm = MyPermutation([0, 2, 1])
    
    # The key test: the returned object should be an instance of MyPermutation
    assert isinstance(perm, MyPermutation), "Should return instance of subclass"
    assert isinstance(perm, Permutation), "Should also be instance of Permutation"
    
    # Test that custom methods work
    assert perm.custom_method() == "custom", "Should have custom methods"
    
    # Test other constructor forms
    perm2 = MyPermutation([[0, 1], [2, 3]])
    assert isinstance(perm2, MyPermutation), "Should return instance of subclass from cycle form"
    
    perm3 = MyPermutation(perm)  # from another permutation
    assert isinstance(perm3, MyPermutation), "Should return instance of subclass from permutation"
    
    perm4 = MyPermutation(3)  # from integer
    assert isinstance(perm4, MyPermutation), "Should return instance of subclass from integer"