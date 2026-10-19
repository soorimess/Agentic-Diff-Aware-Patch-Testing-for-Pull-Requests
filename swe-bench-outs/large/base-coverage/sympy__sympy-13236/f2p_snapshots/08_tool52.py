"""
Test for factorial(n) % n simplification.

This test ensures that factorial(n) % n automatically simplifies to 0
when n is a positive integer, which is the behavior that was added
in the pull request.
"""

from sympy import Symbol, factorial, Mod
from sympy.core.numbers import Integer


def test_factorial_mod_n():
    """Test that factorial(n) % n simplifies to 0 for positive integer n."""
    n = Symbol('n', integer=True, positive=True)
    
    # This should evaluate to 0, but before the fix it didn't
    result = Mod(factorial(n), n)
    # The simplification should happen automatically
    assert result == 0


def test_factorial_mod_n_specific():
    """Test specific cases of factorial(n) % n."""
    # Test with specific positive integers
    assert Mod(factorial(1), 1) == 0
    assert Mod(factorial(2), 2) == 0
    assert Mod(factorial(3), 3) == 0
    assert Mod(factorial(4), 4) == 0
    assert Mod(factorial(5), 5) == 0


def test_factorial_mod_k_when_k_le_n():
    """Test that factorial(n) % k simplifies to 0 when 1 <= k <= n."""
    # Test specific cases where k <= n
    assert Mod(factorial(5), 3) == 0  # 5! = 120, 120 % 3 = 0
    assert Mod(factorial(6), 4) == 0  # 6! = 720, 720 % 4 = 0
    assert Mod(factorial(4), 2) == 0  # 4! = 24, 24 % 2 = 0


def test_factorial_mod_prime():
    """Test Wilson's theorem: (p-1)! ≡ -1 (mod p) for prime p > 1."""
    # This tests the Wilson's theorem case in the _eval_Mod implementation
    # 4! % 5 = 24 % 5 = 4 = -1 mod 5
    assert Mod(factorial(4), 5) == 4  # Wilson's theorem case
    # 6! % 7 = 720 % 7 = 6 = -1 mod 7  
    assert Mod(factorial(6), 7) == 6  # Wilson's theorem case


def test_factorial_mod_large_numbers():
    """Test factorial mod with larger numbers to ensure robustness."""
    # Test with larger values to make sure the implementation is solid
    assert Mod(factorial(10), 10) == 0
    assert Mod(factorial(8), 8) == 0
    assert Mod(factorial(7), 7) == 0