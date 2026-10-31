"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer


def test_basic_eq_returns_not_implemented_for_unknown_types():
    """Test that Basic.__eq__ returns NotImplemented for unknown types."""
    x = Symbol('x')
    
    # Test that when comparing with an object that's not sympifiable,
    # the comparison returns NotImplemented to allow proper delegation
    # This is the core change: instead of returning False, it should return NotImplemented
    
    # The key behavior change is that when _sympify(other) raises SympifyError,
    # it should return NotImplemented instead of False
    
    # This test directly checks that the behavior change works for the main case
    result = x.__eq__(object())  # object() is not a sympifiable type
    
    # Before the fix: result would be False
    # After the fix: result should be NotImplemented
    # This allows Python's comparison protocol to work properly
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_symmetric_equality_with_custom_classes():
    """Test that equality works symmetrically with custom classes."""
    x = Symbol('x')
    
    # Create a custom class that handles SymPy comparisons
    class CustomComparable:
        def __init__(self, value):
            self.value = value
            
        def __eq__(self, other):
            if isinstance(other, Symbol):
                return self.value == 0
            return NotImplemented
            
        def __ne__(self, other):
            return not self.__eq__(other)
    
    custom_obj = CustomComparable(0)
    
    # Test that both directions work consistently
    # custom_obj == x should call CustomComparable.__eq__
    # x == custom_obj should call Symbol.__eq__ and return NotImplemented
    # which should then allow Python to delegate back to CustomComparable.__eq__
    
    # The important thing is that we're testing that the change allows proper delegation
    # This is a demonstration of the behavior that the fix enables
    eq_result_1 = custom_obj == x
    eq_result_2 = x == custom_obj
    
    # Both should be True (since 0 == 0)
    assert eq_result_1 is True
    assert eq_result_2 is True


def test_comparison_with_sympy_objects_still_works():
    """Test that normal SymPy comparisons still work."""
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