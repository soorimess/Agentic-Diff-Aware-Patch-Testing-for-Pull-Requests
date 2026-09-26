"""
Test for Permutation subclassing issue.
This test verifies that Permutation subclasses return instances of the correct type.

Bug: combinatorics.Permutation can't be subclassed properly
The object creation is done in Permutation.__new__, but internally the function 
_af_new is used (which itself is a reference to the static method Permutation._af_new). 
This method eventually creates the object calling Basic.__new__(Perm, perm) which 
hardcodes the Permutation class, making subclassing impossible.

This test ensures that subclasses of Permutation properly create instances of 
the subclass type rather than Permutation type.
"""

from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import Cycle


class MyPermutation(Permutation):
    """A simple subclass of Permutation for testing."""
    pass


def test_permutation_subclassing_basic():
    """Test that Permutation subclasses create instances of the correct type."""
    # Basic instantiation from list
    p1 = MyPermutation([0, 1, 2])
    assert isinstance(p1, MyPermutation), f"Expected MyPermutation, got {type(p1)}"


def test_permutation_subclassing_with_cycle():
    """Test that Permutation subclasses work with Cycle objects."""
    # Test with Cycle - this goes through __new__ which calls _af_new
    c = Cycle(0, 1)
    p3 = MyPermutation(c)
    assert isinstance(p3, MyPermutation), f"Expected MyPermutation, got {type(p3)}"


def test_af_new_directly():
    """Test that _af_new method respects subclass type."""
    # This is the core of the bug - _af_new should create instances of the calling class
    p = MyPermutation._af_new([0, 1, 2])
    assert isinstance(p, MyPermutation), f"Expected MyPermutation from _af_new, got {type(p)}"


def test_permutation_operations_preserve_type():
    """Test that operations preserve subclass type."""
    # Operations between subclasses should return subclass instances
    p1 = MyPermutation([1, 0, 2])
    p2 = MyPermutation([0, 2, 1])
    result = p1 * p2
    assert isinstance(result, MyPermutation), f"Expected MyPermutation from multiplication, got {type(result)}"


def test_permutation_subclassing_empty():
    """Test empty permutation instantiation."""
    p = MyPermutation()
    assert isinstance(p, MyPermutation), f"Expected MyPermutation, got {type(p)}"


def test_permutation_subclassing_integer():
    """Test permutation instantiation with integer (identity)."""
    p = MyPermutation(3)
    assert isinstance(p, MyPermutation), f"Expected MyPermutation, got {type(p)}"


if __name__ == "__main__":
    test_permutation_subclassing_basic()
    test_permutation_subclassing_with_cycle()
    test_af_new_directly()
    test_permutation_operations_preserve_type()
    test_permutation_subclassing_empty()
    test_permutation_subclassing_integer()
    print("All tests passed!")