"""
Regression test for diophantine permute=True issue with syms order.
This reproduces the condition described in the bug report.
"""

from sympy import symbols, diophantine


def test_diophantine_permute_syms_order():
    """
    Test that diophantine with permute=True gives same results 
    regardless of syms order - this is a regression test for a bug
    where syms order affected results when permute=True was used.
    
    The bug was that when syms != var, the permute parameter
    was not passed to the recursive call.
    """
    n, m = symbols('n m')
    expr = n**4 + m**4 - 2**4 - 3**4
    
    # Both of these should return the same complete solution set
    result_mn = diophantine(expr, syms=(m,n), permute=True)
    result_nm = diophantine(expr, syms=(n,m), permute=True)
    
    # This assertion will fail with current buggy code, pass with fixed code
    assert result_mn == result_nm
    
    # Expected complete solution (all sign permutations of (2,3))
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    assert result_mn == expected