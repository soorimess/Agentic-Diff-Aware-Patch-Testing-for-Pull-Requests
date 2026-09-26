from sympy import Product, S
from sympy.abc import n, k

def test_product_bug():
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result = p.subs(n, 2)
    assert result == S(15)/2