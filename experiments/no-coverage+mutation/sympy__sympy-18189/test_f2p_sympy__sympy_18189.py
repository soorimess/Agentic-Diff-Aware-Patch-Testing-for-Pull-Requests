from sympy.solvers.diophantine import diophantine
from sympy import symbols

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Test equation: n**4 + m**4 - 2**4 - 3**4 = 0
    # This should have solutions where n**4 + m**4 = 2**4 + 3**4 = 16 + 81 = 97
    equation = n**4 + m**4 - 2**4 - 3**4
    
    # When symbols are ordered as (m,n) with permute=True, we get all 8 solutions
    result_mn = diophantine(equation, syms=(m,n), permute=True)
    
    # When symbols are ordered as (n,m) with permute=True, we should get the same 8 solutions
    result_nm = diophantine(equation, syms=(n,m), permute=True)
    
    # Both should return the same set of solutions
    expected_solutions = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result_mn == expected_solutions, f"Expected {expected_solutions}, got {result_mn}"
    assert result_nm == expected_solutions, f"Expected {expected_solutions}, got {result_nm}"
    
    # Additional check: the solutions should satisfy the original equation
    for sol in expected_solutions:
        n_val, m_val = sol
        assert n_val**4 + m_val**4 == 2**4 + 3**4