"""
Regression test for Permutation subclassing issue

This test ensures that Permutation subclasses work properly by checking that
instances created through Permutation.__new__ return instances of the subclass,
not of Permutation itself.
"""

from sympy.combinatorics.permutations import Permutation


def test_permutation_subclassing_empty_constructor():
    """Test that MyPermutation() returns a MyPermutation instance, not Permutation."""
    
    # Create a simple subclass of Permutation 
    class MyPermutation(Permutation):
        pass
    
    # The main test case showing the subclassing bug
    # When we create MyPermutation() it should return a MyPermutation instance
    # but due to hardcoded "Perm" references, it returns Permutation instead
    p = MyPermutation()
    assert isinstance(p, MyPermutation), f"MyPermutation() should return MyPermutation instance, got {type(p)}"


def test_permutation_subclassing_size_constructor():
    """Test that MyPermutation(3) returns a MyPermutation instance, not Permutation."""
    
    # Create a simple subclass of Permutation
    class MyPermutation(Permutation):
        pass
    
    # Another case of subclassing bug: MyPermutation(size=3) constructor
    # Current bug: this incorrectly returns Permutation instead of MyPermutation
    p = MyPermutation(3)
    assert isinstance(p, MyPermutation), f"MyPermutation(3) should return MyPermutation instance, got {type(p)}"