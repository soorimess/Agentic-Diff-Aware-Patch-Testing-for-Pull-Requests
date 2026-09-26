from sympy import symbols
from sympy.solvers.diophantine import diophantine

def test_diophantine_permute_inconsistency():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Create the equation n**4 + m**4 - 2**4 - 3**4 = 0
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When symbols are given in order (m,n), should return all 8 solutions with permute=True
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When symbols are given in order (n,m), should also return all 8 solutions with permute=True
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should give the same set of solutions (this is the bug - they don't currently)
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # The test should pass after the fix is applied
    assert result1 == expected
    assert result2 == expected