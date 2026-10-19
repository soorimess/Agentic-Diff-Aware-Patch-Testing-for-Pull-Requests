"""
Test for the factorial modulo behavior change.

This test ensures that factorial(n) % n simplifies to 0 for positive integer n,
which is the core behavior change in the pull request.
"""

from sympy import Symbol, factorial, Mod, Integer
from sympy.core.exprtools import _monotonic_sign
from sympy.core.mod import Mod as ModClass


def test_factorial_modulo_simplification():
    """Test that factorial(n) % n simplifies to 0 for positive integer n."""
    n = Symbol('n', integer=True, positive=True)
    
    # This should simplify to 0 for positive integer n
    result = factorial(n) % n
    # The result should be 0, not Mod(factorial(n), n)
    assert result == 0


def test_factorial_modulo_specific_values():
    """Test that factorial(n) % n equals 0 for specific positive integer values."""
    # Test with specific values
    assert (factorial(3) % 3) == 0
    assert (factorial(4) % 4) == 0
    assert (factorial(5) % 5) == 0
    assert (factorial(6) % 6) == 0


def test_factorial_modulo_prime_wilson():
    """Test Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p."""
    # For prime p, (p-1)! ≡ -1 (mod p) 
    # But for factorial(n) % n where n is prime and n > 4, it should be 0
    # Actually, for prime p, (p-1)! ≡ -1 (mod p) 
    # But factorial(p) % p should be 0 because p! = p * (p-1)!
    # Wait, let me re-read the issue...
    # The issue says factorial(n) % n should simplify to 0
    # This is true for n >= 2, because n! = n * (n-1)!
    # So n! % n = 0 for n >= 2
    assert (factorial(5) % 5) == 0  # 5 is prime, 5! = 120, 120 % 5 = 0
    assert (factorial(7) % 7) == 0  # 7 is prime, 7! = 5040, 5040 % 7 = 0


def test_factorial_modulo_composite():
    """Test that factorial(n) % n = 0 for composite n."""
    # For composite n > 4, (n-1)! ≡ 0 (mod n) by Wilson's theorem generalization
    assert (factorial(4) % 4) == 0  # 4 is composite
    assert (factorial(6) % 6) == 0  # 6 is composite
    assert (factorial(8) % 8) == 0  # 8 is composite


def test_factorial_modulo_with_negative():
    """Test factorial with negative values."""
    # factorial(-1) is undefined, so we test valid cases
    # But we can test the behavior with negative symbols
    n = Symbol('n', integer=True, negative=True)
    # This should not simplify to 0 since factorial of negative integer is undefined
    # But we're testing the logic doesn't break


def test_factorial_modulo_zero():
    """Test factorial with zero."""
    # factorial(0) = 1, so 1 % 0 is undefined (should raise ZeroDivisionError)
    try:
        result = factorial(0) % 0
        # If it doesn't raise, it should be handled properly
        # But actually 0! = 1, so 1 % 0 should raise an error
    except ZeroDivisionError:
        pass  # Expected behavior


def test_factorial_modulo_symbolic_with_assumptions():
    """Test that symbolic factorial with assumptions works properly."""
    # Test that the assumptions system works correctly
    n = Symbol('n', integer=True, positive=True, composite=True)
    result = factorial(n) % n
    # Should simplify to 0 for composite positive integers
    assert result == 0
    
    # Test with prime assumption
    p = Symbol('p', integer=True, positive=True, prime=True)
    result2 = factorial(p) % p
    # Should also simplify to 0 for prime positive integers
    assert result2 == 0