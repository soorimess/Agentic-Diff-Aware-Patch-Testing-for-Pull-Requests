"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer, Basic


def test_basic_eq_returns_not_implemented_for_unknown_types():
    """Test that Basic.__eq__ returns NotImplemented when SympifyError would be raised."""
    x = Symbol('x')
    
    # The core change: when _sympify(other) raises SympifyError, 
    # Basic.__eq__ should return NotImplemented instead of False
    
    # This test directly checks the behavior change
    # When comparing with an object that cannot be sympified, 
    # the comparison should return NotImplemented to allow Python's delegation
    result = x.__eq__(object())  # object() cannot be sympified
    
    # This should return NotImplemented to enable proper Python comparison delegation
    # This is the key behavior change that was requested
    assert result is NotImplemented, f"Expected NotImplemented, got {result}"


def test_comparison_with_sympy_objects_still_works():
    """Test that normal SymPy comparisons still work normally."""
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
    # Copy setup from test_basic.py
    b1 = Basic()
    b2 = Basic(b1)
    b3 = Basic(b2)
    b21 = Basic(b2, b1)
    
    # Test the _has_matcher functionality
    matcher = b21._has_matcher()
    
    # The change was from: return self.__eq__
    # To: return lambda other: self == other
    
    # Verify that the matcher is callable and works as expected
    assert callable(matcher)
    
    # Test that it works with a basic case - should return True for matching subexpression
    result = matcher(b1)
    # This should return a boolean value (True or False) without raising an exception
    assert isinstance(result, (bool, type(True)))
    
    # Test that it works with a non-matching case
    result2 = matcher(b21)  # Should match itself
    assert isinstance(result2, (bool, type(True)))