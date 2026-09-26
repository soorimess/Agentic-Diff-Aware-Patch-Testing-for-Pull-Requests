"""Test for the Product(n + 1 / 2**k, [k, 0, n-1]) bug."""

from sympy import Product
from sympy.abc import n, k

def test_product_bug():
    # Test the specific case from the bug report
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # For n=2, the product should be:
    # (2 + 1/2^0) * (2 + 1/2^1) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    result_n2 = p.subs(n, 2)
    
    # The buggy behavior gives 9/2 instead of 15/2
    # This test should pass with the fixed version and fail with the old version
    assert result_n2 == 15/2