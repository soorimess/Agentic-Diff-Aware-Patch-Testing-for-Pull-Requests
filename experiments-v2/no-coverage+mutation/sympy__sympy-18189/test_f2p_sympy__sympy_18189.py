from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives same results regardless of syms order"""
    n, m = symbols('n m')
    
    # Test equation: n^4 + m^4 - 2^4 - 3^4 = 0
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n), permute=True should give all solutions including negatives
    sol1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m), permute=True should give same set of solutions
    sol2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should give the same set of solutions
    # Expected: {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert sol1 == expected, f"sol1 = {sol1}, expected = {expected}"
    assert sol2 == expected, f"sol2 = {sol2}, expected = {expected}"