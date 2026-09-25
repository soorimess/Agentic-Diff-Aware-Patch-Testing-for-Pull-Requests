"""
Regression test for Product evaluation bug.
Product(n + 1 / 2**k, [k, 0, n-1]) was incorrectly returning 2**(n*(-n + 1)/2) + n**n instead of correct result.
"""

from sympy import Product, symbols, S

def test_product_bug_fix():
    """Test the specific bug in _eval_product where additive terms are handled incorrectly"""
    n, k = symbols('n k')
    
    # The problematic expression that fails in the buggy code
    expr = Product(n + 1 / 2**k, [k, 0, n-1])
    result = expr.doit()
    
    # For n=2, it should be (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    # NOT 2**(2*(-2 + 1)/2) + 2**2 = 2^(-1) + 4 = 1/2 + 4 = 9/2 (buggy result)
    result_n2 = result.subs(n, 2)
    
    # This test should fail in the buggy code and pass in the fixed code 
    assert result_n2 == S(15)/2