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


def test_has_matcher_function():
    """
    Test that Basic._has_matcher returns a function that uses proper comparison.
    """
    x = Symbol('x')
    
    # Test that _has_matcher returns a callable that works correctly
    matcher = x._has_matcher()
    
    # The matcher should be callable
    assert callable(matcher)
    
    # Test that it works with a simple case
    # This tests the change from return self.__eq__ to return lambda other: self == other
    result = matcher(x)  # Should return True when comparing with self
    
    # This test is more about ensuring the function exists and is callable
    # The real test is in the first function above