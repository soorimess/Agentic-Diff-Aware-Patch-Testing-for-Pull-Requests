"""
Regression test for Product evaluation bug in sympy/sympy#13551
This tests the exact issue: Product(n + 1/2**k, [k, 0, n-1]) should not return
2**(n*(-n + 1)/2) + n**n but rather calculate the correct product.
"""

from sympy import Product, symbols, simplify
from sympy.abc import n, k

def test_product_bug_regression():
    """
    Regression test for bug where Product(n + 1/2**k, [k, 0, n-1]) 
    give incorrect result.
    
    The bug: n=2 case returns 9/2 instead of 15/2
    """
    # Evaluate the problematic product directly  
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # The key test case from the bug report
    result_n2 = p.subs(n, 2)
    expected = 15/2  # (2+1) * (2+1/2) = 3 * 5/2 = 15/2
    
    # We will be checking that this assertion fails in the current implementation
    # but would pass once fixed
    assert result_n2 == expected, f"Expected {expected}, but got {result_n2}"


def test_product_verification_n3():
    """Additional test case to help verify correctness"""
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # Another verification case
    result_n3 = p.subs(n, 3) 
    expected = 91/2  # (3+1) * (3+1/2) * (3+1/4) = 4 * 7/2 * 13/4 = 91/2
    
    assert result_n3 == expected, f"Expected {expected}, but got {result_n3}"