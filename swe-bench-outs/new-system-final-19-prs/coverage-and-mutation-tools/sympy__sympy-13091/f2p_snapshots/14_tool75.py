"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer, S
from sympy.core.exprtools import Factors


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


def test_factors_ne_behavior():
    """Test the Factors.__ne__ method change."""
    # Copy setup from test_Factors
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')
    t = Symbol('t')
    
    # Create some Factors objects
    a = Factors({x: 5, y: 3, z: 7})
    b = Factors({y: 4, z: 3, t: 10})
    
    # Test that __ne__ works correctly (the change was to use `not self == other` instead of `not self.__eq__(other)`)
    # This tests the specific change in the diff for Factors.__ne__
    result1 = a.__ne__(b)
    result2 = a != b
    
    # Both should give the same result
    assert result1 == result2
    
    # Test with equal factors
    c = Factors({x: 5, y: 3, z: 7})
    result3 = a.__ne__(c)
    result4 = a != c
    
    # Should be False for equal factors
    assert result3 == result4
    assert result3 is False
    
    # Test that the behavior is consistent with the change
    # The change was from: return not self.__eq__(other)
    # To: return not self == other
    # Both should produce the same result
    assert (a != b) == (not (a == b))
    assert (a != c) == (not (a == c))