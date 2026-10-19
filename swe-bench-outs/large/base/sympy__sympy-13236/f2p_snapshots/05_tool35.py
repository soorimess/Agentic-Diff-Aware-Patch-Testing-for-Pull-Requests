"""
Test for the factorial modulo behavior change.

This test ensures that factorial(n) % n simplifies to 0 for positive integer n,
which is the core behavior change in the pull request.
"""

from sympy import Symbol, factorial, Integer, Pow, Mod


def test_factorial_modulo_simplification():
    """Test that factorial(n) % n simplifies to 0 for positive integer n."""
    n = Symbol('n', integer=True, positive=True)
    
    # This should simplify to 0 for positive integer n
    result = factorial(n) % n
    # The result should be 0, not Mod(factorial(n), n)
    # This is the main behavior change that the PR addresses
    assert result == 0


def test_factorial_modulo_specific_values():
    """Test that factorial(n) % n equals 0 for specific positive integer values."""
    # Test with specific values
    assert (factorial(3) % 3) == 0
    assert (factorial(4) % 4) == 0
    assert (factorial(5) % 5) == 0
    assert (factorial(6) % 6) == 0


def test_factorial_modulo_prime_wilson():
    """Test Wilson's theorem behavior."""
    # For prime p, (p-1)! ≡ -1 (mod p) 
    # But factorial(p) % p should be 0 because p! = p * (p-1)!
    # The key point is that factorial(n) % n = 0 for any positive integer n >= 2
    assert (factorial(5) % 5) == 0  # 5 is prime, 5! = 120, 120 % 5 = 0
    assert (factorial(7) % 7) == 0  # 7 is prime, 7! = 5040, 5040 % 7 = 0


def test_factorial_modulo_composite():
    """Test that factorial(n) % n = 0 for composite n."""
    # For composite n > 4, (n-1)! ≡ 0 (mod n) by Wilson's theorem generalization
    assert (factorial(4) % 4) == 0  # 4 is composite
    assert (factorial(6) % 6) == 0  # 6 is composite
    assert (factorial(8) % 8) == 0  # 8 is composite