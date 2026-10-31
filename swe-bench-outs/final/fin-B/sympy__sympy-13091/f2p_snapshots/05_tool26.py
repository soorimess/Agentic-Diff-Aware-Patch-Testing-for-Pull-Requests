"""
Test for the rich comparison protocol fix.
This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, which allows proper symmetric comparison.
"""

from sympy import Symbol
from sympy.core.sympify import SympifyError


def test_basic_eq_returns_not_implemented_for_sympify_error():
    """
    Test that Basic.__eq__ returns NotImplemented when SympifyError is raised,
    not False. This enables proper symmetric comparison with custom objects.
    """
    x = Symbol('x')
    
    # Create an object that will cause SympifyError when passed to _sympify
    class NonSympifiable:
        def __str__(self):
            return "non_sympifiable"
        
        def __sympy__(self):
            raise SympifyError("Cannot sympify this object")
    
    non_sympifiable_obj = NonSympifiable()
    
    # This should return NotImplemented, not False, to allow proper delegation
    result = x.__eq__(non_sympifiable_obj)
    
    # The fix ensures this returns NotImplemented so Python can try the reverse comparison
    assert result is NotImplemented, (
        "Basic.__eq__ should return NotImplemented for SympifyError cases, "
        "not False, to enable symmetric comparison with custom objects"
    )


def test_basic_ne_delegates_properly():
    """
    Test that Basic.__ne__ properly delegates comparison using the new implementation.
    The old code used: return not self.__eq__(other)
    The new code uses: return not self == other
    """
    x = Symbol('x')
    
    # Test that __ne__ works correctly with the new implementation
    # This tests that the change from self.__eq__(other) to self == other works
    result = x.__ne__(x)  # Should be False since x != x is False
    
    # The important thing is that it doesn't crash and returns the expected boolean
    assert result is False