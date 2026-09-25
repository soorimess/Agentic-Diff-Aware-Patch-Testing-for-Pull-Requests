"""
Test for Permutation subclassing issue.

The bug: Permutation can't be subclassed properly because internal methods
use hardcoded references to Permutation instead of using the class that
called them (cls).
"""
from sympy.combinatorics import Permutation


def test_permutation_subclassing_basic():
    """Test that subclasses of Permutation return instances of the subclass, not Permutation."""
    
    class MyPermutation(Permutation):
        pass

    # This should return a MyPermutation instance, but in the buggy version 
    # it returns a Permutation instance because _af_new uses Basic.__new__(Perm, perm)
    p = MyPermutation([1, 2, 0])
    
    # The result should be an instance of MyPermutation  
    assert isinstance(p, MyPermutation)
    # And it should not be the base Permutation class
    assert type(p) is not Permutation


def test_permutation_subclassing_copy():
    """Test copy constructor maintains subclass type."""
    
    class MyPermutation(Permutation):
        pass
    
    # Create an instance, then use it as source for a copy
    p1 = MyPermutation([1, 2, 0])
    assert isinstance(p1, MyPermutation)
    
    # Copy constructor - make sure it is a proper subclass copy
    p2 = MyPermutation(p1)
    assert isinstance(p2, MyPermutation)
    assert type(p2) is not Permutation
    assert p2.array_form == p1.array_form


def test_permutation_subclassing_operations():
    """Test that operations maintain subclass type."""
    class MyPermutation(Permutation):
        pass
    
    # Test multiplication operations that use _af_new calls in their implementations
    p1 = MyPermutation([1, 2, 0])
    p2 = MyPermutation([2, 0, 1])
    
    # Test binary multiplication
    result = p1 * p2
    assert isinstance(result, MyPermutation)
    assert type(result) is not Permutation
    
    # Test power operation 
    result2 = p1 ** 2
    assert isinstance(result2, MyPermutation)
    assert type(result2) is not Permutation
    
    # Test inverse operation
    result3 = ~p1
    assert isinstance(result3, MyPermutation)
    assert type(result3) is not Permutation