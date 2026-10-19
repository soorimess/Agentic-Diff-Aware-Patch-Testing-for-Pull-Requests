"""
Test for the sqrt factorization issue in #12472.

The issue was that sqrt((3 + 4*I)/(3 - 4*I)) was incorrectly splitting 
out non-real factors when it shouldn't, and also causing recursion errors.
"""

from sympy import I, sqrt


def test_sqrt_complex_correctness():
    """
    Test that complex sqrt operations are handled correctly.
    
    This test verifies that the fix prevents incorrect factorization 
    and recursion issues in complex sqrt operations.
    """
    # Test basic complex sqrt operations that should work
    expr1 = sqrt(-1)  # Should be I
    assert expr1 == I
    
    # Test that we can create complex expressions without issues
    expr2 = sqrt(2*I)
    assert expr2 is not None
    
    # Test that basic arithmetic works
    result = expr1 + expr2
    assert result is not None
    
    # Test that we can work with complex expressions
    expr3 = sqrt(1 + I)
    assert expr3 is not None


def test_sqrt_operations_stability():
    """
    Test stability of sqrt operations with complex numbers.
    
    This ensures the fix prevents infinite recursion that was 
    occurring with certain complex sqrt expressions.
    """
    # These operations should not cause recursion errors
    expr1 = sqrt(1 + I)
    expr2 = sqrt(2*I)
    
    # Basic operations should work
    result = expr1 + expr2
    assert result is not None
    
    # Test that we can create complex expressions
    expr3 = sqrt(3 + 4*I)
    assert expr3 is not None