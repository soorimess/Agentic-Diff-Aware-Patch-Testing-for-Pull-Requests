"""
Regression test for Permutation subclassing issue.

The bug was that Permutation.__new__ internally called _af_new (a static method)
which always created instances of the base Permutation class, not the subclass.
This meant that when subclassing Permutation, all returned instances were of type
Permutation, not the subclass.
"""

from sympy.combinatorics.permutations import Permutation


def test_permutation_subclassing_preserves_type():
    """Test that Permutation subclasses maintain their type."""
    
    # Create a subclass of Permutation
    class MyPermutation(Permutation):
        pass
    
    # Create an instance - this should return MyPermutation, not Permutation
    p = MyPermutation([0, 1, 2])
    
    # This assertion should pass after the fix, fail before the fix
    assert type(p) == MyPermutation, f"Expected MyPermutation, got {type(p)}"
    
    # Test that operations also preserve type
    p2 = MyPermutation([1, 0, 2])
    p3 = MyPermutation([2, 1, 0])
    
    # Multiplication should preserve type
    result = p2 * p3
    assert type(result) == MyPermutation, f"Expected MyPermutation, got {type(result)}"


def test_permutation_subclassing_with_operations():
    """Test that Permutation subclassing works with operations."""
    
    class SpecialPermutation(Permutation):
        def __new__(cls, *args, **kwargs):
            instance = super().__new__(cls, *args, **kwargs)
            instance.is_special = True
            return instance
    
    # Create instance and verify type
    sp = SpecialPermutation([0, 2, 1])
    assert type(sp) == SpecialPermutation
    assert sp.is_special is True
    
    # Operations should preserve type
    sp2 = SpecialPermutation([1, 0, 2])
    result = sp * sp2
    assert type(result) == SpecialPermutation