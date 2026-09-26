from sympy import Product, symbols

def test_product_correctness():
    """
    Regression test for Product(n + 1/2**k, [k, 0, n-1]) bug.
    
    The bug was in how products with sum terms were handled.
    Before the fix, Product(n + 1/2**k, [k, 0, n-1]) would incorrectly return:
    2**(n*(-n + 1)/2) + n**n
    
    After the fix, it should correctly compute the product as:
    (n + 1) * (n + 1/2) * (n + 1/4) * ... * (n + 1/2^(n-1))
    """
    n, k = symbols('n k')
    
    # Create the problematic product
    expr = Product(n + 1 / 2**k, [k, 0, n-1])
    result = expr.doit()
    
    # Test the specific case that was broken
    result_n2 = result.subs(n, 2)
    
    # For n=2, the correct mathematical result is:
    # (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2 = 7.5
    expected_n2 = 15/2
    
    # This assertion should pass with the correct implementation
    # It will fail with the buggy implementation which returns 9/2
    assert result_n2 == expected_n2, f"Product computation is incorrect. Expected {expected_n2}, got {result_n2}"
    
    # Additional check: the buggy result would be 2^(2*(-2 + 1)/2) + 2**2 = 2^(-1) + 4 = 1/2 + 4 = 9/2
    buggy_result_n2 = 2**(2*(-2 + 1)/2) + 2**2
    assert result_n2 != buggy_result_n2, "Result matches the buggy implementation - fix not working"