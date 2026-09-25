from sympy import Product, symbols

def test_bug_fix_verification():
    """Test to verify the fix for Product(n + 1 / 2**k, [k, 0, n-1])"""
    n, k = symbols('n k')
    
    # This is the specific buggy case from the issue report
    expr = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # This should evaluate to the correct result
    # For n=2: (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    result_n2 = expr.subs(n, 2)
    
    # The test verifies we move from the incorrect 9/2 to the correct 15/2
    # We assert we are NOT getting the wrong result 
    assert result_n2 != 9/2, "Still producing buggy result of 9/2"
    
    # We also assert we are getting the right result
    assert result_n2 == 15/2, f"Should get 15/2, but got {result_n2}"