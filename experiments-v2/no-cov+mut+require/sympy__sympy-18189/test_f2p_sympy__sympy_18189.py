from sympy import diophantine, symbols

def test_diophantine_permute_order_independence():
    """Test that diophantine with permute=True gives same results regardless of symbol order"""
    n, m = symbols('n m')
    
    # Test equation: n**4 + m**4 - 2**4 - 3**4 = 0
    # This should have solutions with both signs and permutations
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # When syms=(m,n) - should return all permutations with signs
    result_mn = diophantine(eq, syms=(m,n), permute=True)
    
    # When syms=(n,m) - should return the same set of solutions (this was broken)
    result_nm = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should give the same results
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    # The bug was that syms=(n,m) would only return {(3, 2)} instead of all solutions
    # This test ensures that both orders produce the complete set
    assert result_mn == expected, f"syms=(m,n) failed: expected {expected}, got {result_mn}"
    assert result_nm == expected, f"syms=(n,m) failed: expected {expected}, got {result_nm}"
    
    # Verify that the results are actually the same set
    assert result_mn == result_nm, f"Results differ between symbol orders: {result_mn} vs {result_nm}"