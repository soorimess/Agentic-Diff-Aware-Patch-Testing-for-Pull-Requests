"""
Test for Permutation subclassing regression.
This test ensures that Permutation subclasses return instances of the subclass,
not Permutation objects.
"""

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import Cycle


def test_permutation_subclassing_basic():
    """Test that Permutation subclasses return instances of the subclass."""
    # Make a subclass that doesn't override __init__ to avoid complications
    class MyPermutation(Permutation):
        pass
    
    # Create a subclass instance
    perm = MyPermutation([0, 2, 1])
    
    # The result should be an instance of MyPermutation, not Permutation
    # If the bug exists, this will be False because Permutation.__new__ 
    # always calls _af_new which hardcodes Basic.__new__(Perm, perm)
    # instead of Basic.__new__(cls, perm)
    assert isinstance(perm, MyPermutation), f"Expected MyPermutation, got {type(perm)}"


def test_permutation_subclassing_from_cycle():
    """Test that Permutation subclasses work when created from Cycle."""
    # Make a subclass that doesn't override __init__ to avoid complications
    class MyPermutation(Permutation):
        pass
    
    # Create a subclass instance from a cycle
    perm = MyPermutation(Cycle(0, 1, 2))
    
    # The result should be an instance of MyPermutation, not Permutation
    assert isinstance(perm, MyPermutation), f"Expected MyPermutation, got {type(perm)}"


def test_permutation_subclassing_copy():
    """Test that copying Permutation subclasses preserves the subclass."""
    # Make a subclass that doesn't override __init__ to avoid complications
    class MyPermutation(Permutation):
        pass
    
    # Create a subclass instance
    original = MyPermutation([0, 2, 1])
    
    # Create a copy
    copied = original.copy()
    
    # The copied object should also be an instance of MyPermutation, not Permutation
    assert isinstance(copied, MyPermutation), f"Expected MyPermutation, got {type(copied)}"


def test_permutation_subclassing_power():
    """Test that powers of Permutation subclasses work."""
    # Make a subclass that doesn't override __init__ to avoid complications
    class MyPermutation(Permutation):
        pass
    
    # Create a subclass instance
    perm = MyPermutation([0, 2, 1])
    
    # Test power operation (which should return subtype)
    result = perm**2
    
    # The result should be an instance of MyPermutation, not Permutation
    assert isinstance(result, MyPermutation), f"Expected MyPermutation, got {type(result)}"