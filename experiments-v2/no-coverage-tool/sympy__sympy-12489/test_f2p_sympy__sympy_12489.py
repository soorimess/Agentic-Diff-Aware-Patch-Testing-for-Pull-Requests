"""
Test for Permutation subclassing issue.

This test verifies that Permutation subclasses return instances of the subclass
rather than Permutation instances, which was broken before the fix.
"""

from sympy.combinatorics.permutations import Permutation


def test_permutation_subclassing_direct():
    """Test that _af_new method works correctly with subclasses."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        pass
    
    # Test that calling _af_new on subclass returns subclass instance
    # This directly tests the fix: _af_new should be a classmethod using cls
    result = MyPermutation._af_new([0, 2, 1])
    
    # Before the fix, this would return a Permutation instance
    # After the fix, this should return a MyPermutation instance
    assert isinstance(result, MyPermutation), f"Expected MyPermutation, got {type(result)}"