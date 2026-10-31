"""
Test for the rich comparison protocol fix.
This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, which allows proper symmetric comparison.
"""

from sympy import Symbol
from sympy.core.basic import Basic
from sympy.core.sympify import SympifyError


def test_basic_eq_returns_not_implemented_for_sympify_error():
    """
    Test that Basic.__eq__ returns NotImplemented when SympifyError is raised,
    not False. This is the core fix for symmetric comparison.
    
    The issue was that when comparing with unknown types, SymPy objects would
    return False instead of NotImplemented, breaking symmetric comparison.
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
    # Test with basic instances
    b1 = Basic()
    b2 = Basic(b1)
    
    # Test that __ne__ works correctly with the new implementation
    # This tests the change from self.__eq__(other) to self == other in __ne__
    result = b1.__ne__(b1)  # Should be False since b1 != b1 is False
    
    # The important thing is that it doesn't crash and returns the expected boolean
    assert result is False
    
    # Test with different instances
    result2 = b1.__ne__(b2)  # Should be True since b1 != b2 is True
    assert result2 is True


def test_has_matcher_function():
    """
    Test that Basic._has_matcher returns a function that works correctly.
    This tests the change from return self.__eq__ to return lambda other: self == other
    """
    x = Symbol('x')
    
    # Test that _has_matcher returns a callable function
    matcher = x._has_matcher()
    
    # The matcher should be callable
    assert callable(matcher)
    
    # Test that it works with the same object (should return True)
    result = matcher(x)
    assert result is True
    
    # Test that it works with a different object (should return False)
    y = Symbol('y')
    result2 = matcher(y)
    assert result2 is False