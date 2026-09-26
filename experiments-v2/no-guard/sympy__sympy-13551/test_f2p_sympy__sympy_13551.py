from sympy import Product, simplify, symbols, S
from sympy.abc import n, k

def test_product_n_plus_half_power():
    """
    Regression test for bug in Product(n + 1/2**k, [k, 0, n-1]) evaluation.
    
    This test verifies that the product evaluates correctly:
    - For n=2: Product(k=0 to 1) of (2 + 1/2^k) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    - The incorrect result was 9/2 (which equals 2**(2*(-2 + 1)/2) + 2**2)
    """
    # This is the main test case from the bug report
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # For n=2, the correct value should be 15/2
    # Product(k=0 to 1) of (2 + 1/2^k) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    result_n2 = p.subs(n, 2)
    expected_n2 = S(15)/2
    
    # This assertion should pass after the fix is applied
    assert result_n2 == expected_n2, f"Bug: expected {expected_n2}, got {result_n2}"