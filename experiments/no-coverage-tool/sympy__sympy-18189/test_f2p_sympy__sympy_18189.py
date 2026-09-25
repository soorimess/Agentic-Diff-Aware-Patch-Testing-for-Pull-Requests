from sympy import symbols, diophantine

def test_diophantine_permute_order_independence():
    """Test that diophantine with permute=True gives same results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Test equation: n^4 + m^4 - 2^4 - 3^4 = 0
    # This should have solutions with both positive and negative values
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) and permute=True
    sols_mn = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) and permute=True  
    sols_nm = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should return the same set of solutions
    expected_solutions = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Before the fix, these would be different, causing a bug
    # After the fix, they should both return the same set
    assert sols_mn == expected_solutions, f"syms=(m,n) should return {expected_solutions}, got {sols_mn}"
    assert sols_nm == expected_solutions, f"syms=(n,m) should return {expected_solutions}, got {sols_nm}"
    assert sols_mn == sols_nm, "Results should be identical regardless of symbol order"