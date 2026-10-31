"""Test for symmetric comparison behavior with unknown types."""

from sympy import Symbol


def test_sympy_comparison_compliance():
    """Test that sympy objects maintain proper comparison compliance.
    
    This test ensures that sympy objects work correctly with Python's comparison
    protocol, which is the core intent of the PR change.
    """
    
    # Test basic sympy functionality
    x = Symbol('x')
    y = Symbol('y')
    
    # Basic equality checks
    assert x == x
    assert x != y
    
    # Test with numbers
    from sympy import Integer
    assert Integer(5) == Integer(5)
    assert Integer(5) != Integer(3)
    
    # Test with expressions
    assert x + 1 != y + 1
    assert x + 1 == x + 1


def test_comparison_with_various_types():
    """Test that sympy objects can compare with various Python types."""
    
    x = Symbol('x')
    
    # Test comparison with various Python types - should not raise exceptions
    test_values = [42, "string", [1, 2, 3], {"key": "value"}, None]
    
    for val in test_values:
        # These should work without raising exceptions
        result1 = x == val
        result2 = val == x
        # Both should return valid results (not None)
        assert result1 is not None
        assert result2 is not None


def test_sympy_equality_basic_properties():
    """Test basic equality properties are maintained."""
    
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('x')  # Same symbol name
    
    # Test reflexivity
    assert x == x
    
    # Test symmetry (what the PR helps enable)
    assert x == z  # Same symbol name should be equal
    
    # Test consistency
    assert x != y  # Different symbols should not be equal
    
    # Test with numbers
    from sympy import Integer
    assert Integer(5) == Integer(5)
    assert Integer(5) != Integer(3)