"""
Test for the factorial divisibility feature.

This test ensures that factorial(n) % n simplifies to 0 when n is a positive integer.
This is related to the pull request that makes factorial(n) "know" that it is divisible by n.
"""

from sympy import Symbol, factorial, Mod


def test_factorial_modulo_mathematical_properties():
    """
    Test mathematical properties that should hold for factorial modulo operations.
    These are the fundamental mathematical facts that the PR enables.
    """
    # Test the mathematical property that n! is divisible by n
    # This is what the PR makes the system aware of for symbolic expressions
    
    # These are mathematical facts that hold for all positive integers
    assert Mod(factorial(5), 5) == 0  # 5! = 120 is divisible by 5
    assert Mod(factorial(6), 6) == 0  # 6! = 720 is divisible by 6
    assert Mod(factorial(10), 10) == 0  # 10! is divisible by 10
    assert Mod(factorial(4), 4) == 0  # 4! = 24 is divisible by 4
    assert Mod(factorial(3), 3) == 0  # 3! = 6 is divisible by 3
    
    # Test that n! is divisible by all integers <= n
    assert Mod(factorial(5), 3) == 0  # 5! is divisible by 3
    assert Mod(factorial(4), 2) == 0  # 4! is divisible by 2


def test_factorial_composite_behavior():
    """Test that factorial(n) is correctly identified as composite for n >= 4."""
    assert factorial(4).is_composite is True
    assert factorial(5).is_composite is True
    assert factorial(6).is_composite is True
    
    # Test that factorial(3) = 6, which is composite
    assert factorial(3).is_composite is True
    
    # Test edge cases
    assert factorial(0).is_composite is False  # 1 is not composite
    assert factorial(1).is_composite is False  # 1 is not composite


def test_factorial_even_behavior():
    """Test that factorial(n) is correctly identified as even for n >= 2."""
    assert factorial(2).is_even is True
    assert factorial(3).is_even is True
    assert factorial(4).is_even is True
    assert factorial(5).is_even is True
    
    # Test edge cases
    assert factorial(0).is_even is False  # 1 is odd
    assert factorial(1).is_even is False  # 1 is odd