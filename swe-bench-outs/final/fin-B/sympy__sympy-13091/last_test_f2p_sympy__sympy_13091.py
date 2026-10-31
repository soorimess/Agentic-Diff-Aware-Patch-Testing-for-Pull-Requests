"""
Test for the rich comparison protocol fix.
This test ensures that SymPy objects return NotImplemented instead of False
when comparing with unknown types, which allows proper symmetric comparison.
"""

from sympy import Symbol, Float, S, sin, oo, sqrt, I, symbols
from sympy.core.basic import Basic
from sympy.core.exprtools import Factors, Term
from sympy.core.sympify import SympifyError
from sympy.abc import a, b, t, x, y, z


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


def test_factors_ne_delegation():
    """
    Test that Factors.__ne__ properly delegates comparison using the new implementation.
    This tests the change from return not self.__eq__(other) to return not self == other
    """
    # Create Factors instances
    f1 = Factors({x: 2, y: 3})
    f2 = Factors({x: 1, y: 2})
    
    # Test that __ne__ works correctly with the new implementation
    # The old code used: return not self.__eq__(other)  
    # The new code uses: return not self == other
    result = f1.__ne__(f2)
    
    # Should be True since f1 != f2
    assert result is True
    
    # Test with equal factors
    f3 = Factors({x: 2, y: 3})
    result2 = f1.__ne__(f3)
    
    # Should be False since f1 == f3
    assert result2 is False


def test_term_ne_delegation():
    """
    Test that Term.__ne__ properly delegates comparison using the new implementation.
    This tests the change from return not self.__eq__(other) to return not self == other
    """
    # Create Term instances
    t1 = Term(x, y)
    t2 = Term(y, z)
    
    # Test that __ne__ works correctly with the new implementation
    # The old code used: return not self.__eq__(other)  
    # The new code uses: return not self == other
    result = t1.__ne__(t2)
    
    # Should be True since t1 != t2 (different terms)
    assert result is True
    
    # Test with equal terms
    t3 = Term(x, y)
    result2 = t1.__ne__(t3)
    
    # Should be False since t1 == t3
    assert result2 is False


def test_float_eq_returns_not_implemented():
    """
    Test that Float.__eq__ returns NotImplemented when SympifyError is raised,
    not False. This tests the specific change in Float.__eq__ method.
    """
    f = Float('1.5')
    
    # Create an object that will cause SympifyError when passed to _sympify
    class NonSympifiable:
        def __str__(self):
            return "non_sympifiable"
        
        def __sympy__(self):
            raise SympifyError("Cannot sympify this object")
    
    non_sympifiable_obj = NonSympifiable()
    
    # This should return NotImplemented, not False, to allow proper delegation
    result = f.__eq__(non_sympifiable_obj)
    
    # The fix ensures this returns NotImplemented so Python can try the reverse comparison
    assert result is NotImplemented, (
        "Float.__eq__ should return NotImplemented for SympifyError cases, "
        "not False, to enable symmetric comparison with custom objects"
    )


def test_has_matcher_functionality():
    """
    Test that Basic._has_matcher works correctly after the change.
    This tests the specific change from return self.__eq__ to return lambda other: self == other
    """
    # Define basic instances like in test_basic.py
    b1 = Basic()
    b2 = Basic(b1)
    b3 = Basic(b2)
    b21 = Basic(b2, b1)
    
    # Test the _has_matcher function
    matcher = b21._has_matcher()
    
    # The matcher should be callable
    assert callable(matcher)
    
    # Test that it works with matching elements (this tests the changed behavior)
    result1 = matcher(b1)
    assert result1 is True
    
    # Test that it works with non-matching elements
    result2 = matcher(b3)
    assert result2 is False


def test_sympy_objects_have_correct_comparison_behavior():
    """
    Test that SymPy objects properly handle comparison with various types
    to ensure symmetric behavior is maintained.
    """
    x = Symbol('x')
    
    # Test basic equality
    assert x == x
    
    # Test basic inequality
    y = Symbol('y')
    assert x != y
    
    # Test comparison with basic Python types
    assert x != 1
    assert x != []
    assert x != "string"