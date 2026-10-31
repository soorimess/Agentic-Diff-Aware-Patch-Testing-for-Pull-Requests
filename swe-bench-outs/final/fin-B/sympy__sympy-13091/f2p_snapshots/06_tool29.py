"""
Test for the rich comparison protocol fix.
This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, which allows proper symmetric comparison.
"""

from sympy import Symbol
from sympy.core.sympify import SympifyError


def test_sympy_returns_not_implemented_for_unknown_types():
    """
    Test that SymPy objects return NotImplemented when comparing with unknown types
    that cause SympifyError, enabling symmetric comparison with custom classes.
    
    This addresses the issue where:
    - custom_obj == sympy_obj might return True (because custom_obj.__eq__ is called)
    - sympy_obj == custom_obj might return False (because sympy_obj.__eq__ returns False)
    - This creates an asymmetric equivalence relation
    
    With the fix, sympy_obj.__eq__(custom_obj) should return NotImplemented
    so that Python can delegate to custom_obj.__eq__(sympy_obj) properly.
    """
    x = Symbol('x')
    
    # Create a custom class that implements __eq__ to work with SymPy objects
    class Foo:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            # This should be called when comparing with SymPy objects
            if hasattr(other, 'name') and other.name == 'x':
                return True
            return False
    
    foo_obj = Foo('x')
    
    # Test the key behavior change:
    # Before fix: x.__eq__(foo_obj) returns False (which breaks symmetry)
    # After fix: x.__eq__(foo_obj) returns NotImplemented (which enables delegation)
    
    result = x.__eq__(foo_obj)
    
    # The fix ensures this returns NotImplemented so Python can try the reverse comparison
    assert result is NotImplemented, (
        "SymPy objects should return NotImplemented for unknown types to enable "
        "symmetric comparison with custom classes"
    )
    
    # Test that the reverse comparison works correctly
    result_reverse = foo_obj.__eq__(x)
    assert result_reverse is True, (
        "Custom class should properly compare with SymPy objects"
    )


def test_sympy_returns_not_implemented_for_sympify_error():
    """
    Test that SymPy objects return NotImplemented when SympifyError is raised,
    not False. This is the core change in the PR.
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