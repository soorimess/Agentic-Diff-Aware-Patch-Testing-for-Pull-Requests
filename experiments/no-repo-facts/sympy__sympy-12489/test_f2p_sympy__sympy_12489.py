"""
Test for Permutation subclassing regression.

This test asserts that Permutation subclasses properly return instances 
of the subclass rather than always returning Permutation instances.
"""

from sympy.combinatorics.permutations import Permutation


def test_subclassing_with_size_parameter():
    """
    Test that Permutation subclasses return subclass instances.
    
    This is the primary issue reported: when creating a Permutation subclass 
    with a size parameter, the internal _af_new call would always produce 
    a Permutation instance instead of the subclass instance.
    """
    
    class MyPermutation(Permutation):
        """A simple subclass of Permutation for testing."""
        pass
    
    # Create permutation with size parameter
    perm = MyPermutation(size=3)
    
    # The subclass instance should be returned, not a Permutation
    assert isinstance(perm, MyPermutation), \
        "Subclassed permutation with size should be instance of MyPermutation"


def test_subclassing_basic_functionality():
    """
    Test that basic subclassing functionality still works.
    """
    
    class MyPermutation(Permutation):
        """A simple subclass of Permutation for testing."""
        pass
    
    # Basic constructor should work correctly
    perm = MyPermutation([0, 1, 2])
    
    assert isinstance(perm, MyPermutation), \
        "Basic subclass construction should work"