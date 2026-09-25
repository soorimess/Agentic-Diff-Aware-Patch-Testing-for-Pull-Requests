from sympy import Product, symbols

def test_product_bug_demo():
    """
    This test demonstrates the bug described in the GitHub issue:
    Product(n + 1 / 2**k, [k, 0, n-1]) computes wrong value for n=2.
    """
    n, k = symbols('n k')
    
    # Computes the expression: Product(n + 1 / 2**k, [k, 0, n-1])
    p = Product(n + 1 / 2**k, [k, 0, n-1]).doit()
    
    # For n=2 the expression becomes (2 + 1) * (2 + 1/2) = 3 * 5/2 = 15/2
    # The bug made it produce 9/2 instead
    result = p.subs(n, 2)
    
    # Demonstrating the specific issue we are checking  
    # The correct result is 15/2, but bug produces 9/2
    assert result == 15/2, f"Mathematically incorrect result: got {result}, expected 15/2"