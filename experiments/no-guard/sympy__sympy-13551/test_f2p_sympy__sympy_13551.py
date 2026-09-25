from sympy import *
from sympy.abc import n,k

def test_product_add_evaluation_bug():
    """
    Regression test for Product(n + 1/2**k, [k, 0, n-1]) bug.
    
    The bug was in _eval_product when handling Add expressions.
    The old code incorrectly evaluated: 
    sum([self._eval_product(i, (k, a, n)) for i in p.as_coeff_Add()])
    which gave wrong result for n=2: 9/2 instead of 15/2
    
    The fix correctly evaluates this as exp(Sum(log(p), (k, a, n)))
    """
    # This is the exact failing case from the bug report
    product_expr = Product(n + 1 / 2**k, [k, 0, n-1])
    result = product_expr.doit()
    
    # Manual calculation verification for n=2
    # (2 + 2^0) * (2 + 2^(-1)) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    manual_calculation = (2 + 1) * (2 + Rational(1, 2))  # 3 * 5/2 = 15/2
    
    result_n2 = result.subs(n, 2)
    
    # The bug was returning 9/2 instead of 15/2
    assert result_n2 == Rational(15, 2), \
        "For n=2, Product(n + 1/2**k, [k, 0, n-1]) should be 15/2, got {}".format(result_n2)

def test_specific_product_value():
    """
    Additional verification with another case to confirm the behavior.
    """
    # For n=3: Product_{k=0}^{2} (3 + 1/2^k) = (3 + 1) * (3 + 1/2) * (3 + 1/4) = 4 * 7/2 * 13/4 = 91/2
    product_expr = Product(n + 1 / 2**k, [k, 0, n-1])
    result = product_expr.doit()
    result_n3 = result.subs(n, 3)
    
    # Manual calculation: (3 + 1) * (3 + 1/2) * (3 + 1/4) = 4 * 7/2 * 13/4 = 91/2
    expected_n3 = Rational(91, 2) 
    
    assert result_n3 == expected_n3, \
        "For n=3, Product(n + 1/2**k, [k, 0, n-1]) should be 91/2, got {}".format(result_n3)