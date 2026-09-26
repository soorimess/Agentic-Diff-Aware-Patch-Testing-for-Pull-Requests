from sympy import symbols, diophantine

def test_diophantine_permute_order():
    """Test that diophantine with permute=True gives consistent results regardless of symbol order."""
    n, m = symbols('n m')
    
    # The equation n**4 + m**4 - 2**4 - 3**4 = 0
    # This should have solutions with all combinations of signs for both variables
    eq = n**4 + m**4 - 2**4 - 3**4
    
    # Test with syms=(m,n) - should return all 8 solutions including negative ones
    result1 = diophantine(eq, syms=(m,n), permute=True)
    
    # Test with syms=(n,m) - should return the same set of solutions
    result2 = diophantine(eq, syms=(n,m), permute=True)
    
    # Both should give the same result (all permutations with signs)
    expected = {(-3, -2), (-3, 2), (-2, -3), (-2, 3), (2, -3), (2, 3), (3, -2), (3, 2)}
    
    assert result1 == expected, f"Expected {expected} for syms=(m,n), got {result1}"
    assert result2 == expected, f"Expected {expected} for syms=(n,m), got {result2}"
    
    # The bug was that result2 only returned {(3, 2)} instead of all 8 solutions
    # This test should fail on the buggy code and pass on the fixed code