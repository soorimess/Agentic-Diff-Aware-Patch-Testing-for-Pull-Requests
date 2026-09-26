from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Test the specific case from the bug report
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When symbols are ordered as (m,n)
    sol1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When symbols are ordered as (n,m) 
    sol2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should return the same number of solutions
    assert len(sol1) == len(sol2), "Number of solutions should be the same regardless of symbol order"
    
    # Both should return all 8 solutions (not just 1)
    assert len(sol1) == 8, "Should return all 8 solutions when permute=True"
    assert len(sol2) == 8, "Should return all 8 solutions when permute=True"
    
    # Verify the solutions are correct
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    assert sol1 == expected, f"Expected {expected}, got {sol1}"
    assert sol2 == expected, f"Expected {expected}, got {sol2}"
    
    # Additional test: make sure we get the right type of solutions
    # All solutions should have the property that n^4 + m^4 = 2^4 + 3^4 = 97
    for n_val, m_val in sol1:
        assert n_val**4 + m_val**4 == 2**4 + 3**4, f"Solution ({n_val}, {m_val}) doesn't satisfy equation"
    
    for n_val, m_val in sol2:
        assert n_val**4 + m_val**4 == 2**4 + 3**4, f"Solution ({n_val}, {m_val}) doesn't satisfy equation"