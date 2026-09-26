from sympy import Product, simplify
from sympy.abc import n, k

def test_product_bug():
    """Test for the bug in Product evaluation of n + 1/2^k.
    
    Bug: Product(n + 1 / 2**k, [k, 0, n-1]) incorrectly returns 
    2**(n*(-n + 1)/2) + n**n instead of the correct result.
    
    For n=2: should be 15/2, not 9/2
    """
    # Test case from the bug report
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    result = simplify(p)
    
    # For n=2, the correct value should be:
    # Product(k=0 to 1) of (2 + 1/2^k) = (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    expected_for_n2 = 15/2
    actual_for_n2 = result.subs(n, 2)
    
    # This assertion should fail with the buggy implementation
    assert actual_for_n2 == expected_for_n2, f"Expected {expected_for_n2}, got {actual_for_n2}"