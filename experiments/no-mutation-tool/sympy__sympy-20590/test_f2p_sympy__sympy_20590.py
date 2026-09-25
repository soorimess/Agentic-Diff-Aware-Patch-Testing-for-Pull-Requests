"""
Regression test for Symbol __dict__ behavior.

The pull request modification adds __slots__ = () to the Printable class,
which fixes a bug where Symbol instances gained __dict__ (an unwanted behavior).

This regression test ensures that the fix works properly.
"""

from sympy import Symbol


def test_printable_has_empty_slots():
    """
    Test that Printable class defines __slots__ = () to fix Symbol __dict__ bug.
    
    Before the fix, Symbol instances incorrectly gained the ability to have __dict__
    attributes, which violated the intended __slots__ inheritance behavior.
    
    This test ensures the fix is in place by confirming that Printable now has
    an empty __slots__ tuple.
    """
    from sympy.core._print_helpers import Printable
    
    # The fix was adding __slots__ = () to Printable class
    # This prevents Symbol instances from having __dict__ attribute where they shouldn't
    assert hasattr(Printable, '__slots__')
    assert Printable.__slots__ == (), "Printable should now have empty slots to prevent inappropriate dict creation"
    
    # Verify this affects Symbol behavior appropriately in the inheritance chain
    s = Symbol('test')
    # Symbol should still be able to access __slots__ properly to demonstrate
    # that slots inheritance is working correctly
    assert s.__slots__ == ('name',)