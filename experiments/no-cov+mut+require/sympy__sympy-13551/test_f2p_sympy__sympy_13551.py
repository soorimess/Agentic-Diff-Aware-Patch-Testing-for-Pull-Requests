"""
Regression test for the product evaluation bug in sympy.

The bug manifests when evaluating Product(n + 1/2**k, [k, 0, n-1])
which incorrectly returns 2**(n*(-n + 1)/2) + n**n instead of the correct
value of the product.
"""

from sympy import *
from sympy.abc import n, k

def test_product_addition_behavior():
    """Test Product(n + 1/2**k, [k, 0, n-1]) gives correct result."""
    
    # This is the problematic expression from the bug report
    expr = Product(n + 1 / 2**k, [k, 0, n-1])
    p = expr.doit()
    
    # For n=2, we expect:
    # (2 + 1/2^0) * (2 + 1/2^1) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    result_n2 = p.subs(n, 2)
    expected_n2 = Rational(15, 2)
    
    # The bug causes it to incorrectly return 9/2
    assert result_n2 == expected_n2, f"Bug present: expected {expected_n2}, got {result_n2}"
    
    # Also test with n=3 + 1/4 
    # (3 + 1) * (3 + 1/2) * (3 + 1/4) = 4 * 7/2 * 13/4 = 91/2
    result_n3 = p.subs(n, 3)
    expected_n3 = Rational(91, 2)
    
    assert result_n3 == expected_n3, f"Bug present: expected {expected_n3}, got {result_n3}"

def test_simple_product_still_works():
    """Ensure basic product functionality wasn't broken."""
    # Simple case to make sure we don't break anything else
    p = Product(k, [k, 1, 4]).doit()
    expected = 24  # 1*2*3*4
    assert p == expected