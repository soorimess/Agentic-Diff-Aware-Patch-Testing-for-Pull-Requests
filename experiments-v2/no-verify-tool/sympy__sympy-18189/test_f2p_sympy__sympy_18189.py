"""
Test for diophantine permute behavior with different symbol orders.

This test ensures that when permute=True is specified, the results
should be the same regardless of the order of symbols in the syms parameter.
"""

from sympy import diophantine, symbols

def test_diophantine_permute_symbol_order():
    # Test case from the bug report
    n, m = symbols('n m')
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n) - should return all 8 solutions
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m) - should return the same 8 solutions (bug: was returning only 1)
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should return the same set of solutions
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result1 == expected, f"Expected {expected} but got {result1}"
    assert result2 == expected, f"Expected {expected} but got {result2}"
    assert result1 == result2, "Results should be identical regardless of symbol order"