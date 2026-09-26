"""Test for Product bug regression."""

from sympy import Product
from sympy.abc import n, k


def test_product_n2():
    """Test that Product(n + 1/2**k, [k, 0, n-1]) for n=2 gives 15/2."""
    # Bug: was returning 9/2 instead of 15/2
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result = p.subs(n, 2)
    assert result == 15/2