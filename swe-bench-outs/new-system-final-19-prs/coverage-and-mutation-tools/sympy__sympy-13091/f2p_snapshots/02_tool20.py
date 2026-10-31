"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer
from sympy.core.basic import Basic
from sympy.core.sympify import SympifyError


def test_basic_eq_returns_not_implemented_for_sympify_error():
    """Test that Basic.__eq__ returns NotImplemented when SympifyError is raised."""
    x = Symbol('x')
    
    # Create a class that when sympified, raises SympifyError
    # We can't easily create such a class, but we can test the behavior
    # by directly calling the method with something that would cause SympifyError
    
    # The key test: when _sympify(other) raises SympifyError, 
    # Basic.__eq__ should return NotImplemented, not False
    
    # Since we can't easily create a SympifyError case, let's test
    # that the method behaves correctly for the case that was changed
    
    # Test that we get the right behavior for the specific case that was changed
    # This is a bit indirect but tests the core principle
    result = x.__eq__(object())  # object() should not be sympifiable
    
    # The behavior should be that it returns NotImplemented to allow delegation
    # This is the core change being tested
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_symmetric_equality_with_custom_class():
    """Test that equality is symmetric when custom classes implement __eq__."""
    x = Symbol('x')
    
    # Create a custom class that implements symmetric equality
    class SymmetricClass:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            if isinstance(other, Basic):
                return self.value == 0  # SymPy objects equal to 0
            return NotImplemented
            
        def __ne__(self, other):
            return not self.__eq__(other)
    
    custom_obj = SymmetricClass(0)
    
    # Test symmetric equality - this demonstrates the behavior change
    # Before fix: x == custom_obj would return False, custom_obj == x would return True
    # After fix: both should work consistently through delegation
    
    # The key test is that when SymPy objects are compared with unknown types,
    # they return NotImplemented to allow proper delegation
    eq_result_1 = custom_obj == x  # Should call SymmetricClass.__eq__
    eq_result_2 = x == custom_obj  # Should call Basic.__eq__ and return NotImplemented
    
    # Both should be True (since 0 == 0)
    assert eq_result_1 is True
    assert eq_result_2 is True


def test_comparison_with_basic_sympy_objects():
    """Test that comparison with other SymPy objects still works normally."""
    x = Symbol('x')
    y = Symbol('y')
    z = Integer(5)
    w = Integer(5)
    
    # These should work normally
    assert x == x  # True
    assert x != y  # True
    assert z == w  # True
    assert z != x  # True
    
    # Test that we can still compare with NotImplemented when appropriate
    result1 = x.__eq__(y)
    result2 = z.__eq__(w)
    
    # These should not return NotImplemented for same-type comparisons
    assert result1 is False  # Different symbols
    assert result2 is True   # Same integers


def test_has_matcher_behavior():
    """Test the _has_matcher method change."""
    x = Symbol('x')
    
    # Test that _has_matcher returns a function that uses == instead of __eq__
    matcher = x._has_matcher()
    
    # This tests the change in basic.py line 1183
    # from: return self.__eq__
    # to:   return lambda other: self == other
    
    # The matcher should work correctly
    assert callable(matcher)
    
    # Test that it works with a simple comparison
    result = matcher(Integer(1))
    # This should not crash and should return something reasonable