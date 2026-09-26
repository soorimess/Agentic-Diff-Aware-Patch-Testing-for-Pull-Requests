"""Test for regression of Product(n + 1/2**k, [k, 0, n-1]) bug"""

from sympy import Product
from sympy.abc import n, k


def test_product_bug_fix():
    """
    Regression test for Product(n + 1/2**k, [k, 0, n-1]) bug.
    
    The bug was that the _eval_product method incorrectly applied 
    distributive property to products, computing:
    Product(k=0 to n-1) of (n + 1/2^k) = n^n + 2^(-n(n-1)/2)
    
    This gave 9/2 for n=2 instead of the correct 15/2.
    """
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result = p.subs(n, 2)
    # Correct result should be 15/2
    assert result == 15/2