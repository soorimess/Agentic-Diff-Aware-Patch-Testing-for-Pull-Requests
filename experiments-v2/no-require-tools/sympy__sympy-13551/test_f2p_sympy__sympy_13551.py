from sympy import Product, simplify
from sympy.abc import n, k

def test_product_bug():
    # Test the bug described in the issue
    # Product(n + 1 / 2**k, [k, 0, n-1]) should be computed correctly
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # For n=2, the product should be (2 + 2^0) * (2 + 2^(-1)) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    # But the buggy version returns 2**(n*(-n + 1)/2) + n**n = 2^(2*(-2 + 1)/2) + 2**2 = 2^(-1) + 4 = 1/2 + 4 = 9/2
    result_n2 = p.subs(n, 2)
    expected_n2 = 15/2
    
    # The bug is that result_n2 == 9/2 instead of 15/2
    assert result_n2 == expected_n2, f"Expected {expected_n2}, got {result_n2}"