"""
Regression test for diophantine permute=True bug where results differ based on syms order.

The bug: when using diophantine with permute=True and syms parameter,
the order of symbols in syms affects the result - some solutions are missing
when the symbol ordering doesn't match the internal variable ordering.
"""

from sympy import symbols, diophantine

def test_diophantine_permute_order_independence():
    """Test that diophantine with permute=True gives the same results regardless of syms order."""
    
    # Create symbols n, m
    n, m = symbols('n m')
    
    # Equation: n**4 + m**4 = 2**4 + 3**4 = 16 + 81 = 97
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - This should return all solutions including negative ones
    result1 = diophantine(eq, syms=(m,n), permute=True)
    expected1 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Test with syms=(n,m) - This was originally returning only (3, 2) 
    # but should return the same set of solutions
    result2 = diophantine(eq, syms=(n,m), permute=True) 
    expected2 = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Both should give the same full set of solutions
    assert result1 == expected1, f"Expected {expected1} but got {result1}"  
    assert result2 == expected2, f"Expected {expected2} but got {result2}"
    assert result1 == result2, "Results should be identical regardless of symbol order"