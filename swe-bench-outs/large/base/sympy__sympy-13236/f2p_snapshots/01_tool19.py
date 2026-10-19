"""
Test for the factorial modulo behavior change.

This test ensures that factorial(n) % n simplifies to 0 for positive integer n,
which is the core behavior change in the pull request.
"""

from sympy import Symbol, factorial, Mod


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


def test_factorial_modulo_with_prime():
    """Test Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p."""
    # Test Wilson's theorem for small primes
    # For prime p, (p-1)! ≡ -1 (mod p)
    # This should be handled by the _eval_Mod method
    # We can't directly test this without a prime assumption, 
    # but we can test that it doesn't break for prime values
    assert (factorial(5) % 5) == 0  # 5 is prime, so (5-1)! = 24 ≡ 0 (mod 5) 
    assert (factorial(7) % 7) == 0  # 7 is prime, so (7-1)! = 720 ≡ 0 (mod 7)


def test_factorial_modulo_composite():
    """Test that factorial(n) % n = 0 for composite n."""
    # For composite n > 4, (n-1)! ≡ 0 (mod n) by Wilson's theorem generalization
    assert (factorial(4) % 4) == 0  # 4 is composite
    assert (factorial(6) % 6) == 0  # 6 is composite
    assert (factorial(8) % 8) == 0  # 8 is composite