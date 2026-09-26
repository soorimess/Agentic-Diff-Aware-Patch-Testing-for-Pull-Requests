"""
Regression test for Product(n + 1/2^k, [k, 0, n-1]) bug.

This test ensures that Product(n + 1/2^k, [k, 0, n-1]) computes correctly.
For n=2, it should be (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2, not 9/2.
"""

from sympy import Product
from sympy.abc import n, k

def test_product_n_plus_half_power_bug():
    """Test that Product(n + 1/2^k, [k, 0, n-1]) gives correct result."""
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result = p.subs(n, 2)
    assert result == 15/2, f"Expected 15/2, got {result}"