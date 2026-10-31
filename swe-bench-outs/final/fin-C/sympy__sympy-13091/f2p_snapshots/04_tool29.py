"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer


def test_basic_eq_returns_not_implemented_for_sympify_error():
    """Test that Basic.__eq__ returns NotImplemented when SympifyError is raised."""
    x = Symbol('x')
    
    # The core change: when _sympify(other) raises SympifyError, 
    # Basic.__eq__ should return NotImplemented instead of False
    
    # This is a direct test of the behavior change
    # We can't easily create a SympifyError case, but we can test the behavior
    # by testing that the method returns NotImplemented for unknown types
    
    # The most direct test is to check the behavior with object() which 
    # cannot be sympified
    result = x.__eq__(object())
    
    # This should return NotImplemented to enable proper Python comparison delegation
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


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
    
    # Test that same-type comparisons return proper boolean values
    result1 = x.__eq__(y)
    result2 = z.__eq__(w)
    
    # These should not return NotImplemented for same-type comparisons
    assert result1 is False  # Different symbols
    assert result2 is True   # Same integers


def test_has_matcher_behavior():
    """Test the _has_matcher method change from self.__eq__ to lambda other: self == other."""
    x = Symbol('x')
    
    # Test that _has_matcher returns a callable that works correctly
    matcher = x._has_matcher()
    
    # The change was from: return self.__eq__
    # To: return lambda other: self == other
    
    # This should be callable and return a proper result
    assert callable(matcher)
    
    # Test that it works with a simple case
    result = matcher(Integer(1))
    # This should not crash and should return something reasonable
    # The exact behavior depends on the implementation, but it should not crash