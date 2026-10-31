"""
Test for the fix that makes comparison methods return NotImplemented
instead of False when dealing with unknown types.

This ensures symmetric equality relations when custom classes
implement comparison methods that work with SymPy objects.
"""

from sympy import Symbol, Integer, Float


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


def test_float_eq_behavior():
    """Test the Float.__eq__ method change."""
    # Create Float objects
    f1 = Float('1.5')
    f2 = Float('2.0')
    f3 = Float('1.5')
    
    # Test normal Float comparisons
    assert f1 == f3  # Should be True
    assert f1 != f2  # Should be True
    
    # Test that the behavior is consistent with the change
    # The change was to return NotImplemented instead of False when SympifyError occurs
    # This test verifies that Float comparisons work correctly
    result1 = f1.__eq__(f3)
    result2 = f1 == f3
    
    assert result1 == result2
    assert result1 is True
    
    result3 = f1.__eq__(f2)
    result4 = f1 == f2
    
    assert result3 == result4
    assert result3 is False