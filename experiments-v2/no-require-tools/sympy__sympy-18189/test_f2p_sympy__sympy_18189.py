from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # Test the specific case from the bug report
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n), we get all solutions including negatives
    sol1 = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m), we should get the same set of solutions but potentially in different order
    # Before the fix, this would return only {(3, 2)} instead of all 8 solutions
    sol2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should contain the same solutions (just potentially in different order)
    # The full solution set should be:
    # {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # Check that both results contain the same elements
    assert sol1 == expected, f"sol1 = {sol1}, expected = {expected}"
    assert sol2 == expected, f"sol2 = {sol2}, expected = {expected}"
    
    # Also verify that the results are not empty and contain the expected structure
    assert len(sol1) > 0, "sol1 should not be empty"
    assert len(sol2) > 0, "sol2 should not be empty"
    assert len(sol1) == len(sol2) == 8, f"Both should have 8 solutions, got {len(sol1)} and {len(sol2)}"