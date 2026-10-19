"""
Test for factorial(n) % n simplification.

This test ensures that factorial(n) % n automatically simplifies to 0
when n is a positive integer, which is the behavior that was added
in the pull request.
"""

from sympy import Symbol, factorial, Mod


def test_factorial_mod_n_simplifies_to_zero():
    """Test that factorial(n) % n simplifies to 0 for positive integer n."""
    n = Symbol('n', integer=True, positive=True)
    
    # The main behavior: factorial(n) % n should simplify to 0
    # This was the core issue that was fixed in the pull request
    result = Mod(factorial(n), n)
    assert result == 0


def test_factorial_mod_specific_cases():
    """Test specific factorial mod cases that should work."""
    # Test with specific positive integers
    assert Mod(factorial(1), 1) == 0
    assert Mod(factorial(2), 2) == 0
    assert Mod(factorial(3), 3) == 0
    assert Mod(factorial(4), 4) == 0
    assert Mod(factorial(5), 5) == 0


def test_factorial_mod_divisibility():
    """Test that factorial(n) is divisible by k when 1 <= k <= n."""
    # Test that factorial(n) % k == 0 when k <= n
    assert Mod(factorial(5), 3) == 0  # 5! = 120, 120 % 3 = 0
    assert Mod(factorial(6), 4) == 0  # 6! = 720, 720 % 4 = 0


def test_wilson_theorem():
    """Test Wilson's theorem cases that should NOT simplify to 0."""
    # Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p > 1
    # These should NOT be 0, but should be the Wilson theorem values
    assert Mod(factorial(4), 5) == 4  # 4! % 5 = 24 % 5 = 4 = -1 mod 5
    assert Mod(factorial(6), 7) == 6  # 6! % 7 = 720 % 7 = 6 = -1 mod 7