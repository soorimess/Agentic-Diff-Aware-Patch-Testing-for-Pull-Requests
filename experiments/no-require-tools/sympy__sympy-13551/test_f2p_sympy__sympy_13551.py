"""
Test for product evaluation bug fix.

The bug was that Product(n + 1/2**k, [k, 0, n-1]) was being evaluated incorrectly.
For n=2, it evaluates to 9/2 instead of the correct value 15/2.
"""
from sympy import Product, simplify, S
from sympy.abc import n, k


def test_product_bug_n2():
    """Test that Product(n + 1/2**k, [k, 0, n-1]) gives correct result for n=2."""
    # The problematic expression: Product(n + 1/2**k, [k, 0, n-1])
    # Manual calculation for n=2:
    # Product terms are (2 + 2^0) * (2 + 2^(-1)) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result_n2 = p.subs(n, 2)
    
    # The buggy implementation returns 9/2, but the correct result is 15/2
    expected_n2 = S(15)/2
    assert result_n2 == expected_n2, f"Expected {expected_n2}, got {result_n2}"
    
    
def test_product_bug_n3():
    """Test that Product(n + 1/2**k, [k, 0, n-1]) gives correct result for n=3."""
    # Manual calculation for n=3:
    # Product terms are (3 + 2^0) * (3 + 2^(-1)) * (3 + 2^(-2)) = 4 * 7/2 * 13/4 = 91/2
    
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result_n3 = p.subs(n, 3)
    
    # The correct result is 91/2
    expected_n3 = S(91)/2
    assert result_n3 == expected_n3, f"Expected {expected_n3}, got {result_n3}"