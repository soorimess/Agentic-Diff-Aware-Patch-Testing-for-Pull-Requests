"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer, S
from sympy.core.exprtools import Factors, Term


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


def test_term_ne_behavior():
    """Test the Term.__ne__ method change."""
    # Create some Term objects
    x = Symbol('x')
    y = Symbol('y')
    
    # Create Term objects
    term1 = Term(x)
    term2 = Term(y)
    
    # Test that __ne__ works correctly (the change was to use `not self == other` instead of `not self.__eq__(other)`)
    # This tests the specific change in the diff for Term.__ne__
    result1 = term1.__ne__(term2)
    result2 = term1 != term2
    
    # Both should give the same result
    assert result1 == result2
    
    # Test with equal terms
    term3 = Term(x)
    result3 = term1.__ne__(term3)
    result4 = term1 != term3
    
    # Should be False for equal terms
    assert result3 == result4
    assert result3 is False
    
    # Test that the behavior is consistent with the change
    # The change was from: return not self.__eq__(other)
    # To: return not self == other
    # Both should produce the same result
    assert (term1 != term2) == (not (term1 == term2))
    assert (term1 != term3) == (not (term1 == term3))